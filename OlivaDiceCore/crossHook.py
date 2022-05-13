# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   crossHook.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivaDiceCore

listModel = [
    ['OlivaDiceCore', OlivaDiceCore.data.OlivaDiceCore_ver_short]
]

listPrefix = [
    '.',
    '。',
    '/'
]

def msgHook(event, funcType, sender, dectData, message):
    [host_id, group_id, user_id] = dectData
    tmp_name = 'N/A'
    tmp_id = -1
    if 'name' in sender:
        tmp_name = sender['name']
    if 'id' in sender:
        tmp_id = sender['id']
    return None

def pokeHook(plugin_event, type = 'group'):
    if type == 'group':
        return OlivaDiceCore.data.bot_info
    elif type == 'private':
        return OlivaDiceCore.data.bot_info
    else:
        return OlivaDiceCore.data.bot_info

#跨模块注入点
dictHookList = {
    'model': listModel,
    'prefix': listPrefix
}

dictHookFunc = {
    'msgHook': msgHook,
    'pokeHook': pokeHook
}
