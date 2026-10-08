# -*- encoding: utf-8 -*-
r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   msgCustomManager.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2026, OlivOS-Team
@Desc      :   None
"""

import OlivOS
import OlivaDiceCore

import os
import sys
import json
import random


def getDictStrCustomDefault():
    # 已加载模块的 dictStrCustom 即为默认回复；后加载模块覆盖同名键
    result = {}
    try:
        for key, value in OlivaDiceCore.msgCustom.dictStrCustom.items():
            if isinstance(key, str) and isinstance(value, str):
                result[key] = value
    except Exception:
        pass
    for module in list(sys.modules.values()):
        try:
            values = getattr(getattr(module, 'msgCustom', None), 'dictStrCustom', None)
            if type(values) is not dict:
                continue
            for key, value in values.items():
                if isinstance(key, str) and isinstance(value, str):
                    result[key] = value
        except Exception:
            continue
    return result


def pruneMsgCustomByBotHash(botHash, defaults=None):
    # 与默认完全一致的自定义条目直接删掉，并按默认重新加载
    if defaults is None:
        defaults = getDictStrCustomDefault()
    if botHash not in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict:
        return False
    updates = OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash]
    if type(updates) is not dict:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = {}
        return True
    changed = False
    for key in list(updates.keys()):
        value = updates[key]
        if isinstance(value, str) and key in defaults and value == defaults[key]:
            del updates[key]
            if botHash in OlivaDiceCore.msgCustom.dictStrCustomDict:
                OlivaDiceCore.msgCustom.dictStrCustomDict[botHash][key] = defaults[key]
            changed = True
    return changed


def pruneAndSaveMsgCustom():
    # 其它模块 init 之后再清一次，才能对上 Joy/Master 等默认回复
    defaults = getDictStrCustomDefault()
    for botHash in list(OlivaDiceCore.msgCustom.dictStrCustomUpdateDict.keys()):
        if pruneMsgCustomByBotHash(botHash, defaults=defaults):
            saveMsgCustomByBotHash(botHash, defaults=defaults)


def setMsgCustomByBotHash(botHash, key, value):
    # 写成默认值时不落盘，删掉该条目后重新加载默认回复
    if botHash not in OlivaDiceCore.msgCustom.dictStrCustomDict:
        OlivaDiceCore.msgCustom.dictStrCustomDict[botHash] = OlivaDiceCore.msgCustom.dictStrCustom.copy()
    if botHash not in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = {}
    if type(OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash]) is not dict:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = {}
    defaults = getDictStrCustomDefault()
    if isinstance(value, str) and key in defaults and value == defaults[key]:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash].pop(key, None)
        OlivaDiceCore.msgCustom.dictStrCustomDict[botHash][key] = defaults[key]
    else:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash][key] = value
        OlivaDiceCore.msgCustom.dictStrCustomDict[botHash][key] = value
    saveMsgCustomByBotHash(botHash, defaults=defaults)


def initMsgCustom(bot_info_dict):
    for bot_info_dict_this in bot_info_dict:
        OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this] = {}
        OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this] = OlivaDiceCore.msgCustom.dictStrCustom.copy()
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    botHash_list = os.listdir(OlivaDiceCore.data.dataDirRoot)
    defaults = getDictStrCustomDefault()
    for botHash_list_this in botHash_list:
        botHash = botHash_list_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
        customReplyDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
        customReplyFile = 'customReply.json'
        customReplyPath = customReplyDir + '/' + customReplyFile
        try:
            with open(customReplyPath, 'r', encoding='utf-8') as customReplyPath_f:
                OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = json.loads(customReplyPath_f.read())
                OlivaDiceCore.msgCustom.dictStrCustomDict[botHash].update(
                    OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash]
                )
                pruneMsgCustomByBotHash(botHash, defaults=defaults)
        except Exception:
            continue


def saveMsgCustom(bot_info_dict):
    defaults = getDictStrCustomDefault()
    for botHash in bot_info_dict:
        saveMsgCustomByBotHash(botHash, defaults=defaults)


def saveMsgCustomByBotHash(botHash, defaults=None):
    pruneMsgCustomByBotHash(botHash, defaults=defaults)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
    customReplyDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
    customReplyFile = 'customReply.json'
    customReplyPath = customReplyDir + '/' + customReplyFile
    if botHash not in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = {}
    if type(OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash]) is not dict:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = {}
    with open(customReplyPath, 'w', encoding='utf-8') as customReplyPath_f:
        customReplyPath_f.write(
            json.dumps(OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash], ensure_ascii=False, indent=4)
        )


def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def formatReplySTR(data: str, valDict: dict, flagCross: bool = True, flagSplit: bool = True):
    res: str = data
    if flagSplit:
        res = random.choice(list(res.split('|')))
        res = res.replace('{DEVIDE}', '|')
        res = res.replace('{OR}', '|')
    if flagCross:
        res = OlivaDiceCore.crossHook.dictHookFunc['msgFormatHook'](res, valDict)
    res = formatReplySTRReplace(res, valDict)
    return res


def formatReplySTRConst(data: str, valDict: dict):
    res = data
    res = res.format(**valDict)
    return res


# 用状态机实现高宽容度的变量引用
# 替代Python内置Format
def formatReplySTRReplace(data: str, valDict: dict, flagPure: bool = False):
    raw = data
    res = ''
    reg_res = ''
    reg_key = ''
    flagType = 'str'
    for i in raw:
        if flagType == 'str':
            if i == '{':
                flagType = 'left'
            else:
                reg_res += i
                flagType = 'str'
        elif flagType == 'left':
            if i == '}':
                reg_key = ''
                flagType = 'right'
            else:
                reg_key = i
                flagType = 'key'
        elif flagType == 'key':
            if i == '}':
                flag_hit = False
                # 变量表替换
                if not flag_hit and reg_key in valDict and type(valDict[reg_key] is str):
                    reg_res += str(valDict[reg_key])
                    flag_hit = True
                # 牌堆抽取
                if not flag_hit and not flagPure:
                    tmp_bot_hash = 'unity'
                    plugin_event = None
                    if 'tBotHash' in valDict:
                        tmp_bot_hash = valDict['tBotHash']
                    if 'vValDict' in valDict and 'vPluginEvent' in valDict['vValDict']:
                        plugin_event = valDict['vValDict']['vPluginEvent']
                    reg_res_this = OlivaDiceCore.drawCard.draw(
                        key_str=reg_key, bot_hash=tmp_bot_hash, flag_need_give_back=True, plugin_event=plugin_event
                    )
                    if reg_res_this is not None:
                        reg_res += reg_res_this
                        flag_hit = True
                # 转义字符处理（如 {\f} -> 分页符）
                if not flag_hit:
                    reg_key_unescaped = processEscapeSequences(reg_key)
                    if reg_key_unescaped != reg_key:
                        # 如果发生了转义转换，直接输出转义后的字符
                        reg_res += reg_key_unescaped
                        flag_hit = True
                # 缺省确保原样返回
                if not flag_hit:
                    reg_res += '{%s}' % reg_key
                flagType = 'right'
            else:
                reg_key += i
                flagType = 'key'
        elif flagType == 'right':
            reg_key = ''
            if i == '{':
                flagType = 'left'
            else:
                reg_res += i
                flagType = 'str'
    if flagType == 'key':
        reg_res += '{%s' % reg_key
    res = reg_res
    return res


def processEscapeSequences(data: str):
    """
    处理字符串中的转义序列
    """
    res = data
    escape_map = {
        '\\n': '\n',
        '\\r': '\r',
        '\\t': '\t',
        '\\f': '\f',
        '\\b': '\b',
        '\\a': '\a',
        '\\v': '\v',
    }
    for escape_seq, actual_char in escape_map.items():
        res = res.replace(escape_seq, actual_char)
    return res


def dictTValueInit(plugin_event, dictTValue):
    res = dictTValue
    res['tBotHash'] = plugin_event.bot_info.hash
    if 'vValDict' not in dictTValue:
        dictTValue['vValDict'] = {}
    res['vValDict']['vPluginEvent'] = plugin_event
    return res


def loadAdapterType(botInfo: OlivOS.API.bot_info_T):
    res = 'Native'
    if type(botInfo) is OlivOS.API.bot_info_T:
        if 'platform' in botInfo.platform and 'sdk' in botInfo.platform and 'model' in botInfo.platform:
            if (
                botInfo.platform['platform'] in OlivaDiceCore.msgCustom.dictAdapterMapper
                and botInfo.platform['sdk'] in OlivaDiceCore.msgCustom.dictAdapterMapper[botInfo.platform['platform']]
                and botInfo.platform['model']
                in OlivaDiceCore.msgCustom.dictAdapterMapper[botInfo.platform['platform']][botInfo.platform['sdk']]
            ):
                res = OlivaDiceCore.msgCustom.dictAdapterMapper[botInfo.platform['platform']][botInfo.platform['sdk']][
                    botInfo.platform['model']
                ]
            else:
                res = botInfo.platform['platform'].upper()
    return res
