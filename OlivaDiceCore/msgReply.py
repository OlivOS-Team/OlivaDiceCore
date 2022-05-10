# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReply.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

import html
import time
import uuid

def logProc(Proc, level, message, segment):
    Proc.log(
        log_level = level,
        log_message = message,
        log_segment = segment
    )

def unity_init(plugin_event, Proc):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    #init start
    OlivaDiceCore.console.initConsoleSwitchByBotDict(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.console.readConsoleSwitch()
    OlivaDiceCore.console.saveConsoleSwitch()
    OlivaDiceCore.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.msgCustomManager.saveMsgCustom(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.helpDoc.initHelpDoc(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.drawCard.initDeck(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.pcCard.dataPcCardTemplateInit()
    OlivaDiceCore.pcCard.dataPcCardLoadAll()
    total_count = OlivaDiceCore.pcCard.dataPcCardTotalCount()
    dictTValue['tInitDataCount'] = str(total_count)
    dictTValue['tInitDataType'] = '人物卡'
    tmp_log_str =  dictStrConst['strInitData'].format(**dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])
    OlivaDiceCore.userConfig.dataUserConfigLoadAll()
    total_count = OlivaDiceCore.userConfig.dataUserConfigTotalCount()
    dictTValue['tInitDataCount'] = str(total_count)
    dictTValue['tInitDataType'] = '用户记录'
    tmp_log_str =  dictStrConst['strInitData'].format(**dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])
    #显示Master认主信息
    dictTValue['tInitMasterKey'] = '.master %s' % OlivaDiceCore.data.bot_content['masterKey']
    tmp_log_str =  dictStrConst['strToBeMaster'].format(**dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])
    dictTValue['tVersion'] = OlivaDiceCore.data.OlivaDiceCore_ver_short
    tmp_log_str =  dictStrConst['strShowVersionOnLog'].format(**dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])

def unity_init_after(plugin_event, Proc):
    for bot_info_this in Proc.Proc_data['bot_info_dict']:
        bot_info = Proc.Proc_data['bot_info_dict'][bot_info_this]
        if bot_info.platform['sdk'] in [
            'telegram_poll',
            'fanbook_poll',
            'dodo_link',
            'qqGuild_link',
            'kaiheila_link'
        ]:
            plugin_event_fake = OlivOS.API.Event(
                OlivOS.contentAPI.fake_sdk_event(
                    bot_info = bot_info,
                    fakename = OlivaDiceCore.data.OlivaDiceCore_name
                ),
                Proc.log
            )
            res_data = plugin_event_fake.get_login_info(bot_info)
            if res_data != None:
                if res_data['active']:
                    OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_this]['strBotName'] = res_data['data']['name']

def unity_save(plugin_event, Proc):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    #save start
    OlivaDiceCore.msgCustomManager.saveMsgCustom(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.userConfig.releaseUnityMsgCount([], None, True)
    total_count = OlivaDiceCore.userConfig.dataUserConfigTotalCount()
    dictTValue['tInitDataCount'] = str(total_count)
    dictTValue['tInitDataType'] = '用户记录'
    tmp_log_str =  dictStrConst['strSaveData'].format(**dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Save', 'default')
    ])

