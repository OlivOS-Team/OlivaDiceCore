# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   console.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

import json
import os
import datetime

dictConsoleSwitchTemplate = {
    'default' : {
        'globalEnable' : 1,
        'userConfigCount' : 100,
        'pulseInterval' : 300,
        'autoAcceptGroupAdd' : 1,
        'autoAcceptFriendAdd' : 1,
        'recordBotJoinGroup' : 0,
        'disableReplyPrivate' : 0,
        'disablePrivate' : 0,
        'messageFliterMode' : 0,
        'messageSplitGate' : 650,
        'messageSplitPageLimit' : 10,
        'messageSplitDelay' : 1000,
        'largeRollLimit' : 300,
        'multiRollDetail' : 1,
        'randomMode' : 0,
        'drawRecommendMode' : 1,
        'drawListMode' : 2,
        'helpRecommendGate' : 25,
        'censorMode' : 1,
        'censorMatchMode' : 1,
        'masterList' : [],
        'noticeGroupList' : [],
        'pulseUrlList' : []
    }
}

dictConsoleSwitch = {}

# 备份配置相关
dictBackupConfigTemplate = {
    'default': {
        'isBackup': 0,
        'startDate': '',  # 将在初始化时设置为当前日期
        'passDay': 1,
        'backupTime': '04:00:00',
        'maxBackupCount': 1,
    }
}

dictBackupConfig = {}

def getConsoleSwitchByHash(switchKey, botHash = 'unity'):
    global dictConsoleSwitch
    tmp_res = None
    if botHash in dictConsoleSwitch:
        if switchKey in dictConsoleSwitch[botHash]:
            tmp_res = dictConsoleSwitch[botHash][switchKey]
    return tmp_res

def setConsoleSwitchByHash(switchKey, switchValue, botHash = 'unity'):
    global dictConsoleSwitch
    if botHash in dictConsoleSwitch:
        if switchKey in dictConsoleSwitch[botHash]:
            dictConsoleSwitch[botHash][switchKey] = switchValue

def initConsoleSwitch(botHash, templateName = 'default'):
    global dictConsoleSwitch
    global dictConsoleSwitchTemplate
    if templateName in dictConsoleSwitchTemplate:
        if botHash not in dictConsoleSwitch:
            dictConsoleSwitch[botHash] = {}
        for template_key_this in dictConsoleSwitchTemplate[templateName]:
            if type(dictConsoleSwitchTemplate[templateName][template_key_this]) in [
                list
            ] and template_key_this not in dictConsoleSwitch[botHash]:
                dictConsoleSwitch[botHash][template_key_this] = dictConsoleSwitchTemplate[templateName][template_key_this].copy()
            else:
                dictConsoleSwitch[botHash][template_key_this] = dictConsoleSwitchTemplate[templateName][template_key_this]

def initConsoleSwitchByBotDict(botDict):
    global dictConsoleSwitch
    for botDict_this in botDict:
        botHash = botDict_this
        initConsoleSwitch(botHash)
    initConsoleSwitch('unity')

def saveConsoleSwitch():
    global dictConsoleSwitch
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    for dictConsoleSwitch_this in dictConsoleSwitch:
        botHash = dictConsoleSwitch_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
        consoleSwitchDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
        consoleSwitchFile = 'switch.json'
        consoleSwitchPath = consoleSwitchDir + '/' + consoleSwitchFile
        with open(consoleSwitchPath, 'w', encoding = 'utf-8') as consoleSwitchPath_f:
            consoleSwitchPath_f.write(json.dumps(dictConsoleSwitch[botHash], ensure_ascii = False, indent = 4))

def readConsoleSwitch():
    global dictConsoleSwitch
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    botHash_list = os.listdir(OlivaDiceCore.data.dataDirRoot)
    for botHash_list_this in botHash_list:
        botHash = botHash_list_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
        consoleSwitchDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
        consoleSwitchFile = 'switch.json'
        consoleSwitchPath = consoleSwitchDir + '/' + consoleSwitchFile
        try:
            with open(consoleSwitchPath, 'r', encoding = 'utf-8') as consoleSwitchPath_f:
                dictConsoleSwitch[botHash].update(json.loads(consoleSwitchPath_f.read()))
        except:
            pass

def setMasterListAppend(botHash, dataList):
    global dictConsoleSwitch
    if botHash in dictConsoleSwitch:
        if 'masterList' not in dictConsoleSwitch[botHash]:
            dictConsoleSwitch[botHash]['masterList'] = []
        if type(dictConsoleSwitch[botHash]['masterList']) != list:
            dictConsoleSwitch[botHash]['masterList'] = []
        dictConsoleSwitch[botHash]['masterList'].append(dataList)

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# 备份配置相关函数
def getBackupConfigByKey(configKey):
    global dictBackupConfig
    tmp_res = None
    if 'unity' in dictBackupConfig:
        if configKey in dictBackupConfig['unity']:
            tmp_res = dictBackupConfig['unity'][configKey]
    return tmp_res

def setBackupConfigByKey(configKey, configValue):
    global dictBackupConfig
    if 'unity' in dictBackupConfig:
        if configKey in dictBackupConfig['unity']:
            dictBackupConfig['unity'][configKey] = configValue

def initBackupConfig():
    global dictBackupConfig
    global dictBackupConfigTemplate
    if 'unity' not in dictBackupConfig:
        dictBackupConfig['unity'] = {}
    # 获取当前日期作为默认开始日期
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    for template_key_this in dictBackupConfigTemplate['default']:
        if template_key_this not in dictBackupConfig['unity']:
            if template_key_this == 'startDate':
                # 设置开始日期为当前日期
                dictBackupConfig['unity'][template_key_this] = current_date
            else:
                dictBackupConfig['unity'][template_key_this] = dictBackupConfigTemplate['default'][template_key_this]

def saveBackupConfig():
    global dictBackupConfig
    # 创建备份文件夹
    releaseDir(OlivaDiceCore.data.backupDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/console')
    backupConfigDir = OlivaDiceCore.data.dataDirRoot + '/unity/console'
    backupConfigFile = 'backup.json'
    backupConfigPath = backupConfigDir + '/' + backupConfigFile
    if 'unity' in dictBackupConfig:
        with open(backupConfigPath, 'w', encoding='utf-8') as backupConfigPath_f:
            backupConfigPath_f.write(json.dumps(dictBackupConfig['unity'], ensure_ascii=False, indent=4))

def readBackupConfig():
    global dictBackupConfig
    # 创建备份文件夹
    releaseDir(OlivaDiceCore.data.backupDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/console')
    backupConfigDir = OlivaDiceCore.data.dataDirRoot + '/unity/console'
    backupConfigFile = 'backup.json'
    backupConfigPath = backupConfigDir + '/' + backupConfigFile
    # 初始化unity配置
    if 'unity' not in dictBackupConfig:
        dictBackupConfig['unity'] = {}
    
    try:
        with open(backupConfigPath, 'r', encoding='utf-8') as backupConfigPath_f:
            dictBackupConfig['unity'].update(json.loads(backupConfigPath_f.read()))
    except:
        # 如果文件不存在或读取失败，使用默认配置
        pass
