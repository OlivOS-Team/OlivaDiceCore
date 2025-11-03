# -*- encoding: utf-8 -*-
'''
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
'''

import OlivOS
import OlivaDiceCore

import json
import threading
import time
import hashlib
import os

dictUserConfigData = {}
listUserConfigDataUpdate = []

gMsgCount = 0

gMsgCountLock = threading.Lock()
gUserConfigLock = threading.Lock()

dictUserConfigDefault = {
    'userId' : None,
    'lastHit' : None
}

dictUserConfigNoteDefault = {
    'groupEnable' : True,
    'hostEnable' : True,
    'hostLocalEnable' : True,
    'groupWithHostEnable' : False,
    'groupTemplate' : None,
    'groupTemplateRule' : None,
    'groupRavRule' : None,
    'groupMainDice' : None,
    'groupMainDiceDRight' : None,
    'groupObList' : None,
    'groupInitList' : None,
    'groupInitParaList' : None,
    'groupInitUserList' : None,
    'groupInitCurrentPlayer' : None,
    'userObList' : None,
    'welcomeMsg' : None,
    'RDRecord' : None,
    'RDRecordInt' : 0,
    'RDRecordRaw' : '',
    'RDRecordSkillInt' : None,
    'userName' : '用户',
    'trustLevel' : 0,
    'trustRank' : 1000,
    'autoSnEnabled' : False,
    'showDefault' : False,
    'teamConfig': {},
    'activeTeam': None,
}

dictUserConfigNoteMapping = {
    'groupEnable' : [None, '群禁用'],
    'hostEnable' : [None, '子频道默认禁用'],
    'hostLocalEnable' : [None, '频道禁用'],
    'groupWithHostEnable' : ['子频道特例启用', None]
}

dictUserConfigNoteType = {
    'user': [],
    'group': [
        'groupEnable',
        'groupWithHostEnable'
    ],
    'host': [
        'hostEnable',
        'hostLocalEnable'
    ]
}

# 重定向黑名单：这些数据必须保持独立性，不应被重定向
dictRedirectBlacklist = {
    'groupEnable',
    'hostEnable',
    'hostLocalEnable',
    'groupWithHostEnable',
    'lastHit'
}

def getRedirectedBotHash(botHash, dataKey=None):
    """
    获取重定向后的botHash
    如果当前botHash是从账号，且dataKey不在黑名单中，返回主账号的botHash
    否则返回原botHash
    """
    # 如果dataKey在黑名单中，直接返回原botHash
    if dataKey and dataKey in dictRedirectBlacklist:
        return botHash
    # 检查是否存在主从关系
    masterBotHash = OlivaDiceCore.console.getMasterBotHash(botHash)
    if masterBotHash:
        return masterBotHash
    
    return botHash

def setUserConfigByKey(userId, userType, platform, userConfigKey, userConfigValue, botHash):
    global dictUserConfigData
    global dictUserConfigNoteDefault
    global listUserConfigDataUpdate
    userConfigNoteKey = 'configNote'
    if userConfigKey not in dictUserConfigNoteDefault:
        return
    # 应用重定向逻辑
    redirectedBotHash = getRedirectedBotHash(botHash, userConfigKey)
    
    userHash = getUserHash(
        userId = userId,
        userType = userType,
        platform = platform
    )
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

def getUserConfigByKey(userId, userType, platform, userConfigKey, botHash, default=None):
    global dictUserConfigData
    global dictUserConfigNoteDefault
    userConfigNoteKey = 'configNote'
    userConfigValue = default if default is not None else False
    if userConfigKey in dictUserConfigNoteDefault and default is None:
        userConfigValue = dictUserConfigNoteDefault[userConfigKey]
    # 应用重定向逻辑
    redirectedBotHash = getRedirectedBotHash(botHash, userConfigKey)
    
    userHash = getUserHash(
        userId = userId,
        userType = userType,
        platform = platform
    )
    if userHash in dictUserConfigData:
        if redirectedBotHash in dictUserConfigData[userHash]:
            if userConfigNoteKey in dictUserConfigData[userHash][redirectedBotHash]:
                if userConfigKey in dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey]:
                    userConfigValue = dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey][userConfigKey]
    return userConfigValue

def getUserConfigByKeyWithHash(userHash, userConfigKey, botHash):
    global dictUserConfigData
    global dictUserConfigNoteDefault
    userConfigNoteKey = 'configNote'
    userConfigValue = False
    if userConfigKey in dictUserConfigNoteDefault:
        userConfigValue = dictUserConfigNoteDefault[userConfigKey]
    # 应用重定向逻辑
    redirectedBotHash = getRedirectedBotHash(botHash, userConfigKey)
    
    if userHash in dictUserConfigData:
        if redirectedBotHash in dictUserConfigData[userHash]:
            if userConfigNoteKey in dictUserConfigData[userHash][redirectedBotHash]:
                if userConfigKey in dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey]:
                    userConfigValue = dictUserConfigData[userHash][redirectedBotHash][userConfigNoteKey][userConfigKey]
    return userConfigValue