def poke_reply(plugin_event, Proc):
    if plugin_event.data.target_id == plugin_event.base_info['self_id']:
        replyMsg(plugin_event, OlivaDiceCore.data.bot_info)
    elif plugin_event.data.group_id == -1:
        replyMsg(plugin_event, OlivaDiceCore.data.bot_info)

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tName'] = plugin_event.data.sender['name']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    tmp_hook_host_id = None
    tmp_hook_group_id = None
    tmp_hook_user_id = None
    if 'host_id' in plugin_event.data.__dict__:
        tmp_hook_host_id = plugin_event.data.host_id
    if 'group_id' in plugin_event.data.__dict__:
        tmp_hook_group_id = plugin_event.data.group_id
    if 'user_id' in plugin_event.data.__dict__:
        tmp_hook_user_id = plugin_event.data.user_id
    OlivaDiceCore.crossHook.dictHookFunc['msgHook'](
        plugin_event,
        'recv',
        {
            'name': dictTValue['tName'],
            'id': tmp_hook_user_id
        }, 
        [tmp_hook_host_id, tmp_hook_group_id, tmp_hook_user_id],
        str(plugin_event.data.message)
    )

    tmp_at_str = OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()
    tmp_at_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
    tmp_reast_str = plugin_event.data.message
    #反实例化临时方案，用于对齐OlivOS不同平台字符串标准
    tmp_reast_str = htmlUnescape(tmp_reast_str)
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_sub_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
        if isMatchWordStart(tmp_reast_str, tmp_at_str):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    if isMatchWordStart(tmp_reast_str, tmp_at_str):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        flag_force_reply = True
    if tmp_at_str_sub != None:
        if isMatchWordStart(tmp_reast_str, tmp_at_str_sub):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str_sub)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    [tmp_reast_str, flag_is_command] = msgIsCommand(
        tmp_reast_str,
        OlivaDiceCore.crossHook.dictHookList['prefix']
    )
    if flag_is_command:
        tmp_hagID = None
        tmp_list_hit = []
        flag_is_from_master = OlivaDiceCore.ordinaryInviteManager.isInMasterList(
            plugin_event.bot_info.hash,
            OlivaDiceCore.userConfig.getUserHash(
                plugin_event.data.user_id,
                'user',
                plugin_event.platform['platform']
            )
        )
        if plugin_event.plugin_info['func_type'] == 'group_message':
            if plugin_event.data.host_id != None:
                tmp_list_hit = [
                    [plugin_event.data.host_id, 'host', plugin_event.platform['platform']],
                    ['%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id)), 'group', plugin_event.platform['platform']],
                    [plugin_event.data.user_id,  'user',  plugin_event.platform['platform']]
                ]
                flag_is_from_host = True
            else:
                tmp_list_hit = [
                    [plugin_event.data.group_id, 'group', plugin_event.platform['platform']],
                    [plugin_event.data.user_id,  'user',  plugin_event.platform['platform']]
                ]
            flag_is_from_group = True
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            tmp_list_hit = [
                [plugin_event.data.user_id,  'user',  plugin_event.platform['platform']]
            ]
            flag_is_from_group = False
        if flag_is_from_group:
            if 'role' in plugin_event.data.sender:
                flag_is_from_group_have_admin = True
                if plugin_event.data.sender['role'] in ['owner', 'admin']:
                    flag_is_from_group_admin = True
                elif plugin_event.data.sender['role'] in ['sub_admin']:
                    flag_is_from_group_admin = True
                    flag_is_from_group_sub_admin = True
        if flag_is_from_host and flag_is_from_group:
            tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        elif flag_is_from_group:
            tmp_hagID = str(plugin_event.data.group_id)
        OlivaDiceCore.userConfig.releaseUnityMsgCount(tmp_list_hit, plugin_event.bot_info.hash)
        flag_hostEnable = True
        if flag_is_from_host:
            flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_hostLocalEnable = True
        if flag_is_from_host:
            flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostLocalEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_groupEnable = True
        if flag_is_from_group:
            if flag_is_from_host:
                if flag_hostEnable:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupEnable',
                        botHash = plugin_event.bot_info.hash
                    )
                else:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupWithHostEnable',
                        botHash = plugin_event.bot_info.hash
                    )
            else:
                flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupEnable',
                    botHash = plugin_event.bot_info.hash
                )
        flag_messageFliterModeDisabled = False
        flag_messageFliterMode = OlivaDiceCore.console.getConsoleSwitchByHash(
            'messageFliterMode',
            plugin_event.bot_info.hash
        )
        if flag_messageFliterMode == 1 and flag_is_from_group and not flag_is_from_host:
            flag_messageFliterModeDisabled = True
        elif flag_messageFliterMode == 2 and flag_is_from_host:
            flag_messageFliterModeDisabled = True
        elif flag_messageFliterMode == 3 and flag_is_from_group:
            flag_messageFliterModeDisabled = True
        if flag_is_from_master:
            if isMatchWordStart(tmp_reast_str, 'master'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'master')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if isMatchWordStart(tmp_reast_str, 'exit'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'exit')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reast_str = tmp_reast_str.rstrip(' ')
                    tmp_group_id = None
                    if tmp_reast_str.isdigit():
                        tmp_group_id = int(tmp_reast_str)
                    elif tmp_reast_str[0] == '-' and tmp_reast_str[1:].isdigit():
                        tmp_group_id = (-1) * int(tmp_reast_str[1:])
                    if tmp_group_id != None:
                        dictTValue['tGroupId'] = str(tmp_group_id)
                        tmp_reply_str = dictStrCustom['strBotExitRemote'].format(**dictTValue)
                        sendMsgByEvent(plugin_event, tmp_reply_str, tmp_group_id, 'group')
                        tmp_reply_str = dictStrCustom['strBotExitRemoteShow'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        time.sleep(1)
                        plugin_event.set_group_leave(tmp_group_id)
                elif isMatchWordStart(tmp_reast_str, 'accept'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'accept')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reast_str = tmp_reast_str.rstrip(' ')
                    if len(tmp_reast_str) > 0:
                        tmp_flag = tmp_reast_str
                        dictTValue['tInvateFlag'] = str(tmp_flag)
                        tmp_reply_str = dictStrCustom['strBotAddGroupRemoteAcceptShow'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        time.sleep(1)
                        plugin_event.set_group_add_request(tmp_flag, 'invite', True, '')
                elif isMatchWordStart(tmp_reast_str, 'pulse'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'pulse')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reast_str = tmp_reast_str.rstrip()
                    tmp_reast_str_list = tmp_reast_str.split(' ')
                    tmp_reast_str_list_2 = []
                    tmp_editKey = 'pulseUrlList'
                    tmp_pulseUrl = None
                    tmp_pulseToken = None
                    flag_action = None
                    for tmp_reast_str_list_this in tmp_reast_str_list:
                        if len(tmp_reast_str_list_this) != 0:
                            tmp_reast_str_list_2.append(tmp_reast_str_list_this)
                    tmp_reast_str_list = tmp_reast_str_list_2.copy()
                    if len(tmp_reast_str_list) == 1:
                        tmp_pulseUrl = OlivaDiceCore.data.defaultOlivaDicePulseUrl
                        tmp_pulseToken = tmp_reast_str_list[0]
                        flag_action = 'add'
                    elif len(tmp_reast_str_list) >= 2:
                        tmp_pulseUrl = tmp_reast_str_list[0]
                        tmp_pulseToken = tmp_reast_str_list[1]
                        if tmp_pulseUrl == 'del':
                            flag_action = 'del'
                        else:
                            flag_action = 'add'
                    if tmp_pulseUrl != None and tmp_pulseToken != None:
                        tmp_pulseUrlList_new = []
                        tmp_pulseUrlList = OlivaDiceCore.console.getConsoleSwitchByHash(
                            tmp_editKey,
                            plugin_event.bot_info.hash
                        )
                        flag_done = False
                        if flag_action == 'add':
                            for tmp_pulseUrlList_this in tmp_pulseUrlList:
                                if len(tmp_pulseUrlList_this) == 2:
                                    if tmp_pulseUrlList_this[0] == tmp_pulseUrl:
                                        tmp_pulseUrlList_new.append(
                                            [
                                                tmp_pulseUrl,
                                                tmp_pulseToken
                                            ]
                                        )
                                        flag_done = True
                                    else:
                                        tmp_pulseUrlList_new.append(tmp_pulseUrlList_this)
                            if not flag_done:
                                tmp_pulseUrlList_new.append(
                                    [
                                        tmp_pulseUrl,
                                        tmp_pulseToken
                                    ]
                                )
                                flag_done = True
                        elif flag_action == 'del':
                            for tmp_pulseUrlList_this in tmp_pulseUrlList:
                                if len(tmp_pulseUrlList_this) == 2:
                                    if tmp_pulseToken not in tmp_pulseUrlList_this:
                                        tmp_pulseUrlList_new.append(tmp_pulseUrlList_this)
                            flag_done = True
                        else:
                            tmp_reply_str = dictStrCustom['strMasterConsoleSetInvalid'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        tmp_pulseUrlList = OlivaDiceCore.console.setConsoleSwitchByHash(
                            tmp_editKey,
                            tmp_pulseUrlList_new,
                            plugin_event.bot_info.hash
                        )
                        OlivaDiceCore.console.saveConsoleSwitch()
                        dictTValue['tConsoleKey'] = tmp_editKey
                        tmp_reply_str = dictStrCustom['strMasterConsoleAppend'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    return
                elif isMatchWordStart(tmp_reast_str, 'notice') or isMatchWordStart(tmp_reast_str, 'master'):
                    tmp_editKey = None
                    if isMatchWordStart(tmp_reast_str, 'notice'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'notice')
                        tmp_reast_str = skipSpaceStart(tmp_reast_str)
                        tmp_editKey = 'noticeGroupList'
                    elif isMatchWordStart(tmp_reast_str, 'master'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'master')
                        tmp_reast_str = skipSpaceStart(tmp_reast_str)
                        tmp_editKey = 'masterList'
                    else:
                        return
                    tmp_reast_str = tmp_reast_str.rstrip()
                    tmp_reast_str_list = tmp_reast_str.split(' ')
                    tmp_reast_str_list_2 = []
                    tmp_listValue = None
                    flag_action = None
                    for tmp_reast_str_list_this in tmp_reast_str_list:
                        if len(tmp_reast_str_list_this) != 0:
                            tmp_reast_str_list_2.append(tmp_reast_str_list_this)
                    tmp_reast_str_list = tmp_reast_str_list_2.copy()
                    if len(tmp_reast_str_list) == 1:
                        if tmp_reast_str_list[0] == 'show':
                            flag_action = 'show'
                        else:
                            tmp_listValue = tmp_reast_str_list[-1]
                            flag_action = 'add'
                    elif len(tmp_reast_str_list) >= 2:
                        tmp_listValue = tmp_reast_str_list[-1]
                        if tmp_reast_str_list[0] == 'add':
                            flag_action = 'add'
                        elif tmp_reast_str_list[0] == 'del':
                            flag_action = 'del'
                        elif tmp_reast_str_list[0] == 'show':
                            flag_action = 'show'
                    if tmp_listValue != None:
                        if type(tmp_listValue) == str:
                            if tmp_listValue.isdigit() and tmp_editKey in [
                                'noticeGroupList',
                                'masterList'
                            ] and plugin_event.platform['platform'] not in [
                                'qqGuild'
                            ]:
                                tmp_listValue = int(tmp_listValue)
                            elif tmp_listValue == 'this' and flag_is_from_group and tmp_editKey in [
                                'noticeGroupList'
                            ]:
                                if 'host_id' in plugin_event.data.__dict__:
                                    if plugin_event.data.host_id != None:
                                        tmp_reply_str = dictStrCustom['strMasterConsoleSetInvalid'].format(**dictTValue)
                                        replyMsg(plugin_event, tmp_reply_str)
                                        return
                                tmp_listValue = plugin_event.data.group_id
                            elif tmp_listValue == 'this' and tmp_editKey in [
                                'masterList'
                            ]:
                                tmp_listValue = plugin_event.data.user_id
                            elif isMatchWordStart(tmp_listValue, '[CQ:at,qq=') and tmp_listValue[-1] == ']' and tmp_editKey in [
                                'masterList'
                            ]:
                                tmp_listValue_new = tmp_listValue[len('[CQ:at,qq='):-len(']')]
                                if plugin_event.platform['platform'] not in [
                                    'qqGuild'
                                ]:
                                    if tmp_listValue_new.isdigit():
                                        tmp_listValue = int(tmp_listValue_new)
                                    else:
                                        tmp_reply_str = dictStrCustom['strMasterConsoleSetInvalid'].format(**dictTValue)
                                        replyMsg(plugin_event, tmp_reply_str)
                                        return
                                else:
                                    tmp_listValue = tmp_listValue_new
                            else:
                                tmp_reply_str = dictStrCustom['strMasterConsoleSetInvalid'].format(**dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
                                return
                    if tmp_listValue != None and tmp_editKey != None:
                        tmp_dataList_new = []
                        tmp_dataList = OlivaDiceCore.console.getConsoleSwitchByHash(
                            tmp_editKey,
                            plugin_event.bot_info.hash
                        )
                        flag_done = False
                        if flag_action == 'add':
                            for tmp_dataList_this in tmp_dataList:
                                if len(tmp_dataList_this) == 2:
                                    if tmp_dataList_this[0] == tmp_listValue:
                                        flag_done = True
                                    tmp_dataList_new.append(tmp_dataList_this)
                            if not flag_done:
                                tmp_dataList_new.append(
                                    [
                                        tmp_listValue,
                                        plugin_event.platform['platform']
                                    ]
                                )
                                flag_done = True
                        elif flag_action == 'del':
                            for tmp_dataList_this in tmp_dataList:
                                if len(tmp_dataList_this) == 2:
                                    if tmp_dataList_this[0] != tmp_listValue:
                                        tmp_dataList_new.append(tmp_dataList_this)
                            flag_done = True
                        else:
                            tmp_reply_str = dictStrCustom['strMasterConsoleSetInvalid'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        tmp_dataList = OlivaDiceCore.console.setConsoleSwitchByHash(
                            tmp_editKey,
                            tmp_dataList_new,
                            plugin_event.bot_info.hash
                        )
                        OlivaDiceCore.console.saveConsoleSwitch()
                        dictTValue['tConsoleKey'] = tmp_editKey
                        tmp_reply_str = dictStrCustom['strMasterConsoleAppend'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    elif flag_action == 'show' and tmp_listValue == None and tmp_editKey != None:
                        tmp_dataList_new = []
                        tmp_dataList = OlivaDiceCore.console.getConsoleSwitchByHash(
                            tmp_editKey,
                            plugin_event.bot_info.hash
                        )
                        for tmp_dataList_this in tmp_dataList:
                            if len(tmp_dataList_this) == 2:
                                tmp_dataList_new.append(str(tmp_dataList_this[0]))
                        dictTValue['tConsoleKey'] = tmp_editKey
                        dictTValue['tConsoleValue'] = '\n'.join(tmp_dataList_new)
                        tmp_reply_str = dictStrCustom['strMasterConsoleShowList'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    return
                elif isMatchWordStart(tmp_reast_str, 'host'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'host')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    if isMatchWordStart(tmp_reast_str, 'on'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'on')
                        tmp_reast_str = skipSpaceStart(tmp_reast_str)
                        if flag_is_from_host:
                            if flag_hostEnable != True:
                                    OlivaDiceCore.userConfig.setUserConfigByKey(
                                        userConfigKey = 'hostEnable',
                                        userConfigValue = True,
                                        botHash = plugin_event.bot_info.hash,
                                        userId = plugin_event.data.host_id,
                                        userType = 'host',
                                        platform = plugin_event.platform['platform']
                                    )
                                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                        userHash = OlivaDiceCore.userConfig.getUserHash(
                                            userId = plugin_event.data.host_id,
                                            userType = 'host',
                                            platform = plugin_event.platform['platform']
                                        )
                                    )
                                    tmp_reply_str = dictStrCustom['strBotHostOn'].format(**dictTValue)
                            else:
                                tmp_reply_str = dictStrCustom['strBotAlreadyHostOn'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = dictStrCustom['strBotNotUnderHost'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                    elif isMatchWordStart(tmp_reast_str, 'off'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'off')
                        tmp_reast_str = skipSpaceStart(tmp_reast_str)
                        if flag_is_from_host:
                            if flag_hostEnable != False:
                                    OlivaDiceCore.userConfig.setUserConfigByKey(
                                        userConfigKey = 'hostEnable',
                                        userConfigValue = False,
                                        botHash = plugin_event.bot_info.hash,
                                        userId = plugin_event.data.host_id,
                                        userType = 'host',
                                        platform = plugin_event.platform['platform']
                                    )
                                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                        userHash = OlivaDiceCore.userConfig.getUserHash(
                                            userId = plugin_event.data.host_id,
                                            userType = 'host',
                                            platform = plugin_event.platform['platform']
                                        )
                                    )
                                    tmp_reply_str = dictStrCustom['strBotHostOff'].format(**dictTValue)
                            else:
                                tmp_reply_str = dictStrCustom['strBotAlreadyHostOff'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = dictStrCustom['strBotNotUnderHost'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                else:
                    tmp_reast_str = tmp_reast_str.strip(' ')
                    tmp_reast_list = tmp_reast_str.split(' ')
                    if len(tmp_reast_list) == 1:
                        if plugin_event.bot_info.hash in OlivaDiceCore.console.dictConsoleSwitch:
                            if tmp_reast_list[0] in OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]:
                                if type(OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash][tmp_reast_list[0]]) == int:
                                    dictTValue['tConsoleKey'] = tmp_reast_list[0]
                                    dictTValue['tConsoleValue'] = str(OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash][tmp_reast_list[0]])
                                    tmp_reply_str = dictStrCustom['strMasterConsoleShow'].format(**dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                    return
                        tmp_reply_str = dictStrCustom['strMasterConsoleNotFound'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    elif len(tmp_reast_list) > 1:
                        tmp_reast_str = ' '.join(tmp_reast_list[1:])
                        tmp_reast_str = tmp_reast_str.strip(' ')
                        if not tmp_reast_str.isdigit():
                            tmp_reply_str = dictStrCustom['strMasterConsoleSetInvalid'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        if plugin_event.bot_info.hash in OlivaDiceCore.console.dictConsoleSwitch:
                            if tmp_reast_list[0] in OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]:
                                if type(OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash][tmp_reast_list[0]]) == int:
                                    OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash][tmp_reast_list[0]] = int(tmp_reast_str)
                                    OlivaDiceCore.console.saveConsoleSwitch()   
                                    dictTValue['tConsoleKey'] = tmp_reast_list[0]
                                    dictTValue['tConsoleValue'] = tmp_reast_str
                                    tmp_reply_str = dictStrCustom['strMasterConsoleSet'].format(**dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                    return
                        tmp_reply_str = dictStrCustom['strMasterConsoleNotFound'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'system'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'system')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if isMatchWordStart(tmp_reast_str, 'restart'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'restart')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reply_str = dictStrCustom['strMasterSystemRestart'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    time.sleep(1)
                    Proc.set_restart()
                return
            elif isMatchWordStart(tmp_reast_str, 'str'):
                tmp_reast_str = tmp_reast_str.strip(' ')
                tmp_reast_list = tmp_reast_str.split(' ')
                if len(tmp_reast_list) == 1:
                    if plugin_event.bot_info.hash in OlivaDiceCore.msgCustom.dictStrCustomDict:
                        if tmp_reast_list[0] in OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]:
                            tmp_reply_str = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash][tmp_reast_list[0]]
                            replyMsg(plugin_event, tmp_reply_str)
                elif len(tmp_reast_list) >= 2:
                    tmp_new_str = ' '.join(tmp_reast_list[1:])
                    OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[plugin_event.bot_info.hash][tmp_reast_list[0]] = tmp_new_str
                    OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash][tmp_reast_list[0]] = tmp_new_str
                    OlivaDiceCore.msgCustomManager.saveMsgCustomByBotHash(plugin_event.bot_info.hash)
                    dictTValue['tStrName'] = tmp_reast_list[0]
                    tmp_reply_str = dictStrCustom['strSetStr'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
        else:
            if flag_messageFliterModeDisabled:
                plugin_event.set_block()
                return
            if isMatchWordStart(tmp_reast_str, 'master'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'master')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.strip(' ')
                if tmp_reast_str == OlivaDiceCore.data.bot_content['masterKey']:
                    OlivaDiceCore.data.bot_content['masterKey'] = str(uuid.uuid4())
                    OlivaDiceCore.console.setMasterListAppend(plugin_event.bot_info.hash, [plugin_event.data.user_id, plugin_event.platform['platform']])
                    OlivaDiceCore.console.saveConsoleSwitch()
                    tmp_reply_str = dictStrCustom['strBecomeMaster'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    #显示Master认主信息
                    dictTValue['tInitMasterKey'] = '.master %s' % OlivaDiceCore.data.bot_content['masterKey']
                    tmp_log_str =  dictStrConst['strToBeMaster'].format(**dictTValue)
                    logProc(Proc, 2, tmp_log_str, [
                        ('OlivaDice', 'default'),
                        ('reply', 'default')
                    ])
                else:
                    if (not flag_hostLocalEnable or not flag_groupEnable) and not flag_force_reply:
                        return
                    tmp_reply_str = dictStrCustom['strCantBecomeMaster'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
        if flag_messageFliterModeDisabled:
            plugin_event.set_block()
            return
        if isMatchWordStart(tmp_reast_str, 'bot'):
            tmp_end_list = ['', tmp_at_str]
            if tmp_at_str_sub != None:
                tmp_end_list.append(tmp_at_str_sub)
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'bot')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if isMatchWordStart(tmp_reast_str, 'on'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'on')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                if flag_is_from_group and tmp_reast_str in tmp_end_list:
                    if (flag_is_from_group_have_admin and flag_is_from_group_admin or not flag_is_from_group_have_admin) or flag_is_from_master:
                        if flag_groupEnable != True:
                            if flag_is_from_host:
                                if flag_hostEnable:
                                    OlivaDiceCore.userConfig.setUserConfigByKey(
                                        userConfigKey = 'groupEnable',
                                        userConfigValue = True,
                                        botHash = plugin_event.bot_info.hash,
                                        userId = tmp_hagID,
                                        userType = 'group',
                                        platform = plugin_event.platform['platform']
                                    )
                                else:
                                    if flag_is_from_master:
                                        OlivaDiceCore.userConfig.setUserConfigByKey(
                                            userConfigKey = 'groupWithHostEnable',
                                            userConfigValue = True,
                                            botHash = plugin_event.bot_info.hash,
                                            userId = tmp_hagID,
                                            userType = 'group',
                                            platform = plugin_event.platform['platform']
                                        )
                                    else:
                                        tmp_reply_str = dictStrCustom['strNeedMaster'].format(**dictTValue)
                                        replyMsg(plugin_event, tmp_reply_str)
                                        return
                            else:
                                OlivaDiceCore.userConfig.setUserConfigByKey(
                                    userConfigKey = 'groupEnable',
                                    userConfigValue = True,
                                    botHash = plugin_event.bot_info.hash,
                                    userId = tmp_hagID,
                                    userType = 'group',
                                    platform = plugin_event.platform['platform']
                                )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = tmp_hagID,
                                    userType = 'group',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                            tmp_reply_str = dictStrCustom['strBotOn'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = dictStrCustom['strBotAlreadyOn'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'off'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'off')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                if flag_is_from_group and tmp_reast_str in tmp_end_list:
                    if (flag_is_from_group_have_admin and flag_is_from_group_admin or not flag_is_from_group_have_admin) or flag_is_from_master:
                        if flag_groupEnable != False:
                            if flag_is_from_host:
                                if flag_hostEnable:
                                    OlivaDiceCore.userConfig.setUserConfigByKey(
                                        userConfigKey = 'groupEnable',
                                        userConfigValue = False,
                                        botHash = plugin_event.bot_info.hash,
                                        userId = tmp_hagID,
                                        userType = 'group',
                                        platform = plugin_event.platform['platform']
                                    )
                                else:
                                    if flag_is_from_master:
                                        OlivaDiceCore.userConfig.setUserConfigByKey(
                                            userConfigKey = 'groupWithHostEnable',
                                            userConfigValue = False,
                                            botHash = plugin_event.bot_info.hash,
                                            userId = tmp_hagID,
                                            userType = 'group',
                                            platform = plugin_event.platform['platform']
                                        )
                                    else:
                                        tmp_reply_str = dictStrCustom['strNeedMaster'].format(**dictTValue)
                                        replyMsg(plugin_event, tmp_reply_str)
                                        return
                            else:
                                OlivaDiceCore.userConfig.setUserConfigByKey(
                                    userConfigKey = 'groupEnable',
                                    userConfigValue = False,
                                    botHash = plugin_event.bot_info.hash,
                                    userId = tmp_hagID,
                                    userType = 'group',
                                    platform = plugin_event.platform['platform']
                                )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = tmp_hagID,
                                    userType = 'group',
                                    platform = plugin_event.platform['platform']
                                )
                            )
                            tmp_reply_str = dictStrCustom['strBotOff'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = dictStrCustom['strBotAlreadyOff'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'host'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'host')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if isMatchWordStart(tmp_reast_str, 'on'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'on')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reast_str = tmp_reast_str.rstrip(' ')
                    if flag_is_from_group and tmp_reast_str in tmp_end_list:
                        if ((flag_is_from_group_have_admin and flag_is_from_group_admin and not flag_is_from_group_sub_admin) or not flag_is_from_group_have_admin) or flag_is_from_master:
                            if flag_is_from_host:
                                if flag_hostLocalEnable != True:
                                    OlivaDiceCore.userConfig.setUserConfigByKey(
                                        userConfigKey = 'hostLocalEnable',
                                        userConfigValue = True,
                                        botHash = plugin_event.bot_info.hash,
                                        userId = plugin_event.data.host_id,
                                        userType = 'host',
                                        platform = plugin_event.platform['platform']
                                    )
                                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                        userHash = OlivaDiceCore.userConfig.getUserHash(
                                            userId = plugin_event.data.host_id,
                                            userType = 'host',
                                            platform = plugin_event.platform['platform']
                                        )
                                    )
                                    tmp_reply_str = dictStrCustom['strBotHostLocalOn'].format(**dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                else:
                                    tmp_reply_str = dictStrCustom['strBotAlreadyHostLocalOn'].format(**dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                            else:
                                tmp_reply_str = dictStrCustom['strBotNotUnderHost'].format(**dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
                elif isMatchWordStart(tmp_reast_str, 'off'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'off')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reast_str = tmp_reast_str.rstrip(' ')
                    if flag_is_from_group and tmp_reast_str in tmp_end_list:
                        if ((flag_is_from_group_have_admin and flag_is_from_group_admin and not flag_is_from_group_sub_admin) or not flag_is_from_group_have_admin) or flag_is_from_master:
                            if flag_is_from_host:
                                if flag_hostLocalEnable != False:
                                    OlivaDiceCore.userConfig.setUserConfigByKey(
                                        userConfigKey = 'hostLocalEnable',
                                        userConfigValue = False,
                                        botHash = plugin_event.bot_info.hash,
                                        userId = plugin_event.data.host_id,
                                        userType = 'host',
                                        platform = plugin_event.platform['platform']
                                    )
                                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                        userHash = OlivaDiceCore.userConfig.getUserHash(
                                            userId = plugin_event.data.host_id,
                                            userType = 'host',
                                            platform = plugin_event.platform['platform']
                                        )
                                    )
                                    tmp_reply_str = dictStrCustom['strBotHostLocalOff'].format(**dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                else:
                                    tmp_reply_str = dictStrCustom['strBotAlreadyHostLocalOff'].format(**dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                            else:
                                tmp_reply_str = dictStrCustom['strBotNotUnderHost'].format(**dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'exit'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'exit')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                if flag_is_from_group and tmp_reast_str in tmp_end_list:
                    if (flag_is_from_group_have_admin and flag_is_from_group_admin) or flag_is_from_master:
                        tmp_reply_str = dictStrCustom['strBotExit'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        time.sleep(1)
                        plugin_event.set_group_leave(plugin_event.data.group_id)
            elif isMatchWordStart(tmp_reast_str, 'summary', fullMatch = True) and flag_is_from_master:
                tmp_reply_str = ''
                tmp_reply_str += OlivaDiceCore.data.bot_summary
                replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'model', fullMatch = True):
                tmp_reply_str = ''
                tmp_reply_str_list = []
                for sub_model_this in OlivaDiceCore.crossHook.dictHookList['model']:
                    tmp_reply_str_list.append('%s V.%s' % (sub_model_this[0], sub_model_this[1]))
                tmp_reply_str = '\n'.join(tmp_reply_str_list)
                replyMsg(plugin_event, tmp_reply_str)
            elif len(tmp_reast_str) == 0:
                tmp_reply_str = OlivaDiceCore.data.bot_info + '\n' + dictStrCustom['strBot'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            return
        #此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            plugin_event.set_block()
            return
        #此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            plugin_event.set_block()
            return
        if isMatchWordStart(tmp_reast_str, 'help'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'help')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            if tmp_reast_str == '':
                tmp_reast_str = None
            if tmp_reast_str != None:
                if tmp_reast_str == 'master':
                    tmp_dataList_new = []
                    tmp_dataList = OlivaDiceCore.console.getConsoleSwitchByHash(
                        'masterList',
                        plugin_event.bot_info.hash
                    )
                    for tmp_dataList_this in tmp_dataList:
                        if len(tmp_dataList_this) == 2:
                            tmp_dataList_new.append(str(tmp_dataList_this[0]))
                    dictTValue['tHelpDocResult'] = ', '.join(tmp_dataList_new)
                    tmp_reply_str = dictStrCustom['strHelpDoc'].format(**dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.helpDoc.getHelp(tmp_reast_str, plugin_event.bot_info.hash)
            else:
                tmp_reply_str = OlivaDiceCore.helpDoc.getHelp('default', plugin_event.bot_info.hash)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'draw'):
            flag_hide = False
            tmp_card_count = 1
            tmp_card_count_str = None
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'draw')
            if isMatchWordStart(tmp_reast_str, 'h'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'h')
                flag_hide = True
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            [tmp_reast_str, tmp_card_count_str] = getNumberPara(tmp_reast_str, reverse = True)
            if tmp_card_count_str == '':
                tmp_card_count_str = None
            if tmp_card_count_str != None:
                tmp_card_count = int(tmp_card_count_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reast_str = tmp_reast_str.lstrip('_')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reply_str = None
            if tmp_reast_str == '':
                tmp_reast_str = None
            if tmp_reast_str != None:
                tmp_reply_str = OlivaDiceCore.drawCard.getDrawDeck(
                    tmp_reast_str,
                    plugin_event.bot_info.hash,
                    count = tmp_card_count
                )
                if flag_hide:
                    replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                    tmp_reply_str = dictStrCustom['strDrawDeckHideShow'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
            else:
                tmp_reply_str = OlivaDiceCore.helpDoc.getHelp('draw', plugin_event.bot_info.hash)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'ti', fullMatch = True):
            dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck('即时症状', plugin_event.bot_info.hash)
            tmp_reply_str = dictStrCustom['strDrawTi'].format(**dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'li', fullMatch = True):
            dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck('总结症状', plugin_event.bot_info.hash)
            tmp_reply_str = dictStrCustom['strDrawLi'].format(**dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'name'):
            tmp_card_count = 1
            tmp_card_count_str = None
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'name')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            [tmp_reast_str, tmp_card_count_str] = getNumberPara(tmp_reast_str, reverse = True)
            if tmp_card_count_str == '':
                tmp_card_count_str = None
            if tmp_card_count_str != None:
                tmp_card_count = int(tmp_card_count_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            if tmp_reast_str in ['cn', 'jp', 'en', 'enzh']:
                dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck(
                    '随机姓名_%s' % tmp_reast_str, 
                    plugin_event.bot_info.hash,
                    count = tmp_card_count
                )
            else:
                dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck(
                    '随机姓名',
                    plugin_event.bot_info.hash,
                    count = tmp_card_count
                )
            tmp_reply_str = dictStrCustom['strDrawName'].format(**dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'nn'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'nn')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) > 0:
                tmp_pc_id = plugin_event.data.user_id
                tmp_pc_platform = plugin_event.platform['platform']
                tmp_pc_name = tmp_reast_str
                tmp_pc_name = tmp_pc_name.strip()
                if tmp_pc_name != None:
                    if not OlivaDiceCore.pcCard.checkPcName(tmp_pc_name):
                        return
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                )
                if OlivaDiceCore.pcCard.pcCardRebase(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_pc_name
                ):
                    dictTValue['tPcSelectionNew'] = tmp_pc_name
                    if tmp_pc_name_1 != None:
                        dictTValue['tPcSelection'] = tmp_pc_name_1
                    else:
                        dictTValue['tPcSelection'] = dictTValue['tName']
                    tmp_reply_str = dictStrCustom['strPcRename'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                replyMsgLazyHelpByEvent(plugin_event, 'nn')
            return
        elif isMatchWordStart(tmp_reast_str, 'st'):
            tmp_pc_name = None
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_1 = ''
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'st')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_skill_name = None
            tmp_skill_value = None
            tmp_skill_name_find = None
            tmp_skill_value_find = 0
            tmp_skill_pair_list = []
            if isMatchWordStart(tmp_reast_str, 'show', fullMatch = True):
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    tmp_pcHash
                )
                if tmp_pc_name_1 != None:
                    dictTValue['tName'] = tmp_pc_name_1
                tmp_dict_pc_card = OlivaDiceCore.pcCard.pcCardDataGetByPcName(
                    tmp_pcHash
                )
                flag_begin = True
                tmp_dict_pc_card_dump = {}
                for tmp_dict_pc_card_key in tmp_dict_pc_card:
                    tmp_dict_pc_card_dump[
                        OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                            tmp_pcHash,
                            tmp_dict_pc_card_key,
                            flagShow = True
                        )
                    ] = tmp_dict_pc_card[tmp_dict_pc_card_key]
                tmp_reply_str_1_list = []
                tmp_reply_str_1_dict = {}
                tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    tmp_pcHash,
                    dictTValue['tName'],
                    'enhanceList',
                    []
                )
                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    tmp_pcHash,
                    dictTValue['tName'],
                    'template',
                    'default'
                )
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                tmp_skill_dict = {}
                if 'skill' in tmp_template:
                    tmp_skill_dict = tmp_template['skill']
                flag_hit_skill_list_name_default = '其它'
                for tmp_dict_pc_card_key in tmp_dict_pc_card_dump:
                    flag_hit_skill_list_name = flag_hit_skill_list_name_default
                    tmp_dict_pc_card_key_core = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                        tmp_pcHash,
                        tmp_dict_pc_card_key
                    )
                    tmp_reply_str_1_list_this = '%s:%s' % (
                        tmp_dict_pc_card_key,
                        tmp_dict_pc_card_dump[tmp_dict_pc_card_key]
                    )
                    if tmp_dict_pc_card_key_core in tmp_enhanceList:
                        tmp_reply_str_1_list_this = '[*]' + tmp_reply_str_1_list_this
                    for tmp_skill_dict_this in tmp_skill_dict:
                        if type(tmp_skill_dict[tmp_skill_dict_this]) == list:
                            if tmp_dict_pc_card_key_core in tmp_skill_dict[tmp_skill_dict_this]:
                                flag_hit_skill_list_name = tmp_skill_dict_this
                                break
                    if flag_hit_skill_list_name not in tmp_reply_str_1_dict:
                        tmp_reply_str_1_dict[flag_hit_skill_list_name] = []
                    tmp_reply_str_1_dict[flag_hit_skill_list_name].append(tmp_reply_str_1_list_this)
                for tmp_reply_str_1_dict_this in tmp_reply_str_1_dict:
                    if tmp_reply_str_1_dict_this != flag_hit_skill_list_name_default:
                        tmp_reply_str_1_list.append(
                            '<%s>\n%s' % (
                                tmp_reply_str_1_dict_this,
                                ' '.join(tmp_reply_str_1_dict[tmp_reply_str_1_dict_this])
                            )
                        )
                if flag_hit_skill_list_name_default in tmp_reply_str_1_dict:
                    tmp_reply_str_1_list.append(
                        '<%s>\n%s' % (
                            flag_hit_skill_list_name_default,
                            ' '.join(tmp_reply_str_1_dict[flag_hit_skill_list_name_default])
                        )
                    )
                tmp_reply_str_1 = '\n'.join(tmp_reply_str_1_list)
                dictTValue['tPcShow'] = tmp_reply_str_1
                tmp_reply_str = dictStrCustom['strPcShow'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'list', fullMatch = True):
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                )
                tmp_dict_pc_card = OlivaDiceCore.pcCard.pcCardDataGetUserAll(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                )
                flag_begin = True
                for tmp_dict_pc_card_this in tmp_dict_pc_card:
                    if flag_begin:
                        flag_begin = False
                    else:
                        tmp_reply_str_1 += '\n'
                    tmp_reply_str_1 += '%s' % (tmp_dict_pc_card_this, )
                if tmp_pc_name_1 != None:
                    dictTValue['tPcSelection'] = tmp_pc_name_1
                dictTValue['tPcList'] = tmp_reply_str_1
                tmp_reply_str = dictStrCustom['strPcList'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'set'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'set')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if len(tmp_reast_str) > 0:
                    tmp_pc_name = tmp_reast_str
                    tmp_pc_name = tmp_pc_name.strip()
                    if OlivaDiceCore.pcCard.pcCardDataSetSelectionKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_pc_name
                    ):
                        dictTValue['tPcSelection'] = tmp_pc_name
                        tmp_reply_str = dictStrCustom['strPcSet'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strPcSetError'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'init'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'init')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                flag_force_init = False
                if isMatchWordStart(tmp_reast_str, 'force', fullMatch = True):
                    flag_force_init = True
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'force')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                tmp_dict_pc_card = OlivaDiceCore.pcCard.pcCardDataGetByPcName(
                    tmp_pcHash
                )
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    tmp_pcHash
                )
                tmp_template_name = 'default'
                if tmp_pc_name != None:
                    dictTValue['tName'] = tmp_pc_name
                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    tmp_pcHash,
                    dictTValue['tName'],
                    'template',
                    'default'
                )
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                tmp_init_dict = {}
                tmp_template_customDefault = None
                if 'init' in tmp_template:
                    tmp_init_dict = tmp_template['init']
                if 'customDefault' in tmp_template:
                    tmp_template_customDefault = tmp_template['customDefault']
                tmp_pcCard_list = []
                for tmp_init_dict_this in tmp_init_dict:
                    if not flag_force_init and tmp_init_dict_this in tmp_dict_pc_card:
                        continue
                    if type(tmp_init_dict[tmp_init_dict_this]) == str:
                        tmp_skill_rd = OlivaDiceCore.onedice.RD(
                            tmp_init_dict[tmp_init_dict_this],
                            tmp_template_customDefault,
                            valueTable = tmp_dict_pc_card
                        )
                        tmp_skill_rd.roll()
                        if tmp_skill_rd.resError == None:
                            OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                tmp_pcHash,
                                tmp_init_dict_this,
                                tmp_skill_rd.resInt,
                                dictTValue['tName'],
                                hitList = None,
                                forceMapping = flag_force_init
                            )
                            tmp_pcCard_list.append(
                                '%s:%s' % (
                                    OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                        tmp_pcHash,
                                        tmp_init_dict_this,
                                        flagShow = True
                                    ),
                                    str(tmp_skill_rd.resInt)
                                )
                            )
                dictTValue['tPcInitResult'] = '\n%s' % ' '.join(tmp_pcCard_list)
                dictTValue['tPcTempName'] = tmp_template_name
                tmp_reply_str = dictStrCustom['strPcInitSt'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'del'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'del')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                tmp_pc_name = tmp_reast_str
                tmp_pc_name = tmp_pc_name.strip()
                if len(tmp_pc_name) == 0:
                    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                        tmp_pcHash
                    )
                if tmp_pc_name != None:
                    OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name,
                        'enhanceList',
                        []
                    )
                    if OlivaDiceCore.pcCard.pcCardDataDelSelectionKey(
                        tmp_pcHash,
                        tmp_pc_name
                    ):
                        dictTValue['tPcSelection'] = tmp_pc_name
                        tmp_reply_str = dictStrCustom['strPcDel'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strPcDelError'].format(**dictTValue)
                else:
                    tmp_reply_str = dictStrCustom['strPcDelNone'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'clear', fullMatch = True):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'clear')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    tmp_pcHash
                )
                if tmp_pc_name != None:
                    OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name,
                        'enhanceList',
                        []
                    )
                    OlivaDiceCore.pcCard.pcCardDataDelSelectionKey(
                        tmp_pcHash,
                        tmp_pc_name
                    )
                    OlivaDiceCore.pcCard.pcCardRebase(
                        tmp_pcHash,
                        tmp_pc_name
                    )
                    dictTValue['tPcSelection'] = tmp_pc_name
                    tmp_reply_str = dictStrCustom['strPcClear'].format(**dictTValue)
                else:
                    tmp_reply_str = dictStrCustom['strPcClearNone'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'rm'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rm')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    tmp_pcHash
                )
                tmp_pcSkillName = tmp_reast_str
                tmp_pcSkillName = tmp_pcSkillName.strip()
                tmp_pcSkillName = tmp_pcSkillName.upper()
                if tmp_pcSkillName == '':
                    tmp_pcSkillName = None
                if tmp_pc_name != None and tmp_pcSkillName != None:
                    tmp_enhanceList_new = []
                    tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name,
                        'enhanceList',
                        []
                    )
                    tmp_skill_name_core = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                        tmp_pcHash,
                        tmp_pcSkillName
                    )
                    for tmp_enhanceList_this in tmp_enhanceList:
                        if tmp_skill_name_core != tmp_enhanceList_this:
                            tmp_enhanceList_new.append(tmp_enhanceList_this)
                    OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name,
                        'enhanceList',
                        tmp_enhanceList_new
                    )
                    OlivaDiceCore.pcCard.pcCardDataDelBySkillName(
                        tmp_pcHash,
                        tmp_pcSkillName,
                        tmp_pc_name
                    )
                    dictTValue['tPcSelection'] = tmp_pc_name
                    dictTValue['tSkillName'] = tmp_pcSkillName
                    tmp_reply_str = dictStrCustom['strPcRm'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                elif tmp_pcSkillName != None:
                    tmp_reply_str = dictStrCustom['strPcRmCardNone'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                else:
                    replyMsgLazyHelpByEvent(plugin_event, 'st')
                return
            elif isMatchWordStart(tmp_reast_str, 'temp'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'temp')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                )
                if len(tmp_reast_str) > 0:
                    tmp_template_name = tmp_reast_str
                    tmp_template_name = tmp_template_name.strip()
                    if tmp_pc_name != None:
                        dictTValue['tName'] = tmp_pc_name
                        if OlivaDiceCore.pcCard.pcCardDataSetTemplateKey(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_pc_name,
                            tmp_template_name
                        ):
                            dictTValue['tPcSelection'] = tmp_pc_name
                            dictTValue['tPcTempName'] = tmp_template_name
                            tmp_reply_str = dictStrCustom['strPcTemp'].format(**dictTValue)
                        else:
                            tmp_reply_str = dictStrCustom['strPcTempError'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strPcTempError'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                else:
                    if tmp_pc_name != None:
                        dictTValue['tName'] = tmp_pc_name
                        tmp_template_name = None
                        tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_pc_name
                        )
                        if tmp_template_name == None:
                            tmp_template_name = 'default'
                        dictTValue['tPcSelection'] = tmp_pc_name
                        dictTValue['tPcTempName'] = tmp_template_name
                        tmp_reply_str = dictStrCustom['strPcTempShow'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strPcTempError'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'rule'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rule')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                )
                if len(tmp_reast_str) > 0:
                    tmp_template_rule_name = tmp_reast_str
                    tmp_template_rule_name = tmp_template_rule_name.strip()
                    if tmp_pc_name != None:
                        dictTValue['tName'] = tmp_pc_name
                        tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_pc_name
                        )
                        if tmp_template_name == None:
                            tmp_template_name = 'default'
                        if OlivaDiceCore.pcCard.pcCardDataSetTemplateKey(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_pc_name,
                            tmp_template_name,
                            tmp_template_rule_name
                        ):
                            dictTValue['tPcSelection'] = tmp_pc_name
                            dictTValue['tPcTempName'] = tmp_template_name
                            dictTValue['tPcTempRuleName'] = tmp_template_rule_name
                            tmp_reply_str = dictStrCustom['strPcTempRule'].format(**dictTValue)
                        else:
                            tmp_reply_str = dictStrCustom['strPcTempRuleError'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strPcTempRuleError'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                else:
                    if tmp_pc_name != None:
                        dictTValue['tName'] = tmp_pc_name
                        tmp_template_name = None
                        tmp_template_rule_name = None
                        tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_pc_name
                        )
                        tmp_template_rule_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateRuleKey(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_pc_name
                        )
                        if tmp_template_name == None:
                            tmp_template_name = 'default'
                        if tmp_template_rule_name == None:
                            tmp_template_rule_name = 'default'
                        dictTValue['tPcSelection'] = tmp_pc_name
                        dictTValue['tPcTempName'] = tmp_template_name
                        dictTValue['tPcTempRuleName'] = tmp_template_rule_name
                        tmp_reply_str = dictStrCustom['strPcTempRuleShow'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strPcTempRuleError'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            tmp_reast_str_new = tmp_reast_str
            if len(tmp_reast_str_new) > 0:
                tmp_reast_str_list = tmp_reast_str_new.split(' ')
                tmp_skill_update_flag = None
                tmp_skill_value_update = None
                [tmp_skill_name, tmp_skill_value] = getExpression(tmp_reast_str_new, reverse = True)
                if tmp_skill_name == '':
                    tmp_skill_name = None
                if tmp_skill_value == '':
                    tmp_skill_value = None
                if tmp_skill_value != None:
                    if len(tmp_skill_value) > 1 and tmp_skill_value[0] == '+':
                        tmp_skill_update_flag = '+'
                        tmp_skill_value_update = tmp_skill_value[1:]
                    elif len(tmp_skill_value) > 1 and tmp_skill_value[0] == '-':
                        tmp_skill_update_flag = '-'
                        tmp_skill_value_update = tmp_skill_value[1:]
                    else:
                        tmp_skill_value = None
                if tmp_skill_name != None and tmp_skill_value != None:
                    tmp_skill_name = tmp_skill_name.strip()
                    tmp_skill_name = tmp_skill_name.upper()
                    tmp_pc_id = plugin_event.data.user_id
                    tmp_pc_platform = plugin_event.platform['platform']
                    tmp_skill_value_old = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_skill_name
                    )
                    rd_para_str = str(tmp_skill_value_old) + tmp_skill_value

                    tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        )
                    )
                    if tmp_pc_name_1 != None:
                        dictTValue['tName'] = tmp_pc_name_1
                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        dictTValue['tName']
                    )
                    tmp_template_customDefault = None
                    if tmp_template_name != None:
                        tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                        if 'customDefault' in tmp_template:
                            tmp_template_customDefault = tmp_template['customDefault']
                    rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault)
                    rd_para.roll()
                    if rd_para.resError == None:
                        tmp_skill_value_new = rd_para.resInt
                        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_skill_name,
                            tmp_skill_value_new,
                            dictTValue['tName']
                        )
                        dictTValue['tSkillName'] = tmp_skill_name
                        if tmp_skill_value_update.isdigit() or len(rd_para.resDetail) > 100:
                            if len(str(tmp_skill_value_new)) > 50:
                                dictTValue['tSkillUpdate'] = '%s=%s' % (rd_para_str, str(tmp_skill_value_new)[:50] + '...')
                            else:
                                dictTValue['tSkillUpdate'] = '%s=%s' % (rd_para_str, str(tmp_skill_value_new))
                        else:
                            if len(str(tmp_skill_value_new)) > 50:
                                dictTValue['tSkillUpdate'] = '%s=%s=%s' % (rd_para_str, rd_para.resDetail, str(tmp_skill_value_new)[:50] + '...')
                            else:
                                dictTValue['tSkillUpdate'] = '%s=%s=%s' % (rd_para_str, rd_para.resDetail, str(tmp_skill_value_new))
                        tmp_reply_str = dictStrCustom['strPcUpdateSkillValue'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        return
                tmp_skill_name = None
                tmp_skill_value = None
            if len(tmp_reast_str) > 0:
                tmp_reast_str_bak = tmp_reast_str
                [tmp_pc_name, tmp_reast_str] = splitBy(tmp_reast_str, '-')
                if tmp_reast_str == '-':
                    tmp_pc_name = None
                    return
                elif tmp_reast_str == '':
                    tmp_pc_name == None
                    tmp_reast_str = tmp_reast_str_bak
                elif tmp_pc_name == '':
                    tmp_pc_name = None
                    tmp_reast_str = tmp_reast_str[1:]
                else:
                    tmp_reast_str = tmp_reast_str[1:]
                if tmp_pc_name != None:
                    tmp_pc_name = tmp_pc_name.strip()
                if tmp_pc_name == '':
                    tmp_pc_name = None
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip()
            if tmp_pc_name != None:
                if not OlivaDiceCore.pcCard.checkPcName(tmp_pc_name):
                    return
            while len(tmp_reast_str) > 0 and tmp_skill_name_find == None:
                tmp_skill_name = None
                tmp_skill_value = None
                [tmp_skill_name, tmp_reast_str] = getToNumberPara(tmp_reast_str)
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if len(tmp_reast_str) > 0:
                    [tmp_skill_value, tmp_reast_str] = getNumberPara(tmp_reast_str)
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if tmp_skill_name == '':
                    tmp_skill_name = None
                if tmp_skill_value == '':
                    tmp_skill_value = None
                if tmp_skill_value != None:
                    tmp_skill_value = int(tmp_skill_value)
                if tmp_skill_name != None:
                    if tmp_skill_name[-1] in ['=', ':']:
                        tmp_skill_name = tmp_skill_name[:-1]
                    tmp_skill_name = tmp_skill_name.upper()
                    if len(tmp_skill_pair_list) == 0:
                        if tmp_skill_value != None:
                            tmp_skill_pair_list.append([tmp_skill_name, tmp_skill_value])
                        else:
                            tmp_skill_name_find = tmp_skill_name
                    else:
                        if tmp_skill_value != None:
                            tmp_skill_pair_list.append([tmp_skill_name, tmp_skill_value])
                        else:
                            return
                else:
                    return
            if tmp_skill_name_find == None:
                if len(tmp_skill_pair_list) > 0:
                    tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        )
                    )
                    if tmp_pc_name_1 != None:
                        dictTValue['tName'] = tmp_pc_name_1
                    if tmp_pc_name != None:
                        dictTValue['tName'] = tmp_pc_name
                    for tmp_skill_pair_this in tmp_skill_pair_list:
                        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            tmp_skill_pair_this[0],
                            tmp_skill_pair_this[1],
                            dictTValue['tName']
                        )
                    tmp_reply_str = dictStrCustom['strPcSetSkillValue'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                )
                tmp_skill_value_find = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_skill_name_find
                )
                if tmp_pc_name_1 != None:
                    dictTValue['tName'] = tmp_pc_name_1
                dictTValue['tSkillName'] = tmp_skill_name_find
                dictTValue['tSkillValue'] = str(tmp_skill_value_find)
                tmp_reply_str = dictStrCustom['strPcGetSingleSkillValue'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
        elif isMatchWordStart(tmp_reast_str, 'setcoc'):
            if flag_is_from_group:
                tmp_user_platform = plugin_event.platform['platform']
                tmp_hag_id = tmp_hagID
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'setcoc')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip()
                tmp_switch_setcoc = None
                if tmp_reast_str.isdigit():
                    tmp_switch_setcoc = int(tmp_reast_str)
                    if tmp_switch_setcoc not in [0, 1, 2, 3, 4, 5, 6]:
                        tmp_switch_setcoc = None
                if tmp_switch_setcoc != None:
                    tmp_templateName = 'COC7'
                    tmp_templateRuleName = 'default'
                    if tmp_switch_setcoc in [0, 1, 2, 3, 4, 5]:
                        tmp_templateRuleName = 'C%s' % str(tmp_switch_setcoc)
                    elif tmp_switch_setcoc == 6:
                        tmp_templateRuleName = 'DeltaGreen'
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userConfigKey = 'groupTemplate',
                        userConfigValue = tmp_templateName,
                        botHash = plugin_event.bot_info.hash,
                        userId = tmp_hag_id,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userConfigKey = 'groupTemplateRule',
                        userConfigValue = tmp_templateRuleName,
                        botHash = plugin_event.bot_info.hash,
                        userId = tmp_hag_id,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                    dictTValue['tPcTempName'] = tmp_templateName
                    dictTValue['tPcTempRuleName'] = tmp_templateRuleName
                    if tmp_templateRuleName in OlivaDiceCore.msgCustom.dictSetCOCDetail:
                        dictTValue['tLazyResult'] = ':\n%s' % OlivaDiceCore.msgCustom.dictSetCOCDetail[tmp_templateRuleName]
                    tmp_reply_str = dictStrCustom['strSetGroupTempRule'].format(**dictTValue)
                else:
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userConfigKey = 'groupTemplate',
                        userConfigValue = None,
                        botHash = plugin_event.bot_info.hash,
                        userId = tmp_hag_id,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userConfigKey = 'groupTemplateRule',
                        userConfigValue = None,
                        botHash = plugin_event.bot_info.hash,
                        userId = tmp_hag_id,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                    tmp_reply_str = dictStrCustom['strDelGroupTempRule'].format(**dictTValue)
                OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                    userHash = OlivaDiceCore.userConfig.getUserHash(
                        userId = tmp_hag_id,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                )
            else:
                tmp_reply_str = dictStrCustom['strForGroupOnly'].format(**dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'coc') or isMatchWordStart(tmp_reast_str, 'dnd'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_1 = ''
            tmp_pcCardTemplateName = 'default'
            if isMatchWordStart(tmp_reast_str, 'coc'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'coc')
                tmp_pcCardTemplateName = 'COC7'
            elif isMatchWordStart(tmp_reast_str, 'dnd'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'dnd')
                tmp_pcCardTemplateName = 'DND5E'
            tmp_roll_count = 1
            tmp_roll_count_str = None
            tmp_pcCardTemplate = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_pcCardTemplateName)
            tmp_res_list = []
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) > 0:
                [tmp_roll_count_str, tmp_reast_str] = getNumberPara(tmp_reast_str)
            if tmp_roll_count_str == '':
                tmp_roll_count_str = None
            if tmp_roll_count_str != None:
                if tmp_roll_count_str.isdigit():
                    tmp_roll_count = int(tmp_roll_count_str)
            if tmp_roll_count > 0 and tmp_roll_count <= 10:
                tmp_res_list = []
                tmp_range_list = range(0, tmp_roll_count)
                for tmp_i in tmp_range_list:
                    tmp_res_list_node = {}
                    for tmp_pcCardTemplate_skill_this in tmp_pcCardTemplate['init']:
                        tmp_skill_rd_this = OlivaDiceCore.onedice.RD(tmp_pcCardTemplate['init'][tmp_pcCardTemplate_skill_this])
                        tmp_skill_rd_this.roll()
                        if tmp_skill_rd_this.resError == None:
                            tmp_res_list_node[tmp_pcCardTemplate_skill_this] = tmp_skill_rd_this.resInt
                    tmp_res_list.append(tmp_res_list_node)
                tmp_reply_str_1 = ''
                dictTValue['tPcTempName'] = tmp_pcCardTemplateName
                for tmp_res_list_this in tmp_res_list:
                    tmp_reply_str_1 += '\n'
                    tmp_total_count_1 = 0
                    tmp_total_count_2 = 0
                    for tmp_res_list_this_this in tmp_res_list_this:
                        tmp_skill_name_this_1 = tmp_res_list_this_this
                        if tmp_res_list_this_this in tmp_pcCardTemplate['showName']:
                            tmp_skill_name_this_1 = tmp_pcCardTemplate['showName'][tmp_res_list_this_this]
                        tmp_reply_str_1 += '%s:%d  ' % (tmp_skill_name_this_1, tmp_res_list_this[tmp_res_list_this_this])
                        tmp_total_count_2 += tmp_res_list_this[tmp_res_list_this_this]
                        if tmp_res_list_this_this != 'LUC':
                            tmp_total_count_1 += tmp_res_list_this[tmp_res_list_this_this]
                    if tmp_pcCardTemplateName == 'COC7':
                        tmp_reply_str_1 += '共计:%d/%d %.2f%%' % (tmp_total_count_1, tmp_total_count_2, 100 * tmp_total_count_1 / tmp_total_count_2)
                    elif tmp_pcCardTemplateName == 'DND5E':
                        tmp_reply_str_1 += '共计:%d' % tmp_total_count_1
                dictTValue['tPcInitResult'] = tmp_reply_str_1
                tmp_reply_str = dictStrCustom['strPcInit'].format(**dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            else:
                return
        elif isMatchWordStart(tmp_reast_str, 'sc'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'sc')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) <= 0:
                return
            tmp_reast_str_list = tmp_reast_str.split(' ')
            tmp_sancheck_para = None
            tmp_san_val = None
            if len(tmp_reast_str_list) >= 2:
                tmp_sancheck_para = tmp_reast_str_list[0]
                if tmp_reast_str_list[-1].isdigit():
                    tmp_san_val = tmp_reast_str_list[-1]
            elif len(tmp_reast_str_list) == 1:
                tmp_sancheck_para = tmp_reast_str
            else:
                return
            if tmp_sancheck_para == None:
                return
            tmp_sancheck_para_list = tmp_sancheck_para.split('/')
            tmp_sancheck_para_s = None
            tmp_sancheck_para_f = None
            if len(tmp_sancheck_para_list) >= 2:
                tmp_sancheck_para_s = tmp_sancheck_para_list[0]
                tmp_sancheck_para_f = ''
                flag_begin_tmp_sancheck_para_list = True
                for tmp_sancheck_para_list_this in tmp_sancheck_para_list[1:]:
                    if not flag_begin_tmp_sancheck_para_list:
                        tmp_sancheck_para_f += '/'
                    tmp_sancheck_para_f += tmp_sancheck_para_list_this
            else:
                return
            tmp_pc_name = None
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
            )
            if tmp_pc_name_1 == None:
                tmp_pc_name = dictTValue['tName']
                if OlivaDiceCore.pcCard.pcCardRebase(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_pc_name
                ):
                    pass
                else:
                    return
            else:
                tmp_pc_name = tmp_pc_name_1
            tmp_skill_value = 0
            tmp_skill_value_old = 0
            if tmp_sancheck_para_s != None and tmp_sancheck_para_f != None:
                if tmp_san_val != None:
                    tmp_skill_value = int(tmp_san_val)
                else:
                    tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        'SAN'
                    )
                tmp_skill_value_old = tmp_skill_value
                rd_para = OlivaDiceCore.onedice.RD('1D100')
                rd_para.roll()
                rd_para_2 = None
                tmp_rd_int = None
                tmp_sancheck_para_final = None
                flag_GreatFailed = False
                if rd_para.resError == None:
                    tmp_rd_int = rd_para.resInt
                    dictRuleTempData = {
                        'roll': tmp_rd_int,
                        'skill': tmp_skill_value
                    }
                    tmpSkillCheckType = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                        dictRuleTempData,
                        OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey('COC7'),
                        'default'
                    )
                    if tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS:
                        tmp_sancheck_para_final = tmp_sancheck_para_s
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckSucceed']
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
                        tmp_sancheck_para_final = tmp_sancheck_para_s
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckSucceed']
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
                        tmp_sancheck_para_final = tmp_sancheck_para_s
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckSucceed']
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
                        tmp_sancheck_para_final = tmp_sancheck_para_s
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckSucceed']
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
                        tmp_sancheck_para_final = tmp_sancheck_para_f
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFailed']
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
                        tmp_sancheck_para_final = tmp_sancheck_para_f
                        flag_GreatFailed = True
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckGreatFailed']
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckNope']
                    else:
                        dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckError']
                else:
                    return
                if tmp_sancheck_para_final != None:
                    rd_para_2 = OlivaDiceCore.onedice.RD(tmp_sancheck_para_final)
                    rd_para_2.roll()
                    if rd_para_2.resError == None:
                        if flag_GreatFailed:
                            if rd_para_2.resIntMaxType == OlivaDiceCore.onedice.RD.resExtremeType.INT_POSITIVE_INFINITE:
                                tmp_skill_value = 0
                                dictTValue['tRollSubResult'] = tmp_sancheck_para_final
                                dictTValue['tRollSubResultIntMax'] = dictStrCustom['strIntPositiveInfinite']
                            else:
                                tmp_skill_value -= rd_para_2.resIntMax
                                dictTValue['tRollSubResult'] = tmp_sancheck_para_final
                                dictTValue['tRollSubResultIntMax'] = str(rd_para_2.resIntMax)
                        else:
                            tmp_skill_value -= rd_para_2.resInt
                            dictTValue['tRollSubResult'] = tmp_sancheck_para_final + '=' + str(rd_para_2.resInt)
                        if tmp_skill_value < 0:
                            tmp_skill_value = 0
                        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                            OlivaDiceCore.pcCard.getPcHash(
                                tmp_pc_id,
                                tmp_pc_platform
                            ),
                            'SAN',
                            tmp_skill_value,
                            tmp_pc_name
                        )
                        dictTValue['tName'] = tmp_pc_name
                        dictTValue['tSkillValue'] = str(tmp_skill_value_old)
                        dictTValue['tSkillValueNew'] = str(tmp_skill_value)
                        dictTValue['tRollResult'] = '1D100=' + str(tmp_rd_int)
                        if flag_GreatFailed:
                            tmp_reply_str = dictStrCustom['strSanCheckGreatFailed'].format(**dictTValue)
                        else:
                            tmp_reply_str = dictStrCustom['strSanCheck'].format(**dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
        elif isMatchWordStart(tmp_reast_str, 'ra') or isMatchWordStart(tmp_reast_str, 'rc'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_show = ''
            roll_times_count = 1
            flag_check_success = False
            flag_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_hagID,
                userType = 'group',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'groupTemplate',
                botHash = plugin_event.bot_info.hash
            )
            flag_groupTemplateRule = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_hagID,
                userType = 'group',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'groupTemplateRule',
                botHash = plugin_event.bot_info.hash
            )
            if isMatchWordStart(tmp_reast_str, 'ra'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'ra')
            elif isMatchWordStart(tmp_reast_str, 'rc'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rc')
            else:
                return
            tmp_skill_name = None
            tmp_skill_value = None
            flag_hide_roll = False
            if len(tmp_reast_str) > 0:
                if isMatchWordStart(tmp_reast_str, 'h'):
                    flag_hide_roll = True
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'h')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) > 2:
                tmp_reast_str_list_1 = tmp_reast_str.split('#')
                if len(tmp_reast_str_list_1) > 1:
                    if tmp_reast_str_list_1[0].isdigit():
                        roll_times_count = int(tmp_reast_str_list_1[0])
                        if roll_times_count > 10:
                            roll_times_count = 10
                        tmp_reast_str = tmp_reast_str_list_1[1]
            # 0 
            # 1 b
            # 2 p
            flag_bp_type = 0
            flag_bp_count = None
            if len(tmp_reast_str) > 0:
                if isMatchWordStart(tmp_reast_str, 'b'):
                    flag_bp_type = 1
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'b')
                elif isMatchWordStart(tmp_reast_str, 'B'):
                    flag_bp_type = 1
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'B')
                elif isMatchWordStart(tmp_reast_str, 'p'):
                    flag_bp_type = 2
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'p')
                elif isMatchWordStart(tmp_reast_str, 'P'):
                    flag_bp_type = 2
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'P')
                if flag_bp_type != 0 and len(tmp_reast_str) > 1:
                    if tmp_reast_str[0].isdigit():
                        flag_bp_count = tmp_reast_str[0]
                        tmp_reast_str = tmp_reast_str[1:]
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) > 0:
                [tmp_skill_name, tmp_reast_str] = getToNumberPara(tmp_reast_str)
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if len(tmp_reast_str) > 0:
                    [tmp_skill_value, tmp_reast_str] = getNumberPara(tmp_reast_str)
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if tmp_skill_value != None:
                tmp_skill_value = int(tmp_skill_value)
            if tmp_skill_name == '':
                tmp_skill_name = None
            if tmp_skill_name != None:
                tmp_skill_name = tmp_skill_name.upper()
                if tmp_skill_value != None:
                    pass
                else:
                    tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_skill_name
                    )
            elif tmp_skill_value != None:
                pass
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
            )
            if tmp_pc_name_1 != None:
                dictTValue['tName'] = tmp_pc_name_1
            if tmp_skill_name != None or tmp_skill_value != None:
                tmp_Template = None
                tmp_TemplateRuleName = 'default'
                if tmp_pc_name_1 != None:
                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_pc_name_1
                    )
                    if flag_groupTemplate != None:
                        tmp_template_name = flag_groupTemplate
                    if tmp_template_name != None:
                        tmp_Template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                    tmp_template_rule_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateRuleKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_pc_name_1
                    )
                    if flag_groupTemplateRule != None:
                        tmp_template_rule_name = flag_groupTemplateRule
                    if tmp_template_rule_name != None:
                        tmp_TemplateRuleName = tmp_template_rule_name
                rd_para_str = '1D100'
                tmp_customDefault = None
                if tmp_Template != None:
                    if 'mainDice' in tmp_Template:
                        rd_para_str = tmp_Template['mainDice']
                    if 'customDefault' in tmp_Template:
                        tmp_customDefault = tmp_Template['customDefault']
                if flag_bp_type == 1:
                    rd_para_str = 'B'
                elif flag_bp_type == 2:
                    rd_para_str = 'P'
                if flag_bp_count != None:
                    rd_para_str += flag_bp_count
                flag_need_reply = False
                if roll_times_count == 1:
                    rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_customDefault)
                    rd_para.roll()
                    if rd_para.resError == None:
                        if rd_para.resDetail == None or rd_para.resDetail == '':
                            dictTValue['tRollResult'] = '%s=%d' % (rd_para_str, rd_para.resInt)
                        else:
                            dictTValue['tRollResult'] = '%s=%s=%d' % (rd_para_str, rd_para.resDetail, rd_para.resInt)
                        dictTValue['tSkillValue'] = str(tmp_skill_value)
                        dictRuleTempData = {
                            'roll': rd_para.resInt,
                            'skill': tmp_skill_value
                        }
                        tmpSkillCheckType = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                            dictRuleTempData,
                            tmp_Template,
                            tmp_TemplateRuleName
                        )
                        if tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckSucceed']
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckHardSucceed']
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckExtremeHardSucceed']
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckGreatSucceed']
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFailed']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckGreatFailed']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_01:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate01']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_02:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate02']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_03:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate03']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_04:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate04']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_05:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate05']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_06:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate06']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_07:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate07']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_08:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate08']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_09:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate09']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_10:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate10']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_11:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFate11']
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckNope']
                        else:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckError']
                        flag_need_reply = True
                else:
                    flag_begin = True
                    tmp_tSkillCheckReasult = ''
                    for i in range(roll_times_count):
                        rd_para = OlivaDiceCore.onedice.RD(rd_para_str)
                        rd_para.roll()
                        if rd_para.resError == None:
                            tmp_tSkillCheckReasult += '\n'
                            if flag_bp_type == 0:
                                tmp_tSkillCheckReasult += '%s=%d ' % (rd_para_str, rd_para.resInt)
                            else:
                                tmp_tSkillCheckReasult += '%s=%s=%d ' % (rd_para_str, rd_para.resDetail, rd_para.resInt)
                            dictTValue['tSkillValue'] = str(tmp_skill_value)
                            dictRuleTempData = {
                                'roll': rd_para.resInt,
                                'skill': tmp_skill_value
                            }
                            tmpSkillCheckType = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                                dictRuleTempData,
                                tmp_Template,
                                tmp_TemplateRuleName
                            )
                            if tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckSucceed']
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckHardSucceed']
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckExtremeHardSucceed']
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckGreatSucceed']
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFailed']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckGreatFailed']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_01:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate01']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_02:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate02']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_03:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate03']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_04:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate04']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_05:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate05']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_06:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate06']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_07:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate07']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_08:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate08']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_09:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate09']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_10:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate10']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_11:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckFate11']
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckNope']
                            else:
                                tmp_tSkillCheckReasult += dictStrCustom['strPcSkillCheckError']
                            flag_need_reply = True
                        else:
                            flag_need_reply = False
                            break
                    dictTValue['tRollResult'] = ''
                    dictTValue['tSkillCheckReasult'] = tmp_tSkillCheckReasult
                if flag_check_success:
                    if tmp_pc_name_1 != None and tmp_skill_name != None:
                        tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        )
                        tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                            tmp_pcHash,
                            tmp_pc_name_1,
                            'enhanceList',
                            []
                        )
                        tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                            tmp_pcHash,
                            tmp_pc_name_1,
                            'template',
                            'default'
                        )
                        tmp_skill_name_core = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                            tmp_pcHash,
                            tmp_skill_name
                        )
                        tmp_skipEnhance_list = []
                        tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                        if 'skillConfig' in tmp_template:
                            if 'skipEnhance' in tmp_template['skillConfig']:
                                if type(tmp_template['skillConfig']['skipEnhance']):
                                    tmp_skipEnhance_list = tmp_template['skillConfig']['skipEnhance']
                        if tmp_skill_name_core not in tmp_enhanceList and tmp_skill_name_core not in tmp_skipEnhance_list:
                            tmp_enhanceList.append(tmp_skill_name_core)
                        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                            tmp_pcHash,
                            tmp_pc_name_1,
                            'enhanceList',
                            tmp_enhanceList
                        )
                if flag_need_reply:
                    if tmp_skill_name != None:
                        dictTValue['tSkillName'] = tmp_skill_name
                        tmp_reply_str = dictStrCustom['strPcSkillCheckWithSkillName'].format(**dictTValue)
                        tmp_reply_str_show = dictStrCustom['strPcSkillCheckHideShowWithSkillName'].format(**dictTValue)
                        if flag_hide_roll and flag_is_from_group:
                            dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                            tmp_reply_str = dictStrCustom['strPcSkillCheckHideWithSkillName'].format(**dictTValue)
                    else:
                        tmp_reply_str = dictStrCustom['strPcSkillCheck'].format(**dictTValue)
                        tmp_reply_str_show = dictStrCustom['strPcSkillCheckHideShow'].format(**dictTValue)
                        if flag_hide_roll and flag_is_from_group:
                            dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                            tmp_reply_str = dictStrCustom['strPcSkillCheckHide'].format(**dictTValue)
                    if flag_hide_roll and flag_is_from_group:
                        replyMsg(plugin_event, tmp_reply_str_show)
                        replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                    else:
                        replyMsg(plugin_event, tmp_reply_str)
        elif isMatchWordStart(tmp_reast_str, 'en'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'en')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip()
            tmp_skill_name = None
            tmp_skill_value = None
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                tmp_pc_id,
                tmp_pc_platform
            )
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash
            )
            if tmp_pc_name_1 != None:
                dictTValue['tName'] = tmp_pc_name_1
            if len(tmp_reast_str) > 0:
                [tmp_skill_name, tmp_reast_str] = getToNumberPara(tmp_reast_str)
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if len(tmp_reast_str) > 0:
                    [tmp_skill_value, tmp_reast_str] = getNumberPara(tmp_reast_str)
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if tmp_skill_name == '':
                tmp_skill_name = None
            if tmp_skill_value == '':
                tmp_skill_value = None
            if tmp_skill_name != None:
                tmp_skill_name = tmp_skill_name.upper()
            if tmp_skill_value != None:
                tmp_skill_value = int(tmp_skill_value)
            if tmp_skill_name != None:
                if tmp_skill_value == None:
                    tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        tmp_pcHash,
                        tmp_skill_name
                    )
                if tmp_skill_value != None:
                    rd_para_1 = OlivaDiceCore.onedice.RD('1D100')
                    rd_para_1.roll()
                    if rd_para_1.resError == None:
                        dictTValue['tSkillName'] = tmp_skill_name
                        dictTValue['tSkillValue'] = tmp_skill_value
                        dictTValue['tRollResult'] = '1D100=%s' % str(rd_para_1.resInt)
                        if rd_para_1.resInt > tmp_skill_value or rd_para_1.resInt >= 96:
                            rd_para_str_2 = '%s+1D10' % str(tmp_skill_value)
                            rd_para_2 = OlivaDiceCore.onedice.RD(rd_para_str_2)
                            rd_para_2.roll()
                            if rd_para_2.resError == None:
                                OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                    tmp_pcHash,
                                    tmp_skill_name,
                                    rd_para_2.resInt,
                                    dictTValue['tName']
                                )
                                dictTValue['tRollSubResult'] = '%s=%s=%s' % (rd_para_str_2, rd_para_2.resDetail, (rd_para_2.resInt))
                                dictTValue['tSkillCheckReasult'] = '%s%s' % (
                                    dictStrCustom['strPcSkillCheckSucceed'].format(**dictTValue),
                                    dictStrCustom['strPcSkillEnhanceContent'].format(**dictTValue)
                                )
                                tmp_reply_str = dictStrCustom['strPcSkillEnhanceCheck'].format(**dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
                        else:
                            dictTValue['tSkillCheckReasult'] = dictStrCustom['strPcSkillCheckFailed'].format(**dictTValue)
                            tmp_reply_str = dictStrCustom['strPcSkillEnhanceCheck'].format(**dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        if tmp_pc_name_1 != None:
                            tmp_enhanceList_new = []
                            tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                                tmp_pcHash,
                                tmp_pc_name_1,
                                'enhanceList',
                                []
                            )
                            for tmp_enhanceList_this in tmp_enhanceList:
                                if tmp_enhanceList_this != OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                    tmp_pcHash,
                                    tmp_skill_name
                                ):
                                    tmp_enhanceList_new.append(tmp_enhanceList_this)
                            OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                                tmp_pcHash,
                                tmp_pc_name_1,
                                'enhanceList',
                                tmp_enhanceList_new
                            )
                        return
            else:
                if tmp_pc_name_1 != None:
                    tmp_enhance_count = 0
                    tmp_enhance_succeed_count = 0
                    tmp_enhance_succeed_list = []
                    tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name_1,
                        'enhanceList',
                        []
                    )
                    for tmp_enhanceList_this in tmp_enhanceList:
                        tmp_skill_name = tmp_enhanceList_this
                        tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                            tmp_pcHash,
                            tmp_skill_name
                        )
                        rd_para_1 = OlivaDiceCore.onedice.RD('1D100')
                        rd_para_1.roll()
                        if rd_para_1.resInt > tmp_skill_value or rd_para_1.resInt >= 96:
                            rd_para_str_2 = '%s+1D10' % str(tmp_skill_value)
                            rd_para_2 = OlivaDiceCore.onedice.RD(rd_para_str_2)
                            rd_para_2.roll()
                            if rd_para_2.resError == None:
                                OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                    tmp_pcHash,
                                    tmp_skill_name,
                                    rd_para_2.resInt,
                                    tmp_pc_name_1
                                )
                            tmp_enhance_succeed_count += 1
                            tmp_enhance_succeed_list.append([
                                tmp_skill_name,
                                tmp_skill_value,
                                rd_para_2.resInt
                            ])
                        tmp_enhance_count += 1
                    OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name_1,
                        'enhanceList',
                        []
                    )
                    dictTValue['tSkillEnhanceCount'] = str(tmp_enhance_count)
                    dictTValue['tSkillEnhanceSucceedCount'] = str(tmp_enhance_succeed_count)
                    tmp_enhance_succeed_list_2 = []
                    for tmp_enhance_succeed_list_this in tmp_enhance_succeed_list:
                        tmp_enhance_succeed_list_2.append('%s:[%s+%s]' % (
                                OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                    tmp_pcHash,
                                    tmp_enhance_succeed_list_this[0],
                                    flagShow = True
                                ),
                                str(tmp_enhance_succeed_list_this[1]),
                                str(tmp_enhance_succeed_list_this[2] - tmp_enhance_succeed_list_this[1])
                            )
                        )
                    if len(tmp_enhance_succeed_list_2) > 0:
                        dictTValue['tSkillEnhanceSucceedList'] = '\n%s' % ' '.join(tmp_enhance_succeed_list_2)
                    else:
                        dictTValue['tSkillEnhanceSucceedList'] = ''
                    tmp_reply_str = dictStrCustom['strPcSkillEnhanceAll'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                else:
                    tmp_reply_str = dictStrCustom['strPcSkillEnhanceError'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
        #关闭该调试性质指令
        elif False and isMatchWordStart(tmp_reast_str, 'rrange'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_show = ''
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rrange')
            rd_para_str = '1D100'
            flag_have_para = False
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) > 0:
                [rd_para_str, tmp_reast_str] = getExpression(tmp_reast_str)
                flag_have_para = True
            rd_para = OlivaDiceCore.onedice.RD(rd_para_str)
            rd_para.roll()
            if rd_para.resError == None:
                if len(rd_para_str) <= 50:
                    dictTValue['tRollPara'] = rd_para_str
                else:
                    dictTValue['tRollPara'] = rd_para_str[:50] + '...'
                if len(rd_para.resDetail) <= 50:
                    dictTValue['tRollResultDetail'] = rd_para.resDetail
                else:
                    dictTValue['tRollResultDetail'] = rd_para.resDetail[:50] + '...'
                if len(str(rd_para.resInt)) <= 50:
                    dictTValue['tRollResultInt'] = str(rd_para.resInt)
                else:
                    dictTValue['tRollResultInt'] = str(rd_para.resInt)[:50]
                dictTValue['tRollResultIntRange'] = ''
                if rd_para.resIntMinType == OlivaDiceCore.onedice.RD.resExtremeType.INT_LIMITED:
                    dictTValue['tRollResultIntRange'] += '[' + str(rd_para.resIntMin)
                else:
                    dictTValue['tRollResultIntRange'] += '(-∞'
                dictTValue['tRollResultIntRange'] += ','
                if rd_para.resIntMaxType == OlivaDiceCore.onedice.RD.resExtremeType.INT_LIMITED:
                    dictTValue['tRollResultIntRange'] += str(rd_para.resIntMax) + ']'
                else:
                    dictTValue['tRollResultIntRange'] += '+∞)'
            else:
                if len(rd_para_str) <= 50:
                    dictTValue['tRollPara'] = rd_para_str
                else:
                    dictTValue['tRollPara'] = rd_para_str[:50] + '...'
                dictTValue['tRollResultInt'] = str(rd_para.resError)
            tmp_reply_str = dictStrCustom['strRollRange'].format(**dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
        #基于OneDice标准，这些指令不再需要，指引用户看HelpDoc
        elif isMatchWordStart(tmp_reast_str, 'ww'):
            replyMsgLazyHelpByEvent(plugin_event, 'r')
            return
        elif isMatchWordStart(tmp_reast_str, 'dx'):
            replyMsgLazyHelpByEvent(plugin_event, 'r')
            return
        elif isMatchWordStart(tmp_reast_str, 'r'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_show = ''
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'r')
            #此处只对实体化后的&做处理，因为这是运算符，其余保持原样
            #如果以后有全面反实体化的需求则需直接调整这里
            #tmp_reast_str = tmp_reast_str.replace('&amp;', '&')
            rd_para_str = '1D100'
            rd_reason_str = None
            roll_times_count = 1
            flag_hide_roll = False
            flag_have_para = False
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                tmp_pc_id,
                tmp_pc_platform
            )
            skill_valueTable = OlivaDiceCore.pcCard.pcCardDataGetByPcName(
                tmp_pcHash
            )
            if len(tmp_reast_str) > 0:
                if isMatchWordStart(tmp_reast_str, 'h'):
                    flag_hide_roll = True
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'h')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) > 2:
                tmp_reast_str_list_1 = tmp_reast_str.split('#')
                if len(tmp_reast_str_list_1) > 1:
                    if tmp_reast_str_list_1[0].isdigit():
                        roll_times_count = int(tmp_reast_str_list_1[0])
                        if roll_times_count > 10:
                            roll_times_count = 10
                        tmp_reast_str = tmp_reast_str_list_1[1]
            if len(tmp_reast_str) > 0:
                tmp_rd_para_str = None
                [tmp_rd_para_str, tmp_reast_str] = getExpression(tmp_reast_str, valueTable = skill_valueTable)
                if tmp_rd_para_str != None and tmp_rd_para_str != '':
                    rd_para_str = tmp_rd_para_str
                    flag_have_para = True
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if len(tmp_reast_str) > 0:
                    rd_reason_str = tmp_reast_str
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
            )
            if tmp_pc_name_1 != None:
                dictTValue['tName'] = tmp_pc_name_1
            tmp_template_name = None
            if tmp_pc_name_1 != None:
                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_pc_name_1
                )
            tmp_template = None
            tmp_template_customDefault = None
            if tmp_template_name != None:
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                if 'customDefault' in tmp_template:
                    tmp_template_customDefault = tmp_template['customDefault']
                if 'mainDice' in tmp_template and not flag_have_para:
                    rd_para_str = tmp_template['mainDice']
            if roll_times_count == 1:
                rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault, valueTable = skill_valueTable)
                rd_para.roll()
                tmp_reply_str_1 = ''
                if rd_para.resError == None:
                    if len(rd_para.resDetail) == 0 or len(rd_para.resDetail) > 150:
                        if len(str(rd_para.resInt)) > 100:
                            tmp_reply_str_1 = rd_para_str + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                        else:
                            tmp_reply_str_1 = rd_para_str + '=' + str(rd_para.resInt)
                    else:
                        if len(str(rd_para.resInt)) > 50:
                            tmp_reply_str_1 = rd_para_str + '=' + str(rd_para.resDetail) + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                        else:
                            tmp_reply_str_1 = rd_para_str + '=' + str(rd_para.resDetail) + '=' + str(rd_para.resInt)
                else:
                    dictTValue['tResult'] = str(rd_para.resError)
                    if rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_GENERATE_FATAL:
                        tmp_reply_str_1 = dictStrCustom['strRollError01'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_COMPLETE_FATAL:
                        tmp_reply_str_1 = dictStrCustom['strRollError02'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_RAW_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError03'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_CHILD_PARA_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError04'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_NODE_OPERATION_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError05'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_OPERATION_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError06'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_STACK_EMPTY:
                        tmp_reply_str_1 = dictStrCustom['strRollError07'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_LEFT_VAL_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError08'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_RIGHT_VAL_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError09'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_SUB_VAL_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError10'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_EXTREME_VAL_INVALID:
                        tmp_reply_str_1 = dictStrCustom['strRollError11'].format(**dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_REPLACE_FATAL:
                        tmp_reply_str_1 = dictStrCustom['strRollError12'].format(**dictTValue)
                    else:
                        tmp_reply_str_1 = dictStrCustom['strRollErrorUnknown'].format(**dictTValue)
                    tmp_reply_str_1 += dictStrCustom['strRollErrorHelp'].format(**dictTValue)
                    replyMsg(plugin_event, tmp_reply_str_1)
                    return
                dictTValue['tRollResult'] = tmp_reply_str_1
            else:
                flag_begin = True
                tmp_reply_str_1 = ''
                for i in range(roll_times_count):
                    rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault)
                    rd_para.roll()
                    if rd_para.resError == None:
                        if not flag_begin:
                            tmp_reply_str_1 += ', '
                        else:
                            flag_begin = False
                        if len(str(rd_para.resInt)) > 10:
                            tmp_reply_str_1 += str(rd_para.resInt)[:10] + '...'
                        else:
                            tmp_reply_str_1 += str(rd_para.resInt)
                    else:
                        tmp_reply_str_1 = str(rd_para.resError)
                        break
                dictTValue['tRollResult'] = rd_para_str + '=' + tmp_reply_str_1
            if rd_reason_str != None:
                dictTValue['tRollReason'] = rd_reason_str
                tmp_reply_str = dictStrCustom['strRollWithReason'].format(**dictTValue)
                tmp_reply_str_show = dictStrCustom['strRollHideShowWithReason'].format(**dictTValue)
                if flag_hide_roll and flag_is_from_group:
                    dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                    tmp_reply_str = dictStrCustom['strRollHideWithReason'].format(**dictTValue)
            else:
                tmp_reply_str = dictStrCustom['strRoll'].format(**dictTValue)
                tmp_reply_str_show = dictStrCustom['strRollHideShow'].format(**dictTValue)
                if flag_hide_roll and flag_is_from_group:
                    dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                    tmp_reply_str = dictStrCustom['strRollHide'].format(**dictTValue)
            if flag_hide_roll and flag_is_from_group:
                replyMsg(plugin_event, tmp_reply_str_show)
                replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
            else:
                replyMsg(plugin_event, tmp_reply_str)

def replyMsg(plugin_event, message):
    host_id = None
    group_id = None
    user_id = None
    tmp_name = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]['strBotName']
    tmp_self_id = plugin_event.bot_info.id
    if 'host_id' in plugin_event.data.__dict__:
        host_id = plugin_event.data.host_id
    if 'group_id' in plugin_event.data.__dict__:
        group_id = plugin_event.data.group_id
    if 'user_id' in plugin_event.data.__dict__:
        user_id = plugin_event.data.user_id
    OlivaDiceCore.crossHook.dictHookFunc['msgHook'](
        plugin_event,
        'reply',
        {
            'name': tmp_name,
            'id': tmp_self_id
        },
        [host_id, group_id, user_id],
        str(message)
    )
    return plugin_event.reply(str(message))

def sendMsgByEvent(plugin_event, message, target_id, target_type, host_id = None):
    group_id = None
    user_id = None
    tmp_name = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]['strBotName']
    tmp_self_id = plugin_event.bot_info.id
    if target_type == 'private':
        user_id = target_id
    elif target_type == 'group':
        group_id = target_id
    OlivaDiceCore.crossHook.dictHookFunc['msgHook'](
        plugin_event,
        'send_%s' % target_type,
        {
            'name': tmp_name,
            'id': tmp_self_id
        },
        [host_id, group_id, user_id],
        str(message)
    )
    return plugin_event.send(target_type, target_id, message, host_id = host_id)

def replyMsgPrivateByEvent(plugin_event, message):
    if OlivaDiceCore.console.getConsoleSwitchByHash(
        'disableReplyPrivate',
        plugin_event.bot_info.hash
    ) == 1:
        #2022-01-19腾讯暗改临时会话协议，在此提供关闭群聊向私聊回复的办法
        return
    host_id = None
    group_id = None
    user_id = None
    tmp_name = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]['strBotName']
    tmp_self_id = plugin_event.bot_info.id
    if 'host_id' in plugin_event.data.__dict__:
        host_id = plugin_event.data.host_id
    if 'group_id' in plugin_event.data.__dict__:
        group_id = plugin_event.data.group_id
    if 'user_id' in plugin_event.data.__dict__:
        user_id = plugin_event.data.user_id
    OlivaDiceCore.crossHook.dictHookFunc['msgHook'](
        plugin_event,
        'reply_private',
        {
            'name': tmp_name,
            'id': tmp_self_id
        },
        [host_id, group_id, user_id],
        str(message)
    )
    if 'host_id' in plugin_event.data.__dict__:
        plugin_event.send('private', plugin_event.data.user_id, message, host_id = plugin_event.data.host_id)
    else:
        plugin_event.send('private', plugin_event.data.user_id, message)
    return

