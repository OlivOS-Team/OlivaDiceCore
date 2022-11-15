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
import re
import copy

def logProc(Proc, level, message, segment):
    Proc.log(
        log_level = level,
        log_message = message,
        log_segment = segment
    )

def globalLog(level, message, segment):
    if OlivaDiceCore.data.global_Proc != None:
        logProc(OlivaDiceCore.data.global_Proc, level, message, segment)

def unity_init(plugin_event, Proc):
    OlivaDiceCore.data.global_Proc = Proc
    OlivaDiceCore.userConfig.initDelUTF8WithBom(Proc.Proc_data['bot_info_dict'])
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    #init start
    OlivaDiceCore.console.initConsoleSwitchByBotDict(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.console.readConsoleSwitch()
    OlivaDiceCore.console.saveConsoleSwitch()
    OlivaDiceCore.onediceOverride.initOnedice()
    OlivaDiceCore.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.msgCustomManager.saveMsgCustom(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.helpDoc.initHelpDoc(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.drawCard.initDeck(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.pcCard.dataPcCardTemplateDefaultInit()
    OlivaDiceCore.pcCard.dataPcCardTemplateInit()
    OlivaDiceCore.pcCard.dataPcCardLoadAll()
    total_count = OlivaDiceCore.pcCard.dataPcCardTotalCount()
    dictTValue['tInitDataCount'] = str(total_count)
    dictTValue['tInitDataType'] = '人物卡'
    tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strInitData'], dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])
    OlivaDiceCore.userConfig.dataUserConfigLoadAll()
    total_count = OlivaDiceCore.userConfig.dataUserConfigTotalCount()
    dictTValue['tInitDataCount'] = str(total_count)
    dictTValue['tInitDataType'] = '用户记录'
    tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strInitData'], dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])
    #显示Master认主信息
    dictTValue['tInitMasterKey'] = '.master %s' % OlivaDiceCore.data.bot_content['masterKey']
    tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strToBeMaster'], dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])
    dictTValue['tVersion'] = OlivaDiceCore.data.OlivaDiceCore_ver_short
    tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strShowVersionOnLog'], dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Init', 'default')
    ])

def unity_init_after(plugin_event, Proc):
    for bot_info_this in Proc.Proc_data['bot_info_dict']:
        bot_info = Proc.Proc_data['bot_info_dict'][bot_info_this]
        if bot_info.platform['sdk'] in [
            'telegram_poll',
            'discord_link',
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
    tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strSaveData'], dictTValue)
    logProc(Proc, 2, tmp_log_str, [
        ('OlivaDice', 'default'),
        ('Save', 'default')
    ])

def poke_reply(plugin_event, Proc):
    if plugin_event.data.target_id == plugin_event.base_info['self_id']:
        replyMsg(plugin_event, OlivaDiceCore.crossHook.dictHookFunc['pokeHook'](plugin_event = plugin_event, type = 'group'))
    elif plugin_event.data.group_id == -1:
        replyMsg(plugin_event, OlivaDiceCore.crossHook.dictHookFunc['pokeHook'](plugin_event = plugin_event, type = 'private'))
    elif plugin_event.data.group_id == None:
        replyMsg(plugin_event, OlivaDiceCore.crossHook.dictHookFunc['pokeHook'](plugin_event = plugin_event, type = 'private'))

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tName'] = plugin_event.data.sender['name']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    valDict = {}
    valDict['dictTValue'] = dictTValue
    valDict['dictStrCustom'] = dictStrCustom
    valDict['tmp_platform'] = plugin_event.platform['platform']
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)

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

    # 输入流缓存区
    if OlivaDiceCore.msgReplyModel.replyCONTEXT_regGet(
        plugin_event = plugin_event,
        tmp_reast_str = tmp_reast_str
    ):
        plugin_event.set_block()

    [tmp_reast_str, flag_is_command] = msgIsCommand(
        tmp_reast_str,
        OlivaDiceCore.crossHook.dictHookList['prefix']
    )
    if flag_is_command:
        tmp_hostID = None
        tmp_hagID = None
        tmp_userID = plugin_event.data.user_id
        valDict['tmp_userID'] = tmp_userID
        tmp_list_hit = []
        flag_is_from_master = OlivaDiceCore.ordinaryInviteManager.isInMasterList(
            plugin_event.bot_info.hash,
            OlivaDiceCore.userConfig.getUserHash(
                plugin_event.data.user_id,
                'user',
                plugin_event.platform['platform']
            )
        )
        valDict['flag_is_from_master'] = flag_is_from_master
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
        tmp_user_name = None
        if 'name' in plugin_event.data.sender:
            tmp_user_name = plugin_event.data.sender['name']
        if tmp_user_name == None:
            tmp_user_name = '用户'
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userConfigKey = 'userName',
            userConfigValue = tmp_user_name,
            botHash = plugin_event.bot_info.hash,
            userId = plugin_event.data.user_id,
            userType = 'user',
            platform = plugin_event.platform['platform']
        )
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
            tmp_hostID = str(plugin_event.data.host_id)
        elif flag_is_from_group:
            tmp_hagID = str(plugin_event.data.group_id)
        valDict['tmp_hagID'] = tmp_hagID
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
        valDict['tmp_reast_str'] = tmp_reast_str
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
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotExitRemote'], dictTValue)
                        sendMsgByEvent(plugin_event, tmp_reply_str, tmp_group_id, 'group')
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotExitRemoteShow'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        time.sleep(1)
                        plugin_event.set_group_leave(tmp_group_id)
                elif isMatchWordStart(tmp_reast_str, 'remote'):
                    tmp_user_platform = plugin_event.platform['platform']
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'remote')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    if isMatchWordStart(tmp_reast_str, 'on') or isMatchWordStart(tmp_reast_str, 'off'):
                        flag_will_enable = None
                        flag_now_enable = None
                        tmp_userId_in = None
                        tmp_reply_str = None
                        if isMatchWordStart(tmp_reast_str, 'on'):
                            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'on')
                            tmp_reast_str = skipSpaceStart(tmp_reast_str)
                            tmp_userId_in = tmp_reast_str
                            flag_will_enable = True
                        elif isMatchWordStart(tmp_reast_str, 'off'):
                            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'off')
                            tmp_reast_str = skipSpaceStart(tmp_reast_str)
                            tmp_userId_in = tmp_reast_str
                            flag_will_enable = False
                        if flag_will_enable != None:
                            tmp_groupUserHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_userId_in,
                                userType = 'group',
                                platform = tmp_user_platform
                            )
                            tmp_groupUserId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                                userHash = tmp_groupUserHash,
                                userDataKey = 'userId',
                                botHash = plugin_event.bot_info.hash
                            )
                            dictTValue['tId'] = str(tmp_userId_in)
                            if tmp_groupUserId != None:
                                dictTValue['tId'] = str(tmp_groupUserId)
                            else:
                                tmp_groupUserId = tmp_userId_in
                            tmp_groupUserId_list = tmp_groupUserId.split('|')
                            tmp_groupUserId_list_new = []
                            for tmp_groupUserId_list_this in tmp_groupUserId_list:
                                if tmp_groupUserId_list_this != '':
                                    tmp_groupUserId_list_new.append(tmp_groupUserId_list_this)
                            tmp_groupUserId_list = tmp_groupUserId_list_new
                            if len(tmp_groupUserId_list) == 0:
                                return
                            elif len(tmp_groupUserId_list) == 1:
                                tmp_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                                    userHash = tmp_groupUserHash,
                                    userConfigKey = 'groupEnable',
                                    botHash = plugin_event.bot_info.hash
                                )
                                flag_now_enable = tmp_groupEnable
                                if flag_now_enable != flag_will_enable:
                                    OlivaDiceCore.userConfig.setUserConfigByKey(
                                        userConfigKey = 'groupEnable',
                                        userConfigValue = flag_will_enable,
                                        botHash = plugin_event.bot_info.hash,
                                        userId = tmp_groupUserId,
                                        userType = 'group',
                                        platform = tmp_user_platform
                                    )
                                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                        userHash = tmp_groupUserHash
                                    )
                                    if flag_will_enable:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOn'], dictTValue)
                                    else:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOff'], dictTValue)
                                elif flag_now_enable == flag_will_enable:
                                    if flag_will_enable:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOnAlready'], dictTValue)
                                    else:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOffAlready'], dictTValue)
                            elif len(tmp_groupUserId_list) == 2:
                                tmp_hostUserId_in = tmp_groupUserId_list[0]
                                tmp_hostUserHash = OlivaDiceCore.userConfig.getUserHash(
                                    userId = tmp_hostUserId_in,
                                    userType = 'host',
                                    platform = tmp_user_platform
                                )
                                tmp_hostUserId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                                    userHash = tmp_hostUserHash,
                                    userDataKey = 'userId',
                                    botHash = plugin_event.bot_info.hash
                                )
                                if tmp_hostUserId != None:
                                    tmp_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                                        userHash = tmp_hostUserHash,
                                        userConfigKey = 'hostEnable',
                                        botHash = plugin_event.bot_info.hash
                                    )
                                    flag_userConfigKey = 'groupEnable'
                                    if tmp_hostEnable:
                                        flag_userConfigKey = 'groupEnable'
                                    else:
                                        flag_userConfigKey = 'groupWithHostEnable'
                                    tmp_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                                        userHash = tmp_groupUserHash,
                                        userConfigKey = flag_userConfigKey,
                                        botHash = plugin_event.bot_info.hash
                                    )
                                    flag_now_enable = tmp_groupEnable
                                    if flag_now_enable != flag_will_enable:
                                        OlivaDiceCore.userConfig.setUserConfigByKey(
                                            userConfigKey = flag_userConfigKey,
                                            userConfigValue = flag_will_enable,
                                            botHash = plugin_event.bot_info.hash,
                                            userId = tmp_groupUserId,
                                            userType = 'group',
                                            platform = tmp_user_platform
                                        )
                                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                            userHash = tmp_groupUserHash
                                        )
                                        if flag_will_enable:
                                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOn'], dictTValue)
                                        else:
                                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOff'], dictTValue)
                                    elif flag_now_enable == flag_will_enable:
                                        if flag_will_enable:
                                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOnAlready'], dictTValue)
                                        else:
                                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOffAlready'], dictTValue)
                                else:
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteNone'], dictTValue)
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteNone'], dictTValue)
                        if tmp_reply_str != None:
                            replyMsg(plugin_event, tmp_reply_str)
                    elif isMatchWordStart(tmp_reast_str, 'host'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'host')
                        tmp_reast_str = skipSpaceStart(tmp_reast_str)
                        flag_will_enable = None
                        flag_now_enable = None
                        flag_userConfigKey = 'hostLocalEnable'
                        if isMatchWordStart(tmp_reast_str, 'default'):
                            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'default')
                            tmp_reast_str = skipSpaceStart(tmp_reast_str)
                            flag_userConfigKey = 'hostEnable'
                        if isMatchWordStart(tmp_reast_str, 'on'):
                            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'on')
                            tmp_reast_str = skipSpaceStart(tmp_reast_str)
                            tmp_userId_in = tmp_reast_str
                            flag_will_enable = True
                        elif isMatchWordStart(tmp_reast_str, 'off'):
                            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'off')
                            tmp_reast_str = skipSpaceStart(tmp_reast_str)
                            tmp_userId_in = tmp_reast_str
                            flag_will_enable = False
                        if len(tmp_userId_in) == 0:
                            return
                        if flag_will_enable != None:
                            tmp_hostUserHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_userId_in,
                                userType = 'host',
                                platform = tmp_user_platform
                            )
                            tmp_hostUserId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                                userHash = tmp_hostUserHash,
                                userDataKey = 'userId',
                                botHash = plugin_event.bot_info.hash
                            )
                            dictTValue['tId'] = str(tmp_userId_in)
                            if tmp_hostUserId != None:
                                dictTValue['tId'] = str(tmp_hostUserId)
                            else:
                                tmp_hostUserId = tmp_userId_in
                            tmp_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                                userHash = tmp_hostUserHash,
                                userConfigKey = flag_userConfigKey,
                                botHash = plugin_event.bot_info.hash
                            )
                            flag_now_enable = tmp_hostLocalEnable
                            if flag_now_enable != flag_will_enable:
                                OlivaDiceCore.userConfig.setUserConfigByKey(
                                    userConfigKey = flag_userConfigKey,
                                    userConfigValue = flag_will_enable,
                                    botHash = plugin_event.bot_info.hash,
                                    userId = tmp_hostUserId,
                                    userType = 'host',
                                    platform = tmp_user_platform
                                )
                                OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                    userHash = tmp_hostUserHash
                                )
                                if flag_userConfigKey == 'hostEnable':
                                    if flag_will_enable:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteDefaultOn'], dictTValue)
                                    else:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteDefaultOff'], dictTValue)
                                else:
                                    if flag_will_enable:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOn'], dictTValue)
                                    else:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOff'], dictTValue)
                            elif flag_now_enable == flag_will_enable:
                                if flag_userConfigKey == 'hostEnable':
                                    if flag_will_enable:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteDefaultOnAlready'], dictTValue)
                                    else:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteDefaultOffAlready'], dictTValue)
                                else:
                                    if flag_will_enable:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOnAlready'], dictTValue)
                                    else:
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterRemoteOffAlready'], dictTValue)
                        if tmp_reply_str != None:
                            replyMsg(plugin_event, tmp_reply_str)
                    return
                elif isMatchWordStart(tmp_reast_str, 'accept'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'accept')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reast_str = tmp_reast_str.rstrip(' ')
                    if len(tmp_reast_str) > 0:
                        tmp_flag = tmp_reast_str
                        dictTValue['tInvateFlag'] = str(tmp_flag)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAddGroupRemoteAcceptShow'], dictTValue)
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
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleSetInvalid'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        tmp_pulseUrlList = OlivaDiceCore.console.setConsoleSwitchByHash(
                            tmp_editKey,
                            tmp_pulseUrlList_new,
                            plugin_event.bot_info.hash
                        )
                        OlivaDiceCore.console.saveConsoleSwitch()
                        dictTValue['tConsoleKey'] = tmp_editKey
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleAppend'], dictTValue)
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
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleSetInvalid'], dictTValue)
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
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleSetInvalid'], dictTValue)
                                        replyMsg(plugin_event, tmp_reply_str)
                                        return
                                else:
                                    tmp_listValue = tmp_listValue_new
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleSetInvalid'], dictTValue)
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
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleSetInvalid'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        tmp_dataList = OlivaDiceCore.console.setConsoleSwitchByHash(
                            tmp_editKey,
                            tmp_dataList_new,
                            plugin_event.bot_info.hash
                        )
                        OlivaDiceCore.console.saveConsoleSwitch()
                        dictTValue['tConsoleKey'] = tmp_editKey
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleAppend'], dictTValue)
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
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleShowList'], dictTValue)
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
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotHostOn'], dictTValue)
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAlreadyHostOn'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotNotUnderHost'], dictTValue)
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
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotHostOff'], dictTValue)
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAlreadyHostOff'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotNotUnderHost'], dictTValue)
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
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleShow'], dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                    return
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleNotFound'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    elif len(tmp_reast_list) > 1:
                        tmp_reast_str = ' '.join(tmp_reast_list[1:])
                        tmp_reast_str = tmp_reast_str.strip(' ')
                        if not tmp_reast_str.isdigit():
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleSetInvalid'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        if plugin_event.bot_info.hash in OlivaDiceCore.console.dictConsoleSwitch:
                            if tmp_reast_list[0] in OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash]:
                                if type(OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash][tmp_reast_list[0]]) == int:
                                    OlivaDiceCore.console.dictConsoleSwitch[plugin_event.bot_info.hash][tmp_reast_list[0]] = int(tmp_reast_str)
                                    OlivaDiceCore.console.saveConsoleSwitch()   
                                    dictTValue['tConsoleKey'] = tmp_reast_list[0]
                                    dictTValue['tConsoleValue'] = tmp_reast_str
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleSet'], dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                    return
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterConsoleNotFound'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'system'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'system')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if isMatchWordStart(tmp_reast_str, 'restart'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'restart')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMasterSystemRestart'], dictTValue)
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
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSetStr'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'helpdoc'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'helpdoc')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.strip(' ')
                tmp_reast_list = tmp_reast_str.split(' ')
                tmp_reast_list_len = len(tmp_reast_list)
                if tmp_reast_list_len == 1:
                    tmp_helpdoc_key = tmp_reast_list[0]
                    OlivaDiceCore.helpDoc.delHelpDocByBotHash(
                        botHash = plugin_event.bot_info.hash,
                        helpdocKey = tmp_helpdoc_key
                    )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strHelpdocDel'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                elif tmp_reast_list_len >= 2:
                    tmp_helpdoc_key = tmp_reast_list[0]
                    tmp_helpdoc_val = ' '.join(tmp_reast_list[1:])
                    OlivaDiceCore.helpDoc.setHelpDocByBotHash(
                        botHash = plugin_event.bot_info.hash,
                        helpdocKey = tmp_helpdoc_key,
                        helpdocVal = tmp_helpdoc_val
                    )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strHelpdocSet'], dictTValue)
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
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBecomeMaster'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    #显示Master认主信息
                    dictTValue['tInitMasterKey'] = '.master %s' % OlivaDiceCore.data.bot_content['masterKey']
                    tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strToBeMaster'], dictTValue)
                    logProc(Proc, 2, tmp_log_str, [
                        ('OlivaDice', 'default'),
                        ('reply', 'default')
                    ])
                else:
                    if (not flag_hostLocalEnable or not flag_groupEnable) and not flag_force_reply:
                        return
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCantBecomeMaster'], dictTValue)
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
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedMaster'], dictTValue)
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
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotOn'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAlreadyOn'], dictTValue)
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
                                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedMaster'], dictTValue)
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
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotOff'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAlreadyOff'], dictTValue)
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
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotHostLocalOn'], dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                else:
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAlreadyHostLocalOn'], dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotNotUnderHost'], dictTValue)
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
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotHostLocalOff'], dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                                else:
                                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAlreadyHostLocalOff'], dictTValue)
                                    replyMsg(plugin_event, tmp_reply_str)
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotNotUnderHost'], dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'exit'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'exit')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                if flag_is_from_group and tmp_reast_str in tmp_end_list:
                    if (flag_is_from_group_have_admin and flag_is_from_group_admin) or flag_is_from_master:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotExit'], dictTValue)
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
                tmp_reply_str = OlivaDiceCore.data.bot_info + '\n' + OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBot'], dictTValue)
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
        if OlivaDiceCore.msgReplyModel.replyCONTEXT_fliter(tmp_reast_str):
            pass
        elif isMatchWordStart(tmp_reast_str, 'help'):
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
                            tmp_userName = '骰主'
                            tmp_userRawId = tmp_dataList_this[0]
                            tmp_userPlatform = tmp_dataList_this[1]
                            tmp_botHash = plugin_event.bot_info.hash
                            tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_userRawId,
                                userType = 'user',
                                platform = tmp_userPlatform
                            )
                            tmp_userId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                                userHash = tmp_userHash,
                                userDataKey = 'userId',
                                botHash = tmp_botHash
                            )
                            if tmp_userId != None:
                                tmp_userName = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                                    userHash = tmp_userHash,
                                    userConfigKey = 'userName',
                                    botHash = tmp_botHash
                                )
                            tmp_dataList_new.append(
                                '[%s] - (%s)' % (
                                    str(tmp_userName),
                                    str(tmp_dataList_this[0])
                                )
                            )
                    dictTValue['tHelpDocResult'] = '\n'.join(tmp_dataList_new)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strHelpDoc'], dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.helpDoc.getHelp(
                        tmp_reast_str,
                        plugin_event.bot_info.hash,
                        plugin_event = plugin_event
                    )
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
            tmp_deck_name = re.sub(r'\s+', r':', tmp_reast_str)
            if tmp_deck_name == '':
                tmp_deck_name = None
            if tmp_deck_name != None:
                tmp_reply_str = OlivaDiceCore.drawCard.getDrawDeck(
                    tmp_deck_name,
                    plugin_event.bot_info.hash,
                    count = tmp_card_count,
                    valDict = valDict
                )
                if flag_hide:
                    replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDrawDeckHideShow'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
            else:
                tmp_reply_str = OlivaDiceCore.helpDoc.getHelp('draw', plugin_event.bot_info.hash)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'ob'):
            tmp_user_platform = plugin_event.platform['platform']
            flag_solo = False
            if isMatchWordStart(tmp_reast_str, 'ob', fullMatch = True):
                flag_solo = True
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'ob')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if isMatchWordStart(tmp_reast_str, 'clear', fullMatch = True):
                if flag_is_from_group:
                    if (flag_is_from_group_have_admin and flag_is_from_group_admin or not flag_is_from_group_have_admin) or flag_is_from_master:
                        tmp_reply_str = None
                        tmp_groupHash = OlivaDiceCore.userConfig.getUserHash(
                            userId = tmp_hagID,
                            userType = 'group',
                            platform = tmp_user_platform
                        )
                        tmp_groupObList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                            userId = tmp_hagID,
                            userType = 'group',
                            platform = plugin_event.platform['platform'],
                            userConfigKey = 'groupObList',
                            botHash = plugin_event.bot_info.hash
                        )
                        if tmp_groupObList_list == None:
                            tmp_groupObList_list = []
                        for tmp_groupObList_list_this in tmp_groupObList_list:
                            tmp_userId_this = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                                userHash = tmp_groupObList_list_this,
                                userDataKey = 'userId',
                                botHash = plugin_event.bot_info.hash
                            )
                            if tmp_userId_this != None:
                                tmp_userObList_this_new = []
                                tmp_userObList_this = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                                    userHash = tmp_groupObList_list_this,
                                    userConfigKey = 'userObList',
                                    botHash = plugin_event.bot_info.hash
                                )
                                if tmp_userObList_this == None:
                                    tmp_userObList_this = []
                                if tmp_groupHash in tmp_userObList_this:
                                    for tmp_userObList_this_this in tmp_userObList_this:
                                        if tmp_groupHash != tmp_userObList_this_this:
                                            tmp_userObList_this_new.append(tmp_userObList_this_this)
                                OlivaDiceCore.userConfig.setUserConfigByKey(
                                    userConfigKey = 'userObList',
                                    userConfigValue = tmp_userObList_this_new,
                                    botHash = plugin_event.bot_info.hash,
                                    userId = tmp_userId_this,
                                    userType = 'user',
                                    platform = tmp_user_platform
                                )
                                OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                    userHash = tmp_groupObList_list_this
                                )
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'groupObList',
                            userConfigValue = [],
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_hagID,
                            userType = 'group',
                            platform = tmp_user_platform
                        )
                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                            userHash = tmp_groupHash
                        )
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObClear'], dictTValue)
                        if tmp_reply_str != None:
                            replyMsg(plugin_event, tmp_reply_str)
            if isMatchWordStart(tmp_reast_str, 'list', fullMatch = True):
                if flag_is_from_group:
                    tmp_reply_str = None
                    tmp_reply_str_list = []
                    tmp_groupHash = OlivaDiceCore.userConfig.getUserHash(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                    tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
                        userId = tmp_userID,
                        userType = 'user',
                        platform = tmp_user_platform
                    )
                    tmp_groupObList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupObList',
                        botHash = plugin_event.bot_info.hash
                    )
                    if tmp_groupObList_list == None:
                        tmp_groupObList_list = []
                    for tmp_groupObList_list_this in tmp_groupObList_list:
                        tmp_userName_this = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                            userHash = tmp_groupObList_list_this,
                            userConfigKey = 'userName',
                            botHash = plugin_event.bot_info.hash
                        )
                        tmp_userId_this = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                            userHash = tmp_groupObList_list_this,
                            userDataKey = 'userId',
                            botHash = plugin_event.bot_info.hash
                        )
                        if tmp_userId_this == None:
                            tmp_userId_this = 'N/A'
                        tmp_reply_str_list.append(
                            '[%s] - (%s)' % (
                                str(tmp_userName_this),
                                str(tmp_userId_this)
                            )
                        )
                    if len(tmp_reply_str_list) > 0:
                        dictTValue['tResult'] = '\n'.join(tmp_reply_str_list)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObList'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObListNone'], dictTValue)
                    if tmp_reply_str != None:
                        replyMsg(plugin_event, tmp_reply_str)
            elif flag_solo or isMatchWordStart(tmp_reast_str, 'exit', fullMatch = True) or isMatchWordStart(tmp_reast_str, 'join', fullMatch = True):
                if flag_is_from_group:
                    flag_ob_will_enable = None
                    if isMatchWordStart(tmp_reast_str, 'exit', fullMatch = True):
                        flag_ob_will_enable = False
                    elif isMatchWordStart(tmp_reast_str, 'join', fullMatch = True):
                        flag_ob_will_enable = True
                    tmp_reply_str = None
                    flag_ob_is_enable = False
                    tmp_groupHash = OlivaDiceCore.userConfig.getUserHash(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                    tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
                        userId = tmp_userID,
                        userType = 'user',
                        platform = tmp_user_platform
                    )
                    tmp_groupObList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = tmp_user_platform,
                        userConfigKey = 'groupObList',
                        botHash = plugin_event.bot_info.hash
                    )
                    tmp_userObList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_userID,
                        userType = 'user',
                        platform = tmp_user_platform,
                        userConfigKey = 'userObList',
                        botHash = plugin_event.bot_info.hash
                    )
                    tmp_userName = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_userID,
                        userType = 'user',
                        platform = tmp_user_platform,
                        userConfigKey = 'userName',
                        botHash = plugin_event.bot_info.hash
                    )
                    dictTValue['tUserName'] = tmp_userName
                    if tmp_groupObList_list == None:
                        tmp_groupObList_list = []
                    if type(tmp_groupObList_list) != list:
                        tmp_groupObList_list = []
                    if tmp_userObList_list == None:
                        tmp_userObList_list = []
                    if type(tmp_userObList_list) != list:
                        tmp_userObList_list = []
                    if tmp_userHash in tmp_groupObList_list:
                        flag_ob_is_enable = True
                    if flag_ob_will_enable == None:
                        flag_ob_will_enable = not flag_ob_is_enable
                    if not flag_ob_is_enable and flag_ob_will_enable:
                        if tmp_userHash not in tmp_groupObList_list:
                            tmp_groupObList_list.append(tmp_userHash)
                        if tmp_groupHash not in tmp_userObList_list:
                            tmp_userObList_list.append(tmp_groupHash)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObJoin'], dictTValue)
                    elif flag_ob_is_enable and not flag_ob_will_enable:
                        tmp_groupObList_list_new = []
                        tmp_userObList_list_new = []
                        for tmp_groupObList_list_this in tmp_groupObList_list:
                            if tmp_userHash != tmp_groupObList_list_this:
                                tmp_groupObList_list_new.append(tmp_groupObList_list_this)
                        tmp_groupObList_list = tmp_groupObList_list_new
                        for tmp_userObList_list_this in tmp_userObList_list:
                            if tmp_groupHash != tmp_userObList_list_this:
                                tmp_userObList_list_new.append(tmp_userObList_list_this)
                        tmp_userObList_list = tmp_userObList_list_new
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObExit'], dictTValue)
                    elif flag_ob_is_enable and flag_ob_will_enable:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObJoinAlready'], dictTValue)
                    elif not flag_ob_is_enable and not flag_ob_will_enable:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObExitAlready'], dictTValue)
                    if flag_ob_is_enable != flag_ob_will_enable:
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'groupObList',
                            userConfigValue = tmp_groupObList_list,
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_hagID,
                            userType = 'group',
                            platform = tmp_user_platform
                        )
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'userObList',
                            userConfigValue = tmp_userObList_list,
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_userID,
                            userType = 'user',
                            platform = tmp_user_platform
                        )
                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                            userHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_hagID,
                                userType = 'group',
                                platform = tmp_user_platform
                            )
                        )
                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                            userHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_userID,
                                userType = 'user',
                                platform = tmp_user_platform
                            )
                        )
                    if tmp_reply_str != None:
                        replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, 'exit'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'exit')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if isMatchWordStart(tmp_reast_str, 'all', fullMatch = True):
                    tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
                        userId = tmp_userID,
                        userType = 'user',
                        platform = tmp_user_platform
                    )
                    tmp_userObList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_userID,
                        userType = 'user',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'userObList',
                        botHash = plugin_event.bot_info.hash
                    )
                    if tmp_userObList_list == None:
                        tmp_userObList_list = []
                    for tmp_userObList_list_this in tmp_userObList_list:
                        tmp_groupObList_list = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                            userHash = tmp_userObList_list_this,
                            userConfigKey = 'groupObList',
                            botHash = plugin_event.bot_info.hash
                        )
                        if tmp_groupObList_list == None:
                            tmp_groupObList_list = []
                        if tmp_userHash in tmp_groupObList_list:
                            tmp_groupObList_list_new = []
                            for tmp_groupObList_list_this in tmp_groupObList_list:
                                if tmp_userHash != tmp_groupObList_list_this:
                                    tmp_groupObList_list_new.append(tmp_groupObList_list_this)
                            tmp_groupObList_list = tmp_groupObList_list_new
                        tmp_hugId_this = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                            userHash = tmp_userObList_list_this,
                            userDataKey = 'userId',
                            botHash = plugin_event.bot_info.hash
                        )
                        if tmp_hugId_this != None:
                            OlivaDiceCore.userConfig.setUserConfigByKey(
                                userConfigKey = 'groupObList',
                                userConfigValue = tmp_groupObList_list,
                                botHash = plugin_event.bot_info.hash,
                                userId = tmp_hugId_this,
                                userType = 'group',
                                platform = tmp_user_platform
                            )
                            OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                                userHash = tmp_userObList_list_this
                            )
                    tmp_userObList_list = []
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userConfigKey = 'userObList',
                        userConfigValue = tmp_userObList_list,
                        botHash = plugin_event.bot_info.hash,
                        userId = tmp_userID,
                        userType = 'user',
                        platform = tmp_user_platform
                    )
                    tmp_userName = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_userID,
                        userType = 'user',
                        platform = tmp_user_platform,
                        userConfigKey = 'userName',
                        botHash = plugin_event.bot_info.hash
                    )
                    dictTValue['tUserName'] = tmp_userName
                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                        userHash = tmp_userHash
                    )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObExitAll'], dictTValue)
                    if tmp_reply_str != None:
                        replyMsg(plugin_event, tmp_reply_str)
        elif isMatchWordStart(tmp_reast_str, 'ti', fullMatch = True):
            dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck('即时症状', plugin_event.bot_info.hash, valDict = valDict)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDrawTi'], dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'li', fullMatch = True):
            dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck('总结症状', plugin_event.bot_info.hash, valDict = valDict)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDrawLi'], dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'uinfo'):
            tmp_user_platform = plugin_event.platform['platform']
            flag_solo = False
            flag_onHit = False
            if isMatchWordStart(tmp_reast_str, 'uinfo', fullMatch = True):
                flag_solo = True
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'uinfo')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_userId_in = None
            flag_userInfoType = 'user'
            if flag_is_from_host and isMatchWordStart(tmp_reast_str, 'host', fullMatch = True):
                flag_userInfoType = 'host'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'host')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_userId_in = tmp_hostID
                flag_onHit = True
            elif flag_is_from_master and isMatchWordStart(tmp_reast_str, 'host'):
                flag_userInfoType = 'host'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'host')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_userId_in = tmp_reast_str
                flag_onHit = True
            elif flag_is_from_group and isMatchWordStart(tmp_reast_str, 'group', fullMatch = True):
                flag_userInfoType = 'group'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'group')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_userId_in = tmp_hagID
                flag_onHit = True
            elif flag_is_from_master and isMatchWordStart(tmp_reast_str, 'group'):
                flag_userInfoType = 'group'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'group')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_userId_in = tmp_reast_str
                flag_onHit = True
            elif isMatchWordStart(tmp_reast_str, 'user', fullMatch = True):
                flag_userInfoType = 'user'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'user')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_userId_in = tmp_userID
                flag_onHit = True
            elif flag_is_from_master and isMatchWordStart(tmp_reast_str, 'user'):
                flag_userInfoType = 'user'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'user')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_userId_in = tmp_reast_str
                flag_onHit = True
            elif flag_solo:
                flag_userInfoType = 'user'
                tmp_userId_in = tmp_userID
                flag_onHit = True
            if flag_onHit:
                tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
                    userId = tmp_userId_in,
                    userType = flag_userInfoType,
                    platform = tmp_user_platform
                )
                tmp_userId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                    userHash = tmp_userHash,
                    userDataKey = 'userId',
                    botHash = plugin_event.bot_info.hash
                )
                if tmp_userId != None:
                    tmp_reply_str = None
                    tmp_dictTValue = {
                        'tUserName': 'N/A',
                        'tUserId': 'N/A',
                        'tUserHash': 'N/A',
                        'tUserPlatform': 'N/A',
                        'tUserLastHit': 'N/A',
                        'tUserConfig': '',
                        'tTrustLevel': 'N/A',
                        'tTrustRank': 'N/A'
                    }
                    tmp_reply_str_temp = '[{tUserName}] - ({tUserId})\n记录哈希: {tUserHash}\n平台: {tUserPlatform}\n最后触发: {tUserLastHit}\n信任等级/评分: {tTrustLevel} / {tTrustRank}{tUserConfig}'
                    if flag_userInfoType == 'user':
                        tmp_dictTValue['tUserName'] = '用户'
                        tmp_userName = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                            userHash = tmp_userHash,
                            userConfigKey = 'userName',
                            botHash = plugin_event.bot_info.hash
                        )
                        tmp_dictTValue['tUserName'] = tmp_userName
                    elif flag_userInfoType == 'group':
                        tmp_dictTValue['tUserName'] = '群'
                    elif flag_userInfoType == 'host':
                        tmp_dictTValue['tUserName'] = '频道'
                    tmp_dictTValue['tTrustLevel'] = str(OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                        userHash = tmp_userHash,
                        userConfigKey = 'trustLevel',
                        botHash = plugin_event.bot_info.hash
                    ))
                    tmp_dictTValue['tTrustRank'] = str(OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                        userHash = tmp_userHash,
                        userConfigKey = 'trustRank',
                        botHash = plugin_event.bot_info.hash
                    ))
                    tmp_userPlatform = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                        userHash = tmp_userHash,
                        userDataKey = 'platform',
                        botHash = plugin_event.bot_info.hash
                    )
                    tmp_userLastHit = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                        userHash = tmp_userHash,
                        userDataKey = 'lastHit',
                        botHash = plugin_event.bot_info.hash
                    )
                    tmp_userConfigNote = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                        userHash = tmp_userHash,
                        userDataKey = 'configNote',
                        botHash = plugin_event.bot_info.hash
                    )
                    tmp_userConfigNote_list = []
                    if flag_userInfoType in OlivaDiceCore.userConfig.dictUserConfigNoteType:
                        for dictUserConfigNoteMapping_this in OlivaDiceCore.userConfig.dictUserConfigNoteType[flag_userInfoType]:
                            if type(tmp_userConfigNote) != dict:
                                continue
                            if dictUserConfigNoteMapping_this in tmp_userConfigNote:
                                if type(tmp_userConfigNote[dictUserConfigNoteMapping_this]) == bool:
                                    if dictUserConfigNoteMapping_this in OlivaDiceCore.userConfig.dictUserConfigNoteMapping:
                                        if type(
                                            OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                dictUserConfigNoteMapping_this
                                            ]
                                        ) == str:
                                            if tmp_userConfigNote[dictUserConfigNoteMapping_this]:
                                                tmp_userConfigNote_list.append(
                                                    OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                        dictUserConfigNoteMapping_this
                                                    ]
                                                )
                                        elif type(
                                            OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                dictUserConfigNoteMapping_this
                                            ]
                                        ) == list:
                                            if len(
                                                OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                    dictUserConfigNoteMapping_this
                                                ]
                                            ) == 2:
                                                if tmp_userConfigNote[dictUserConfigNoteMapping_this]:
                                                    if OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                        dictUserConfigNoteMapping_this
                                                    ][0] != None:
                                                        tmp_userConfigNote_list.append(
                                                            OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                                dictUserConfigNoteMapping_this
                                                            ][0]
                                                        )
                                                else:
                                                    if OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                        dictUserConfigNoteMapping_this
                                                    ][1] != None:
                                                        tmp_userConfigNote_list.append(
                                                            OlivaDiceCore.userConfig.dictUserConfigNoteMapping[
                                                                dictUserConfigNoteMapping_this
                                                            ][1]
                                                        )
                    if len(tmp_userConfigNote_list) > 0:
                        tmp_dictTValue['tUserConfig'] = '\n%s' % ' - '.join(tmp_userConfigNote_list)
                    tmp_dictTValue['tUserId'] = tmp_userId
                    tmp_dictTValue['tUserHash'] = tmp_userHash
                    tmp_dictTValue['tUserPlatform'] = tmp_userPlatform
                    if tmp_userLastHit == None:
                        tmp_dictTValue['tUserLastHit'] = '无记录'
                    else:
                        tmp_dictTValue['tUserLastHit'] = time.strftime(
                            "%Y-%m-%d %H:%M:%S",
                            time.localtime(
                                tmp_userLastHit
                            )
                        )
                    tmp_reply_str = tmp_reply_str_temp.format(**tmp_dictTValue)
                else:
                    tmp_reply_str = '未找到相关记录'
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
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
                    count = tmp_card_count,
                    valDict = valDict
                )
            else:
                dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck(
                    '随机姓名',
                    plugin_event.bot_info.hash,
                    count = tmp_card_count,
                    valDict = valDict
                )
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDrawName'], dictTValue)
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
                    tmp_pc_name = OlivaDiceCore.pcCard.fixName(tmp_pc_name)
                    if not OlivaDiceCore.pcCard.checkPcName(tmp_pc_name):
                        return
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_hagID
                )
                if OlivaDiceCore.pcCard.pcCardRebase(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_pc_name,
                    tmp_hagID
                ):
                    dictTValue['tPcSelectionNew'] = tmp_pc_name
                    if tmp_pc_name_1 != None:
                        dictTValue['tPcSelection'] = tmp_pc_name_1
                    else:
                        dictTValue['tPcSelection'] = dictTValue['tName']
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRename'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                replyMsgLazyHelpByEvent(plugin_event, 'nn')
            return
        elif isMatchWordStart(tmp_reast_str, 'sn'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'sn')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_mode = 'coc'
            flag_force = True
            sn_title = None
            sn_title_new = None
            if tmp_hagID == None:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
            if '' == tmp_reast_str.lower():
                flag_mode = 'coc'
                flag_force = False
            elif tmp_reast_str.lower() in ['dnd', 'dnd5e']:
                flag_mode = 'dnd'
            elif tmp_reast_str.lower() in ['coc', 'coc6', 'coc7']:
                flag_mode = 'coc'
            else:
                flag_mode = 'custom'
                sn_title_new = tmp_reast_str
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                tmp_pc_id,
                tmp_pc_platform
            )
            tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash,
                tmp_hagID
            )
            tmp_Record = {}
            if tmp_pc_name != None:
                tmp_Record = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    pcHash = tmp_pcHash,
                    pcCardName = tmp_pc_name,
                    dataKey = 'noteRecord',
                    resDefault = {}
                )
                if '名片' in tmp_Record:
                    sn_title = tmp_Record['名片']
            if flag_force or sn_title == None:
                if 'coc' == flag_mode:
                    sn_title = '{tName} hp{HP}/{HPMAX} san{SAN}/{SANMAX} dex{DEX}'
                elif 'dnd' == flag_mode:
                    sn_title = '{tName} hp{HP}/{HPMAX} mp{MP}/{MPMAX} dex{DEX}'
                elif 'custom' == flag_mode:
                    sn_title = sn_title_new
            if sn_title != None:
                if flag_force:
                    OlivaDiceCore.msgReplyModel.setPcNoteOrRecData(
                        plugin_event = plugin_event,
                        tmp_pc_id = tmp_pc_id,
                        tmp_pc_platform = tmp_pc_platform,
                        tmp_hagID = tmp_hagID,
                        dictTValue = dictTValue,
                        dictStrCustom = dictStrCustom,
                        keyName = 'noteRecord',
                        tmp_key = '名片',
                        tmp_value = sn_title,
                        flag_mode = 'note',
                        enableFalse = False
                    )
                    plugin_event:OlivOS.API.Event
                sn_title = OlivaDiceCore.msgReplyModel.getNoteFormat(
                    data = sn_title,
                    pcHash = tmp_pcHash,
                    hagID = tmp_hagID
                )
                plugin_event.set_group_card(
                    group_id = plugin_event.data.group_id,
                    user_id = plugin_event.data.user_id,
                    card = sn_title,
                    host_id = plugin_event.data.host_id
                )
                dictTValue['tResult'] = sn_title
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnSet'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            else:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnPcCardNone'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
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
                    tmp_pcHash,
                    tmp_hagID
                )
                if tmp_pc_name_1 != None:
                    dictTValue['tName'] = tmp_pc_name_1
                tmp_dict_pc_card = OlivaDiceCore.pcCard.pcCardDataGetByPcName(
                    tmp_pcHash,
                    hagId = tmp_hagID
                )
                flag_begin = True
                tmp_dict_pc_card_dump = {}
                for tmp_dict_pc_card_key in tmp_dict_pc_card:
                    tmp_dict_pc_card_dump[
                        OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                            tmp_pcHash,
                            tmp_dict_pc_card_key,
                            flagShow = True,
                            hagId = tmp_hagID
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
                        tmp_dict_pc_card_key,
                        hagId = tmp_hagID
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
                if tmp_pc_name_1 != None:
                    tmp_class_map = {
                        '映射': 'mappingRecord',
                        '记录': 'noteRecord'
                    }
                    for keyName_key in tmp_class_map:
                        tmp_Record = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                            pcHash = tmp_pcHash,
                            pcCardName = tmp_pc_name_1,
                            dataKey = tmp_class_map[keyName_key],
                            resDefault = {}
                        )
                        if len(tmp_Record) > 0:
                            tmp_reply_str_1_list.append(
                                '<%s>\n%s' % (
                                    keyName_key,
                                    '\n'.join(
                                        [
                                            '%s:%s' % (
                                                tmp_Record_this, OlivaDiceCore.msgReplyModel.getNoteFormat(
                                                    data = tmp_Record[tmp_Record_this],
                                                    pcHash = tmp_pcHash,
                                                    hagID = tmp_hagID
                                                ) if keyName_key in ['记录'] else tmp_Record[tmp_Record_this]
                                            ) for tmp_Record_this in tmp_Record
                                        ]
                                    )
                                )
                            )
                tmp_reply_str_1 = '\n'.join(tmp_reply_str_1_list)
                dictTValue['tPcShow'] = tmp_reply_str_1
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcShow'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'show'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'show')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.strip(' ')
                tmp_skill_name = tmp_reast_str
                if tmp_skill_name == '':
                    tmp_skill_name = None
                if tmp_skill_name != None:
                    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_hagID
                    )
                    tmp_skill_value_find = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_skill_name,
                        hagId = tmp_hagID
                    )
                    if tmp_pc_name != None:
                        dictTValue['tName'] = tmp_pc_name
                    dictTValue['tSkillName'] = tmp_skill_name
                    dictTValue['tSkillValue'] = str(tmp_skill_value_find)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetSingleSkillValue'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'list', fullMatch = True):
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_hagID
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
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcList'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'lock', fullMatch = True):
                if flag_is_from_group:
                    tmp_pc_hash = OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                    tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pc_hash, tmp_hagID)
                    if tmp_pc_name_1 != None:
                        if OlivaDiceCore.pcCard.pcCardDataSetSelectionKeyLock(
                            tmp_pc_hash,
                            tmp_pc_name_1,
                            tmp_hagID
                        ):
                            dictTValue['tName'] = tmp_pc_name_1
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcLock'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                        else:
                            dictTValue['tName'] = tmp_pc_name_1
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcLockError'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcLockNone'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'unlock', fullMatch = True):
                if flag_is_from_group:
                    tmp_pc_hash = OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                    tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKeyLock(tmp_pc_hash, tmp_hagID)
                    if tmp_pc_name_1 != None:
                        OlivaDiceCore.pcCard.pcCardDataDelSelectionKeyLock(tmp_pc_hash, tmp_hagID)
                        dictTValue['tName'] = tmp_pc_name_1
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcUnLock'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcUnLockNone'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'set'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'set')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if len(tmp_reast_str) > 0:
                    tmp_pc_name = tmp_reast_str
                    tmp_pc_name = tmp_pc_name.strip()
                    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    )
                    tmp_flag_done = False
                    if OlivaDiceCore.pcCard.pcCardDataGetSelectionKeyLock(
                        tmp_pcHash,
                        tmp_hagID
                    ) == None:
                        tmp_flag_done = OlivaDiceCore.pcCard.pcCardDataSetSelectionKey(
                            tmp_pcHash,
                            tmp_pc_name
                        )
                    else:
                        tmp_flag_done = OlivaDiceCore.pcCard.pcCardDataSetSelectionKeyLock(
                            tmp_pcHash,
                            tmp_pc_name,
                            tmp_hagID
                        )
                    if tmp_flag_done:
                        dictTValue['tPcSelection'] = tmp_pc_name
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSet'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetError'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'init'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'init')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                flag_force_init = False
                if isMatchWordStart(tmp_reast_str, 'force'):
                    flag_force_init = True
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'force')
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                tmp_dict_pc_card = OlivaDiceCore.pcCard.pcCardDataGetByPcName(
                    tmp_pcHash,
                    hagId = tmp_hagID
                )
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    tmp_pcHash,
                    tmp_hagID
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
                                forceMapping = flag_force_init,
                                hagId = tmp_hagID
                            )
                            tmp_pcCard_list.append(
                                '%s:%s' % (
                                    OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                        tmp_pcHash,
                                        tmp_init_dict_this,
                                        flagShow = True,
                                        hagId = tmp_hagID
                                    ),
                                    str(tmp_skill_rd.resInt)
                                )
                            )
                dictTValue['tPcInitResult'] = '\n%s' % ' '.join(tmp_pcCard_list)
                dictTValue['tPcTempName'] = tmp_template_name
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitSt'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'new'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'new')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip('')
                tmp_pc_name = None
                if len(tmp_reast_str) > 0:
                    tmp_pc_name = tmp_reast_str
                if tmp_pc_name != None:
                    tmp_pc_name = OlivaDiceCore.pcCard.fixName(tmp_pc_name)
                    if not OlivaDiceCore.pcCard.checkPcName(tmp_pc_name):
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcNewError'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        return
                    else:
                        tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        )
                        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                            tmp_pcHash,
                            '__new',
                            0,
                            tmp_pc_name,
                            hagId = tmp_hagID
                        )
                        OlivaDiceCore.pcCard.pcCardDataDelBySkillName(
                            tmp_pcHash,
                            '__new',
                            tmp_pc_name
                        )
                        dictTValue['tPcSelection'] = tmp_pc_name
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcNew'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                return
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
                        tmp_pcHash,
                        tmp_hagID
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
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcDel'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcDelError'], dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcDelNone'], dictTValue)
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
                    tmp_pcHash,
                    tmp_hagID
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
                        tmp_pc_name,
                        skipDel = True
                    )
                    OlivaDiceCore.pcCard.pcCardRebase(
                        tmp_pcHash,
                        tmp_pc_name,
                        tmp_hagID
                    )
                    dictTValue['tPcSelection'] = tmp_pc_name
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcClear'], dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcClearNone'], dictTValue)
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
                    tmp_pcHash,
                    tmp_hagID
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
                        tmp_pcSkillName,
                        hagId = tmp_hagID
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
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRm'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                elif tmp_pcSkillName != None:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRmCardNone'], dictTValue)
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
                    ),
                    tmp_hagID
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
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTemp'], dictTValue)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempError'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempError'], dictTValue)
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
                        #显示群内规则设定
                        tmp_hag_id = tmp_hagID
                        tmp_user_platform = plugin_event.platform['platform']
                        tmp_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                            userConfigKey = 'groupTemplate',
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_hag_id,
                            userType = 'group',
                            platform = tmp_user_platform,
                        )
                        tmp_groupTemplateRule = OlivaDiceCore.userConfig.getUserConfigByKey(
                            userConfigKey = 'groupTemplateRule',
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_hag_id,
                            userType = 'group',
                            platform = tmp_user_platform
                        )
                        dictTValue['tResult'] = ''
                        if tmp_groupTemplate != None and tmp_groupTemplateRule != None:
                            dictTValue['tPcTempName'] = tmp_groupTemplate
                            dictTValue['tPcTempRuleName'] = tmp_groupTemplateRule
                            dictTValue['tResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGroupTempRuleShow'], dictTValue)
                        dictTValue['tPcSelection'] = tmp_pc_name
                        dictTValue['tPcTempName'] = tmp_template_name
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempShow'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempError'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'rule'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rule')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_hagID
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
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempRule'], dictTValue)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempRuleError'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempRuleError'], dictTValue)
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
                        #显示群内规则设定
                        tmp_hag_id = tmp_hagID
                        tmp_user_platform = plugin_event.platform['platform']
                        tmp_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                            userConfigKey = 'groupTemplate',
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_hag_id,
                            userType = 'group',
                            platform = tmp_user_platform,
                        )
                        tmp_groupTemplateRule = OlivaDiceCore.userConfig.getUserConfigByKey(
                            userConfigKey = 'groupTemplateRule',
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_hag_id,
                            userType = 'group',
                            platform = tmp_user_platform
                        )
                        dictTValue['tResult'] = ''
                        if tmp_groupTemplate != None and tmp_groupTemplateRule != None:
                            dictTValue['tPcTempName'] = tmp_groupTemplate
                            dictTValue['tPcTempRuleName'] = tmp_groupTemplateRule
                            dictTValue['tResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGroupTempRuleShow'], dictTValue)
                        dictTValue['tPcSelection'] = tmp_pc_name
                        dictTValue['tPcTempName'] = tmp_template_name
                        dictTValue['tPcTempRuleName'] = tmp_template_rule_name
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempRuleShow'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcTempRuleError'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'note') or isMatchWordStart(tmp_reast_str, 'rec'):
                flag_mode = 'note'
                keyName = 'noteRecord'
                if isMatchWordStart(tmp_reast_str, 'note'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'note')
                    flag_mode = 'note'
                    keyName = 'noteRecord'
                elif isMatchWordStart(tmp_reast_str, 'rec'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rec')
                    flag_mode = 'rec'
                    keyName = 'mappingRecord'
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_key = None
                tmp_value = None
                tmp_reast_str_list = tmp_reast_str.split(' ')
                tmp_reast_str_list = [tmp_reast_str_list_this for tmp_reast_str_list_this in tmp_reast_str_list if tmp_reast_str_list_this != '']
                if len(tmp_reast_str_list) > 0:
                    tmp_key = tmp_reast_str_list[0]
                    tmp_key = OlivaDiceCore.pcCard.fixName(tmp_key)
                if flag_mode == 'note':
                    if len(tmp_reast_str_list) > 1:
                        tmp_value = ' '.join(tmp_reast_str_list[1:])
                elif flag_mode == 'rec':
                    if len(tmp_reast_str_list) > 1:
                        tmp_value = tmp_reast_str_list[1]
                OlivaDiceCore.msgReplyModel.setPcNoteOrRecData(
                    plugin_event = plugin_event,
                    tmp_pc_id = tmp_pc_id,
                    tmp_pc_platform = tmp_pc_platform,
                    tmp_hagID = tmp_hagID,
                    dictTValue = dictTValue,
                    dictStrCustom = dictStrCustom,
                    keyName = keyName,
                    tmp_key = tmp_key,
                    tmp_value = tmp_value,
                    flag_mode = flag_mode,
                    enableFalse = True
                )
                return
            tmp_reast_str_new = tmp_reast_str
            if len(tmp_reast_str_new) > 0:
                tmp_reast_str_list = tmp_reast_str_new.split(' ')
                tmp_skill_update_flag = None
                tmp_skill_value_update = None
                op_list = ['+', '-', '*', '/']
                [tmp_skill_name, tmp_skill_value] = getExpression(tmp_reast_str_new, reverse = True)
                if tmp_skill_name == '':
                    tmp_skill_name = None
                if tmp_skill_value == '':
                    tmp_skill_value = None
                if tmp_skill_value != None:
                    if tmp_skill_value[0] not in op_list:
                        tmp_split_list_all = [[tmp_reast_str_new.split(op_this), op_this] for op_this in op_list]
                        tmp_split_list_match = None
                        for tmp_split_list_this in tmp_split_list_all:
                            if (
                                len(tmp_split_list_this[0]) > 1
                            ) and ((
                                    tmp_split_list_match == None
                                ) or (
                                    len(tmp_split_list_this[0][0]) < tmp_split_list_match[0][0]
                            )):
                                tmp_split_list_match = tmp_split_list_this
                        if tmp_split_list_match != None:
                            tmp_skill_name_new = tmp_split_list_match[0][0]
                            tmp_skill_value_new = tmp_split_list_match[1] + tmp_split_list_match[1].join(tmp_split_list_match[0][1:])
                            tmp_roll_para_new = '0%s' % tmp_skill_value_new
                            rd_para_new = OlivaDiceCore.onedice.RD(tmp_roll_para_new)
                            rd_para_new.roll()
                            if rd_para_new.resError == None:
                                tmp_skill_name = tmp_skill_name_new
                                tmp_skill_value = tmp_skill_value_new
                if tmp_skill_value != None:
                    if len(tmp_skill_value) > 1 and tmp_skill_value[0] == '+':
                        tmp_skill_update_flag = '+'
                        tmp_skill_value_update = tmp_skill_value[1:]
                    elif len(tmp_skill_value) > 1 and tmp_skill_value[0] == '-':
                        tmp_skill_update_flag = '-'
                        tmp_skill_value_update = tmp_skill_value[1:]
                    elif len(tmp_skill_value) > 1 and tmp_skill_value[0] == '*':
                        tmp_skill_update_flag = '*'
                        tmp_skill_value_update = tmp_skill_value[1:]
                    elif len(tmp_skill_value) > 1 and tmp_skill_value[0] == '/':
                        tmp_skill_update_flag = '/'
                        tmp_skill_value_update = tmp_skill_value[1:]
                    else:
                        tmp_skill_value = None
                if tmp_skill_name != None:
                    tmp_skill_name = tmp_skill_name.strip(' ')
                    tmp_skill_name = OlivaDiceCore.pcCard.fixName(tmp_skill_name, flagMode = 'skillName')
                    if not OlivaDiceCore.pcCard.checkPcName(tmp_skill_name):
                        tmp_skill_name = None
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
                        tmp_skill_name,
                        hagId = tmp_hagID
                    )
                    rd_para_str = str(tmp_skill_value_old) + tmp_skill_value

                    tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_hagID
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
                            dictTValue['tName'],
                            hagId = tmp_hagID
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
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcUpdateSkillValue'], dictTValue)
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
                tmp_pc_name = OlivaDiceCore.pcCard.fixName(tmp_pc_name)
                if not OlivaDiceCore.pcCard.checkPcName(tmp_pc_name):
                    return
            while len(tmp_reast_str) > 0 and tmp_skill_name_find == None:
                tmp_skill_name = None
                tmp_skill_value = None
                flag_is_mapping = False
                if tmp_reast_str[0] in ['&']:
                    flag_is_mapping = True
                    tmp_reast_str_list_0 = tmp_reast_str.split('=')
                    if len(tmp_reast_str_list_0) > 1:
                        tmp_skill_name = tmp_reast_str_list_0[0][1:]
                        tmp_reast_str = '='.join(tmp_reast_str_list_0[1:])
                        if len(tmp_reast_str) > 0:
                            [tmp_skill_value, tmp_reast_str] = getExpression(tmp_reast_str)
                            tmp_reast_str = skipSpaceStart(tmp_reast_str)
                else:
                    [tmp_skill_name, tmp_reast_str] = getToNumberPara(tmp_reast_str)
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    if len(tmp_reast_str) > 0:
                        [tmp_skill_value, tmp_reast_str] = getNumberPara(tmp_reast_str)
                        tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if tmp_skill_name == '':
                    tmp_skill_name = None
                if tmp_skill_value == '':
                    tmp_skill_value = None
                if not flag_is_mapping and tmp_skill_value != None:
                    tmp_skill_value = int(tmp_skill_value)
                if tmp_skill_name != None:
                    if tmp_skill_name[-1] in ['=', ':']:
                        if not flag_is_mapping:
                            tmp_skill_name = tmp_skill_name[:-1]
                    tmp_skill_name = OlivaDiceCore.pcCard.fixName(tmp_skill_name)
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
                        ),
                        tmp_hagID
                    )
                    if tmp_pc_name_1 != None:
                        dictTValue['tName'] = tmp_pc_name_1
                    if tmp_pc_name != None:
                        dictTValue['tName'] = tmp_pc_name
                    for tmp_skill_pair_this in tmp_skill_pair_list:
                        if type(tmp_skill_pair_this[1]) == int:
                            OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                OlivaDiceCore.pcCard.getPcHash(
                                    tmp_pc_id,
                                    tmp_pc_platform
                                ),
                                tmp_skill_pair_this[0],
                                tmp_skill_pair_this[1],
                                dictTValue['tName'],
                                hagId = tmp_hagID
                            )
                        elif type(tmp_skill_pair_this[1]) == str:
                            OlivaDiceCore.msgReplyModel.setPcNoteOrRecData(
                                plugin_event = plugin_event,
                                tmp_pc_id = tmp_pc_id,
                                tmp_pc_platform = tmp_pc_platform,
                                tmp_hagID = tmp_hagID,
                                dictTValue = dictTValue,
                                dictStrCustom = dictStrCustom,
                                keyName = 'mappingRecord',
                                tmp_key = tmp_skill_pair_this[0],
                                tmp_value = tmp_skill_pair_this[1],
                                flag_mode = 'rec',
                                enableFalse = False
                            )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetSkillValue'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_hagID
                )
                tmp_skill_value_find = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_skill_name_find,
                    hagId = tmp_hagID
                )
                if tmp_pc_name_1 != None:
                    dictTValue['tName'] = tmp_pc_name_1
                dictTValue['tSkillName'] = tmp_skill_name_find
                dictTValue['tSkillValue'] = str(tmp_skill_value_find)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetSingleSkillValue'], dictTValue)
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
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSetGroupTempRule'], dictTValue)
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
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDelGroupTempRule'], dictTValue)
                OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                    userHash = OlivaDiceCore.userConfig.getUserHash(
                        userId = tmp_hag_id,
                        userType = 'group',
                        platform = tmp_user_platform
                    )
                )
            else:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'set'):
            OlivaDiceCore.msgReplyModel.replySET_command(plugin_event, Proc, valDict)
        elif (
            isMatchWordStart(tmp_reast_str, 'coc6')
        ) or (
            isMatchWordStart(tmp_reast_str, 'coc')
        ) or (
            isMatchWordStart(tmp_reast_str, 'dnd')
        ):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_1 = ''
            tmp_pcCardTemplateName = 'default'
            if isMatchWordStart(tmp_reast_str, 'coc6'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'coc6')
                tmp_pcCardTemplateName = 'COC6'
            elif isMatchWordStart(tmp_reast_str, 'coc'):
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
                    if tmp_pcCardTemplateName in ['COC7']:
                        tmp_reply_str_1 += '共计:%d/%d %.2f%%' % (tmp_total_count_1, tmp_total_count_2, 100 * tmp_total_count_1 / tmp_total_count_2)
                    elif tmp_pcCardTemplateName in ['COC6', 'DND5E']:
                        tmp_reply_str_1 += '共计:%d' % tmp_total_count_1
                dictTValue['tPcInitResult'] = tmp_reply_str_1
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInit'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            else:
                return
        elif isMatchWordStart(tmp_reast_str, 'sc'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'sc')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) <= 0:
                replyMsgLazyHelpByEvent(plugin_event, 'sc')
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
                replyMsgLazyHelpByEvent(plugin_event, 'sc')
                return
            if tmp_sancheck_para == None:
                replyMsgLazyHelpByEvent(plugin_event, 'sc')
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
                replyMsgLazyHelpByEvent(plugin_event, 'sc')
                return
            tmp_pc_name = None
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                ),
                tmp_hagID
            )
            if tmp_pc_name_1 == None:
                tmp_pc_name = dictTValue['tName']
                if OlivaDiceCore.pcCard.pcCardRebase(
                    OlivaDiceCore.pcCard.getPcHash(
                        tmp_pc_id,
                        tmp_pc_platform
                    ),
                    tmp_pc_name,
                    tmp_hagID
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
                        'SAN',
                        hagId = tmp_hagID
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
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
                        tmp_sancheck_para_final = tmp_sancheck_para_s
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
                        tmp_sancheck_para_final = tmp_sancheck_para_s
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
                        tmp_sancheck_para_final = tmp_sancheck_para_s
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
                        tmp_sancheck_para_final = tmp_sancheck_para_f
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
                        tmp_sancheck_para_final = tmp_sancheck_para_f
                        flag_GreatFailed = True
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatFailed'], dictTValue)
                    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckNope'], dictTValue)
                    else:
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckError'], dictTValue)
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
                            tmp_pc_name,
                            hagId = tmp_hagID
                        )
                        dictTValue['tName'] = tmp_pc_name
                        dictTValue['tSkillValue'] = str(tmp_skill_value_old)
                        dictTValue['tSkillValueNew'] = str(tmp_skill_value)
                        dictTValue['tRollResult'] = '1D100=' + str(tmp_rd_int)
                        if flag_GreatFailed:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheckGreatFailed'], dictTValue)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheck'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    else:
                        dictTValue['tName'] = tmp_pc_name
                        dictTValue['tSkillValue'] = str(tmp_skill_value_old)
                        dictTValue['tRollResult'] = '1D100=' + str(tmp_rd_int)
                        dictTValue['tRollSubResult'] = tmp_sancheck_para_final
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheckError'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
            else:
                replyMsgLazyHelpByEvent(plugin_event, 'sc')
        elif isMatchWordStart(tmp_reast_str, 'ri'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'ri')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if tmp_hagID == None:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
            OlivaDiceCore.msgReplyModel.replyRI_command(
                plugin_event = plugin_event,
                tmp_reast_str = tmp_reast_str,
                tmp_pc_id = tmp_pc_id,
                tmp_pc_platform = tmp_pc_platform,
                tmp_hagID = tmp_hagID,
                dictTValue = dictTValue,
                dictStrCustom = dictStrCustom,
                flag_reply = True
            )
        elif isMatchWordStart(tmp_reast_str, 'init'):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            bot_hash = plugin_event.bot_info.hash
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'init')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if tmp_hagID == None:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
            if isMatchWordStart(tmp_reast_str, 'set'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'set')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                OlivaDiceCore.msgReplyModel.replyRI_command(
                    plugin_event = plugin_event,
                    tmp_reast_str = tmp_reast_str,
                    tmp_pc_id = tmp_pc_id,
                    tmp_pc_platform = tmp_pc_platform,
                    tmp_hagID = tmp_hagID,
                    dictTValue = dictTValue,
                    dictStrCustom = dictStrCustom,
                    flag_reply = True
                )
                return
            elif isMatchWordStart(tmp_reast_str, 'del'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'del')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.strip(' ')
                tmp_name = tmp_reast_str
                tmp_groupHash = OlivaDiceCore.userConfig.getUserHash(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform
                )
                # groupInitParaList
                tmp_groupInitList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitParaList',
                    botHash = bot_hash
                )
                if tmp_groupInitList_list == None:
                    tmp_groupInitList_list = {}
                if tmp_name in tmp_groupInitList_list:
                    tmp_groupInitList_list.pop(tmp_name)
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = tmp_pc_platform,
                        userConfigKey = 'groupInitParaList',
                        userConfigValue = tmp_groupInitList_list,
                        botHash = bot_hash
                    )
                # groupInitList
                tmp_groupInitList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitList',
                    botHash = bot_hash
                )
                if tmp_groupInitList_list == None:
                    tmp_groupInitList_list = {}
                if tmp_name in tmp_groupInitList_list:
                    tmp_groupInitList_list.pop(tmp_name)
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = tmp_pc_platform,
                        userConfigKey = 'groupInitList',
                        userConfigValue = tmp_groupInitList_list,
                        botHash = bot_hash
                    )
                OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                    userHash = tmp_groupHash
                )
                dictTValue['tName'] = tmp_name
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitDel'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'reset', fullMatch = True):
                tmp_groupInitParaList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitParaList',
                    botHash = bot_hash
                )
                tmp_groupInitList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitList',
                    botHash = bot_hash
                )
                if tmp_groupInitList_list == None:
                    tmp_groupInitList_list = {}
                if tmp_groupInitParaList_list == None:
                    tmp_groupInitParaList_list = {}
                for tmp_groupInitParaList_list_this in tmp_groupInitParaList_list:
                    tmp_value_final = None
                    tmp_value = tmp_groupInitParaList_list[tmp_groupInitParaList_list_this]
                    tmp_value_rd = OlivaDiceCore.onedice.RD(tmp_value)
                    tmp_value_rd.roll()
                    if tmp_value_rd.resError == None:
                        tmp_value_final = tmp_value_rd.resInt
                    if tmp_value_final != None:
                        tmp_groupInitList_list[tmp_groupInitParaList_list_this] = tmp_value_final
                OlivaDiceCore.userConfig.setUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitParaList',
                    userConfigValue = tmp_groupInitParaList_list,
                    botHash = bot_hash
                )
                OlivaDiceCore.userConfig.setUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitList',
                    userConfigValue = tmp_groupInitList_list,
                    botHash = bot_hash
                )
                tmp_groupHash = OlivaDiceCore.userConfig.getUserHash(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform
                )
                OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                    userHash = tmp_groupHash
                )
                tmp_groupInitList_list_sort = [
                    [tmp_groupInitList_list_this, tmp_groupInitList_list[tmp_groupInitList_list_this]]
                    for tmp_groupInitList_list_this in tmp_groupInitList_list
                ]
                tmp_groupInitList_list_sort.sort(key = lambda x : x[1], reverse = True)
                count = 1
                tmp_groupInitList_list_final = []
                for tmp_groupInitList_list_sort_this in tmp_groupInitList_list_sort:
                    dictTValue['tId'] = str(count)
                    dictTValue['tSubName'] = str(tmp_groupInitList_list_sort_this[0])
                    dictTValue['tSubResult'] = str(tmp_groupInitList_list_sort_this[1])
                    if dictTValue['tSubName'] in tmp_groupInitParaList_list:
                        dictTValue['tSubResult'] = '%s=%s' % (
                            tmp_groupInitParaList_list[dictTValue['tSubName']],
                            str(tmp_groupInitList_list_sort_this[1])
                        )
                    tmp_groupInitList_list_final.append(
                        OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitShowNode'], dictTValue)
                    )
                    count += 1
                dictTValue['tResult'] = '\n'.join(tmp_groupInitList_list_final)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitReset'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'clear', fullMatch = True):
                OlivaDiceCore.userConfig.setUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitParaList',
                    userConfigValue = {},
                    botHash = bot_hash
                )
                OlivaDiceCore.userConfig.setUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitList',
                    userConfigValue = {},
                    botHash = bot_hash
                )
                tmp_groupHash = OlivaDiceCore.userConfig.getUserHash(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform
                )
                OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                    userHash = tmp_groupHash
                )
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitClear'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
            elif '' == tmp_reast_str:
                tmp_groupInitList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_pc_platform,
                    userConfigKey = 'groupInitList',
                    botHash = bot_hash
                )
                if tmp_groupInitList_list == None:
                    tmp_groupInitList_list = {}
                tmp_groupInitList_list_sort = [
                    [tmp_groupInitList_list_this, tmp_groupInitList_list[tmp_groupInitList_list_this]]
                    for tmp_groupInitList_list_this in tmp_groupInitList_list
                ]
                tmp_groupInitList_list_sort.sort(key = lambda x : x[1], reverse = True)
                count = 1
                tmp_groupInitList_list_final = []
                for tmp_groupInitList_list_sort_this in tmp_groupInitList_list_sort:
                    dictTValue['tId'] = str(count)
                    dictTValue['tSubName'] = str(tmp_groupInitList_list_sort_this[0])
                    dictTValue['tSubResult'] = str(tmp_groupInitList_list_sort_this[1])
                    tmp_groupInitList_list_final.append(
                        OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitShowNode'], dictTValue)
                    )
                    count += 1
                dictTValue['tResult'] = '\n'.join(tmp_groupInitList_list_final)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitShow'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
        elif isMatchWordStart(tmp_reast_str, 'rav'):
            OlivaDiceCore.msgReplyModel.replyRAV_command(plugin_event, Proc, valDict)
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
            flag_op = None
            tmp_op_value = None
            tmp_skill_value_str = None
            if tmp_skill_name != None:
                if len(tmp_skill_name) >= 1 and tmp_skill_name[-1] in [
                    '+', '-', '*', '/'
                ]:
                    flag_op = tmp_skill_name[-1]
                    tmp_skill_name = tmp_skill_name[:-1]
                    tmp_skill_name = tmp_skill_name.rstrip(' ')
                    tmp_op_value = tmp_skill_value
                    tmp_skill_value = None
                    if len(tmp_reast_str) > 0:
                        [tmp_skill_value, tmp_reast_str] = getNumberPara(tmp_reast_str)
                        tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    if tmp_skill_value != None:
                        tmp_skill_value = int(tmp_skill_value)
                tmp_skill_name = tmp_skill_name.upper()
                if tmp_skill_value != None:
                    pass
                else:
                    tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        OlivaDiceCore.pcCard.getPcHash(
                            tmp_pc_id,
                            tmp_pc_platform
                        ),
                        tmp_skill_name,
                        hagId = tmp_hagID
                    )
                if flag_op != None and tmp_op_value != None and tmp_skill_value != None:
                    tmp_skill_value_rd_str = str(tmp_skill_value) + str(flag_op) + str(tmp_op_value)
                    tmp_skill_value_rd = OlivaDiceCore.onedice.RD(tmp_skill_value_rd_str)
                    tmp_skill_value_rd.roll()
                    if tmp_skill_value_rd.resError == None:
                        tmp_skill_value = tmp_skill_value_rd.resInt
                        tmp_skill_value_str = '%s=%s' % (tmp_skill_value_rd_str, str(tmp_skill_value))
            elif tmp_skill_value != None:
                pass
            if tmp_skill_value_str == None and tmp_skill_value != None:
                tmp_skill_value_str = str(tmp_skill_value)
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                ),
                tmp_hagID
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
                        dictTValue['tSkillValue'] = tmp_skill_value_str
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
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHardSucceed'], dictTValue)
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckExtremeHardSucceed'], dictTValue)
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatSucceed'], dictTValue)
                            flag_check_success = True
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatFailed'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_01:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate01'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_02:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate02'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_03:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate03'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_04:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate04'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_05:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate05'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_06:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate06'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_07:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate07'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_08:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate08'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_09:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate09'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_10:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate10'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_11:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate11'], dictTValue)
                        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckNope'], dictTValue)
                        else:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckError'], dictTValue)
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
                            dictTValue['tSkillValue'] = tmp_skill_value_str
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
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHardSucceed'], dictTValue)
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckExtremeHardSucceed'], dictTValue)
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatSucceed'], dictTValue)
                                flag_check_success = True
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatFailed'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_01:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate01'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_02:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate02'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_03:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate03'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_04:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate04'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_05:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate05'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_06:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate06'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_07:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate07'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_08:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate08'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_09:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate09'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_10:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate10'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_11:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate11'], dictTValue)
                            elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckNope'], dictTValue)
                            else:
                                tmp_tSkillCheckReasult += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckError'], dictTValue)
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
                            tmp_skill_name,
                            hagId = tmp_hagID
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
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckWithSkillName'], dictTValue)
                        tmp_reply_str_show = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHideShowWithSkillName'], dictTValue)
                        if flag_hide_roll and flag_is_from_group:
                            dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHideWithSkillName'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheck'], dictTValue)
                        tmp_reply_str_show = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHideShow'], dictTValue)
                        if flag_hide_roll and flag_is_from_group:
                            dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHide'], dictTValue)
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
                tmp_pcHash,
                tmp_hagID
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
                        tmp_skill_name,
                        hagId = tmp_hagID
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
                                    dictTValue['tName'],
                                    hagId = tmp_hagID
                                )
                                dictTValue['tRollSubResult'] = '%s=%s=%s' % (rd_para_str_2, rd_para_2.resDetail, (rd_para_2.resInt))
                                dictTValue['tSkillCheckReasult'] = '%s%s' % (
                                    OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue),
                                    OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceContent'], dictTValue)
                                )
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceCheck'], dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
                        else:
                            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceCheck'], dictTValue)
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
                                    tmp_skill_name,
                                    hagId = tmp_hagID
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
                            tmp_skill_name,
                            hagId = tmp_hagID
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
                                    tmp_pc_name_1,
                                    hagId = tmp_hagID
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
                                    flagShow = True,
                                    hagId = tmp_hagID
                                ),
                                str(tmp_enhance_succeed_list_this[1]),
                                str(tmp_enhance_succeed_list_this[2] - tmp_enhance_succeed_list_this[1])
                            )
                        )
                    if len(tmp_enhance_succeed_list_2) > 0:
                        dictTValue['tSkillEnhanceSucceedList'] = '\n%s' % ' '.join(tmp_enhance_succeed_list_2)
                    else:
                        dictTValue['tSkillEnhanceSucceedList'] = ''
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceAll'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceError'], dictTValue)
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
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollRange'], dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
        #基于OneDice标准，这些指令不再需要，指引用户看HelpDoc
        #elif isMatchWordStart(tmp_reast_str, 'ww'):
        #    replyMsgLazyHelpByEvent(plugin_event, 'r')
        #    return
        #elif isMatchWordStart(tmp_reast_str, 'dx'):
        #    replyMsgLazyHelpByEvent(plugin_event, 'r')
        #    return
        elif isMatchWordStart(tmp_reast_str, 'rr'):
            OlivaDiceCore.msgReplyModel.replyRR_command(plugin_event, Proc, valDict)
        elif (
            isMatchWordStart(tmp_reast_str, 'rx')
        ) or (
            isMatchWordStart(tmp_reast_str, 'r')
        ) or (
            isMatchWordStart(tmp_reast_str, 'ww')
        ) or (
            isMatchWordStart(tmp_reast_str, 'w')
        ) or (
            isMatchWordStart(tmp_reast_str, 'dxx')
        ) or (
            isMatchWordStart(tmp_reast_str, 'dx')
        ):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_show = ''
            flag_roll_mode = 'r'
            if isMatchWordStart(tmp_reast_str, 'rx'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rx')
                flag_roll_mode = 'rx'
            elif isMatchWordStart(tmp_reast_str, 'r'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'r')
                flag_roll_mode = 'r'
            elif isMatchWordStart(tmp_reast_str, 'ww'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'ww')
                flag_roll_mode = 'ww'
            elif isMatchWordStart(tmp_reast_str, 'w'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'w')
                flag_roll_mode = 'w'
            elif isMatchWordStart(tmp_reast_str, 'dxx'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'dxx')
                flag_roll_mode = 'dxx'
            elif isMatchWordStart(tmp_reast_str, 'dx'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'dx')
                flag_roll_mode = 'dx'
            #此处只对实体化后的&做处理，因为这是运算符，其余保持原样
            #如果以后有全面反实体化的需求则需直接调整这里
            #tmp_reast_str = tmp_reast_str.replace('&amp;', '&')
            rd_para_str = '1D100'
            if flag_roll_mode in ['r', 'rx']:
                rd_para_str = '1D100'
            elif flag_roll_mode in ['ww', 'w']:
                rd_para_str = '10A10'
            elif flag_roll_mode in ['dx', 'dxx']:
                rd_para_str = '10C10'
            tmp_user_platform = plugin_event.platform['platform']
            rd_reason_str = None
            roll_times_count = 1
            flag_hide_roll = False
            flag_have_para = False
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                tmp_pc_id,
                tmp_pc_platform
            )
            tmp_pc_name_0 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash,
                tmp_hagID
            )
            skill_valueTable_raw = OlivaDiceCore.pcCard.pcCardDataGetByPcName(
                tmp_pcHash,
                hagId = tmp_hagID
            )
            skill_valueTable = skill_valueTable_raw.copy()
            if tmp_pc_name_0 != None:
                skill_valueTable.update(
                    OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        pcHash = tmp_pcHash,
                        pcCardName = tmp_pc_name_0,
                        dataKey = 'mappingRecord',
                        resDefault = {}
                    )
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
                if flag_roll_mode in ['rx']:
                    [tmp_rd_para_str, tmp_reast_str] = getExpression(tmp_reast_str, valueTable = None)
                else:
                    [tmp_rd_para_str, tmp_reast_str] = getExpression(tmp_reast_str, valueTable = skill_valueTable)
                if tmp_rd_para_str != None and tmp_rd_para_str != '':
                    rd_para_str = tmp_rd_para_str
                    if flag_roll_mode in ['ww', 'w']:
                        rd_para_str = re.sub(r'^(\d+)$', r'\1a10', rd_para_str)
                        rd_para_str = re.sub(r'^(\{.+\})$', r'\1a10', rd_para_str)
                        rd_para_str = re.sub(r'^(\d+)([+\-*xX/].+)$', r'\1a10\2', rd_para_str)
                        rd_para_str = re.sub(r'^(\{.+\})([+\-*xX/].+)$', r'\1a10\2', rd_para_str)
                    elif flag_roll_mode in ['dx', 'dxx']:
                        rd_para_str = re.sub(r'^(\d+)$', r'\1c10', rd_para_str)
                        rd_para_str = re.sub(r'^(\{.+\})$', r'\1c10', rd_para_str)
                        rd_para_str = re.sub(r'^(\d+)([+\-*xX/].+)$', r'\1c10\2', rd_para_str)
                        rd_para_str = re.sub(r'^(\{.+\})([+\-*xX/].+)$', r'\1c10\2', rd_para_str)
                    flag_have_para = True
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if len(tmp_reast_str) > 0:
                    rd_reason_str = tmp_reast_str
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                ),
                tmp_hagID
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
                    if flag_roll_mode in ['r', 'rx']:
                        rd_para_str = tmp_template['mainDice']
            rd_para_main_str = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_user_platform,
                userConfigKey = 'groupMainDice',
                botHash = plugin_event.bot_info.hash
            )
            rd_para_main_D_right = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_user_platform,
                userConfigKey = 'groupMainDiceDRight',
                botHash = plugin_event.bot_info.hash
            )
            if rd_para_main_str != None and not flag_have_para and flag_roll_mode in ['r', 'rx']:
                rd_para_str = rd_para_main_str
            tmp_template_customDefault = copy.deepcopy(tmp_template_customDefault)
            if type(rd_para_main_D_right) == int:
                if type(tmp_template_customDefault) != dict:
                    tmp_template_customDefault = {}
                    if 'd' not in tmp_template_customDefault:
                        tmp_template_customDefault['d'] = {}
                tmp_template_customDefault['d']['rightD'] = rd_para_main_D_right
            if roll_times_count == 1:
                rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault, valueTable = skill_valueTable)
                rd_para.roll()
                OlivaDiceCore.onediceOverride.saveRDDataUser(
                    data = rd_para,
                    botHash = plugin_event.bot_info.hash,
                    userId = tmp_userID,
                    platform = tmp_user_platform
                )
                tmp_reply_str_1 = ''
                if rd_para.resError == None:
                    tmp_resDetail_str = ''
                    tmp_resDetail_short_str = ''
                    if flag_roll_mode in ['w', 'dxx']:
                        tmp_resDetail_short_str = OlivaDiceCore.onediceOverride.RDDataFormat(
                            data = rd_para.resDetailData,
                            mode = 'short'
                        )
                        if tmp_resDetail_short_str == None:
                            tmp_resDetail_short_str = ''
                        if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                            tmp_reply_str_1 = rd_para_str + '=' + (', '.join(
                                OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                            ))
                        elif len(str(rd_para.resInt)) > 100:
                            tmp_reply_str_1 = rd_para_str + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                        else:
                            tmp_reply_str_1 = rd_para_str + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)
                    elif flag_roll_mode in ['ww', 'dx']:
                        if flag_roll_mode in ['ww']:
                            tmp_resDetail_str = OlivaDiceCore.onediceOverride.RDDataFormat(
                                data = rd_para.resDetailData,
                                mode = 'ww'
                            )
                        elif flag_roll_mode in ['dx']:
                            tmp_resDetail_str = OlivaDiceCore.onediceOverride.RDDataFormat(
                                data = rd_para.resDetailData,
                                mode = 'dx'
                            )
                        tmp_resDetail_short_str = OlivaDiceCore.onediceOverride.RDDataFormat(
                            data = rd_para.resDetailData,
                            mode = 'short'
                        )
                        if tmp_resDetail_str == None:
                            tmp_resDetail_str = ''
                        if tmp_resDetail_short_str == None:
                            tmp_resDetail_short_str = ''
                        if tmp_resDetail_short_str != tmp_resDetail_str:
                            tmp_resDetail_str += '=%s' % tmp_resDetail_short_str
                        if len(tmp_resDetail_str) == 0 or len(tmp_resDetail_str) > OlivaDiceCore.console.getConsoleSwitchByHash(
                            'largeRollLimit',
                            plugin_event.bot_info.hash
                        ):
                            if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                                tmp_reply_str_1 = rd_para_str + '=' + (', '.join(
                                    OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                ))
                            elif len(str(rd_para.resInt)) > 100:
                                tmp_reply_str_1 = rd_para_str + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                            else:
                                tmp_reply_str_1 = rd_para_str + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)
                        else:
                            if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                                tmp_reply_str_1 = rd_para_str + '=' + str(tmp_resDetail_str) + '=' + (', '.join(
                                    OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                ))
                            elif len(str(rd_para.resInt)) > 50:
                                tmp_reply_str_1 = rd_para_str + '=' + str(tmp_resDetail_str) + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                            else:
                                tmp_reply_str_1 = rd_para_str + '=' + str(tmp_resDetail_str) + '=' + str(rd_para.resInt)
                    elif flag_roll_mode in ['r', 'rx'] or True:
                        rd_para_str_new = None
                        tmp_resDetail_str = None
                        tmp_default_is1step = OlivaDiceCore.onediceOverride.RDDataFormat_default_is1step(rd_para.resDetailData)
                        if tmp_default_is1step != False:
                            rd_para_str_new = OlivaDiceCore.onediceOverride.RDDataFormat_default_1step(rd_para.resDetailData)
                        if tmp_default_is1step == 1:
                            tmp_resDetail_str = None
                        else:
                            tmp_resDetail_str = OlivaDiceCore.onediceOverride.RDDataFormat(
                                data = rd_para.resDetailData,
                                mode = 'default'
                            )
                        tmp_resInt_str = str(rd_para.resInt)
                        if tmp_resDetail_str == None:
                            tmp_resDetail_str = ''
                        if tmp_resDetail_str == str(tmp_resInt_str):
                            tmp_resDetail_str = ''
                        if rd_para_str_new == None:
                            rd_para_str_new = rd_para_str
                        if len(tmp_resDetail_str) == 0 or len(tmp_resDetail_str) > 150:
                            if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                                tmp_reply_str_1 = rd_para_str_new + '=' + (', '.join(
                                    OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                ))
                            elif len(str(tmp_resInt_str)) > 100:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resInt_str)[:50] + '...的天文数字'
                            else:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resInt_str)
                        else:
                            if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_str) + '=' + (', '.join(
                                    OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                ))
                            elif len(str(tmp_resInt_str)) > 50:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_str) + '=' + str(tmp_resInt_str)[:50] + '...的天文数字'
                            else:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_str) + '=' + str(tmp_resInt_str)
                else:
                    dictTValue['tResult'] = str(rd_para.resError)
                    dictTValue['tRollPara'] = str(rd_para_str)
                    if rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_GENERATE_FATAL:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError01'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_COMPLETE_FATAL:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError02'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_RAW_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError03'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_CHILD_PARA_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError04'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_NODE_OPERATION_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError05'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_OPERATION_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError06'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_STACK_EMPTY:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError07'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_LEFT_VAL_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError08'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_RIGHT_VAL_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError09'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_SUB_VAL_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError10'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_EXTREME_VAL_INVALID:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError11'], dictTValue)
                    elif rd_para.resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_REPLACE_FATAL:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError12'], dictTValue)
                    else:
                        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollErrorUnknown'], dictTValue)
                    tmp_reply_str_1 += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollErrorHelp'], dictTValue)
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
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollWithReason'], dictTValue)
                tmp_reply_str_show = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollHideShowWithReason'], dictTValue)
                if flag_hide_roll and flag_is_from_group:
                    dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollHideWithReason'], dictTValue)
            else:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRoll'], dictTValue)
                tmp_reply_str_show = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollHideShow'], dictTValue)
                if flag_hide_roll and flag_is_from_group:
                    dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollHide'], dictTValue)
            if flag_hide_roll and flag_is_from_group:
                replyMsg(plugin_event, tmp_reply_str_show)
                replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
            else:
                replyMsg(plugin_event, tmp_reply_str)
    nativeMsgBlocker(plugin_event, Proc)
    return


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
    return pluginReply(plugin_event, str(message))

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
    return pluginSend(plugin_event, target_type, target_id, message, host_id = host_id)

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
        pluginSend(plugin_event, 'private', plugin_event.data.user_id, message, host_id = plugin_event.data.host_id)
    else:
        pluginSend(plugin_event, 'private', plugin_event.data.user_id, message)
    replyMsgPrivateForObByEvent(plugin_event, message)
    return

