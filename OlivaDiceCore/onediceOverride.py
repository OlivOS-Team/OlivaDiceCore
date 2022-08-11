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
import json

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

def saveRDDataUser(data:OlivaDiceCore.onedice.RD, botHash:str, userId:str, platform:str):
    if data.resError == None:
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userConfigKey = 'RDRecord',
            userConfigValue = data.resDetailData,
            botHash = botHash,
            userId = userId,
            userType = 'user',
            platform = platform
        )
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userConfigKey = 'RDRecordRaw',
            userConfigValue = data.originDataRaw,
            botHash = botHash,
            userId = userId,
            userType = 'user',
            platform = platform
        )
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userConfigKey = 'RDRecordInt',
            userConfigValue = data.resInt,
            botHash = botHash,
            userId = userId,
            userType = 'user',
            platform = platform
        )
        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
            userHash = OlivaDiceCore.userConfig.getUserHash(
                userId = userId,
                userType = 'user',
                platform = platform
            )
        )

# getRDDataUser
def getRDDataUser(botHash:str, userId:str, platform:str):
    res = getRDDataUserByHash(
        botHash = botHash,
        userHash = OlivaDiceCore.userConfig.getUserHash(
            userId = userId,
            userType = 'user',
            platform = platform
        )
    )
    return res

def getRDDataUserByHash(botHash:str, userHash:str):
    res = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
        userConfigKey = 'RDRecord',
        botHash = botHash,
        userHash = userHash
    )
    return res

# getRDDataRawUser
def getRDDataRawUser(botHash:str, userId:str, platform:str):
    res = getRDDataRawUserByHash(
        botHash = botHash,
        userHash = OlivaDiceCore.userConfig.getUserHash(
            userId = userId,
            userType = 'user',
            platform = platform
        )
    )
    return res

def getRDDataRawUserByHash(botHash:str, userHash:str):
    res = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
        userConfigKey = 'RDRecordRaw',
        botHash = botHash,
        userHash = userHash
    )
    return res

# getRDDataIntUser
def getRDDataIntUser(botHash:str, userId:str, platform:str):
    res = getRDDataIntUserByHash(
        botHash = botHash,
        userHash = OlivaDiceCore.userConfig.getUserHash(
            userId = userId,
            userType = 'user',
            platform = platform
        )
    )
    return res

def getRDDataIntUserByHash(botHash:str, userHash:str):
    res = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
        userConfigKey = 'RDRecordInt',
        botHash = botHash,
        userHash = userHash
    )
    return res

# format
dictFormatMappingMode = {
    '默认': 'default',
    '美化': 'pretty',
    '无限': 'ww',
    '双重十字': 'dx'
}

def RDDataFormat(data:'list|None', mode:str = 'default'):
    res = None
    mode_real = mode
    if mode in dictFormatMappingMode:
        mode_real = dictFormatMappingMode[mode]
    if data != None and type(data) == list:
        if mode_real == 'debug':
            res = RDDataFormat_debug(data)
        elif mode_real == 'default':
            res = RDDataFormat_default(data)
        elif mode_real == 'pretty':
            res = RDDataFormat_default(data, 'pretty')
        elif mode_real == 'dx':
            res = RDDataFormat_default(data, 'dx')
        elif mode_real == 'ww':
            res = RDDataFormat_default(data, 'ww')
    return res

def RDDataFormat_debug(data:list):
    res = str(data)
    try:
        res = json.dumps(data, ensure_ascii = False, indent = 4)
    except:
        pass
    return res

