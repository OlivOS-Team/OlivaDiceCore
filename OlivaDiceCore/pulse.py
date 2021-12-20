# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   pulse.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import time
import requests as req

import OlivOS
import OlivaDiceCore

dictPulseTs = {}

def unity_heartbeat(plugin_event, Proc):
    global dictPulseTs
    tmp_ts = int(time.time())
    tmp_pulse_interval = 300
    tmp_pulse_url_list = []
    tmp_master_list = []
    flag_need_pulse = False
    if plugin_event.bot_info.hash in OlivaDiceCore.console.dictConsoleSwitch:
        if 'pulseInterval' in OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]:
            tmp_pulse_interval = OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]['pulseInterval']
        if 'pulseUrlList' in OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]:
            tmp_pulse_url_list = OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]['pulseUrlList']
        if 'masterList' in OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]:
            tmp_master_list = OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]['masterList']
    if plugin_event.bot_info.hash in dictPulseTs:
        if tmp_ts - dictPulseTs[plugin_event.bot_info.hash] > 300:
            dictPulseTs[plugin_event.bot_info.hash] = tmp_ts
            flag_need_pulse = True
    else:
        dictPulseTs[plugin_event.bot_info.hash] = tmp_ts
        flag_need_pulse = True
    if flag_need_pulse:
        try:
            tmp_res = plugin_event.get_login_info()
            tmp_nickname = None
            tmp_user_id = plugin_event.bot_info.id
            tmp_master = ''
            tmp_master_list_1 = []
            if tmp_res['active'] == True:
                tmp_nickname = tmp_res['data']['name']
                OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]['strBotName'] = tmp_res['data']['name']
            for tmp_master_list_this in tmp_master_list:
                tmp_master_list_1.append(str(tmp_master_list_this[0]))
            tmp_master = ','.join(tmp_master_list_1)
        except:
            pass
        for tmp_pulse_url_list_this in tmp_pulse_url_list:
            do_pulse(
                user_id = tmp_user_id,
                name = tmp_nickname,
                token = tmp_pulse_url_list_this[1],
                time_ts = tmp_ts,
                masterid = tmp_master,
                platform = plugin_event.platform['platform'],
                url = tmp_pulse_url_list_this[0]
            )

def do_pulse(user_id, name, token, time_ts, masterid = '0', platform = 'default', url = None):
    tmp_payload_dict = {
        'token': token,
        'user_id': user_id,
        'time_ts': time_ts,
        'version': OlivaDiceCore.data.bot_info_basic_short,
        'name': name,
        'masterid': masterid,
        'interval': 330,
        'isGlobalon': 1,
        'isPublic': 1,
        'isVisible': 1,
        'platform': platform
    }
    payload = tmp_payload_dict
    send_url = url
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': OlivaDiceCore.data.bot_version_short_header
    }
    if send_url != None:
        msg_res = req.request("POST", send_url, headers = headers, data = payload)
