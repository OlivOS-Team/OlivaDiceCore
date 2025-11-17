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
        'recordBotJoinGroup' : 1,
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

# 主从关系配置相关
dictAccountRelationConfigTemplate = {
    'default': {
        'relations': {}
    }
}

dictAccountRelationConfig = {}

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

# 主从关系配置管理函数
def initAccountRelationConfig():
    """初始化主从关系配置"""
    global dictAccountRelationConfig
    global dictAccountRelationConfigTemplate
    if 'unity' not in dictAccountRelationConfig:
        dictAccountRelationConfig['unity'] = {}
    for template_key_this in dictAccountRelationConfigTemplate['default']:
        if template_key_this not in dictAccountRelationConfig['unity']:
            dictAccountRelationConfig['unity'][template_key_this] = dictAccountRelationConfigTemplate['default'][template_key_this].copy()

def saveAccountRelationConfig():
    """保存主从关系配置"""
    global dictAccountRelationConfig
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/console')
    accountRelationConfigDir = OlivaDiceCore.data.dataDirRoot + '/unity/console'
    accountRelationConfigFile = 'accountRelation.json'
    accountRelationConfigPath = accountRelationConfigDir + '/' + accountRelationConfigFile
    if 'unity' in dictAccountRelationConfig:
        with open(accountRelationConfigPath, 'w', encoding='utf-8') as accountRelationConfigPath_f:
            accountRelationConfigPath_f.write(json.dumps(dictAccountRelationConfig['unity'], ensure_ascii=False, indent=4))

def readAccountRelationConfig():
    """读取主从关系配置"""
    global dictAccountRelationConfig
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/console')
    accountRelationConfigDir = OlivaDiceCore.data.dataDirRoot + '/unity/console'
    accountRelationConfigFile = 'accountRelation.json'
    accountRelationConfigPath = accountRelationConfigDir + '/' + accountRelationConfigFile
    # 初始化unity配置
    if 'unity' not in dictAccountRelationConfig:
        dictAccountRelationConfig['unity'] = {}
    try:
        with open(accountRelationConfigPath, 'r', encoding='utf-8') as accountRelationConfigPath_f:
            loaded_config = json.loads(accountRelationConfigPath_f.read())
            # 检查是否需要转换旧格式
            if 'relations' in loaded_config:
                relations = loaded_config['relations']
                needs_conversion = False
                for key, value in relations.items():
                    if isinstance(value, str):
                        needs_conversion = True
                        break
                if needs_conversion:
                    new_relations = {}
                    for slave, master in relations.items():
                        if isinstance(master, str):
                            if master not in new_relations:
                                new_relations[master] = []
                            new_relations[master].append(slave)
                    loaded_config['relations'] = new_relations
                    dictAccountRelationConfig['unity'] = loaded_config
                    saveAccountRelationConfig()
                else:
                    dictAccountRelationConfig['unity'].update(loaded_config)
            else:
                dictAccountRelationConfig['unity'].update(loaded_config)
    except:
        # 如果文件不存在或读取失败，使用默认配置
        pass

def getMasterBotHash(slaveBotHash):
    """获取从账号对应的主账号Hash"""
    global dictAccountRelationConfig
    if 'unity' in dictAccountRelationConfig:
        if 'relations' in dictAccountRelationConfig['unity']:
            relations = dictAccountRelationConfig['unity']['relations']
            # 遍历所有主账号，查找哪个主账号包含这个从账号
            for masterHash, slaveList in relations.items():
                if slaveBotHash in slaveList:
                    return masterHash
    return None

def getMasterBotHashList(slaveBotHash):
    """获取从账号对应的主账号Hash列表"""
    result = getMasterBotHash(slaveBotHash)
    return [result] if result else []

def setAccountRelation(slaveBotHash, masterBotHash):
    """设置主从关系（将从账号添加到主账号的从账号列表）"""
    global dictAccountRelationConfig
    if 'unity' not in dictAccountRelationConfig:
        dictAccountRelationConfig['unity'] = {}
    if 'relations' not in dictAccountRelationConfig['unity']:
        dictAccountRelationConfig['unity']['relations'] = {}
    # 获取主账号的从账号列表
    if masterBotHash in dictAccountRelationConfig['unity']['relations']:
        slave_list = dictAccountRelationConfig['unity']['relations'][masterBotHash]
        # 添加新从账号（如果不存在）
        if slaveBotHash not in slave_list:
            slave_list.append(slaveBotHash)
    else:
        # 新建关系
        dictAccountRelationConfig['unity']['relations'][masterBotHash] = [slaveBotHash]

def removeAccountRelation(slaveBotHash, masterBotHash=None):
    """删除主从关系"""
    global dictAccountRelationConfig
    if 'unity' in dictAccountRelationConfig:
        if 'relations' in dictAccountRelationConfig['unity']:
            relations = dictAccountRelationConfig['unity']['relations']
            # 如果未指定主账号，先查找
            if masterBotHash is None:
                masterBotHash = getMasterBotHash(slaveBotHash)
            if masterBotHash and masterBotHash in relations:
                slave_list = relations[masterBotHash]
                if slaveBotHash in slave_list:
                    slave_list.remove(slaveBotHash)
                if not slave_list:
                    del relations[masterBotHash]

def getAllAccountRelations():
    """获取所有主从关系"""
    global dictAccountRelationConfig
    if 'unity' in dictAccountRelationConfig:
        if 'relations' in dictAccountRelationConfig['unity']:
            return dictAccountRelationConfig['unity']['relations'].copy()
    return {}
