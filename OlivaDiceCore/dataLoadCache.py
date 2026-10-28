# -*- encoding: utf-8 -*-
r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   dataLoadCache.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2026, OlivOS-Team
@Desc      :   人物卡/用户记录启动加载的快照缓存
"""

# 启动时人物卡与用户记录各有数万个小 JSON 文件，逐个打开文件的系统调用开销远大于解析本身。
# 这里把上一次加载的内容（去掉缩进空白的 JSON 文本）连同文件状态（修改时间、大小、创建/变更时间）
# 存成一个快照文件。下次加载时只列目录取状态：状态与快照一致的文件直接解析快照里的文本，不再打开；
# 新增或状态变化的文件照常读取解析。快照只是缓存，原始 JSON 文件仍是唯一的数据来源：
# 快照丢失、损坏、校验失败或格式版本变化时自动退回逐个读取，并在本次加载后重建。
# 解析失败的文件不进快照，每次照常读取并记录错误日志，与原有行为一致。
#
# 解析仍用 json.loads：得到的对象结构与逐个读取完全相同，常驻内存也一致
# （换成 marshal/pickle 解析虽快约 2 秒，但对象布局不同，常驻内存会多出十几 MB）。
#
# 内存：快照按条目顺序流式读取，同时只保留有限几条；新快照边加载边写入临时文件，
# 加载结束时原子替换。加载过程不会额外常驻整份快照。
#
# 一致性：文件状态（修改时间+大小+创建时间）在 Windows 上不能 100% 证明内容没变——
# 内容改了、大小不变、修改时间又被改回原值（同步/还原工具、os.utime）时三项都对得上。
# 所以状态一致只是「候选命中」，还要用原文件做内容核对：
#  - 每次加载按轮转顺序核对 1/snapshotVerifyRounds 的命中文件（读原文件比对 CRC），
#    snapshotVerifyRounds 次加载即把全部文件完整核对一遍；
#  - 修改时间在 snapshotVerifyRecentSeconds 之内的文件每次都核对；
#  - 任何一个文件核对不一致：该文件改用原文件内容，且本次之后整份快照作废重建
#    （发现过一次说明有工具在绕过修改时间，其余条目也不再信任）。
# 核对读的是原始字节、比对的是原始字节的 CRC，与解析无关。

import OlivaDiceCore

import collections
import gc
import json
import os
import stat
import struct
import time
import zlib

cacheDirRoot = './plugin/cache/OlivaDice'

snapshotMagic = b'OlivaDiceDataLoadSnapshot|5|json\n'
jsonDumpSeparators = (',', ':')
# 路径长度、修改时间、文件大小、创建/变更时间、内容长度、内容 CRC32、原文件 CRC32
snapshotEntryHead = struct.Struct('<IqqqqII')
# 内容核对：每次加载核对的比例（1/N）与「最近修改」的时间窗
snapshotVerifyRounds = 8
snapshotVerifyRecentSeconds = 24 * 3600
snapshotReadBuffer = 1024 * 1024
# 请求的路径不在当前位置时最多向后预读的条目数，以及预读缓冲的上限
snapshotLookahead = 256
snapshotPendingLimit = 1024

flagNormCase = os.name == 'nt'


def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# 目录项状态：普通文件为 (修改时间, 大小, 创建/变更时间)；存在但不是普通文件或取不到状态时为 False
flagEntryOther = False


def getEntryKey(entry):
    # Windows 下 DirEntry.stat() 直接复用列目录时取到的信息，不额外访问文件；
    # 用 st_mode 判断普通文件，省掉 is_file() 的一次调用
    try:
        st = entry.stat()
        if not stat.S_ISREG(st.st_mode):
            return flagEntryOther
        return (st.st_mtime_ns, st.st_size, st.st_ctime_ns)
    except OSError:
        return flagEntryOther


def readFileBytes(path):
    """读取文件原文；文件在列目录之后被删除时返回 None

    Windows 下另一处正在用 os.replace 原子替换同一个文件时，打开会短暂得到 PermissionError，
    这里与写入侧（writeUserConfigDataAtomic）对称地短暂重试。
    """
    for tmp_retry in range(10):
        try:
            with open(path, 'rb') as data_f:
                return data_f.read()
        except FileNotFoundError:
            return None
        except PermissionError:
            if tmp_retry >= 9:
                raise
            time.sleep(0.02)
    return None


def isTempFileName(name):
    """写入侧原子替换使用的临时文件（<文件名>.<随机>.tmp），不是数据文件"""
    return name.endswith('.tmp')


def scanDir(dir_path):
    """列目录，返回与 os.listdir 相同顺序的文件名列表，以及文件名到目录项状态的映射

    只保留比较所需的状态元组，不保留 DirEntry 对象（数万个文件时能省下一半内存）。
    """
    names = []
    entries = {}
    with os.scandir(dir_path) as it:
        for entry in it:
            # 原子替换写入过程中的临时文件随时可能消失，内容也不完整，不当作数据加载
            if isTempFileName(entry.name):
                continue
            names.append(entry.name)
            entries[entry.name.lower() if flagNormCase else entry.name] = getEntryKey(entry)
    return names, entries


def getScanEntry(entries, name):
    """返回目录项状态；文件不存在时返回 None"""
    if flagNormCase:
        return entries.get(name.lower())
    return entries.get(name)


def jsonDataParseSafe(data, dataType, dataName):
    """与原 jsonDataLoadSafe 相同的容错语义：解码或解析失败时记录日志并返回空字典

    原版按文本模式读取（会把 CRLF 换成 LF），JSON 中字符串内不允许出现裸换行，
    所以直接解码字节与文本模式读取得到的解析结果相同。
    """
    try:
        return json.loads(str(data, 'utf-8')), True
    except Exception as e:
        tmp_log_str = OlivaDiceCore.msgCustomManager.formatReplySTRConst(
            OlivaDiceCore.msgCustom.dictStrConst['strInitDataError'],
            {'tInitDataType': dataType, 'tInitDataName': dataName, 'tResult': str(e)},
        )
        OlivaDiceCore.msgReply.globalLog(3, tmp_log_str, [('OlivaDice', 'default'), ('Init', 'default')])
        return {}, False


def getVerifyRound(snapshot_path):
    try:
        with open(snapshot_path + '.round', 'r', encoding='utf-8') as round_f:
            return int(round_f.read().strip()) % snapshotVerifyRounds
    except (OSError, ValueError):
        return 0


def setVerifyRound(snapshot_path, value):
    try:
        releaseDir(os.path.dirname(snapshot_path))
        with open(snapshot_path + '.round', 'w', encoding='utf-8') as round_f:
            round_f.write(str(value))
    except OSError:
        pass


class pauseGC(object):
    """批量加载期间暂停循环垃圾回收

    一次性创建数十万个 dict/list，会反复触发对新对象的全量扫描，而这些对象都不会成为垃圾。
    退出时恢复进入前的状态，不影响原本就关闭了 GC 的场景。
    """

    def __enter__(self):
        self.flagEnabled = gc.isenabled()
        gc.disable()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.flagEnabled:
            gc.enable()
        return False


class DataLoadSnapshot(object):
    """按「加载顺序」读写的快照

    目录的遍历顺序在两次加载之间通常不变，所以旧快照按条目顺序流式读取：
    请求的路径正好是下一条时直接使用；不是时（新增、删除）向后预读一小段放进有上限的缓冲，
    之后的请求先查缓冲。缓冲里一直没被用到的条目对应已删除的文件，超过上限时丢弃。
    内存里同时保留的快照条目不超过 snapshotPendingLimit 条。
    """

    def __init__(self, name, dataType):
        self.name = name
        self.dataType = dataType
        self.path = cacheDirRoot + '/' + name + '.snapshot'
        self.tmpPath = self.path + '.tmp'
        self.countHit = 0
        self.countRead = 0
        self.countWrite = 0
        self.countOld = 0
        self.countVerify = 0
        self.countMismatch = 0
        self.verifyRound = getVerifyRound(self.path)
        self.timeNow = time.time()
        self.oldFile = None
        self.oldNext = None
        self.oldDone = True
        self.flagOldValid = False
        self.oldPending = collections.OrderedDict()
        self.newFile = None
        self.flagWriteFailed = False
        self.__openOld()
        self.__openNew()

    def __openOld(self):
        try:
            self.oldFile = open(self.path, 'rb', buffering=snapshotReadBuffer)
            if self.oldFile.read(len(snapshotMagic)) != snapshotMagic:
                self.__closeOld()
                return
            self.oldDone = False
            self.flagOldValid = True
            self.__advanceOld()
        except OSError:
            self.__closeOld()

    def __closeOld(self):
        self.oldDone = True
        self.oldNext = None
        if self.oldFile is not None:
            try:
                self.oldFile.close()
            except OSError:
                pass
        self.oldFile = None

    def __advanceOld(self):
        """读出下一条旧快照条目放到 oldNext；读到结尾或格式错误时结束读取"""
        if self.oldDone:
            self.oldNext = None
            return
        try:
            head = self.oldFile.read(snapshotEntryHead.size)
            if len(head) == 0:
                self.__closeOld()
                return
            if len(head) != snapshotEntryHead.size:
                raise ValueError('snapshot truncated')
            path_len, mtime_ns, size, ctime_ns, data_len, crc, file_crc = snapshotEntryHead.unpack(head)
            path_bytes = self.oldFile.read(path_len)
            data = self.oldFile.read(data_len)
            if len(path_bytes) != path_len or len(data) != data_len:
                raise ValueError('snapshot truncated')
            self.countOld += 1
            self.oldNext = (str(path_bytes, 'utf-8'), (mtime_ns, size, ctime_ns), data, crc, file_crc)
        except Exception:
            # 截断或格式错误：已读出的条目仍各自经过 CRC 校验后才会使用，剩余部分作废
            self.flagOldValid = False
            self.__closeOld()

    def __takeOld(self, path):
        """取出 path 对应的旧条目，找不到返回 None"""
        old = self.oldPending.pop(path, None)
        if old is not None:
            return old
        if self.oldNext is not None and self.oldNext[0] == path:
            old = self.oldNext
            self.__advanceOld()
            return old
        # 不在当前位置：可能是新增文件，也可能前面有已删除文件的条目。向后预读一小段放进缓冲
        for _ in range(snapshotLookahead):
            if self.oldNext is None:
                return None
            if self.oldNext[0] == path:
                old = self.oldNext
                self.__advanceOld()
                return old
            self.oldPending[self.oldNext[0]] = self.oldNext
            if len(self.oldPending) > snapshotPendingLimit:
                self.oldPending.popitem(last=False)
            self.__advanceOld()
        return None

    def __openNew(self):
        try:
            releaseDir(cacheDirRoot)
            self.newFile = open(self.tmpPath, 'wb')
            self.newFile.write(snapshotMagic)
        except OSError as e:
            self.newFile = None
            self.flagWriteFailed = True
            self.__logWriteFailed(e)

    def __writeNew(self, path, key, data, crc, file_crc):
        if self.newFile is None:
            return
        try:
            path_bytes = path.encode('utf-8')
            self.newFile.write(
                snapshotEntryHead.pack(len(path_bytes), key[0], key[1], key[2], len(data), crc, file_crc)
            )
            self.newFile.write(path_bytes)
            self.newFile.write(data)
            self.countWrite += 1
        except OSError as e:
            self.__abortNew()
            self.flagWriteFailed = True
            self.__logWriteFailed(e)

    def __abortNew(self):
        if self.newFile is not None:
            try:
                self.newFile.close()
            except OSError:
                pass
        self.newFile = None
        try:
            if os.path.exists(self.tmpPath):
                os.unlink(self.tmpPath)
        except OSError:
            pass

    def __logWriteFailed(self, e):
        OlivaDiceCore.msgReply.globalLog(
            3, '写入数据加载缓存失败[%s]：%s' % (self.path, str(e)), [('OlivaDice', 'default'), ('Init', 'default')]
        )

    def __needVerify(self, path, key):
        """命中候选是否需要用原文件核对内容"""
        if self.timeNow - key[0] / 1e9 < snapshotVerifyRecentSeconds:
            return True
        return zlib.crc32(path.encode('utf-8')) % snapshotVerifyRounds == self.verifyRound

    def load(self, path, key, dataName):
        """返回文件的解析结果；目录项状态与快照一致、校验通过、且（需要时）内容核对一致时使用快照

        key 为 scanDir 记录的目录项状态；为 False（取不到状态）时不使用快照、也不写入快照。
        """
        if not key:
            key = None
        data = None
        if key is not None:
            old = self.__takeOld(path)
            if old is not None and old[1] == key:
                try:
                    if zlib.crc32(old[2]) == old[3]:
                        flag_use = True
                        if self.__needVerify(path, key):
                            self.countVerify += 1
                            data = readFileBytes(path)
                            if data is None or zlib.crc32(data) != old[4]:
                                # 状态一致但内容不同：本条改用原文件，并让整份快照作废
                                flag_use = False
                                self.countMismatch += 1
                        if flag_use:
                            res = json.loads(str(old[2], 'utf-8'))
                            self.countHit += 1
                            self.__writeNew(path, key, old[2], old[3], old[4])
                            return res
                except Exception:
                    pass
        if data is None:
            data = readFileBytes(path)
        if data is None:
            # 列目录之后文件被删除：与「打开前就不存在」一致，按空记录处理，不进快照
            self.countRead += 1
            return {}
        self.countRead += 1
        res, flag_ok = jsonDataParseSafe(data, self.dataType, dataName)
        # 读取过程中文件被改动时大小会对不上，这种情况不写入快照，下次重新读取
        if flag_ok and key is not None and len(data) == key[1]:
            try:
                payload = json.dumps(res, ensure_ascii=False, separators=jsonDumpSeparators).encode('utf-8')
                # 重新序列化必须能还原出同样的结果（例如浮点、超大整数、重复键等边界情况），否则不进快照
                if json.loads(str(payload, 'utf-8')) == res:
                    self.__writeNew(path, key, payload, zlib.crc32(payload), zlib.crc32(data))
            except (ValueError, TypeError, RecursionError):
                pass
        return res

    def finish(self):
        """记录命中情况；有变化时用新快照原子替换旧快照，没有变化时保留旧快照不重写"""
        OlivaDiceCore.msgReply.globalLog(
            2,
            '[%s]数据加载缓存：命中[%d]个文件，读取[%d]个文件，内容核对[%d]个文件' % (
                self.dataType, self.countHit, self.countRead, self.countVerify
            ),
            [('OlivaDice', 'default'), ('Init', 'default')],
        )
        if self.countMismatch > 0:
            OlivaDiceCore.msgReply.globalLog(
                3,
                '[%s]数据加载缓存：发现[%d]个文件修改时间未变但内容已变，已改用原文件，缓存将整体重建' % (
                    self.dataType, self.countMismatch
                ),
                [('OlivaDice', 'default'), ('Init', 'default')],
            )
        # 旧快照里剩下的条目对应已删除的文件，读到结尾才能知道条目数是否与本次一致
        while self.oldNext is not None:
            self.__advanceOld()
        self.oldPending.clear()
        flag_old_complete = self.flagOldValid
        self.__closeOld()
        flag_changed = self.countRead > 0 or self.countOld != self.countWrite or not flag_old_complete
        setVerifyRound(self.path, (self.verifyRound + 1) % snapshotVerifyRounds)
        if self.newFile is None:
            return
        if self.countMismatch > 0:
            # 有文件绕过了修改时间：本次写出的新快照里其它条目同样不可信，直接删掉，下次全部重读
            self.__abortNew()
            try:
                if os.path.exists(self.path):
                    os.unlink(self.path)
            except OSError as e:
                self.__logWriteFailed(e)
            return
        try:
            self.newFile.close()
            self.newFile = None
            if flag_changed:
                os.replace(self.tmpPath, self.path)
            else:
                os.unlink(self.tmpPath)
        except OSError as e:
            self.__abortNew()
            self.__logWriteFailed(e)
