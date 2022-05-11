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
    'userId' : None
}

dictUserConfigNoteDefault = {
    'groupEnable' : True,
    'hostEnable' : True,
    'hostLocalEnable' : True,
    'groupWithHostEnable' : False,
    'groupTemplate' : None,
    'groupTemplateRule' : None,
    'groupObList' : None,
    'userObList' : None,
    'userName' : '用户'
}

def setUserConfigByKey(userId, userType, platform, userConfigKey, userConfigValue, botHash):
    global dictUserConfigData
    global dictUserConfigNoteDefault
    global listUserConfigDataUpdate
    userConfigNoteKey = 'configNote'
    if userConfigKey not in dictUserConfigNoteDefault:
        return
    userHash = getUserHash(
        userId = userId,
        userType = userType,
        platform = platform
    )
    if userHash not in listUserConfigDataUpdate:
        listUserConfigDataUpdate.append(userHash)
    if userHash not in dictUserConfigData:
        dictUserConfigData[userHash] = {}
    if botHash not in dictUserConfigData[userHash]:
        dictUserConfigData[userHash][botHash] = {}
    if userConfigNoteKey not in dictUserConfigData[userHash][botHash]:
        dictUserConfigData[userHash][botHash][userConfigNoteKey] = {}
    dictUserConfigData[userHash][botHash]['userId'] = userId
    dictUserConfigData[userHash][botHash]['userType'] = userType
    dictUserConfigData[userHash][botHash]['platform'] = platform
    dictUserConfigData[userHash][botHash][userConfigNoteKey][userConfigKey] = userConfigValue

def getUserConfigByKey(userId, userType, platform, userConfigKey, botHash):
    global dictUserConfigData
    global dictUserConfigNoteDefault
    userConfigNoteKey = 'configNote'
    userConfigValue = False
    userHash = getUserHash(
        userId = userId,
        userType = userType,
        platform = platform
    )
    if userConfigKey in dictUserConfigNoteDefault:
        userConfigValue = dictUserConfigNoteDefault[userConfigKey]
    if userHash in dictUserConfigData:
        if botHash in dictUserConfigData[userHash]:
            if userConfigNoteKey in dictUserConfigData[userHash][botHash]:
                if userConfigKey in dictUserConfigData[userHash][botHash][userConfigNoteKey]:
                    userConfigValue = dictUserConfigData[userHash][botHash][userConfigNoteKey][userConfigKey]
    return userConfigValue

def getUserConfigByKeyWithHash(userHash, userConfigKey, botHash):
    global dictUserConfigData
    global dictUserConfigNoteDefault
    userConfigNoteKey = 'configNote'
    userConfigValue = False
    if userConfigKey in dictUserConfigNoteDefault:
        userConfigValue = dictUserConfigNoteDefault[userConfigKey]
    if userHash in dictUserConfigData:
        if botHash in dictUserConfigData[userHash]:
            if userConfigNoteKey in dictUserConfigData[userHash][botHash]:
                if userConfigKey in dictUserConfigData[userHash][botHash][userConfigNoteKey]:
                    userConfigValue = dictUserConfigData[userHash][botHash][userConfigNoteKey][userConfigKey]
    return userConfigValue

def getUserDataByKeyWithHash(userHash, userDataKey, botHash):
    global dictUserConfigData
    global dictUserConfigDefault
    userDataValue = None
    if userDataKey in dictUserConfigDefault:
        userDataValue = dictUserConfigDefault[userDataKey]
    if userHash in dictUserConfigData:
        if botHash in dictUserConfigData[userHash]:
            if userDataKey in dictUserConfigData[userHash][botHash]:
                userDataValue = dictUserConfigData[userHash][botHash][userDataKey]
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
                dictUserConfigData[userHash] = json.loads(userConfigDataPath_f.read())

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