def replyMsgPrivateForObByEvent(plugin_event, message):
    host_id = None
    group_id = None
    user_id = None
    tmp_hagID = None
    if 'host_id' in plugin_event.data.__dict__:
        host_id = plugin_event.data.host_id
    if 'group_id' in plugin_event.data.__dict__:
        group_id = plugin_event.data.group_id
    if 'user_id' in plugin_event.data.__dict__:
        user_id = plugin_event.data.user_id
    if host_id != None:
        tmp_hagID = '%s|%s' % (str(host_id), str(group_id))
    else:
        tmp_hagID = str(group_id)
    tmp_groupObList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'groupObList',
        botHash = plugin_event.bot_info.hash
    )
    if tmp_groupObList_list == None:
        tmp_groupObList_list = []
    for tmp_groupObList_list_this in tmp_groupObList_list:
        tmp_userId_this = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
            userHash = tmp_groupObList_list_this,
            userDataKey = 'userId',
            botHash = plugin_event.bot_info.hash
        )
        if tmp_userId_this != None and tmp_userId_this != user_id:
            if 'host_id' in plugin_event.data.__dict__:
                pluginSend(plugin_event, 'private', tmp_userId_this, message, host_id = plugin_event.data.host_id)
            else:
                pluginSend(plugin_event, 'private', tmp_userId_this, message)
    return

