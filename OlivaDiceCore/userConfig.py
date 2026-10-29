# -*- encoding: utf-8 -*-
r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   userConfig.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
"""

import OlivaDiceCore

import json
import copy
import tempfile
import threading
import time
import hashlib
import os

dictUserConfigData = {}
listUserConfigDataUpdate = []

gMsgCount = 0

gMsgCountLock = threading.Lock()
gUserConfigLock = threading.Lock()

dictUserConfigDefault = {'userId': None, 'lastHit': None}

dictUserConfigNoteDefault = {
    'groupEnable': True,
    'hostEnable': True,
    'hostLocalEnable': True,
    'groupWithHostEnable': False,
    'groupTemplate': None,
    'groupTemplateRule': None,
    'groupRavRule': None,
    'groupMainDice': None,
    'groupMainDiceDRight': None,
    'groupMainDiceDLeft': None,
    'groupObList': None,
    'groupInitList': None,
    'groupInitParaList': None,
    'groupInitUserList': None,
    'groupInitCurrentPlayer': None,
    'groupInitRound': 1,
    'userObList': None,
    'welcomeMsg': None,
    'RDRecord': None,
    'RDRecordInt': 0,
    'RDRecordRaw': '',
    'RDRecordSkillInt': None,
    'userName': '用户',
    'trustLevel': 0,
    'trustRank': 1000,
    'autoSnEnabled': False,
    'showDefault': False,
    'teamConfig': {},
    'activeTeam': None,
    'mythicHardeningEnable': False,
}

dictUserConfigNoteMapping = {
    'groupEnable': [None, '群禁用'],
    'hostEnable': [None, '子频道默认禁用'],
    'hostLocalEnable': [None, '频道禁用'],
    'groupWithHostEnable': ['子频道特例启用', None],
}

dictUserConfigNoteType = {
    'user': [],
    'group': ['groupEnable', 'groupWithHostEnable'],
    'host': ['hostEnable', 'hostLocalEnable'],
}

# 重定向黑名单：这些数据必须保持独立性，不应被重定向
dictRedirectBlacklist = {
    'groupEnable',  # 这个是控制群开关
    'hostEnable',
    'hostLocalEnable',
    'groupWithHostEnable',
    'lastHit',  # 这个主要是控制群hit，用于group_clear
    # 这个注释掉是因为已经在log on里面处理了，这里就不处理，否则会在og on之后无法log off
    # 'logEnable' # 这里是让log on的时候不走从账号，从而使得不会重复记录
}


def getRedirectedBotHash(botHash, dataKey=None, forceNoRedirect=False):
    """
    获取重定向后的botHash
    如果当前botHash是从账号，且dataKey不在黑名单中，返回主账号的botHash
    否则返回原botHash
    """
    # 强制不重定向
    if forceNoRedirect:
        return botHash
    if dataKey and dataKey in dictRedirectBlacklist:
        return botHash
    masterBotHashList = OlivaDiceCore.console.getMasterBotHashList(botHash)
    if masterBotHashList and len(masterBotHashList) > 0:
        return masterBotHashList[0]
    return botHash


def setUserConfigByKey(userId, userType, platform, userConfigKey, userConfigValue, botHash, forceNoRedirect=False):
    userConfigNoteKey = 'configNote'
    if userConfigKey not in dictUserConfigNoteDefault:
        return
    # 应用重定向逻辑（纯读取，留在锁外，避免与 console 的锁形成锁序依赖）
    redirectedBotHash = getRedirectedBotHash(botHash, userConfigKey, forceNoRedirect)
    userHash = getUserHash(userId=userId, userType=userType, platform=platform)
    # OlivOS 在线程池中并发派发插件事件，此处必须与写盘快照互斥
    gUserConfigLock.acquire()
    try:
        if userHash not in listUserConfigDataUpdate:
            listUserConfigDataUpdate.append(userHash)
        if userHash not in dictUserConfigData:
            dictUserConfigData[userHash] = {}
        if redirectedBotHash not in dictUserConfigData[userHash]:
            dictUserConfigData[userHash][redirectedBotHash] = {}
        if userConfigNoteKey not in dictUserConfigData[userHash][redirectedBotHash]:
            dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey] = {}
        dictUserConfigData[userHash][redirectedBotHash]['userId'] = userId
        dictUserConfigData[userHash][redirectedBotHash]['userType'] = userType
        dictUserConfigData[userHash][redirectedBotHash]['platform'] = platform
        if 'lastHit' not in dictUserConfigData[userHash][redirectedBotHash]:
            dictUserConfigData[userHash][redirectedBotHash]['lastHit'] = dictUserConfigDefault['lastHit']
        dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey][userConfigKey] = userConfigValue
    finally:
        gUserConfigLock.release()


dictConfigKeyToConsoleSwitchMapping = {'showDefault': 'defaultShowDefault', 'autoSnEnabled': 'defaultAutoSn'}


def getDefaultValueByConfigKey(userConfigKey):
    """
    获取配置项的默认值，优先从全局开关中读取
    """
    if userConfigKey in dictConfigKeyToConsoleSwitchMapping:
        consoleSwitchKey = dictConfigKeyToConsoleSwitchMapping[userConfigKey]
        consoleSwitchValue = OlivaDiceCore.console.getConsoleSwitchByHash(consoleSwitchKey, 'unity')
        if consoleSwitchValue is not None:
            return consoleSwitchValue == 1
    if userConfigKey in dictUserConfigNoteDefault:
        return dictUserConfigNoteDefault[userConfigKey]
    return False


def getUserConfigByKey(userId, userType, platform, userConfigKey, botHash, default=None, forceNoRedirect=False):
    userConfigNoteKey = 'configNote'
    userConfigValue = default if default is not None else False
    if userConfigKey in dictUserConfigNoteDefault and default is None:
        userConfigValue = getDefaultValueByConfigKey(userConfigKey)
    # 应用重定向逻辑
    redirectedBotHash = getRedirectedBotHash(botHash, userConfigKey, forceNoRedirect)
    userHash = getUserHash(userId=userId, userType=userType, platform=platform)
    if userHash in dictUserConfigData:
        if redirectedBotHash in dictUserConfigData[userHash]:
            if userConfigNoteKey in dictUserConfigData[userHash][redirectedBotHash]:
                if userConfigKey in dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey]:
                    userConfigValue = dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey][userConfigKey]
    return userConfigValue


def getUserConfigByKeyWithHash(userHash, userConfigKey, botHash, forceNoRedirect=False):
    userConfigNoteKey = 'configNote'
    userConfigValue = False
    if userConfigKey in dictUserConfigNoteDefault:
        userConfigValue = getDefaultValueByConfigKey(userConfigKey)
    # 应用重定向逻辑
    redirectedBotHash = getRedirectedBotHash(botHash, userConfigKey, forceNoRedirect)
    if userHash in dictUserConfigData:
        if redirectedBotHash in dictUserConfigData[userHash]:
            if userConfigNoteKey in dictUserConfigData[userHash][redirectedBotHash]:
                if userConfigKey in dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey]:
                    userConfigValue = dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey][userConfigKey]
    return userConfigValue


def getUserDataByKeyWithHash(userHash, userDataKey, botHash):
    userDataValue = None
    if userDataKey in dictUserConfigDefault:
        userDataValue = dictUserConfigDefault[userDataKey]
    # 应用重定向逻辑
    redirectedBotHash = getRedirectedBotHash(botHash, userDataKey)
    if userHash in dictUserConfigData:
        if redirectedBotHash in dictUserConfigData[userHash]:
            if userDataKey in dictUserConfigData[userHash][redirectedBotHash]:
                userDataValue = dictUserConfigData[userHash][redirectedBotHash][userDataKey]
    return userDataValue


# basic
def setMsgCount():
    global gMsgCount
    gMsgCountLock.acquire()
    gMsgCount -= 1
    gMsgCountLock.release()


def releaseUnityMsgCount(data, botHash, flagForceWrite=False):
    global gMsgCount
    global listUserConfigDataUpdate
    flag_need_release = False
    tmp_dictUserConfigData = {}
    gMsgCountLock.acquire()
    if gMsgCount <= 0:
        gMsgCount = OlivaDiceCore.console.getConsoleSwitchByHash('userConfigCount')
        flag_need_release = True
    gMsgCountLock.release()
    gUserConfigLock.acquire()
    try:
        for data_this in data:
            [userId, userType, platform] = data_this
            tmp_UserHash = getUserHash(userId, userType, platform)
            if tmp_UserHash not in listUserConfigDataUpdate:
                listUserConfigDataUpdate.append(tmp_UserHash)
            if tmp_UserHash not in dictUserConfigData:
                dictUserConfigData[tmp_UserHash] = {}
            if botHash not in dictUserConfigData[tmp_UserHash]:
                dictUserConfigData[tmp_UserHash][botHash] = {}
            dictUserConfigData[tmp_UserHash][botHash]['userId'] = userId
            dictUserConfigData[tmp_UserHash][botHash]['userType'] = userType
            dictUserConfigData[tmp_UserHash][botHash]['platform'] = platform
            dictUserConfigData[tmp_UserHash][botHash]['lastHit'] = int(time.time())
        if flag_need_release or flagForceWrite:
            # 锁内只做快照，且必须逐条深拷贝：浅拷贝得到的仍是同一份内层 dict，
            # 锁一释放就会被并发写入改动，序列化时可能抛 RuntimeError 或写出不一致内容
            tmp_listUserConfigDataUpdate = list(listUserConfigDataUpdate)
            tmp_dictUserConfigData = {
                tmp_userHash: copy.deepcopy(dictUserConfigData[tmp_userHash])
                for tmp_userHash in tmp_listUserConfigDataUpdate
                if tmp_userHash in dictUserConfigData
            }
            listUserConfigDataUpdate = []
    finally:
        gUserConfigLock.release()
    if flag_need_release or flagForceWrite:
        writeUserConfig(tmp_dictUserConfigData, tmp_listUserConfigDataUpdate)


# io
def writeUserConfigDataAtomic(userConfigDataPath, data):
    """同目录临时文件 + 原子替换，避免写入中断或并发写导致 JSON 残缺"""
    userConfigDataDir = os.path.dirname(userConfigDataPath)
    releaseDir(userConfigDataDir)
    jsonStr = json.dumps(data, ensure_ascii=False, indent=4)
    tmp_fd, tmpPath = tempfile.mkstemp(
        dir=userConfigDataDir, prefix=os.path.basename(userConfigDataPath) + '.', suffix='.tmp'
    )
    try:
        with os.fdopen(tmp_fd, 'w', encoding='utf-8') as tmpPath_f:
            tmpPath_f.write(jsonStr)
        # Windows 下目标文件正被其他进程打开（杀毒扫描、备份等）时 os.replace 会失败，
        # 短暂重试；仍失败则退化为直接写入，避免整次配置更新丢失
        for tmp_retry in range(5):
            try:
                os.replace(tmpPath, userConfigDataPath)
                return
            except PermissionError:
                if tmp_retry >= 4:
                    with open(userConfigDataPath, 'w', encoding='utf-8') as userConfigDataPath_f:
                        userConfigDataPath_f.write(jsonStr)
                    return
                time.sleep(0.02)
    finally:
        if os.path.exists(tmpPath):
            try:
                os.unlink(tmpPath)
            except OSError:
                pass


def writeUserConfig(data, updateList):
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    for data_this in updateList:
        if data_this in data:
            userHash = data_this
            for data_userHash_this in data[userHash]:
                botHash = data_userHash_this
                releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
                releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user')
                userConfigDataPath = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user/' + userHash
                writeUserConfigDataAtomic(userConfigDataPath, data[userHash])


def writeUserConfigByUserHash(userHash):
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    gUserConfigLock.acquire()
    try:
        tmp_dictUserConfigData_this = None
        if userHash in dictUserConfigData:
            tmp_dictUserConfigData_this = copy.deepcopy(dictUserConfigData[userHash])
    finally:
        gUserConfigLock.release()
    if tmp_dictUserConfigData_this is not None:
        for tmp_dictUserConfigData_this_this in tmp_dictUserConfigData_this:
            botHash = tmp_dictUserConfigData_this_this
            releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
            releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user')
            userConfigDataPath = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user/' + userHash
            writeUserConfigDataAtomic(userConfigDataPath, tmp_dictUserConfigData_this)


def readUserConfig():
    # 通过 dataLoadCache 快照跳过未变化文件的打开与读取，加载结果与逐个读取一致
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    snapshot = OlivaDiceCore.dataLoadCache.DataLoadSnapshot('userConfig', '用户记录')
    with OlivaDiceCore.dataLoadCache.pauseGC():
        botHash_list = os.listdir(OlivaDiceCore.data.dataDirRoot)
        for botHash_list_this in botHash_list:
            botHash = botHash_list_this
            releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
            releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user')
            userConfigDataDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user'
            userHash_list, userHash_entries = OlivaDiceCore.dataLoadCache.scanDir(userConfigDataDir)
            for userHash_list_this in userHash_list:
                userHash = userHash_list_this
                userConfigDataFile = userHash
                userConfigDataPath = userConfigDataDir + '/' + userConfigDataFile
                if userHash not in dictUserConfigData:
                    dictUserConfigData[userHash] = {}
                dictUserConfigData[userHash] = snapshot.load(
                    userConfigDataPath,
                    OlivaDiceCore.dataLoadCache.getScanEntry(userHash_entries, userHash),
                    f'{botHash}/{userConfigDataFile}',
                )
    snapshot.finish()


def jsonDataLoadSafe(data_f, dataType, dataName):
    tmp_userConfigData = {}
    try:
        tmp_userConfigData = json.loads(data_f.read())
    except Exception as e:
        tmp_log_str = OlivaDiceCore.msgCustomManager.formatReplySTRConst(
            OlivaDiceCore.msgCustom.dictStrConst['strInitDataError'],
            {'tInitDataType': dataType, 'tInitDataName': dataName, 'tResult': str(e)},
        )
        OlivaDiceCore.msgReply.globalLog(3, tmp_log_str, [('OlivaDice', 'default'), ('Init', 'default')])
        tmp_userConfigData = {}
    return tmp_userConfigData


def dataUserConfigLoadAll():
    global gMsgCount
    gMsgCount = OlivaDiceCore.console.getConsoleSwitchByHash('userConfigCount')
    readUserConfig()


def dataUserConfigTotalCount(userType: 'str|None' = None, botHash: 'str|None' = None):
    total_count = 0
    for userHash in dictUserConfigData:
        if userType is None:
            total_count += 1
        else:
            for botHash_this in dictUserConfigData[userHash]:
                if (
                    botHash is None
                    or botHash == botHash_this
                ):
                    if (
                        type(dictUserConfigData[userHash][botHash_this]) is dict
                        and 'userType' in dictUserConfigData[userHash][botHash_this]
                        and userType == dictUserConfigData[userHash][botHash_this]['userType']
                    ):
                        total_count += 1
    return total_count


def getUserHash(userId, userType, platform, subId=None):
    hash_tmp = hashlib.new('md5')
    if subId is not None:
        tmp_strID = '%s|%s' % (str(subId), str(userId))
        hash_tmp.update(tmp_strID.encode(encoding='UTF-8'))
    else:
        hash_tmp.update(str(userId).encode(encoding='UTF-8'))
    hash_tmp.update(str(userType).encode(encoding='UTF-8'))
    hash_tmp.update(str(platform).encode(encoding='UTF-8'))
    if subId is not None:
        hash_tmp.update(str(subId).encode(encoding='UTF-8'))
    return hash_tmp.hexdigest()


def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def initDelUTF8WithBom(bot_info_dict):
    for bot_info_dict_this in bot_info_dict:
        botHash = bot_info_dict_this
        setDelUTF8WithBom(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console/customReply.json')
        setDelUTF8WithBom(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console/helpdocDefault.json')
        setDelUTF8WithBom(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console/switch.json')
    setDelUTF8WithBom(OlivaDiceCore.data.dataDirRoot + '/unity/console/customReply.json')
    setDelUTF8WithBom(OlivaDiceCore.data.dataDirRoot + '/unity/console/helpdocDefault.json')
    setDelUTF8WithBom(OlivaDiceCore.data.dataDirRoot + '/unity/console/switch.json')
    pass


def setDelUTF8WithBom(filePath):
    flag_is_bom = False
    free_len = 0
    bom_len = 0
    free_data = 0
    bom_data = 0
    try:
        with open(filePath, 'r', encoding='utf-8') as filePath_f:
            free_data = str(filePath_f.read())
            free_len = len(free_data)
        with open(filePath, 'r', encoding='utf-8-sig') as filePath_f:
            bom_data = str(filePath_f.read())
            bom_len = len(bom_data)
        if free_len > bom_len:
            flag_is_bom = True
        if flag_is_bom:
            with open(filePath, 'w', encoding='utf-8') as filePath_f:
                filePath_f.write(bom_data)
    except Exception:
        pass
