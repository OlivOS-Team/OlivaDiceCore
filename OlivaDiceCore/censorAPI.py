'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   censorAPI.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2022-2023, OlivOS-Team
@Desc      :   None
'''

import OlivaDiceCore

import os
import codecs
import copy
import time
import json

gCensorDFA = {}

gCensorList = {}
gCensorConfigList = {}
gCensorInfoList = {}

gCensorConfigListUnitTemplate = {
    'censorList': []
}

def formatUTF8WithBOM(data:bytes):
    res = data
    if res[:3] == codecs.BOM_UTF8:
        res = res[3:]
    return res

def readListFromFile(path):
    res = []
    try:
        with open(path, 'rb') as path_f:
            path_fs = formatUTF8WithBOM(path_f.read()).decode('utf-8')
            res = path_fs.replace('\r\n', '\n').split('\n')
    except:
        res = []
    return res

def readConfigListByHash(bot_hash):
    global gCensorConfigList, gCensorConfigListUnitTemplate
    res = copy.deepcopy(gCensorConfigListUnitTemplate)
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console')
    fileDir = OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console'
    fileName = 'censor.json'
    path = fileDir + '/' + fileName
    try:
        with open(path, 'rb') as path_f:
            path_fs = formatUTF8WithBOM(path_f.read()).decode('utf-8')
            res = json.loads(path_fs)
    except:
        res = copy.deepcopy(gCensorConfigListUnitTemplate)
    gCensorConfigList[bot_hash] = res

def writeConfigListByHash(bot_hash):
    global gCensorConfigList, gCensorConfigListUnitTemplate
    res = copy.deepcopy(gCensorConfigListUnitTemplate)
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console')
    fileDir = OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console'
    fileName = 'censor.json'
    path = fileDir + '/' + fileName
    if bot_hash in gCensorConfigList:
        res = gCensorConfigList[bot_hash]
    try:
        with open(path, 'w', encoding = 'utf-8') as path_f:
            path_fs = json.dumps(res, ensure_ascii = False, indent = 4)
            path_f.write(path_fs)
    except:
        pass

def addConfigList(bot_hash, setWord):
    global gCensorConfigList
    if bot_hash in gCensorConfigList \
    and 'censorList' in gCensorConfigList[bot_hash] \
    and type(gCensorConfigList[bot_hash]['censorList']) is list:
        if setWord not in gCensorConfigList[bot_hash]['censorList']:
            gCensorConfigList[bot_hash]['censorList'].append(setWord)

def getConfigList(bot_hash):
    global gCensorConfigList
    res = []
    if bot_hash in gCensorConfigList \
    and 'censorList' in gCensorConfigList[bot_hash] \
    and type(gCensorConfigList[bot_hash]['censorList']) is list:
        res = gCensorConfigList[bot_hash]['censorList']
    return res

def delConfigList(bot_hash, setWord):
    global gCensorConfigList
    if bot_hash in gCensorConfigList \
    and 'censorList' in gCensorConfigList[bot_hash] \
    and type(gCensorConfigList[bot_hash]['censorList']) is list:
        gCensorConfigList[bot_hash]['censorList']
        if setWord in gCensorConfigList[bot_hash]['censorList']:
            gCensorConfigList[bot_hash]['censorList'].remove(setWord)

def initCensor(bot_info_dict):
    global gCensorDFA, gCensorList, gCensorInfoList, gCensorConfigList

    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/censor')
    fileDir = OlivaDiceCore.data.dataDirRoot + '/unity/censor'
    fileList = os.listdir(fileDir)
    censorList_unity = []
    dictTValue['tName'] = '全局'
    readConfigListByHash('unity')
    writeConfigListByHash('unity')
    for fileList_this in fileList:
        fileName = fileList_this
        filePath = fileDir + '/' + fileName
        censorList_unity += readListFromFile(filePath)
        gCensorList['unity'] = censorList_unity
    for bot_hash in bot_info_dict:
        dictTValue['tName'] = bot_hash
        if bot_hash in bot_info_dict:
            dictTValue['tName'] = '%s|%s' % (
                bot_info_dict[bot_hash].platform['platform'],
                str(bot_info_dict[bot_hash].id)
            )
        gCensorInfoList[bot_hash] = dictTValue['tName']
        censorList_this = []
        releaseDir(OlivaDiceCore.data.dataDirRoot)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/censor')
        fileDir = OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/censor'
        fileList = os.listdir(fileDir)
        readConfigListByHash(bot_hash)
        writeConfigListByHash(bot_hash)
        for fileList_this in fileList:
            fileName = fileList_this
            filePath = fileDir + '/' + fileName
            censorList_this += readListFromFile(filePath)
        gCensorList[bot_hash] = censorList_this
        initCensorByHash(bot_hash)


def initCensorByHash(bot_hash):
    global gCensorDFA, gCensorList, gCensorInfoList, gCensorConfigList

    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    dictTValue['tName'] = bot_hash
    if bot_hash in gCensorInfoList:
        dictTValue['tName'] = gCensorInfoList[bot_hash]

    censorList_this = []
    for bot_hash_this in ['unity', bot_hash]:
        if bot_hash_this in gCensorList:
            censorList_this += gCensorList[bot_hash_this]
    for bot_hash_this in ['unity', bot_hash]:
        censorList_this += getConfigList(bot_hash_this)

    time_start = time.perf_counter()
    gCensorDFA[bot_hash] = OlivaDiceCore.censorDFA.DFA(censorList_this)
    time_end = time.perf_counter()
    dictTValue['tInitDataCount'] = str(len(censorList_this))
    dictTValue['tInitDataTimeCost'] = '%.2fms' % ((time_end - time_start) * 1000)
    OlivaDiceCore.msgReply.globalLog(
        2,
        OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strInitCensor'], dictTValue),
        [
            ('OlivaDice', 'default'),
            ('Init', 'default')
        ]
    )

def patchCensorByHash(bot_hash, patchList:list):
    global gCensorDFA

    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    dictTValue['tName'] = bot_hash
    if bot_hash in gCensorInfoList:
        dictTValue['tName'] = gCensorInfoList[bot_hash]

    time_start = time.perf_counter()
    if bot_hash in gCensorDFA:
        gCensorDFA[bot_hash].loadl(patchList)
    time_end = time.perf_counter()

    dictTValue['tInitDataCount'] = str(len(patchList))
    dictTValue['tInitDataTimeCost'] = '%.2fms' % ((time_end - time_start) * 1000)
    OlivaDiceCore.msgReply.globalLog(
        2,
        OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strPatchCensor'], dictTValue),
        [
            ('OlivaDice', 'default'),
            ('Init', 'default')
        ]
    )

def doCensorReplace(botHash:str, msg:str):
    global gCensorDFA
    res = msg
    if botHash in gCensorDFA:
        res = gCensorDFA[botHash].doReplace(
            inData = msg,
            mode = OlivaDiceCore.censorDFA.maxMatchType
        )
    return res

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