def replyMsgLazyHelpByEvent(plugin_event, help_key):
    tmp_reply_str = OlivaDiceCore.helpDoc.getHelp(str(help_key), plugin_event.bot_info.hash)
    if tmp_reply_str == None or tmp_reply_str == '':
        return None
    return replyMsg(plugin_event, str(tmp_reply_str))


#原始接口调用

def pluginReply(plugin_event, message):
    botHash = plugin_event.bot_info.hash
    messageSplitGate = OlivaDiceCore.console.getConsoleSwitchByHash(
        'messageSplitGate',
        botHash
    )
    messageSplitPageLimit = OlivaDiceCore.console.getConsoleSwitchByHash(
        'messageSplitPageLimit',
        botHash
    )
    messageSplitDelay = OlivaDiceCore.console.getConsoleSwitchByHash(
        'messageSplitDelay',
        botHash
    )
    messageSplitDelay = messageSplitDelay / 1000
    message = message.replace('{SPLIT}', '\f')
    message_list = message.split('\f')
    message_list_new = []
    for message_list_this in message_list:
        tmp_message = message_list_this
        while len(tmp_message) > messageSplitGate:
            message_list_new.append(tmp_message[:messageSplitGate])
            tmp_message = tmp_message[messageSplitGate:]
        message_list_new.append(tmp_message)
    message_list = message_list_new
    count = 1
    flag_need_split = len(message_list) > 1
    for message_list_this in message_list:
        if len(message_list_this) > 0:
            tmp_message = message_list_this
            if flag_need_split:
                tmp_message = '[第%s页]\n%s' % (
                    str(count),
                    message_list_this
                )
            plugin_event.reply(tmp_message)
            if flag_need_split:
                count += 1
                time.sleep(messageSplitDelay)
        if not flag_need_split or count > messageSplitPageLimit:
            break

