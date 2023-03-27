# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgCustomManager.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

import os
import json
import random

def initMsgCustom(bot_info_dict):
    for bot_info_dict_this in bot_info_dict:
        OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this] = {}
        OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this] = OlivaDiceCore.msgCustom.dictStrCustom.copy()
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    botHash_list = os.listdir(OlivaDiceCore.data.dataDirRoot)
    for botHash_list_this in botHash_list:
        botHash = botHash_list_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
        customReplyDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
        customReplyFile = 'customReply.json'
        customReplyPath = customReplyDir + '/' + customReplyFile
        try:
            with open(customReplyPath, 'r', encoding = 'utf-8') as customReplyPath_f:
                OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = json.loads(customReplyPath_f.read())
                OlivaDiceCore.msgCustom.dictStrCustomDict[botHash].update(
                    OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash]
                )
        except:
            continue

def saveMsgCustom(bot_info_dict):
    for botHash in bot_info_dict:
        saveMsgCustomByBotHash(botHash)

def saveMsgCustomByBotHash(botHash):
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
    customReplyDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
    customReplyFile = 'customReply.json'
    customReplyPath = customReplyDir + '/' + customReplyFile
    if botHash not in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = {}
    if type(OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash]) != dict:
        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash] = {}
    with open(customReplyPath, 'w', encoding = 'utf-8') as customReplyPath_f:
        customReplyPath_f.write(json.dumps(OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[botHash], ensure_ascii = False, indent = 4))

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def formatReplySTR(data:str, valDict:dict, flagCross:bool = True, flagSplit:bool = True):
    res:str = data
    if flagSplit:
        res = random.choice(list(res.split('|')))
        res = res.replace('{DEVIDE}', '|')
        res = res.replace('{OR}', '|')
    if flagCross:
        res = OlivaDiceCore.crossHook.dictHookFunc['msgFormatHook'](res, valDict)
    res = formatReplySTRReplace(res, valDict)
    return res

def formatReplySTRConst(data:str, valDict:dict):
    res = data
    res = res.format(**valDict)
    return res

# 用状态机实现高宽容度的变量引用
# 替代Python内置Format
def formatReplySTRReplace(data:str, valDict:dict, flagPure:bool = False):
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
                if not flag_hit and reg_key in valDict and type(valDict[reg_key] == str):
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
                        key_str = reg_key,
                        bot_hash = tmp_bot_hash,
                        flag_need_give_back = True,
                        plugin_event = plugin_event
                    )
                    if reg_res_this != None:
                        reg_res += reg_res_this
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

def dictTValueInit(plugin_event, dictTValue):
    res = dictTValue
    res['tBotHash'] = plugin_event.bot_info.hash
    if 'vValDict' not in dictTValue:
        dictTValue['vValDict'] = {}
    res['vValDict']['vPluginEvent'] = plugin_event
    return res

def loadAdapterType(botInfo:OlivOS.API.bot_info_T):
    res = 'Native'
    if type(botInfo) is OlivOS.API.bot_info_T:
        if 'platform' in botInfo.platform \
        and 'sdk' in botInfo.platform \
        and 'model' in botInfo.platform:
            if botInfo.platform['platform'] in OlivaDiceCore.msgCustom.dictAdapterMapper \
            and botInfo.platform['sdk'] in OlivaDiceCore.msgCustom.dictAdapterMapper\
            [botInfo.platform['platform']] \
            and botInfo.platform['model'] in OlivaDiceCore.msgCustom.dictAdapterMapper\
            [botInfo.platform['platform']][botInfo.platform['sdk']]:
                res = OlivaDiceCore.msgCustom.dictAdapterMapper[
                    botInfo.platform['platform']
                ][
                    botInfo.platform['sdk']
                ][
                    botInfo.platform['model']
                ]
            else:
                res = botInfo.platform['platform'].upper()
    return res
