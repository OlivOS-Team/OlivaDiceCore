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

def initMsgCustom(bot_info_dict):
    for bot_info_dict_this in bot_info_dict:
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
                OlivaDiceCore.msgCustom.dictStrCustomDict[botHash].update(json.loads(customReplyPath_f.read()))
        except:
            continue

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
