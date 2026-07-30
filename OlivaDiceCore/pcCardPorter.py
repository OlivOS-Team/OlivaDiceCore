# -*- encoding: utf-8 -*-
r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   pcCardPorter.py
@Author    :   Desom-fu
@License   :   AGPL
@Copyright :   (C) 2020-2026, OlivOS-Team
@Desc      :   人物卡引继(.port): 同骰引继码 + 跨骰数据码(ODC)的完整实现
               msgReply.py 中仅保留入口, 全部逻辑在本模块

两级结构:
  同骰引继码: 6位本机授权码(token -> pcHash), 数据不走消息通道, 与卡数无关
  跨骰引继码: ODC 数据码, 码本身即全部数据, 任何装了本插件的骰都能解码

ODC 数据码管线:
  L0 语义裁剪(同义词归并 + 模板默认值差分)
  L1 紧凑二进制(模板码表索引增量编码 + varint)
  L2 压缩(直存/zlib/zlib+模板预置字典/lzma 自动择优, 纯标准库)
  L3 封包(版本 | flags | [码表指纹] | 载荷 | CRC16), 超长自动分段
  L4 文本装甲(base16384 汉字 14bit/字 或 base64url)
"""

import OlivOS
import OlivaDiceCore

import base64
import copy
import json
import lzma
import os
import struct
import time
import uuid
import zlib

# =========================================================
# 常量
# =========================================================

ODC_PREFIX = 'ODC1'
ODC_VERSION = 1

HIY_KEYS = ['普通成功', '困难成功', '极难成功', '大成功', '失败', '大失败']

# 码表索引仅对内置模板启用(双端随核心版本内置, 一致性可控);
# 自定义模板一律字面编码, 保证没装同款模板的骰也能解码
BUILTIN_TEMPLATES = ['default', 'COC7', '纯净COC7', 'COC6', 'DND5E', 'DX3', 'FATE']

# 每卡 flags 位
CF_TEMPLATE = 1
CF_CHECKRULES = 2
CF_ENHANCE = 4
CF_MAPPING = 8
CF_NOTE = 16
CF_MH = 32
CF_HIY = 64
CF_EXTRA = 128

# 封包 flags: 低2位压缩算法, bit2 分段
PK_ALGO_STORE = 0
PK_ALGO_ZLIB = 1
PK_ALGO_ZDICT = 2
PK_ALGO_LZMA = 3
PK_FLAG_PART = 4

_LZMA_FILT = [{'id': lzma.FILTER_LZMA2, 'preset': 9 | lzma.PRESET_EXTREME}]

# 防解压炸弹与结构上限
MAX_DECOMPRESS = 512 * 1024
MAX_CARDS = 128
MAX_SKILLS_PER_CARD = 2048
MAX_STR_LEN = 4096

# 同骰引继码表: code -> {'pcHash':..., 'userId':..., 'platform':..., 'expire':...}
dictPortCode = {}

# 跨骰码分段收集会话: pcHash -> {'transferId':..., 'total':..., 'parts':{idx:bytes}, 'expire':...}
dictPortSession = {}

SESSION_TTL = 600


# =========================================================
# 基础编码工具: varint / zigzag / 字符串
# =========================================================

def _w_varint(out, n):
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return


def _r_varint(buf, pos):
    shift = 0
    res = 0
    while True:
        if pos >= len(buf):
            raise ValueError('数据不完整')
        b = buf[pos]
        pos += 1
        res |= (b & 0x7F) << shift
        if not (b & 0x80):
            return res, pos
        shift += 7
        if shift > 63:
            raise ValueError('数值超限')


def _zz(n):
    n = int(n)
    return (n << 1) if n >= 0 else ((-n) << 1) - 1


def _unzz(n):
    return (n >> 1) if not (n & 1) else -((n + 1) >> 1)


def _w_str(out, s):
    b = str(s).encode('utf-8')
    if len(b) > MAX_STR_LEN:
        b = b[:MAX_STR_LEN]
    _w_varint(out, len(b))
    out.extend(b)


def _r_str(buf, pos):
    ln, pos = _r_varint(buf, pos)
    if ln > MAX_STR_LEN or pos + ln > len(buf):
        raise ValueError('字符串超限')
    return buf[pos:pos + ln].decode('utf-8'), pos + ln


# =========================================================
# 文本装甲: base16384 风格汉字装甲 / base64url
# =========================================================

def armorCJK(blob):
    bits = len(blob) * 8
    n = int.from_bytes(blob, 'big')
    pad = (-bits) % 14
    n <<= pad
    total = (bits + pad) // 14
    chars = []
    for i in range(total - 1, -1, -1):
        chars.append(chr(0x4E00 + ((n >> (i * 14)) & 0x3FFF)))
    chars.append(chr(0x3D00 + pad))
    return ''.join(chars)


def dearmorCJK(s):
    if len(s) < 2:
        raise ValueError('数据不完整')
    pad = ord(s[-1]) - 0x3D00
    if pad < 0 or pad > 13:
        raise ValueError('装甲格式错误')
    body = s[:-1]
    n = 0
    for ch in body:
        v = ord(ch) - 0x4E00
        if v < 0 or v > 0x3FFF:
            raise ValueError('装甲字符错误')
        n = (n << 14) | v
    bits = len(body) * 14 - pad
    if bits < 0:
        raise ValueError('数据不完整')
    n >>= pad
    return n.to_bytes((bits + 7) // 8, 'big')


def armorB64(blob):
    return base64.urlsafe_b64encode(blob).rstrip(b'=').decode()


def dearmorB64(s):
    return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))


# =========================================================
# 模板码表 / 预置字典
# =========================================================

def getTemplateDict():
    return OlivaDiceCore.pcCard.dictPcCardTemplateDefault.get('unity', {})


def getTemplateByName(templateName):
    templates = getTemplateDict()
    if templateName in templates:
        return templates[templateName]
    return templates.get('default', {})


def templateSkillTable(template):
    """从模板确定性导出规范技能名表(排序保证双端一致)"""
    names = set()
    for key in ('defaultSkillValue', 'synonyms', 'mapping', 'showName'):
        val = template.get(key)
        if type(val) is dict:
            names.update(val.keys())
    return sorted(names)


def templateSynMap(template):
    """alias -> primary (synonyms 已在 dataPcCardTemplateInit 中大写化)"""
    syn = {}
    synonyms = template.get('synonyms')
    if type(synonyms) is dict:
        for p, aliases in synonyms.items():
            for a in aliases:
                syn[a] = p
            syn[p] = p
    return syn


def templateZdict(template, templateName):
    parts = templateSkillTable(template) + HIY_KEYS
    parts += ['人物卡', 'default', templateName]
    d = '\n'.join(parts).encode('utf-8')
    return d[:32000]


def dictFingerprint(zd):
    return zlib.crc32(zd) & 0xFF


def zdictLookup(fp):
    templates = getTemplateDict()
    for tname in BUILTIN_TEMPLATES:
        if tname in templates:
            zd = templateZdict(templates[tname], tname)
            if dictFingerprint(zd) == fp:
                return zd
    return None


# =========================================================
# L0 语义裁剪(无损)
# =========================================================

def canonicalizeCard(skills, template):
    """同义词组归并为主名条目 + 去掉与模板默认值相等的条目"""
    syn = templateSynMap(template)
    defaults = template.get('defaultSkillValue')
    if type(defaults) is not dict:
        defaults = {}
    groups = {}
    literal = {}
    for k, v in skills.items():
        p = syn.get(k)
        if p is None:
            literal[k] = v
        else:
            groups.setdefault(p, {})[k] = v
    canon = {}
    for p, kv in groups.items():
        vals = set(kv.values())
        if len(vals) == 1:
            canon[p] = vals.pop()
        else:
            # 组内值不一致的历史卡: 逐键字面保留
            for k, v in kv.items():
                literal[k] = v
    canon.update(literal)
    res = {}
    for k, v in canon.items():
        if k in defaults and defaults[k] == v:
            continue
        res[k] = v
    return res


def expandCard(canon, template):
    """导入端: 主名条目按同义词组展开(显式条目优先, 与 .st 回放行为一致)"""
    synonyms = template.get('synonyms')
    if type(synonyms) is not dict:
        synonyms = {}
    out = dict(canon)
    for k, v in canon.items():
        if k in synonyms:
            for a in synonyms[k]:
                if a not in out:
                    out[a] = v
    return out


# =========================================================
# L1 二进制序列化
# =========================================================

def encodeUser(user, forceLiteral=False):
    """user 结构见 collectUserData; forceLiteral=True 生成不依赖码表版本的通用码"""
    templates = getTemplateDict()
    out = bytearray()
    names = list(user['cards'].keys())
    _w_varint(out, len(names))
    for name in names:
        c = user['cards'][name]
        tname = c.get('template') or 'default'
        template = getTemplateByName(tname)
        if not forceLiteral and tname in BUILTIN_TEMPLATES and tname in templates:
            table = templateSkillTable(template)
        else:
            table = []
        tidx = {}
        for i, k in enumerate(table):
            tidx[k] = i
        _w_str(out, name)
        flags = 0
        if c.get('template'):
            flags |= CF_TEMPLATE
        if c.get('checkRules'):
            flags |= CF_CHECKRULES
        if c.get('enhanceList'):
            flags |= CF_ENHANCE
        if c.get('mappingRecord'):
            flags |= CF_MAPPING
        if c.get('noteRecord'):
            flags |= CF_NOTE
        if c.get('mh'):
            flags |= CF_MH
        if c.get('hiy'):
            flags |= CF_HIY
        if c.get('extra'):
            flags |= CF_EXTRA
        out.append(flags)
        if flags & CF_TEMPLATE:
            if c['template'] in BUILTIN_TEMPLATES:
                _w_varint(out, BUILTIN_TEMPLATES.index(c['template']) + 1)
            else:
                _w_varint(out, 0)
                _w_str(out, c['template'])
        if flags & CF_CHECKRULES:
            rules = sorted((template.get('checkRules') or {}).keys())
            if c['checkRules'] in rules:
                _w_varint(out, rules.index(c['checkRules']) + 1)
            else:
                _w_varint(out, 0)
                _w_str(out, c['checkRules'])
        canon = canonicalizeCard(c['skills'], template)
        # 码表内条目按索引排序做增量编码, 表外条目字面存放
        idxed = []
        lits = []
        for k, v in canon.items():
            if k in tidx:
                idxed.append((tidx[k], int(v)))
            else:
                lits.append((k, int(v)))
        idxed.sort()
        _w_varint(out, len(idxed))
        prev = -1
        for i, v in idxed:
            _w_varint(out, i - prev)
            prev = i
            _w_varint(out, _zz(v))
        _w_varint(out, len(lits))
        for k, v in lits:
            _w_str(out, k)
            _w_varint(out, _zz(v))
        if flags & CF_ENHANCE:
            _w_varint(out, len(c['enhanceList']))
            for k in c['enhanceList']:
                if k in tidx:
                    _w_varint(out, tidx[k] + 1)
                else:
                    _w_varint(out, 0)
                    _w_str(out, k)
        if flags & CF_MAPPING:
            _w_varint(out, len(c['mappingRecord']))
            for k, v in c['mappingRecord'].items():
                _w_str(out, k)
                _w_str(out, v)
        if flags & CF_NOTE:
            _w_varint(out, len(c['noteRecord']))
            for k, v in c['noteRecord'].items():
                _w_str(out, k)
                _w_str(out, v)
        if flags & CF_HIY:
            hiy = c['hiy']
            mask = 0
            for i, k in enumerate(HIY_KEYS):
                if hiy.get(k):
                    mask |= (1 << i)
            out.append(mask)
            for i, k in enumerate(HIY_KEYS):
                if mask & (1 << i):
                    _w_varint(out, int(hiy[k]))
            extra = {}
            for k, v in hiy.items():
                if k not in HIY_KEYS and type(v) is int:
                    extra[k] = v
            _w_varint(out, len(extra))
            for k, v in extra.items():
                _w_str(out, k)
                _w_varint(out, _zz(v))
        if flags & CF_EXTRA:
            _w_varint(out, len(c['extra']))
            for k, v in c['extra'].items():
                _w_str(out, k)
                _w_str(out, json.dumps(v, ensure_ascii=False, separators=(',', ':')))
    sel = user.get('selection')
    _w_varint(out, names.index(sel) + 1 if sel in names else 0)
    lock = user.get('lockList') or {}
    _w_varint(out, len(lock))
    for hag, cname in lock.items():
        hag = str(hag)
        if hag.isdigit() and len(hag) < 19:
            out.append(0)
            _w_varint(out, int(hag))
        elif '|' in hag:
            a, b = hag.split('|', 1)
            if a.isdigit() and b.isdigit() and len(a) < 19 and len(b) < 19:
                out.append(1)
                _w_varint(out, int(a))
                _w_varint(out, int(b))
            else:
                out.append(2)
                _w_str(out, hag)
        else:
            out.append(2)
            _w_str(out, hag)
        if cname in names:
            _w_varint(out, names.index(cname) + 1)
        else:
            _w_varint(out, 0)
            _w_str(out, cname)
    return bytes(out)


def decodeUser(buf):
    templates = getTemplateDict()
    pos = 0
    n, pos = _r_varint(buf, pos)
    if n > MAX_CARDS:
        raise ValueError('卡片数量超限')
    cards = {}
    names = []
    for _i in range(n):
        name, pos = _r_str(buf, pos)
        names.append(name)
        if pos >= len(buf):
            raise ValueError('数据不完整')
        flags = buf[pos]
        pos += 1
        c = {
            'skills': {},
            'template': None,
            'checkRules': None,
            'enhanceList': None,
            'mappingRecord': None,
            'noteRecord': None,
            'hiy': None,
            'mh': bool(flags & CF_MH),
            'extra': None,
        }
        if flags & CF_TEMPLATE:
            r, pos = _r_varint(buf, pos)
            if r == 0:
                c['template'], pos = _r_str(buf, pos)
            elif r <= len(BUILTIN_TEMPLATES):
                c['template'] = BUILTIN_TEMPLATES[r - 1]
            else:
                raise ValueError('模板索引错误')
        tname = c['template'] or 'default'
        template = getTemplateByName(tname)
        if tname in BUILTIN_TEMPLATES and tname in templates:
            table = templateSkillTable(template)
        else:
            table = []
        if flags & CF_CHECKRULES:
            r, pos = _r_varint(buf, pos)
            if r == 0:
                c['checkRules'], pos = _r_str(buf, pos)
            else:
                rules = sorted((template.get('checkRules') or {}).keys())
                if r <= len(rules):
                    c['checkRules'] = rules[r - 1]
                else:
                    c['checkRules'] = 'default'
        cnt, pos = _r_varint(buf, pos)
        if cnt > MAX_SKILLS_PER_CARD:
            raise ValueError('技能数量超限')
        canon = {}
        prev = -1
        for _j in range(cnt):
            d, pos = _r_varint(buf, pos)
            prev += d
            v, pos = _r_varint(buf, pos)
            if prev >= len(table):
                raise ValueError('码表索引越界, 请确认双方插件版本一致')
            canon[table[prev]] = _unzz(v)
        cnt, pos = _r_varint(buf, pos)
        if cnt > MAX_SKILLS_PER_CARD:
            raise ValueError('技能数量超限')
        for _j in range(cnt):
            k, pos = _r_str(buf, pos)
            v, pos = _r_varint(buf, pos)
            canon[k] = _unzz(v)
        c['skills'] = expandCard(canon, template)
        if flags & CF_ENHANCE:
            cnt, pos = _r_varint(buf, pos)
            if cnt > MAX_SKILLS_PER_CARD:
                raise ValueError('成长列表超限')
            lst = []
            for _j in range(cnt):
                r, pos = _r_varint(buf, pos)
                if r == 0:
                    k, pos = _r_str(buf, pos)
                elif r <= len(table):
                    k = table[r - 1]
                else:
                    raise ValueError('码表索引越界')
                lst.append(k)
            c['enhanceList'] = lst
        if flags & CF_MAPPING:
            cnt, pos = _r_varint(buf, pos)
            d = {}
            for _j in range(cnt):
                k, pos = _r_str(buf, pos)
                v, pos = _r_str(buf, pos)
                d[k] = v
            c['mappingRecord'] = d
        if flags & CF_NOTE:
            cnt, pos = _r_varint(buf, pos)
            d = {}
            for _j in range(cnt):
                k, pos = _r_str(buf, pos)
                v, pos = _r_str(buf, pos)
                d[k] = v
            c['noteRecord'] = d
        if flags & CF_HIY:
            if pos >= len(buf):
                raise ValueError('数据不完整')
            mask = buf[pos]
            pos += 1
            d = {}
            for i, k in enumerate(HIY_KEYS):
                if mask & (1 << i):
                    v, pos = _r_varint(buf, pos)
                    d[k] = v
            cnt, pos = _r_varint(buf, pos)
            for _j in range(cnt):
                k, pos = _r_str(buf, pos)
                v, pos = _r_varint(buf, pos)
                d[k] = _unzz(v)
            c['hiy'] = d
        if flags & CF_EXTRA:
            cnt, pos = _r_varint(buf, pos)
            d = {}
            for _j in range(cnt):
                k, pos = _r_str(buf, pos)
                v, pos = _r_str(buf, pos)
                try:
                    d[k] = json.loads(v)
                except Exception:
                    d[k] = v
            c['extra'] = d
        cards[name] = c
    r, pos = _r_varint(buf, pos)
    selection = names[r - 1] if 0 < r <= len(names) else None
    cnt, pos = _r_varint(buf, pos)
    lock = {}
    for _i in range(cnt):
        if pos >= len(buf):
            raise ValueError('数据不完整')
        t = buf[pos]
        pos += 1
        if t == 0:
            v, pos = _r_varint(buf, pos)
            hag = str(v)
        elif t == 1:
            a, pos = _r_varint(buf, pos)
            b, pos = _r_varint(buf, pos)
            hag = '%s|%s' % (a, b)
        else:
            hag, pos = _r_str(buf, pos)
        r, pos = _r_varint(buf, pos)
        if r == 0:
            cname, pos = _r_str(buf, pos)
        elif r <= len(names):
            cname = names[r - 1]
        else:
            raise ValueError('锁定卡索引错误')
        lock[hag] = cname
    return {'cards': cards, 'selection': selection, 'lockList': lock}


# =========================================================
# L2/L3 压缩 + 封包 + 分段
# =========================================================

def pack(payload, zdict=None):
    """压缩自动择优, 返回单体封包(未分段)"""
    cands = [(PK_ALGO_STORE, payload)]
    co = zlib.compressobj(9, zlib.DEFLATED, -15, 9)
    cands.append((PK_ALGO_ZLIB, co.compress(payload) + co.flush()))
    if zdict:
        co = zlib.compressobj(9, zlib.DEFLATED, -15, 9, zlib.Z_DEFAULT_STRATEGY, zdict)
        cands.append((PK_ALGO_ZDICT, co.compress(payload) + co.flush()))
    try:
        cands.append((PK_ALGO_LZMA, lzma.compress(payload, format=lzma.FORMAT_RAW, filters=_LZMA_FILT)))
    except Exception:
        pass
    algo, comp = min(cands, key=lambda c: len(c[1]))
    head = bytes([ODC_VERSION, algo])
    if algo == PK_ALGO_ZDICT:
        head += bytes([dictFingerprint(zdict)])
    body = head + comp
    return body + struct.pack('<H', zlib.crc32(body) & 0xFFFF)


def unpack(blob):
    """解开单体封包"""
    if len(blob) < 4:
        raise ValueError('数据不完整')
    body = blob[:-2]
    crc = struct.unpack('<H', blob[-2:])[0]
    if zlib.crc32(body) & 0xFFFF != crc:
        raise ValueError('CRC')
    ver = body[0]
    if ver != ODC_VERSION:
        raise ValueError('VERSION')
    flags = body[1]
    algo = flags & 3
    pos = 2
    if algo == PK_ALGO_STORE:
        return bytes(body[pos:])
    if algo == PK_ALGO_LZMA:
        do = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=_LZMA_FILT)
        res = do.decompress(bytes(body[pos:]), MAX_DECOMPRESS)
        if not do.eof:
            raise ValueError('数据超限')
        return res
    zdict = None
    if algo == PK_ALGO_ZDICT:
        if pos >= len(body):
            raise ValueError('数据不完整')
        fp = body[pos]
        pos += 1
        zdict = zdictLookup(fp)
        if zdict is None:
            raise ValueError('DICT')
    do = zlib.decompressobj(-15, zdict) if zdict else zlib.decompressobj(-15)
    res = do.decompress(bytes(body[pos:]), MAX_DECOMPRESS)
    if do.unconsumed_tail:
        raise ValueError('数据超限')
    return res


def wrapPart(fragment, transferId, idx, total):
    body = bytes([ODC_VERSION, PK_FLAG_PART]) + struct.pack('<HBB', transferId, idx, total) + fragment
    return body + struct.pack('<H', zlib.crc32(body) & 0xFFFF)


def tryParsePart(blob):
    """若为分段包返回 (transferId, idx, total, fragment), 否则返回 None"""
    if len(blob) < 8:
        return None
    body = blob[:-2]
    crc = struct.unpack('<H', blob[-2:])[0]
    if zlib.crc32(body) & 0xFFFF != crc:
        raise ValueError('CRC')
    if body[0] != ODC_VERSION:
        raise ValueError('VERSION')
    if not (body[1] & PK_FLAG_PART):
        return None
    transferId, idx, total = struct.unpack('<HBB', body[2:6])
    return (transferId, idx, total, bytes(body[6:]))


def makeCodes(payload, zdict, armorMode, splitGate):
    """payload(明文二进制) -> 一个或多个带前缀的完整码"""
    blob = pack(payload, zdict)
    armor = armorCJK if armorMode == 0 else armorB64
    tag = 'C' if armorMode == 0 else 'A'
    one = ODC_PREFIX + tag + armor(blob)
    if len(one) <= splitGate:
        return [one]
    # 分段: 按装甲后长度反推每段字节数(预留前缀与8字节分段包头/CRC的余量)
    if armorMode == 0:
        chunk = max(32, (splitGate - 8) * 14 // 8 - 16)
    else:
        chunk = max(32, (splitGate - 8) * 3 // 4 - 16)
    frags = [blob[i:i + chunk] for i in range(0, len(blob), chunk)]
    while len(frags) > 255:
        chunk *= 2
        frags = [blob[i:i + chunk] for i in range(0, len(blob), chunk)]
    transferId = int.from_bytes(os.urandom(2), 'big')
    res = []
    for i, frag in enumerate(frags):
        res.append(ODC_PREFIX + tag + armor(wrapPart(frag, transferId, i + 1, len(frags))))
    return res


def dearmorCode(code):
    code = code.strip()
    if not code.startswith(ODC_PREFIX) or len(code) < 6:
        raise ValueError('FORMAT')
    tag = code[4]
    body = code[5:]
    if tag == 'C':
        return dearmorCJK(body)
    if tag == 'A':
        return dearmorB64(body)
    raise ValueError('FORMAT')


# =========================================================
# 数据采集与写入(对接 pcCard 五份存储)
# =========================================================

KNOWN_TEMPLATE_KEYS = ['template', 'checkRules', 'enhanceList', 'mappingRecord', 'noteRecord']


def collectUserData(pcHash, cardNameList=None):
    """从 pcCard 五份存储采集用户数据, cardNameList=None 表示全部"""
    hostKey = 'unity'
    dataAll = OlivaDiceCore.pcCard.dictPcCardData.get(hostKey, {}).get(pcHash, {})
    temAll = OlivaDiceCore.pcCard.dictPcCardTemplate.get(hostKey, {}).get(pcHash, {})
    hiyAll = OlivaDiceCore.pcCard.dictPcCardHiy.get(hostKey, {}).get(pcHash, {})
    mhAll = OlivaDiceCore.pcCard.dictPcCardMH.get(hostKey, {}).get(pcHash, {})
    selAll = OlivaDiceCore.pcCard.dictPcCardSelection.get(hostKey, {}).get(pcHash, {})
    cards = {}
    for name, skills in dataAll.items():
        if cardNameList is not None and name not in cardNameList:
            continue
        if type(skills) is not dict:
            continue
        ti = temAll.get(name, {})
        if type(ti) is not dict:
            ti = {}
        intSkills = {}
        badSkills = {}
        for k, v in skills.items():
            if type(v) is int:
                intSkills[k] = v
            elif type(v) is bool:
                intSkills[k] = int(v)
            else:
                badSkills[k] = v
        extra = {}
        for k, v in ti.items():
            if k not in KNOWN_TEMPLATE_KEYS:
                extra[k] = v
        if badSkills:
            extra['__nonIntSkills'] = badSkills
        hiy = hiyAll.get(name)
        if type(hiy) is not dict or not hiy:
            hiy = None
        mh = False
        if type(mhAll.get(name)) is dict:
            mh = bool(mhAll[name].get('status', False))
        cards[name] = {
            'skills': intSkills,
            'template': ti.get('template'),
            'checkRules': ti.get('checkRules'),
            'enhanceList': ti.get('enhanceList') if ti.get('enhanceList') else None,
            'mappingRecord': ti.get('mappingRecord') if ti.get('mappingRecord') else None,
            'noteRecord': ti.get('noteRecord') if ti.get('noteRecord') else None,
            'hiy': hiy,
            'mh': mh,
            'extra': extra if extra else None,
        }
    selection = selAll.get('selection')
    lockList = selAll.get('lockList', {})
    if cardNameList is not None:
        if selection not in cards:
            selection = next(iter(cards), None)
        lockList = {}
    return {
        'cards': cards,
        'selection': selection if selection in cards else None,
        'lockList': dict(lockList) if type(lockList) is dict else {},
    }


def _uniqueCardName(existing, name):
    if name not in existing:
        return name
    idx = 2
    while True:
        cand = '%s_%s' % (name[:44], idx)
        if cand not in existing:
            return cand
        idx += 1


def writeUserData(pcHash, user, flagForce=False, flagNoLock=False):
    """把 user 数据写入目标 pcHash 的五份存储, 返回统计"""
    hostKey = 'unity'
    for d in (
        OlivaDiceCore.pcCard.dictPcCardData,
        OlivaDiceCore.pcCard.dictPcCardSelection,
        OlivaDiceCore.pcCard.dictPcCardTemplate,
        OlivaDiceCore.pcCard.dictPcCardHiy,
        OlivaDiceCore.pcCard.dictPcCardMH,
    ):
        if hostKey not in d:
            d[hostKey] = {}
        if pcHash not in d[hostKey]:
            d[hostKey][pcHash] = {}
    dataAll = OlivaDiceCore.pcCard.dictPcCardData[hostKey][pcHash]
    temAll = OlivaDiceCore.pcCard.dictPcCardTemplate[hostKey][pcHash]
    hiyAll = OlivaDiceCore.pcCard.dictPcCardHiy[hostKey][pcHash]
    mhAll = OlivaDiceCore.pcCard.dictPcCardMH[hostKey][pcHash]
    selAll = OlivaDiceCore.pcCard.dictPcCardSelection[hostKey][pcHash]
    nameMap = {}
    countNew = 0
    countRename = 0
    countOverwrite = 0
    for name, c in user['cards'].items():
        tmp_name = OlivaDiceCore.pcCard.fixName(str(name))
        if not OlivaDiceCore.pcCard.checkPcName(tmp_name) or tmp_name == '':
            tmp_name = '人物卡'
        if tmp_name in dataAll:
            if flagForce:
                countOverwrite += 1
            else:
                tmp_name = _uniqueCardName(dataAll, tmp_name)
                countRename += 1
        else:
            countNew += 1
        nameMap[name] = tmp_name
        dataAll[tmp_name] = dict(c['skills'])
        ti = {}
        if c.get('template'):
            ti['template'] = c['template']
        if c.get('checkRules'):
            ti['checkRules'] = c['checkRules']
        if c.get('enhanceList'):
            ti['enhanceList'] = list(c['enhanceList'])
        if c.get('mappingRecord'):
            ti['mappingRecord'] = dict(c['mappingRecord'])
        if c.get('noteRecord'):
            ti['noteRecord'] = dict(c['noteRecord'])
        if c.get('extra'):
            for k, v in c['extra'].items():
                if k != '__nonIntSkills':
                    ti[k] = copy.deepcopy(v)
            if '__nonIntSkills' in c['extra'] and type(c['extra']['__nonIntSkills']) is dict:
                for k, v in c['extra']['__nonIntSkills'].items():
                    dataAll[tmp_name][k] = v
        if ti:
            temAll[tmp_name] = ti
        elif tmp_name in temAll:
            temAll.pop(tmp_name)
        if c.get('hiy'):
            hiyAll[tmp_name] = dict(c['hiy'])
        if c.get('mh'):
            mhAll[tmp_name] = {'status': True}
    sel = user.get('selection')
    if sel in nameMap:
        selAll['selection'] = nameMap[sel]
    elif 'selection' not in selAll and nameMap:
        selAll['selection'] = next(iter(nameMap.values()))
    lockApplied = []
    if not flagNoLock:
        lock = user.get('lockList') or {}
        if lock:
            if 'lockList' not in selAll:
                selAll['lockList'] = {}
            for hag, cname in lock.items():
                target = nameMap.get(cname)
                if target is None:
                    continue
                selAll['lockList'][str(hag)] = target
                lockApplied.append(str(hag))
    OlivaDiceCore.pcCard.dataPcCardSave(hostKey, pcHash)
    return {
        'new': countNew,
        'rename': countRename,
        'overwrite': countOverwrite,
        'total': len(nameMap),
        'lockApplied': lockApplied,
        'nameMap': nameMap,
    }


# =========================================================
# 同骰引继码表
# =========================================================

def _getConsole(key, botHash, default):
    res = OlivaDiceCore.console.getConsoleSwitchByHash(key, botHash)
    if type(res) is not int:
        return default
    return res


def cleanPortCode():
    now = time.time()
    for code in list(dictPortCode.keys()):
        expire = dictPortCode[code].get('expire')
        if expire is not None and expire < now:
            dictPortCode.pop(code, None)
    for key in list(dictPortSession.keys()):
        if dictPortSession[key].get('expire', 0) < now:
            dictPortSession.pop(key, None)


def makePortCode(pcHash, botHash):
    cleanPortCode()
    ttl = _getConsole('portCodeTTL', botHash, 86400)
    code = uuid.uuid4().hex[:6].upper()
    while code in dictPortCode:
        code = uuid.uuid4().hex[:6].upper()
    dictPortCode[code] = {
        'pcHash': pcHash,
        'expire': (time.time() + ttl) if ttl > 0 else None,
    }
    return code


def peekPortCodeInfo(code):
    cleanPortCode()
    return dictPortCode.get(str(code).strip().upper())


def peekPortCode(code):
    """校验一个同骰引继码(不消耗), 返回 pcHash 或 None"""
    info = peekPortCodeInfo(code)
    if info is None:
        return None
    return info['pcHash']


def consumePortCode(code):
    """消耗一个同骰引继码(一次性, 成功使用后调用)"""
    dictPortCode.pop(str(code).strip().upper(), None)


# =========================================================
# 命令处理主体
# =========================================================

def _fmt(dictStrCustom, dictTValue, key):
    return OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom[key], dictTValue)


def _reply(plugin_event, dictStrCustom, dictTValue, key):
    OlivaDiceCore.msgReply.replyMsg(plugin_event, _fmt(dictStrCustom, dictTValue, key))


def _getPortExportDir():
    dataDirRoot = OlivaDiceCore.data.dataDirRoot
    exportDir = dataDirRoot + '/unity/extend/portExport'
    OlivaDiceCore.pcCard.releaseDir(exportDir)
    return exportDir


def initPortExportDir():
    _getPortExportDir()


def _cleanupPortExportFiles(botHash):
    fileLimit = _getConsole('portExportFileLimit', botHash, 10)
    if fileLimit <= 0:
        return
    exportDir = _getPortExportDir()
    fileInfoList = []
    for fileName in os.listdir(exportDir):
        if not fileName.startswith('port_export_') or not fileName.endswith('.txt'):
            continue
        filePath = os.path.realpath(exportDir + '/' + fileName)
        if not os.path.isfile(filePath):
            continue
        try:
            fileMTime = os.path.getmtime(filePath)
        except OSError:
            continue
        fileInfoList.append((fileMTime, fileName, filePath))
    fileInfoList.sort(key=lambda item: (item[0], item[1]), reverse=True)
    for _fileMTime, _fileName, filePath in fileInfoList[fileLimit:]:
        try:
            os.remove(filePath)
        except OSError:
            pass


def _writePortGuideFile(pcHash, codes, botHash, sourcePlatform=None, sourceUserId=None):
    exportTimestamp = int(time.time())
    hashSeed = '%s|%s|%s|%s|%s' % (
        pcHash,
        str(sourcePlatform or ''),
        str(sourceUserId or ''),
        str(time.time_ns()),
        str(len(codes)),
    )
    shortHash = '%06X' % (zlib.crc32(hashSeed.encode('utf-8')) & 0xFFFFFF)
    fileName = 'port_export_%s_%s_%s.txt' % (pcHash[:8], exportTimestamp, shortHash)
    filePath = _getPortExportDir() + '/' + fileName
    lineList = [
        'OlivaDice 跨骰引继码导入说明',
        '',
        '来源平台: %s' % str(sourcePlatform or '未知'),
        '来源user_id: %s' % str(sourceUserId or '未知'),
        '导出时间: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exportTimestamp)),
        '',
        '1. 机器人在聊天里直发时只发送引继码正文，不额外附上 .port in 命令前缀。',
        '2. 本文件中每一段都已补全为 .port in ODC1... 格式，可直接复制发送。',
        '3. 本文件中的每一段都是一条完整的引继码，不需要手动拼接。',
        '4. 请复制“第N/M段”标题下方紧随的一整行 .port in ODC1... 内容，并逐条发送给目标骰。',
        '5. 多段码的发送顺序不限；系统会按同一批次的段数自动收集，收齐后立刻开始导入。',
        '6. 如需覆盖同名人物卡，可改用 .port in force 引继码。',
        '7. 如不想恢复群锁定信息，可改用 .port in nolock 引继码。',
        '',
        '以下为引继码正文：',
        '',
    ]
    total = len(codes)
    for idx, code in enumerate(codes, 1):
        lineList.extend([
            '第%s/%s段' % (idx, total),
            '.port in %s' % code,
            '',
        ])
    with open(filePath, 'w', encoding='utf-8') as file_obj:
        file_obj.write('\n'.join(lineList).rstrip() + '\n')
    _cleanupPortExportFiles(botHash)
    return filePath, fileName


def _replyFile(plugin_event, filePath, fileName):
    filePath = os.path.realpath(filePath)
    msgObj = OlivOS.messageAPI.Message_templet(
        'olivos_para',
        [OlivOS.messageAPI.PARA.file(file=filePath, path=filePath, name=fileName)],
    )
    plugin_event.reply(msgObj)


def _parseAccountToken(token):
    """兼容旧写法 '平台:账号' -> (user_id, platform) 或 None"""
    if ':' not in token:
        return None
    platform, userId = token.split(':', 1)
    platform = platform.strip()
    userId = userId.strip()
    if platform == '' or userId == '':
        return None
    return (userId, platform)


def _getPortPlatformList():
    try:
        platformList = OlivOS.accountMetadataAPI.accountTypeDataList_platform
    except Exception:
        platformList = []
    return sorted([str(platform) for platform in platformList], key=len, reverse=True)


def _matchPortPlatform(token):
    token = str(token).strip()
    if token == '':
        return None
    tokenLower = token.lower()
    for platform in _getPortPlatformList():
        if tokenLower == platform.lower():
            return platform
    return None


def _parseAccountGreedyToken(token):
    """兼容 logger 风格尾部贪婪匹配: 平台+账号 或 账号+平台"""
    token = str(token).strip()
    if token == '':
        return None
    tokenLower = token.lower()
    for platform in _getPortPlatformList():
        platformLower = platform.lower()
        if tokenLower.startswith(platformLower) and len(token) > len(platform):
            userId = token[len(platform):].strip()
            if userId != '':
                return (userId, platform)
        if tokenLower.endswith(platformLower) and len(token) > len(platform):
            userId = token[:-len(platform)].strip()
            if userId != '':
                return (userId, platform)
    return None


def _splitAccountArgs(tokens):
    """从参数中拆出指定账号, 优先兼容旧写法, 新写法要求放在尾部"""
    rest = list(tokens)
    suffixTokens = []
    restNew = []
    for tok in rest:
        if str(tok).strip().lower() in ['split']:
            suffixTokens.append(tok)
        else:
            restNew.append(tok)
    rest = restNew
    for idx, tok in enumerate(rest):
        acct = _parseAccountToken(tok)
        if acct is not None:
            return acct, rest[:idx] + rest[idx + 1:] + suffixTokens
    if len(rest) >= 2:
        platform = _matchPortPlatform(rest[-2])
        userId = str(rest[-1]).strip()
        if platform is not None and userId != '':
            return (userId, platform), rest[:-2] + suffixTokens
        platform = _matchPortPlatform(rest[-1])
        userId = str(rest[-2]).strip()
        if platform is not None and userId != '':
            return (userId, platform), rest[:-2] + suffixTokens
    if rest:
        acct = _parseAccountGreedyToken(rest[-1])
        if acct is not None:
            return acct, rest[:-1] + suffixTokens
    return None, rest + suffixTokens


def _ttlText(botHash):
    ttl = _getConsole('portCodeTTL', botHash, 86400)
    if ttl <= 0:
        return '永久'
    if ttl % 3600 == 0:
        return '%s小时' % (ttl // 3600)
    return '%s秒' % ttl


def _exportUser(plugin_event, dictStrCustom, dictTValue, pcHash, args, botHash, sourcePlatform=None, sourceUserId=None):
    """处理 code out 的实际导出, args 为剩余参数 token 列表; 成功发码返回 True"""
    splitGate = _getConsole('portSplitGate', botHash, 550)
    flagAll = False
    flagSplit = False
    cardNames = []
    for tok in args:
        tok_l = tok.lower()
        if tok_l == 'all':
            flagAll = True
        elif tok_l == 'split':
            flagSplit = True
        else:
            cardNames.append(tok)
    if flagAll:
        user = collectUserData(pcHash)
    elif cardNames:
        userAll = collectUserData(pcHash)
        missing = [x for x in cardNames if x not in userAll['cards']]
        if missing:
            dictTValue['tPcName'] = '、'.join(missing)
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortCardNotFound')
            return False
        user = collectUserData(pcHash, cardNameList=cardNames)
    else:
        user = collectUserData(pcHash)
    if not user['cards']:
        _reply(plugin_event, dictStrCustom, dictTValue, 'strPortNoCard')
        return False
    payload = encodeUser(user, forceLiteral=True)
    codes = makeCodes(payload, None, 0, splitGate)
    dictTValue['tPortCardCount'] = str(len(user['cards']))
    dictTValue['tPortCardList'] = '、'.join(user['cards'].keys())
    if len(codes) == 1:
        dictTValue['tPortCode'] = codes[0]
        dictTValue['tPortLen'] = str(len(codes[0]))
        _reply(plugin_event, dictStrCustom, dictTValue, 'strPortOutResult')
    elif flagSplit:
        dictTValue['tPortPartCount'] = str(len(codes))
        head = _fmt(dictStrCustom, dictTValue, 'strPortOutResultSplit')
        OlivaDiceCore.msgReply.replyMsg(plugin_event, head + '{SPLIT}' + '{SPLIT}'.join(codes))
    else:
        filePath, fileName = _writePortGuideFile(
            pcHash, codes, botHash, sourcePlatform=sourcePlatform, sourceUserId=sourceUserId
        )
        dictTValue['tPortPartCount'] = str(len(codes))
        dictTValue['tPortFileName'] = fileName
        dictTValue['tPortFilePath'] = filePath
        _reply(plugin_event, dictStrCustom, dictTValue, 'strPortOutResultFile')
        _replyFile(plugin_event, filePath, fileName)
    return True


def _importBlob(plugin_event, dictStrCustom, dictTValue, pcHash, blob, flagForce, flagNoLock):
    """单体封包 -> 解码写入并回执, 返回 'done';
    分段包 -> 收集, 未集齐返回 'part'(不回执, 由调用方决定是否提示进度)"""
    part = tryParsePart(blob)
    if part is not None:
        transferId, idx, total, fragment = part
        cleanPortCode()
        sess = dictPortSession.get(pcHash)
        if sess is None or sess.get('transferId') != transferId or sess.get('total') != total:
            sess = {'transferId': transferId, 'total': total, 'parts': {}}
            dictPortSession[pcHash] = sess
        sess['parts'][idx] = fragment
        sess['expire'] = time.time() + SESSION_TTL
        missing = [str(i) for i in range(1, total + 1) if i not in sess['parts']]
        if missing:
            dictTValue['tPortPartIdx'] = str(len(sess['parts']))
            dictTValue['tPortPartTotal'] = str(total)
            dictTValue['tPortPartMissing'] = '、'.join(missing)
            return 'part'
        blob = b''.join(sess['parts'][i] for i in range(1, total + 1))
        dictPortSession.pop(pcHash, None)
    payload = unpack(blob)
    user = decodeUser(payload)
    if not user['cards']:
        _reply(plugin_event, dictStrCustom, dictTValue, 'strPortInEmpty')
        return 'done'
    res = writeUserData(pcHash, user, flagForce=flagForce, flagNoLock=flagNoLock)
    dictTValue['tPortCardCount'] = str(res['total'])
    dictTValue['tPortNewCount'] = str(res['new'])
    dictTValue['tPortRenameCount'] = str(res['rename'])
    dictTValue['tPortOverwriteCount'] = str(res['overwrite'])
    dictTValue['tPortCardList'] = '、'.join(res['nameMap'].values())
    dictTValue['tPortLockCount'] = str(len(res['lockApplied']))
    _reply(plugin_event, dictStrCustom, dictTValue, 'strPortInDone')
    return 'done'


def replyPort(plugin_event, cmd_str, dictStrCustom, dictTValue, hagID, flagIsFromMaster):
    """`.port` 命令入口(msgReply.py 只调用本函数)"""
    botHash = plugin_event.bot_info.hash
    if _getConsole('portEnable', botHash, 1) != 1:
        return
    tmp_userId = plugin_event.data.user_id
    tmp_platform = plugin_event.platform['platform']
    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_userId, tmp_platform)
    tokens = str(cmd_str).strip().split()
    if not tokens:
        _reply(plugin_event, dictStrCustom, dictTValue, 'strPortUsage')
        return
    sub = tokens[0].lower()
    args = tokens[1:]

    # ---------- .port code : 生成两种引继码 ----------
    if sub == 'code':
        flagOut = False
        if args and args[0].lower() == 'out':
            flagOut = True
            args = args[1:]
        target_pcHash = tmp_pcHash
        sourceUserId = str(tmp_userId)
        sourcePlatform = str(tmp_platform)
        acct, rest = _splitAccountArgs(args)
        if acct is not None:
            if not flagIsFromMaster:
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortNeedMaster')
                return
            target_pcHash = OlivaDiceCore.pcCard.getPcHash(acct[0], acct[1])
            sourceUserId = str(acct[0])
            sourcePlatform = str(acct[1])
            dictTValue['tPortTarget'] = '平台[%s] 账号[%s]' % (acct[1], acct[0])
        if flagOut:
            # 普通用户凭别人的同骰码导出对方数据
            codeArg = None
            for tok in list(rest):
                if len(tok) == 6 and all(ch in '0123456789ABCDEFabcdef' for ch in tok):
                    codeArg = tok
                    rest.remove(tok)
                    break
            if codeArg is not None:
                codeInfo = peekPortCodeInfo(codeArg)
                if codeInfo is None:
                    _reply(plugin_event, dictStrCustom, dictTValue, 'strPortCodeInvalid')
                    return
                target_pcHash = codeInfo['pcHash']
                if codeInfo.get('userId') is not None:
                    sourceUserId = str(codeInfo['userId'])
                if codeInfo.get('platform') is not None:
                    sourcePlatform = str(codeInfo['platform'])
                if sourcePlatform not in ['', 'None'] and sourceUserId not in ['', 'None']:
                    dictTValue['tPortTarget'] = '平台[%s] 账号[%s]' % (sourcePlatform, sourceUserId)
            if target_pcHash != tmp_pcHash and not collectUserData(target_pcHash)['cards']:
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortTargetNoCard')
                return
            if _exportUser(
                plugin_event,
                dictStrCustom,
                dictTValue,
                target_pcHash,
                rest,
                botHash,
                sourcePlatform=sourcePlatform,
                sourceUserId=sourceUserId,
            ):
                if codeArg is not None:
                    consumePortCode(codeArg)
            return
        # 同骰码
        if not collectUserData(target_pcHash)['cards']:
            if target_pcHash != tmp_pcHash:
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortTargetNoCard')
            else:
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortNoCard')
            return
        code = makePortCode(target_pcHash, botHash)
        dictPortCode[code]['userId'] = sourceUserId
        dictPortCode[code]['platform'] = sourcePlatform
        dictTValue['tPortCode'] = code
        dictTValue['tPortTTL'] = _ttlText(botHash)
        if target_pcHash != tmp_pcHash:
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortCodeSameOther')
        else:
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortCodeSame')
        return

    # ---------- .port pull : 同骰码兑换 ----------
    if sub == 'pull':
        flagForce = False
        code = None
        pullArgs = []
        for tok in args:
            if tok.lower() == 'force':
                flagForce = True
            else:
                pullArgs.append(tok)
        src_pcHash = None
        flagByCode = False
        if flagIsFromMaster:
            acct, pullArgs = _splitAccountArgs(pullArgs)
            if acct is not None:
                src_pcHash = OlivaDiceCore.pcCard.getPcHash(acct[0], acct[1])
                dictTValue['tPortTarget'] = '平台[%s] 账号[%s]' % (acct[1], acct[0])
        if pullArgs:
            code = pullArgs[0]
        if code is None and src_pcHash is None:
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortUsage')
            return
        if src_pcHash is None:
            codeInfo = peekPortCodeInfo(code)
            if codeInfo is not None:
                src_pcHash = codeInfo['pcHash']
                flagByCode = True
                if codeInfo.get('platform') is not None and codeInfo.get('userId') is not None:
                    dictTValue['tPortTarget'] = '平台[%s] 账号[%s]' % (
                        str(codeInfo['platform']), str(codeInfo['userId'])
                    )
        if src_pcHash is None:
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortCodeInvalid')
            return
        if src_pcHash == tmp_pcHash:
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortPullSelf')
            return
        user = collectUserData(src_pcHash)
        if not user['cards']:
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortTargetNoCard')
            return
        res = writeUserData(tmp_pcHash, user, flagForce=flagForce, flagNoLock=False)
        if flagByCode:
            consumePortCode(code)
        dictTValue['tPortCardCount'] = str(res['total'])
        dictTValue['tPortNewCount'] = str(res['new'])
        dictTValue['tPortRenameCount'] = str(res['rename'])
        dictTValue['tPortOverwriteCount'] = str(res['overwrite'])
        dictTValue['tPortCardList'] = '、'.join(res['nameMap'].values())
        _reply(plugin_event, dictStrCustom, dictTValue, 'strPortPullDone')
        return

    # ---------- .port in : 跨骰数据码导入 ----------
    if sub == 'in':
        flagForce = False
        flagNoLock = False
        codeTokens = []
        for tok in args:
            tok_l = tok.lower()
            if tok_l == 'force':
                flagForce = True
            elif tok_l == 'nolock':
                flagNoLock = True
            elif tok.startswith(ODC_PREFIX):
                codeTokens.append(tok)
            elif len(tok) == 6 and all(ch in '0123456789ABCDEFabcdef' for ch in tok):
                # 拿同骰码走错入口, 给出精准提示
                dictTValue['tPortCode'] = tok.upper()
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortInButSameCode')
                return
        if not codeTokens:
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortUsage')
            return
        try:
            status = None
            for codeTok in codeTokens:
                status = _importBlob(
                    plugin_event, dictStrCustom, dictTValue, tmp_pcHash,
                    dearmorCode(codeTok), flagForce, flagNoLock,
                )
            if status == 'part':
                # 仅在处理完本条消息中的全部码后仍未集齐时提示一次进度
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortInPart')
        except ValueError as e:
            reason = str(e)
            if reason == 'CRC':
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortCrcError')
            elif reason == 'VERSION':
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortVersionError')
            elif reason == 'DICT':
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortDictError')
            elif reason == 'FORMAT':
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortBadFormat')
            else:
                dictTValue['tPortError'] = reason
                _reply(plugin_event, dictStrCustom, dictTValue, 'strPortInError')
        except Exception:
            dictTValue['tPortError'] = '未知错误'
            _reply(plugin_event, dictStrCustom, dictTValue, 'strPortInError')
        return

    _reply(plugin_event, dictStrCustom, dictTValue, 'strPortUsage')