def pluginSend(plugin_event, send_type, target_id, message, host_id = None):
    botHash = plugin_event.bot_info.hash
    messageSplitGate = OlivaDiceCore.console.getConsoleSwitchByHash(
        'messageSplitGate',
        botHash
    )
    messageSplitPageLimit = OlivaDiceCore.console.getConsoleSwitchByHash(
        'messageSplitPageLimit',
        botHash
    )
    messageSplitDelay = OlivaDiceCore.console.getConsoleSwitchByHash(
        'messageSplitDelay',
        botHash
    )
    messageSplitDelay = messageSplitDelay / 1000
    message = message.replace('{SPLIT}', '\f')
    message_list = message.split('\f')
    message_list_new = []
    for message_list_this in message_list:
        tmp_message = message_list_this
        while len(tmp_message) > messageSplitGate:
            message_list_new.append(tmp_message[:messageSplitGate])
            tmp_message = tmp_message[messageSplitGate:]
        message_list_new.append(tmp_message)
    message_list = message_list_new
    count = 1
    flag_need_split = len(message_list) > 1
    for message_list_this in message_list:
        if len(message_list_this) > 0:
            tmp_message = message_list_this
            if flag_need_split:
                tmp_message = '[第%s页]\n%s' % (
                    str(count),
                    message_list_this
                )
            plugin_event.send(send_type, target_id, tmp_message, host_id = host_id)
            if flag_need_split:
                count += 1
                time.sleep(messageSplitDelay)
        if not flag_need_split or count > messageSplitPageLimit:
            break