def replyMsgLazyHelpByEvent(plugin_event, help_key):
    tmp_reply_str = OlivaDiceCore.helpDoc.getHelp(str(help_key), plugin_event.bot_info.hash)
    return replyMsg(plugin_event, str(tmp_reply_str))

def htmlUnescape(input):
    return html.unescape(input)

def msgIsCommand(data, prefix_list):
    res = False
    res_data = data
    if type(data) == str:
        for prefix_list_this in prefix_list:
            if isMatchWordStart(data, prefix_list_this):
                res_data = getMatchWordStartRight(data, prefix_list_this)
                res = True
                break
    return [res_data, res]

def skipSpaceStart(data):
    tmp_output_str = ''
    if len(data) > 0:
        flag_have_para = False
        tmp_offset = 0
        tmp_total_offset = 0
        while True:
            tmp_offset += 1
            tmp_total_offset = tmp_offset - 1
            if tmp_total_offset >= len(data):
                break
            if data[tmp_total_offset] != ' ':
                flag_have_para = True
                break
        if flag_have_para:
            tmp_output_str = data[tmp_total_offset:]
    return tmp_output_str

def skipToRight(data, key):
    tmp_output_str = ''
    if len(data) > 0:
        flag_have_para = False
        tmp_offset = 0
        tmp_total_offset = 0
        while True:
            tmp_offset += 1
            tmp_total_offset = tmp_offset - 1
            if tmp_total_offset >= len(data):
                break
            if data[tmp_total_offset] == key:
                flag_have_para = True
                break
        if flag_have_para:
            tmp_output_str = data[tmp_total_offset:]
    return tmp_output_str