def RDDataFormat_default(data:list, mode = 'default'):
    res = ''
    for data_this in data:
        if int == type(data_this):
            res += str(data_this)
        elif str == type(data_this):
            res += data_this
        elif dict == type(data_this):
            if 'op' in data_this:
                if data_this['op'] in ['(', ')', '+', '-', '*', '/', '^', '<', '>']:
                    res += data_this['op']
            elif 'key' in data_this and 'result' in data_this:
                if checkRDdataNodeKeyOP(data_this, 'd'):
                    if checkRDdataNodeKeyVActive(data_this, 'k') or checkRDdataNodeKeyVActive(data_this, 'q'):
                        if checkRDdataNodeResult(data_this, 0):
                            res += '{%s}' % (', '.join(getRDdataNodeResultListStr(data_this, 0)))
                        if checkRDdataNodeResult(data_this, 1):
                            res += '[%s]' % ('+'.join(getRDdataNodeResultListStr(data_this, 1)))
                        if checkRDdataNodeResult(data_this, 2):
                            res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                    elif checkRDdataNodeKeyVActive(data_this, 'b') or checkRDdataNodeKeyVActive(data_this, 'p'):
                        if checkRDdataNodeResult(data_this, 0):
                            tmp_data_this_list = []
                            for data_this_this in data_this['result'][0]:
                                if type(data_this_this) == list and len(data_this_this) == 1:
                                    tmp_data_this_list.append(RDDataFormat_default(data_this_this))
                            if mode == 'pretty':
                                res += '{\n%s\n}' % (',\n'.join(tmp_data_this_list))
                            else:
                                res += '{%s}' % (', '.join(tmp_data_this_list))
                        if checkRDdataNodeResult(data_this, 1):
                            res += '[%s]' % ('+'.join(getRDdataNodeResultListStr(data_this, 1)))
                        if checkRDdataNodeResult(data_this, 2):
                            res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                    else:
                        if checkRDdataNodeResult(data_this, 0):
                            res += '{%s}' % ('+'.join(getRDdataNodeResultListStr(data_this, 0)))
                        if checkRDdataNodeResult(data_this, 2):
                            res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                elif checkRDdataNodeKeyOP(data_this, 'a'):
                    if checkRDdataNodeResult(data_this, 0):
                        if mode in ['dx', 'ww']:
                            count = 0
                            tmp_data_this_list_0 = []
                            for data_this_this_0 in data_this['result'][0]:
                                tmp_data_this_list_0.append(
                                    '{%s}(%s)' % (
                                        ', '.join([
                                            RDDataFormat_default_getMark(data_this_this_0_this)
                                            for data_this_this_0_this in data_this_this_0
                                        ]),
                                        str(data_this['result'][1][count]) if len(data_this['result'][1]) >= count else str(0)
                                    )
                                )
                                count += 1
                        else:
                            tmp_data_this_list_0 = [
                                '{%s}' % (', '.join([
                                    RDDataFormat_default_getMark(data_this_this_0_this)
                                    for data_this_this_0_this in data_this_this_0
                                ])) for data_this_this_0 in data_this['result'][0]
                            ]
                        if mode in ['dx', 'ww']:
                            res += '{轮数: %s\n%s\n}' % (
                                str(len(data_this['result'][0])),
                                '+\n'.join(tmp_data_this_list_0)
                            )
                        elif mode == 'pretty':
                            res += '{\n%s\n}' % (',\n'.join(tmp_data_this_list_0))
                        else:
                            res += '{%s}' % (', '.join(tmp_data_this_list_0))
                    if checkRDdataNodeResult(data_this, 1):
                        if mode in ['dx', 'ww']:
                            pass
                        else:
                            res += '[%s]' % ('+'.join(getRDdataNodeResultListStr(data_this, 1)))
                    if checkRDdataNodeResult(data_this, 2):
                        res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                elif checkRDdataNodeKeyOP(data_this, 'c'):
                    if checkRDdataNodeResult(data_this, 0):
                        tmp_data_this_list_0 = [
                            '{%s}' % (', '.join([
                                RDDataFormat_default_getMark(data_this_this_0_this)
                                for data_this_this_0_this in data_this_this_0
                            ])) for data_this_this_0 in data_this['result'][0]
                        ]
                        if mode in ['dx', 'ww']:
                            res += '{轮数: %s\n%s\n}' % (
                                str(len(data_this['result'][0])),
                                ',\n'.join(tmp_data_this_list_0)
                            )
                        elif mode == 'pretty':
                            res += '{\n%s\n}' % (',\n'.join(tmp_data_this_list_0))
                        else:
                            res += '{%s}' % (', '.join(tmp_data_this_list_0))
                    if checkRDdataNodeResult(data_this, 1):
                        res += '[%s*%s+%s]' % tuple(getRDdataNodeResultListStr(data_this, 1))
                    if checkRDdataNodeResult(data_this, 2):
                        res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                elif checkRDdataNodeKeyOP(data_this, 'b'):
                    if checkRDdataNodeResult(data_this, 0):
                        tmp_data_this_list_1 = []
                        if checkRDdataNodeResult(data_this, 1):
                            tmp_data_this_list_1 = [
                                RDDataFormat_default_getMark(data_this_this_1)
                                for data_this_this_1 in data_this['result'][1]
                            ]
                        res += ''.join([
                            '{1D100=%s 奖励骰:[%s]}' % (
                                str(data_this_this_0),
                                ', '.join(tmp_data_this_list_1)
                            ) for data_this_this_0 in data_this['result'][0]
                        ])
                    if checkRDdataNodeResult(data_this, 2):
                        res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                elif checkRDdataNodeKeyOP(data_this, 'p'):
                    if checkRDdataNodeResult(data_this, 0):
                        tmp_data_this_list_1 = []
                        if checkRDdataNodeResult(data_this, 1):
                            tmp_data_this_list_1 = [
                                RDDataFormat_default_getMark(data_this_this_1)
                                for data_this_this_1 in data_this['result'][1]
                            ]
                        res += ''.join([
                            '{1D100=%s 惩罚骰:[%s]}' % (
                                str(data_this_this_0),
                                ', '.join(tmp_data_this_list_1)
                            ) for data_this_this_0 in data_this['result'][0]
                        ])
                    if checkRDdataNodeResult(data_this, 2):
                        res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                elif checkRDdataNodeKeyOP(data_this, 'f'):
                    if checkRDdataNodeResult(data_this, 0) and checkRDdataNodeResult(data_this, 1) and checkRDdataNodeResult(data_this, 2):
                        tmp_data_this_list_0 = []
                        for data_this_this_0 in data_this['result'][0]:
                            if type(data_this_this_0) == int:
                                if data_this_this_0 > 0:
                                    tmp_data_this_list_0.append('+')
                                elif data_this_this_0 < 0:
                                    tmp_data_this_list_0.append('-')
                                else:
                                    tmp_data_this_list_0.append('0')
                        tmp_data_this_str_1 = ''
                        flag_first = True
                        for data_this_this_1 in data_this['result'][1]:
                            if type(data_this_this_1) == int:
                                if data_this_this_1 >= 0:
                                    if not flag_first:
                                        tmp_data_this_str_1 += '+'
                                tmp_data_this_str_1 += str(data_this_this_1)
                            flag_first = False
                        res += '{%s}[%s](%s)' % (
                            ' '.join(tmp_data_this_list_0),
                            tmp_data_this_str_1,
                            ', '.join(getRDdataNodeResultListStr(data_this, 2))
                        )
                elif checkRDdataNodeKeyOP(data_this, '&'):
                    if checkRDdataNodeResult(data_this, 0) and checkRDdataNodeResult(data_this, 1) and checkRDdataNodeResult(data_this, 2):
                        tmp_data_this_list = []
                        for data_this_this in data_this['result'][0]:
                            tmp_data_this_list.append(RDDataFormat_default(data_this_this))
                        res += '{%s}' % ('&'.join(tmp_data_this_list))
                        res += '[%s]' % ('&'.join(getRDdataNodeResultListStr(data_this, 1)))
                        res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                elif checkRDdataNodeKeyOP(data_this, '|'):
                    if checkRDdataNodeResult(data_this, 0) and checkRDdataNodeResult(data_this, 1) and checkRDdataNodeResult(data_this, 2):
                        tmp_data_this_list = []
                        for data_this_this in data_this['result'][0]:
                            if type(data_this_this) == list and len(data_this_this) == 1:
                                tmp_data_this_list.append(RDDataFormat_default(data_this_this))
                        res += '{%s}' % ('|'.join(tmp_data_this_list))
                        res += '[%s]' % ('|'.join(getRDdataNodeResultListStr(data_this, 1)))
                        res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                elif checkRDdataNodeKeyOP(data_this, '?'):
                    if checkRDdataNodeKeyVActive(data_this, ':'):
                        if checkRDdataNodeResult(data_this, 0):
                            if len(data_this['result'][0]) >= 3:
                                res += '{%s?%s:%s}' % (
                                    RDDataFormat_default(data_this['result'][0][0]),
                                    RDDataFormat_default(data_this['result'][0][1]),
                                    RDDataFormat_default(data_this['result'][0][2])
                                )
                        if checkRDdataNodeResult(data_this, 2):
                            res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
                    else:
                        if checkRDdataNodeResult(data_this, 0):
                            if len(data_this['result'][0]) >= 1:
                                res += '{%s?}' % (
                                    RDDataFormat_default(data_this['result'][0][0])
                                )
                        if checkRDdataNodeResult(data_this, 1):
                            res += '[%s?]' % (' '.join(getRDdataNodeResultListStr(data_this, 1)))
                        if checkRDdataNodeResult(data_this, 2):
                            res += '(%s)' % (', '.join(getRDdataNodeResultListStr(data_this, 2)))
    if '' == res:
        res = None
    return res

def RDDataFormat_default_getMark(data:'int|dict'):
    res = ''
    if type(data) == int:
        res = str(data)
    elif type(data) == dict:
        if 'op' in data and 'v' in data:
            if data['op'] == 'mark01':
                res = '[%s]' % RDDataFormat_default_getMark(data['v'])
            elif data['op'] == 'mark02':
                res = '<%s>' % RDDataFormat_default_getMark(data['v'])
    return res

def checkRDdataNodeResult(data:dict, offset:int):
    return 'result' in data and len(data['result']) > offset and len(data['result'][offset]) > 0

def checkRDdataNodeKeyOP(data:dict, key:str):
    return 'key' in data and 'op' in data['key'] and key == data['key']['op']

def checkRDdataNodeKeyV(data:dict, key:str):
    return 'key' in data and 'v' in data['key'] and key in data['key']['v']

def checkRDdataNodeKeyVActive(data:dict, key:str):
    return 'key' in data and 'v' in data['key'] and key in data['key']['v'] and data['key']['v'][key] != None

def getRDdataNodeResultListStr(data:dict, offset:int, callback = None):
    return [str(int_this) for int_this in data['result'][offset]]