#阻塞普通消息
def nativeMsgBlocker(plugin_event, Proc):
    flag_is_from_host = False
    flag_is_from_group = False
    flag_hostEnable = True
    flag_hostLocalEnable = True
    flag_groupEnable = True
    flag_messageFliterModeDisabled = False
    tmp_hagID = None
    if plugin_event.plugin_info['func_type'] == 'group_message':
        if plugin_event.data.host_id != None:
            flag_is_from_host = True
        flag_is_from_group = True
    elif plugin_event.plugin_info['func_type'] == 'private_message':
        flag_is_from_group = False
    tmp_hagID = getHagIDFromMsg(plugin_event, Proc)
    if flag_is_from_host:
        flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = plugin_event.data.host_id,
            userType = 'host',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'hostEnable',
            botHash = plugin_event.bot_info.hash
        )
    if flag_is_from_host:
        flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = plugin_event.data.host_id,
            userType = 'host',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'hostLocalEnable',
            botHash = plugin_event.bot_info.hash
        )
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
    #消息过滤器
    if flag_messageFliterModeDisabled:
        plugin_event.set_block()
        return
    #此频道关闭时中断处理
    if not flag_hostLocalEnable:
        plugin_event.set_block()
        return
    #此群关闭时中断处理
    if not flag_groupEnable:
        plugin_event.set_block()
        return

