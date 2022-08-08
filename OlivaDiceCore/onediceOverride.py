# -*- encoding: utf-8 -*-
'''
   ____  _   ____________  ________________
  / __ \/ | / / ____/ __ \/  _/ ____/ ____/
 / / / /  |/ / __/ / / / // // /   / __/   
/ /_/ / /|  / /___/ /_/ // // /___/ /___   
\____/_/ |_/_____/_____/___/\____/_____/   

@File      :   onediceOverride.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import random
import requests as req

import OlivaDiceCore

#random_default_mode = 'default'
random_default_mode = 'random_org'


dictRandomInt = {
    'default': []
}


def get_data_from_random_org():
    res = []
    send_url = 'https://www.random.org/integers/?num=1000&min=-1000000000&max=1000000000&col=1&base=10&format=plain&rnd=new'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': OlivaDiceCore.data.bot_version_short_header
    }
    msg_res = req.request("POST", send_url, headers = headers, timeout = 4)
    res_text = str(msg_res.text)
    res_text = res_text.lstrip('\n')
    res_text = res_text.rstrip('\n')
    res = res_text.split('\n')
    if len(res) < 1000:
        res = None
    return res


def initOnedice():
    global random_default_mode
    for bot_this in OlivaDiceCore.data.global_Proc.Proc_data['bot_info_dict']:
        if OlivaDiceCore.console.getConsoleSwitchByHash(
            'randomMode',
            bot_this
        ) == 1:
            random_default_mode = 'default'


class RD(OlivaDiceCore.onedice.RD):
    def random(self, nMin, nMax, mode = None):
        global dictRandomInt
        global random_default_mode
        if mode == None:
            mode = random_default_mode
        res = None
        if mode == 'default':
            res = random.randint(nMin, nMax)
        elif mode == 'random_org':
            res = random.randint(nMin, nMax)
            if len(dictRandomInt['default']) <= 0:
                try:
                    tmp_random_int_list = get_data_from_random_org()
                    if tmp_random_int_list == None:
                        random_default_mode = 'default'
                        res = random.randint(nMin, nMax)
                        return res
                    if len(tmp_random_int_list) > 0:
                        dictRandomInt['default'] = tmp_random_int_list
                    else:
                        res = random.randint(nMin, nMax)
                        return res
                except:
                    random_default_mode = 'default'
                    res = random.randint(nMin, nMax)
                    return res
            tmp_random_int_this = dictRandomInt['default'].pop()
            tmp_random_int_data = None
            if type(tmp_random_int_this) == str:
                if tmp_random_int_this.isdigit() or (len(tmp_random_int_this) > 2 and tmp_random_int_this[0] == '-' and tmp_random_int_this[1:].isdigit()):
                    tmp_random_int_data = int((int(tmp_random_int_this) + 1000000000) % (nMax - nMin + 1)) + nMin
                    res = tmp_random_int_data
                    return res
            res = random.randint(nMin, nMax)
        return res

OlivaDiceCore.onedice.RD = RD