def splitBy(data, key):
    tmp_output_str_1 = ''
    tmp_output_str_2 = ''
    if len(data) > 0:
        flag_have_para = False
        tmp_offset = 0
        tmp_total_offset = 0
        while True:
            tmp_offset += 1
            tmp_total_offset = tmp_offset - 1
            if tmp_total_offset >= len(data):
                break
            if data[tmp_total_offset] == key:
                flag_have_para = True
                break
        if flag_have_para:
            tmp_output_str_1 = data[:tmp_total_offset]
            tmp_output_str_2 = data[tmp_total_offset:]
    return [tmp_output_str_1, tmp_output_str_2]

def getExpression(data, reverse = False, valueTable = None):
    tmp_output_str_1 = ''
    tmp_output_str_reg = ''
    tmp_output_str_2 = ''
    if len(data) > 0:
        flag_have_para = False
        tmp_offset = 0
        tmp_total_offset = 0
        tmp_offset_len = 1
        flag_not_hit = True
        while True:
            flag_not_hit = True
            flag_value = False
            tmp_offset += tmp_offset_len
            tmp_offset_len = 1
            if reverse:
                tmp_total_offset = len(data) - tmp_offset
            else:
                tmp_total_offset = tmp_offset - 1
            if not reverse and tmp_total_offset >= len(data):
                flag_have_para = True
                break
            if reverse and tmp_total_offset <= 0:
                flag_have_para = True
                break
            if flag_not_hit and data[tmp_total_offset].isdigit():
                flag_not_hit = False
            if flag_not_hit and not reverse and valueTable != None:
                for idx in range(tmp_total_offset, len(data)):
                    if data[tmp_total_offset:idx + 1].upper() in valueTable:
                        tmp_offset_len = idx - tmp_total_offset + 1
                        flag_not_hit = False
                        flag_value = True
            if flag_not_hit and data[tmp_total_offset] in OlivaDiceCore.onedice.dictOperationPriority:
                flag_not_hit = False
            if flag_not_hit and data[tmp_total_offset] in OlivaDiceCore.onedice.listOperationSub:
                flag_not_hit = False
            if flag_not_hit:
                flag_have_para = True
                if reverse:
                    tmp_total_offset += 1
                break
            else:
                if flag_value:
                    tmp_output_str_reg += '{%s}' % data[tmp_total_offset:tmp_total_offset + tmp_offset_len].upper()
                else:
                    tmp_output_str_reg += data[tmp_total_offset:tmp_total_offset + tmp_offset_len]
        if flag_have_para:
            tmp_output_str_1 = data[:tmp_total_offset]
            tmp_output_str_2 = data[tmp_total_offset:]
            if not reverse and valueTable != None:
                tmp_output_str_1 = tmp_output_str_reg
    return [tmp_output_str_1, tmp_output_str_2]