def getHagIDFromMsg(plugin_event, Proc):
    tmp_hagID = None
    flag_is_from_host = False
    flag_is_from_group = False
    if plugin_event.plugin_info['func_type'] == 'group_message':
        if plugin_event.data.host_id != None:
            flag_is_from_host = True
        flag_is_from_group = True
    elif plugin_event.plugin_info['func_type'] == 'private_message':
        flag_is_from_group = False
    if flag_is_from_host and flag_is_from_group:
        tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
    elif flag_is_from_group:
        tmp_hagID = str(plugin_event.data.group_id)
    return tmp_hagID


#其他

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
            if reverse and tmp_total_offset < 0:
                tmp_total_offset = 0
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
                if (not flag_not_hit) and (data[tmp_total_offset:tmp_total_offset + tmp_offset_len] in OlivaDiceCore.onedice.dictOperationPriority or data[tmp_total_offset:tmp_total_offset + tmp_offset_len] in OlivaDiceCore.onedice.listOperationSub):
                    flag_value = False
            for range_this in reversed(range(1, OlivaDiceCore.onedice.lenOperationMax + 1)):
                if flag_not_hit and (
                    tmp_total_offset + range_this <= len(data)
                ) and data[tmp_total_offset:tmp_total_offset + range_this] in OlivaDiceCore.onedice.dictOperationPriority:
                    tmp_offset_len = range_this
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
            if reverse and tmp_total_offset < 0:
                tmp_total_offset = 0
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
