# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgEvent.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

import copy

def deepCopyEventUInfo(src:OlivOS.API.Event):
    res = OlivOS.API.Event(
        sdk_event = OlivOS.contentAPI.fake_sdk_event(src.bot_info),
        log_func = None
    )
    res.sdk_event = src.sdk_event
    res.sdk_event_type = src.sdk_event_type
    res.base_info = copy.deepcopy(src.base_info)
    res.platform = copy.deepcopy(src.platform)
    res.bot_info = src.bot_info
    res.plugin_info = src.plugin_info.copy()
    res.active = False
    res.blocked = False
    res.log_func = src.log_func
    return res

def getReRxEvent_group_message(src:OlivOS.API.Event, message:str):
    res = deepCopyEventUInfo(src)
    target_message = message
    res.data = res.group_message(
        group_id = '',
        user_id = '',
        message = '',
        sub_type = 'group'
    )
    res.plugin_info['func_type'] = 'group_message'
    if type(src.data) is OlivOS.API.Event.group_message:
        res.active = True
        res.data.sub_type = src.data.sub_type
        res.data.user_id = src.data.user_id
        res.data.group_id = src.data.group_id
        res.data.host_id = src.data.host_id
        res.data.message_id = '-1'
        res.data.font = src.data.font
        res.data.sender = copy.deepcopy(src.data.sender)
        res.data.extend = copy.deepcopy(src.data.extend)
    elif type(src.data) is OlivOS.API.Event.poke:
        if src.data.group_id not in [-1, '-1', None]:
            res.active = True
            res.data.user_id = src.data.user_id
            res.data.group_id = src.data.group_id
            res.data.host_id = None
            res.data.message_id = '-1'
            res.data.font = None
            res.data.sender = {
                'name': 'Nobody',
                'id': res.data.user_id,
                'nickname': 'Nobody',
                'user_id': res.data.user_id,
            }
            res.data.extend = {}
    elif type(src.data) is OlivOS.API.Event.group_member_increase:
        res.active = True
        res.data.user_id = src.data.user_id
        res.data.group_id = src.data.group_id
        res.data.host_id = None
        res.data.message_id = '-1'
        res.data.font = None
        res.data.sender = {
            'name': 'Nobody',
            'id': res.data.user_id,
            'nickname': 'Nobody',
            'user_id': res.data.user_id,
        }
        res.data.extend = {}

    getReRxEvent_message_format(res, target_message)

    return res

def getReRxEvent_private_message(src:OlivOS.API.Event, message:str):
    res = deepCopyEventUInfo(src)
    target_message = message
    res.data = res.private_message(
        user_id = '',
        message = '',
        sub_type = 'private'
    )
    res.plugin_info['func_type'] = 'private_message'
    if type(src.data) is OlivOS.API.Event.private_message:
        res.active = True
        res.data.sub_type = src.data.sub_type
        res.data.user_id = src.data.user_id
        res.data.message_id = '-1'
        res.data.font = src.data.font
        res.data.sender = copy.deepcopy(src.data.sender)
        res.data.extend = copy.deepcopy(src.data.extend)
    elif type(src.data) is OlivOS.API.Event.poke:
        if src.data.group_id in [-1, '-1', None]:
            res.active = True
            res.data.user_id = src.data.user_id
            res.data.message_id = '-1'
            res.data.font = None
            res.data.sender = {
                'name': 'Nobody',
                'id': res.data.user_id,
                'nickname': 'Nobody',
                'user_id': res.data.user_id,
            }
            res.data.extend = {}

    getReRxEvent_message_format(res, target_message)

    return res

def getReRxEvent_message_format(target:OlivOS.API.Event, message:str):
    target.data.message_sdk = OlivOS.messageAPI.Message_templet(
        mode_rx = 'old_string',
        data_raw = message
    )
    target.data.message_sdk.data_raw = target.data.message_sdk.get(target.plugin_info['message_mode_rx'])
    target.data.message_sdk.mode_rx = target.plugin_info['message_mode_rx']
    target.data.message = target.data.message_sdk.get(target.plugin_info['message_mode_tx'])
    target.data.raw_message = target.data.message
    target.data.raw_message_sdk = target.data.message_sdk
