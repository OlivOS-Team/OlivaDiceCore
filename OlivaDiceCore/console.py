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

dictConsoleSwitchTemplate = {
    'default' : {
        'globalEnable' : 1,
        'userConfigCount' : 100
    }
}

dictConsoleSwitch = {}

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
    if botHash not in dictConsoleSwitch:
        if templateName in dictConsoleSwitchTemplate:
            dictConsoleSwitch[botHash] = dictConsoleSwitchTemplate[templateName].copy()

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
        with open(consoleSwitchPath, 'r', encoding = 'utf-8') as consoleSwitchPath_f:
            dictConsoleSwitch[botHash] = json.loads(consoleSwitchPath_f.read())
    
def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
