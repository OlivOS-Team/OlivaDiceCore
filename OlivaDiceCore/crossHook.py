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
    ['OlivaDiceCore', OlivaDiceCore.data.OlivaDiceCore_ver]
]

def msgHook(event, funcType, dectData, message):
    [host_id, group_id, user_id] = dectData
    return None

#跨模块注入点
dictHookList = {
    'model': listModel
}

dictHookFunc = {
    'msgHook': msgHook
}