def getNumberPara(data, reverse = False):
    tmp_output_str_1 = ''
    tmp_output_str_2 = ''
    if len(data) > 0:
        flag_have_para = False
        tmp_offset = 0
        tmp_total_offset = 0
        while True:
            tmp_offset += 1
            if reverse:
                tmp_total_offset = len(data) - tmp_offset
            else:
                tmp_total_offset = tmp_offset - 1
            if not reverse and tmp_total_offset >= len(data):
                flag_have_para = True
                break
            if reverse and tmp_total_offset <= 0:
                flag_have_para = True
                break
            if data[tmp_total_offset].isdigit():
                pass
            else:
                flag_have_para = True
                if reverse:
                    tmp_total_offset += 1
                break
        if flag_have_para:
            tmp_output_str_1 = data[:tmp_total_offset]
            tmp_output_str_2 = data[tmp_total_offset:]
    return [tmp_output_str_1, tmp_output_str_2]

def getToNumberPara(data):
    tmp_output_str_1 = ''
    tmp_output_str_2 = ''
    if len(data) > 0:
        flag_have_para = False
        tmp_offset = 0
        tmp_total_offset = 0
        while True:
            tmp_offset += 1
            tmp_total_offset = tmp_offset - 1
            if tmp_total_offset >= len(data):
                flag_have_para = True
                break
            if data[tmp_total_offset].isdigit():
                flag_have_para = True
                break
            if data[tmp_total_offset] == ' ':
                flag_have_para = True
                break

        if flag_have_para:
            tmp_output_str_1 = data[:tmp_total_offset]
            tmp_output_str_2 = data[tmp_total_offset:]
        else:
            tmp_output_str_2 = data
    return [tmp_output_str_1, tmp_output_str_2]

def isMatchWordStart(data, key, ignoreCase = True, fullMatch = False):
    tmp_output = False
    tmp_data = data
    tmp_key = key
    if ignoreCase:
        tmp_data = tmp_data.lower()
        tmp_key = tmp_key.lower()
    if not fullMatch and len(tmp_data) >= len(tmp_key):
        if tmp_data[:len(tmp_key)] == tmp_key:
            tmp_output = True
    elif fullMatch and tmp_data == tmp_key:
        tmp_output = True
    return tmp_output

def getMatchWordStartRight(data, key, ignoreCase = True):
    tmp_output_str = ''
    tmp_data = data
    tmp_key = key
    if ignoreCase:
        tmp_data = tmp_data.lower()
        tmp_key = tmp_key.lower()
    if len(tmp_data) > len(tmp_key):
        if tmp_data[:len(tmp_key)] == tmp_key:
            tmp_output_str = data[len(key):]
    return tmp_output_str