def getUserDataByKeyWithHash(userHash, userDataKey, botHash):
    global dictUserConfigData
    global dictUserConfigDefault
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

#basic
def setMsgCount():
    global gMsgCount
    gMsgCountLock.acquire()
    gMsgCount -= 1
    gMsgCountLock.release()

def releaseUnityMsgCount(data, botHash, flagForceWrite = False):
    global gMsgCountInit
    global gMsgCount
    global dictUserConfigData
    global listUserConfigDataUpdate
    flag_need_release = False
    tmp_dictUserConfigData = {}
    gMsgCountLock.acquire()
    if gMsgCount <= 0:
        gMsgCount = OlivaDiceCore.console.getConsoleSwitchByHash('userConfigCount')
        flag_need_release = True
    gMsgCountLock.release()
    gUserConfigLock.acquire()
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
        tmp_dictUserConfigData = dictUserConfigData.copy()
        tmp_listUserConfigDataUpdate = listUserConfigDataUpdate.copy()
        listUserConfigDataUpdate = []
    gUserConfigLock.release()
    if flag_need_release or flagForceWrite:
        writeUserConfig(tmp_dictUserConfigData, tmp_listUserConfigDataUpdate)

#io
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
                with open(userConfigDataPath, 'w', encoding = 'utf-8') as userConfigDataPath_f:
                    userConfigDataPath_f.write(json.dumps(data[userHash], ensure_ascii = False, indent = 4))

def writeUserConfigByUserHash(userHash):
    global dictUserConfigData
    global listUserConfigDataUpdate
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    if userHash in dictUserConfigData:
        gUserConfigLock.acquire()
        tmp_dictUserConfigData_this = dictUserConfigData[userHash].copy()
        gUserConfigLock.release()
        for tmp_dictUserConfigData_this_this in tmp_dictUserConfigData_this:
            botHash = tmp_dictUserConfigData_this_this
            releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
            releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user')
            userConfigDataPath = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user/' + userHash
            with open(userConfigDataPath, 'w', encoding = 'utf-8') as userConfigDataPath_f:
                userConfigDataPath_f.write(json.dumps(tmp_dictUserConfigData_this, ensure_ascii = False, indent = 4))

def readUserConfig():
    global dictUserConfigData
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    botHash_list = os.listdir(OlivaDiceCore.data.dataDirRoot)
    for botHash_list_this in botHash_list:
        botHash = botHash_list_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user')
        userHash_list = os.listdir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user')
        for userHash_list_this in userHash_list:
            userHash = userHash_list_this
            userConfigDataDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/user'
            userConfigDataFile = userHash
            userConfigDataPath = userConfigDataDir + '/' + userConfigDataFile
            if userHash not in dictUserConfigData:
                dictUserConfigData[userHash] = {}
            with open(userConfigDataPath, 'r', encoding = 'utf-8') as userConfigDataPath_f:
                dictUserConfigData[userHash] = jsonDataLoadSafe(userConfigDataPath_f, "用户记录", f"{botHash}/{userConfigDataFile}")

def jsonDataLoadSafe(data_f, dataType, dataName):
    tmp_userConfigData = {}
    try:
        tmp_userConfigData = json.loads(data_f.read())
    except Exception as e:
        tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(
            OlivaDiceCore.msgCustom.dictStrConst['strInitDataError'],
            {
                "tInitDataType": dataType,
                "tInitDataName": dataName,
                "tResult": str(e)
            }
        )
        OlivaDiceCore.msgReply.globalLog(3, tmp_log_str, [
            ('OlivaDice', 'default'),
            ('Init', 'default')
        ])
        tmp_userConfigData = {}
    return tmp_userConfigData

def dataUserConfigLoadAll():
    global gMsgCount
    gMsgCount = OlivaDiceCore.console.getConsoleSwitchByHash('userConfigCount')
    readUserConfig()

def dataUserConfigTotalCount():
    total_count = 0
    for dictUserConfigData_this in dictUserConfigData:
        total_count += 1
    return total_count

def getUserHash(userId, userType, platform, subId = None):
    hash_tmp = hashlib.new('md5')
    if subId != None:
        tmp_strID = '%s|%s' % (str(subId), str(userId))
        hash_tmp.update(tmp_strID.encode(encoding='UTF-8'))
    else:
        hash_tmp.update(str(userId).encode(encoding='UTF-8'))
    hash_tmp.update(str(userType).encode(encoding='UTF-8'))
    hash_tmp.update(str(platform).encode(encoding='UTF-8'))
    if subId != None:
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
        with open(filePath, 'r', encoding = 'utf-8') as filePath_f:
            free_data = str(filePath_f.read())
            free_len = len(free_data)
        with open(filePath, 'r', encoding = 'utf-8-sig') as filePath_f:
            bom_data = str(filePath_f.read())
            bom_len = len(bom_data)
        if free_len > bom_len:
            flag_is_bom = True
        if flag_is_bom:
            with open(filePath, 'w', encoding = 'utf-8') as filePath_f:
                filePath_f.write(bom_data)
    except:
        pass
