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
    OlivaDiceCore.censorAPI.initCensor(Proc.Proc_data['bot_info_dict'])
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
            'qqGuildv2_link',
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
        if plugin_event.data.group_id not in [-1, None, '-1']:
            new_plugin_event = OlivaDiceCore.msgEvent.getReRxEvent_group_message(
                src = plugin_event,
                message = '[戳一戳]'
            )
            replyMsg(
                new_plugin_event,
                OlivaDiceCore.crossHook.dictHookFunc['pokeHook'](plugin_event = new_plugin_event, type = 'group')
            )
        elif plugin_event.data.group_id in [-1, None, '-1']:
            new_plugin_event = OlivaDiceCore.msgEvent.getReRxEvent_private_message(
                src = plugin_event,
                message = '[戳一戳]'
            )
            replyMsg(
                new_plugin_event,
                OlivaDiceCore.crossHook.dictHookFunc['pokeHook'](plugin_event = new_plugin_event, type = 'private')
            )

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tUserName'] = plugin_event.data.sender['name']
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
    tmp_id_str = str(plugin_event.base_info['self_id'])
    tmp_at_str_sub = None
    tmp_id_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
            tmp_id_str_sub = str(plugin_event.data.extend['sub_self_id'])
    tmp_reast_str = plugin_event.data.message
    tmp_reast_str = to_half_width(tmp_reast_str) # 转半角
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
    if flag_force_reply is False:
        tmp_reast_str_old = tmp_reast_str
        tmp_reast_obj = OlivOS.messageAPI.Message_templet(
            'old_string',
            tmp_reast_str
        )
        tmp_at_list = []
        for tmp_reast_obj_this in tmp_reast_obj.data:
            tmp_para_str_this = tmp_reast_obj_this.CQ()
            if type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.at:
                tmp_at_list.append(str(tmp_reast_obj_this.data['id']))
                tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
            elif type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.text:
                if tmp_para_str_this.strip(' ') == '':
                    tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
                else:
                    break
            else:
                break
        if tmp_id_str in tmp_at_list:
            flag_force_reply = True
        if tmp_id_str_sub in tmp_at_list:
            flag_force_reply = True
        if 'all' in tmp_at_list:
            flag_force_reply = True
        if flag_force_reply is True:
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
        else:
            tmp_reast_str = tmp_reast_str_old
    #反实例化临时方案，用于对齐OlivOS不同平台字符串标准
    tmp_reast_str = htmlUnescape(tmp_reast_str)

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
        valDict['flag_is_from_group'] = flag_is_from_group
        valDict['flag_is_from_group_admin'] = flag_is_from_group_admin
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
        # 默认tName是人物卡名
        tmp_pc_id = plugin_event.data.user_id
        tmp_pc_platform = plugin_event.platform['platform']
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
        
        if flag_is_from_master:
            if isMatchWordStart(tmp_reast_str, 'master'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'master')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if re.compile(r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$')\
                    .match(tmp_reast_str):
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBecomeMasterAlready'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                if isMatchWordStart(tmp_reast_str, ['exit','bye']):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['exit','bye'])
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    tmp_reast_str = tmp_reast_str.rstrip(' ')
                    tmp_group_id = None
                    if tmp_reast_str.isdecimal():
                        tmp_group_id = int(tmp_reast_str)
                    elif tmp_reast_str[0] == '-' and tmp_reast_str[1:].isdecimal():
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
                    if isMatchWordStart(tmp_reast_str, ['on', 'off']):
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
                elif isMatchWordStart(tmp_reast_str, ['notice', 'master']):
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
                            if tmp_listValue.isdecimal() and tmp_editKey in [
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
                                    if tmp_listValue_new.isdecimal():
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
                        if not tmp_reast_str.isdecimal():
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
                else:
                    replyMsgLazyHelpByEvent(plugin_event, 'system')
                return
            elif isMatchWordStart(tmp_reast_str, 'str'):
                tmp_reast_str = tmp_reast_str.strip(' ')
                tmp_reast_list = tmp_reast_str.split(' ')
                if len(tmp_reast_list) == 1 and len(tmp_reast_list[0]) > 0:
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
                else:
                    replyMsgLazyHelpByEvent(plugin_event, 'str')
                return
            elif isMatchWordStart(tmp_reast_str, 'helpdoc'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'helpdoc')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.strip(' ')
                tmp_reast_list = tmp_reast_str.split(' ')
                tmp_reast_list_len = len(tmp_reast_list)
                if tmp_reast_list_len == 1 and len(tmp_reast_list[0]) > 0:
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
                else:
                    replyMsgLazyHelpByEvent(plugin_event, 'helpdoc')
                return
            elif isMatchWordStart(tmp_reast_str, 'censor'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'censor')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.strip(' ')
                bot_hash = plugin_event.bot_info.hash
                if isMatchWordStart(tmp_reast_str, ['add', '+']):
                    if isMatchWordStart(tmp_reast_str, 'add'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'add')
                    elif isMatchWordStart(tmp_reast_str, '+'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '+')
                    tmp_censor_list_old = tmp_reast_str.replace('\r\n', '\n').split('\n')
                    tmp_censor_list = []
                    for tmp_censor_this in tmp_censor_list_old:
                        tmp_censor_list += tmp_censor_this.split('|')
                    tmp_censor_list_old = tmp_censor_list
                    tmp_censor_list = []
                    for tmp_censor_this in tmp_censor_list_old:
                        if len(tmp_censor_this) > 0:
                            tmp_censor_list.append(tmp_censor_this)
                    for tmp_censor_this in tmp_censor_list:
                        OlivaDiceCore.censorAPI.addConfigList(bot_hash, tmp_censor_this)
                    OlivaDiceCore.censorAPI.writeConfigListByHash(bot_hash)
                    OlivaDiceCore.censorAPI.patchCensorByHash(bot_hash, tmp_censor_list)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strAddCensor'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                elif isMatchWordStart(tmp_reast_str, ['del', '-']):
                    if isMatchWordStart(tmp_reast_str, 'del'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'del')
                    elif isMatchWordStart(tmp_reast_str, '-'):
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '-')
                    tmp_censor_list_old = tmp_reast_str.replace('\r\n', '\n').split('\n')
                    tmp_censor_list = []
                    for tmp_censor_this in tmp_censor_list_old:
                        tmp_censor_list += tmp_censor_this.split('|')
                    tmp_censor_list_old = tmp_censor_list
                    tmp_censor_list = []
                    for tmp_censor_this in tmp_censor_list_old:
                        if len(tmp_censor_this) > 0:
                            tmp_censor_list.append(tmp_censor_this)
                    for tmp_censor_this in tmp_censor_list:
                        OlivaDiceCore.censorAPI.delConfigList(bot_hash, tmp_censor_this)
                    OlivaDiceCore.censorAPI.writeConfigListByHash(bot_hash)
                    OlivaDiceCore.censorAPI.initCensorByHash(bot_hash)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDelCensor'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                else:
                    replyMsgLazyHelpByEvent(plugin_event, 'censor')
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
        if isMatchWordStart(tmp_reast_str, 'bot', isCommand = True):
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
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedAdmin'], dictTValue)
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
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedAdmin'], dictTValue)
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
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedAdmin'], dictTValue)
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
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedAdmin'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
            elif isMatchWordStart(tmp_reast_str, ['exit','bye']):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['exit','bye'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str = tmp_reast_str.rstrip(' ')
                if flag_is_from_group and tmp_reast_str in tmp_end_list:
                    if (flag_is_from_group_have_admin and flag_is_from_group_admin) or flag_is_from_master:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotExit'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        time.sleep(1)
                        plugin_event.set_group_leave(plugin_event.data.group_id)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedAdmin'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
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
                dictTValue['tAdapter'] = OlivaDiceCore.msgCustomManager.loadAdapterType(plugin_event.bot_info)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(OlivaDiceCore.data.bot_info_auto, dictTValue) \
                + '\n' + OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBot'], dictTValue)
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
        #放弃使用全前缀匹配方案
        if OlivaDiceCore.msgReplyModel.replyCONTEXT_fliter(tmp_reast_str):
            pass
        elif isMatchWordStart(tmp_reast_str, 'welcome', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'welcome')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if flag_is_from_group:
                if (flag_is_from_group_have_admin and flag_is_from_group_admin) or flag_is_from_master:
                    if len(tmp_reast_str) > 0:
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'welcomeMsg',
                            userConfigValue = tmp_reast_str,
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
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strWelcomeSet'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    else:
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'welcomeMsg',
                            userConfigValue = None,
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
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strWelcomeDel'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNeedAdmin'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, ['help', 'find'], isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['help', 'find'])
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
        elif isMatchWordStart(tmp_reast_str, 'dismiss', isCommand = True):
            tmp_reply_str = OlivaDiceCore.helpDoc.getHelp('dismiss', plugin_event.bot_info.hash)
            replyMsg(plugin_event, tmp_reply_str)
        elif isMatchWordStart(tmp_reast_str, 'draw', isCommand = True):
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
        elif isMatchWordStart(tmp_reast_str, 'ob', isCommand = True):
            tmp_user_platform = plugin_event.platform['platform']
            flag_solo = False
            if isMatchWordStart(tmp_reast_str, 'ob', fullMatch = True):
                flag_solo = True
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'ob')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if isMatchWordStart(tmp_reast_str, ['clear', 'clr'], fullMatch = True):
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
            elif flag_solo or isMatchWordStart(tmp_reast_str, ['exit', 'join'], fullMatch = True):
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
                        trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObExit'], dictTValue)
                    elif flag_ob_is_enable and flag_ob_will_enable:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObJoinAlready'], dictTValue)
                    elif not flag_ob_is_enable and not flag_ob_will_enable:
                        trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
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
                        if not flag_ob_is_enable:
                            plugin_event.set_group_card(
                                group_id = plugin_event.data.group_id,
                                user_id = tmp_pc_id,
                                card = f'ob_{tmp_userName}',
                                host_id = plugin_event.data.host_id
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
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strObExitAll'], dictTValue)
                    if tmp_reply_str != None:
                        replyMsg(plugin_event, tmp_reply_str)
        elif isMatchWordStart(tmp_reast_str, 'ti', fullMatch = True, isCommand = True):
            dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck('即时症状', plugin_event.bot_info.hash, valDict = valDict)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDrawTi'], dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'li', fullMatch = True, isCommand = True):
            dictTValue['tResult'] = OlivaDiceCore.drawCard.getDrawDeck('总结症状', plugin_event.bot_info.hash, valDict = valDict)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDrawLi'], dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'uinfo', isCommand = True):
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
        elif isMatchWordStart(tmp_reast_str, 'name', isCommand = True):
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
        elif isMatchWordStart(tmp_reast_str, 'nn', isCommand = True):
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
                    is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                    if is_new_card:
                        OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                replyMsgLazyHelpByEvent(plugin_event, 'nn')
            return
        elif isMatchWordStart(tmp_reast_str, 'sn', isCommand = True):
            is_at, at_user_id, tmp_reast_str = parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin)
            if is_at and not at_user_id:
                return
            tmp_pc_id = at_user_id if at_user_id else plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'sn')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                tmp_pc_id,
                tmp_pc_platform
            )
            tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash,
                tmp_hagID
            )
            tmp_template_name = None
            tmp_template_rule_name = None
            tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                tmp_pcHash,
                tmp_pc_name
            )
            tmp_template_rule_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateRuleKey(
                tmp_pcHash,
                tmp_pc_name
            )
            if tmp_template_name == None:
                tmp_template_name = 'default'
            if tmp_template_rule_name == None:
                tmp_template_rule_name = 'default'
            flag_mode = 'coc'
            flag_force = True
            tmp_pc_card_snTitle = None
            sn_title = None
            sn_title_new = None
            if tmp_hagID == None:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
            if isMatchWordStart(tmp_reast_str, 'auto'):
                if is_at: return
                auto_sn_enabled = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_pc_id,
                    userType = 'user',
                    platform = tmp_pc_platform,
                    userConfigKey = 'autoSnEnabled',
                    botHash = plugin_event.bot_info.hash,
                    default = False
                )
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'auto')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                if isMatchWordStart(tmp_reast_str, 'on', fullMatch = True):
                    # sn auto on 命令
                    if auto_sn_enabled:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnAutoAlreadyOn'], dictTValue)
                    else:
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'autoSnEnabled',
                            userConfigValue = True,
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_pc_id,
                            userType = 'user',
                            platform = tmp_pc_platform
                        )
                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                            userHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_pc_id,
                                userType = 'user',
                                platform = tmp_pc_platform
                            )
                        )
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnAutoOn'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                elif isMatchWordStart(tmp_reast_str, 'off', fullMatch = True):
                    # sn auto off 命令
                    if not auto_sn_enabled:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnAutoAlreadyOff'], dictTValue)
                    else:
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'autoSnEnabled',
                            userConfigValue = False,
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_pc_id,
                            userType = 'user',
                            platform = tmp_pc_platform
                        )
                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                            userHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_pc_id,
                                userType = 'user',
                                platform = tmp_pc_platform
                            )
                        )
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnAutoOff'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                else:
                    # 原有逻辑
                    new_auto_sn_enabled = not auto_sn_enabled
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userConfigKey = 'autoSnEnabled',
                        userConfigValue = new_auto_sn_enabled,
                        botHash = plugin_event.bot_info.hash,
                        userId = tmp_pc_id,
                        userType = 'user',
                        platform = tmp_pc_platform
                    )
                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                        userHash = OlivaDiceCore.userConfig.getUserHash(
                            userId = tmp_pc_id,
                            userType = 'user',
                            platform = tmp_pc_platform
                        )
                    )
                    if new_auto_sn_enabled:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnAutoOn'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnAutoOff'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
            if '' == tmp_reast_str.lower():
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                if 'snTitle' in tmp_template:
                    tmp_pc_card_snTitle = tmp_template['snTitle']
                    flag_mode = 'template'
                    flag_force = False
                else:
                    flag_mode = 'coc'
                    flag_force = False
            elif tmp_reast_str.lower() in ['dnd', 'dnd5e']:
                flag_mode = 'dnd'
            elif tmp_reast_str.lower() in ['coc', 'coc6', 'coc7']:
                flag_mode = 'coc'
            elif tmp_reast_str.lower() in ['default','template']:
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                if 'snTitle' in tmp_template:
                    tmp_pc_card_snTitle = tmp_template['snTitle']
                else:
                    tmp_pc_card_snTitle = '{tName} hp{HP}/{HPMAX} san{SAN}/{SANMAX} dex{DEX}'
                flag_mode = 'template'
            else:
                flag_mode = 'custom'
                sn_title_new = tmp_reast_str
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
                elif 'template' == flag_mode:
                    sn_title = tmp_pc_card_snTitle
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
                    user_id = tmp_pc_id,
                    card = sn_title,
                    host_id = plugin_event.data.host_id
                )
                dictTValue['tResult'] = sn_title
                if is_at:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnSetAtOther'], dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnSet'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            else:
                if is_at:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnPcCardNoneAtOther'], dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSnPcCardNone'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, ['st','pc'], isCommand = True):
            tmp_reply_str = ''
            is_at, at_user_id, tmp_reast_str = parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin)
            if is_at:
                if not at_user_id:
                    return
                dictTValue['tName'] = dictTValue['tUserName01']
            tmp_pc_id = at_user_id if at_user_id else plugin_event.data.user_id
            tmp_pc_name = None
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_1 = ''
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['st','pc'])
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            forced_is_new_card = False
            forced_is_new_card_time = 0
            tmp_skill_name = None
            tmp_skill_value = None
            tmp_skill_name_find = None
            tmp_skill_value_find = 0
            tmp_skill_pair_list = []
            if isMatchWordStart(tmp_reast_str, 'show', fullMatch = True):
                is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                if is_new_card:
                    OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
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
                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    tmp_pcHash,
                    dictTValue['tName'],
                    'template',
                    'default'
                )
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                default_skill_values = tmp_template.get('defaultSkillValue', {}) if tmp_template else {}
                # 检查是否开启默认值显示模式
                show_default_enabled = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_pc_id,
                    userType = 'user',
                    platform = tmp_pc_platform,
                    userConfigKey = 'showDefault',
                    botHash = plugin_event.bot_info.hash,
                    default = False
                )
                # 保存原始数据用于标记比较
                tmp_dict_pc_card_original = tmp_dict_pc_card.copy()
                processed_core_skills = set()  # 用于去重别名技能
                for tmp_dict_pc_card_key in tmp_dict_pc_card:
                    skill_value = tmp_dict_pc_card[tmp_dict_pc_card_key]
                    # 获取技能的核心名称用于去重检查
                    core_skill_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                        tmp_pcHash,
                        tmp_dict_pc_card_key,
                        hagId = tmp_hagID
                    )
                    # 如果这个核心技能已经处理过，跳过（去重别名）
                    if core_skill_name in processed_core_skills:
                        continue
                    processed_core_skills.add(core_skill_name)
                    
                    # 尝试用原始技能名获取默认值，如果没找到再用核心技能名
                    default_value = default_skill_values.get(tmp_dict_pc_card_key, 
                                   default_skill_values.get(core_skill_name, 0))
                    
                    if show_default_enabled:
                        # 默认值显示模式：只显示非默认值的技能
                        if skill_value == default_value:
                            continue  # 跳过等于默认值的技能
                        display_value = skill_value
                    else:
                        # 正常模式：跳过值为0且与默认值相同的技能
                        if skill_value == 0:
                            if skill_value == default_value:
                                continue
                        display_value = skill_value
                    tmp_dict_pc_card_dump[
                        OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                            tmp_pcHash,
                            tmp_dict_pc_card_key,
                            flagShow = True,
                            hagId = tmp_hagID
                        )
                    ] = display_value
                tmp_reply_str_1_list = []
                tmp_reply_str_1_dict = {}
                tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    tmp_pcHash,
                    dictTValue['tName'],
                    'enhanceList',
                    []
                )                
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
                    # 确定技能属于哪个分组
                    for tmp_skill_dict_this in tmp_skill_dict:
                        if type(tmp_skill_dict[tmp_skill_dict_this]) == list:
                            if tmp_dict_pc_card_key_core in tmp_skill_dict[tmp_skill_dict_this]:
                                flag_hit_skill_list_name = tmp_skill_dict_this
                                break
                    # 检查标记条件
                    is_enhanced = tmp_dict_pc_card_key_core in tmp_enhanceList
                    is_non_default = False
                    # 对非"其它"分组的技能，检查是否与默认值不同（仅在非默认值显示模式下）
                    if (not show_default_enabled and 
                        flag_hit_skill_list_name != flag_hit_skill_list_name_default):
                        # 使用原始值而不是显示值进行比较，与前面逻辑保持一致的默认值获取方式
                        original_value = tmp_dict_pc_card_original[tmp_dict_pc_card_key]
                        # 寻找对应的原始技能键来获取默认值
                        original_skill_key = None
                        for orig_key in tmp_dict_pc_card_original:
                            if OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(tmp_pcHash, orig_key, hagId=tmp_hagID) == tmp_dict_pc_card_key_core:
                                original_skill_key = orig_key
                                break
                        if original_skill_key:
                            default_value = default_skill_values.get(original_skill_key, 
                                           default_skill_values.get(tmp_dict_pc_card_key_core, 0))
                        else:
                            default_value = default_skill_values.get(tmp_dict_pc_card_key_core, 0)
                        if original_value != default_value:
                            is_non_default = True
                    # 根据条件组合标记
                    if show_default_enabled:
                        # 默认值显示模式下只保留增强标记
                        if is_enhanced:
                            tmp_reply_str_1_list_this = '[*]' + tmp_reply_str_1_list_this
                    else:
                        # 正常模式下显示所有标记
                        if is_enhanced and is_non_default:
                            tmp_reply_str_1_list_this = '[*/+]' + tmp_reply_str_1_list_this
                        elif is_enhanced:
                            tmp_reply_str_1_list_this = '[*]' + tmp_reply_str_1_list_this
                        elif is_non_default:
                            tmp_reply_str_1_list_this = '[+]' + tmp_reply_str_1_list_this
                    if flag_hit_skill_list_name not in tmp_reply_str_1_dict:
                        tmp_reply_str_1_dict[flag_hit_skill_list_name] = []
                    tmp_reply_str_1_dict[flag_hit_skill_list_name].append(tmp_reply_str_1_list_this)
                # 对每个技能组内的技能按数值排序
                for tmp_reply_str_1_dict_this in tmp_reply_str_1_dict:
                    # 按数值大小排序（从大到小）
                    tmp_reply_str_1_dict[tmp_reply_str_1_dict_this].sort(
                        key=lambda x: int(x.split(':')[-1]) if x.split(':')[-1].replace('[*]', '').replace('[+]', '').replace('[*/+]', '').isdigit() else 0,
                        reverse=True
                    )
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
                # 根据defaultshow状态设置不同的说明文字
                if show_default_enabled:
                    dictTValue['tDefaultShow'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDefaultShowOn'], dictTValue)
                else:
                    dictTValue['tDefaultShow'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDefaultShowOff'], dictTValue)
                if is_at:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcShowAtOther'], dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcShow'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'show'):
                is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                if is_new_card:
                    OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'show')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pcCardRule = 'default'
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
                pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
                pc_skill_names = [s.upper() for s in pc_skills.keys() if not s.startswith('__')]
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
                tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                if tmp_pcCardRule_new:
                    tmp_pcCardRule = tmp_pcCardRule_new
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_pcCardRule)
                synonyms = tmp_template.get('synonyms', {}) if tmp_template else {}
                # 获取特殊技能并合并到普通技能列表
                special_skills = []
                if tmp_pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial:
                    special_skills = OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[tmp_pcCardRule]
                all_skills = pc_skill_names + special_skills
                if tmp_pc_name is None:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRmCardNone'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                elif not tmp_reast_str:
                    replyMsgLazyHelpByEvent(plugin_event, 'st')
                    return
                input_str = tmp_reast_str.strip().upper()
                # 按空格分割输入字符串
                input_parts = input_str.split()
                result_lines = []
                seen_skills = set() 
                for part in input_parts:
                    remaining_str = part.upper()
                    matched_skills = []
                    unmatched_groups = []
                    current_unmatched = []
                    skill_mapping = {}
                    # 构建技能映射表
                    for skill in all_skills:
                        main_skill = None
                        for main_key in synonyms:
                            if skill in synonyms[main_key]:
                                main_skill = main_key.upper()
                                break
                        skill_mapping[skill] = main_skill if main_skill else skill
                    while remaining_str:
                        matched = False
                        max_len = 0
                        matched_skill = None
                        # 按长度从长到短排序匹配
                        for skill in sorted(all_skills, key=len, reverse=True):
                            skill_upper = skill.upper()
                            skill_len = len(skill_upper)
                            if skill_len > len(remaining_str):
                                continue
                            if remaining_str.startswith(skill_upper):
                                matched_skill = skill_mapping[skill]
                                max_len = skill_len
                                matched = True
                                break
                        if matched:
                            if current_unmatched:
                                unmatched_groups.append(''.join(current_unmatched))
                                current_unmatched = []
                            # 检查是否已经添加过这个技能
                            if matched_skill not in seen_skills:
                                matched_skills.append((matched_skill, max_len, True))
                                seen_skills.add(matched_skill)
                            remaining_str = remaining_str[max_len:]
                        else:
                            current_unmatched.append(remaining_str[0])
                            remaining_str = remaining_str[1:]
                    if current_unmatched:
                        unmatched_groups.append(''.join(current_unmatched))
                    # 处理匹配到的技能
                    for skill, length, is_matched in matched_skills:
                        if is_matched:
                            if skill in special_skills and skill not in pc_skill_names:
                                skill_value = OlivaDiceCore.skillCheck.getSpecialSkill(
                                    skill,
                                    tmp_pcCardRule,
                                    pc_skills
                                )
                                if skill_value is None:
                                    skill_value = "0"
                            else:
                                skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                                    tmp_pcHash,
                                    skill,
                                    hagId = tmp_hagID
                                )
                            display_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                tmp_pcHash,
                                skill,
                                flagShow=True,
                                hagId=tmp_hagID
                            )
                            result_lines.append(f"[{display_name}]: {skill_value}")
                    # 处理未匹配的部分
                    for group in unmatched_groups:
                        display_name = group.upper()
                        if display_name not in seen_skills:
                            skill_value = '0'
                            result_lines.append(f"[{display_name}]: {skill_value}")
                            seen_skills.add(display_name)
                dictTValue['tName'] = tmp_pc_name
                dictTValue['tSkillName'] = input_str
                dictTValue['tSkillValue'] = '\n'.join(result_lines)
                # 根据匹配到的技能数量选择不同的回复模板
                total_skills = len(result_lines)
                if total_skills == 1:
                    dictTValue['tSkillName'] = display_name
                    dictTValue['tSkillValue'] = skill_value
                    if is_at:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetSingleSkillValueAtOther'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetSingleSkillValue'], dictTValue)
                else:
                    if is_at:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetMultiSkillValueAtOther'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetMultiSkillValue'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'list', fullMatch = True):
                if is_at: return
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
                if is_at: return
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
                if is_at: return
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
                if is_at: return
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
                    is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                    if is_new_card:
                        OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'init'):
                if is_at: return
                is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                if is_new_card:
                    OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
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
                trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
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
                        OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event)
                        dictTValue['tPcSelection'] = tmp_pc_name
                        if is_at:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcNewAtOther'], dictTValue)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcNew'], dictTValue)
                        trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'del'):
                if is_at: return
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
                trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, ['defaultshow','ds'], isCommand = True):
                if is_at: return
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['defaultshow','ds'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                current_show_default = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_pc_id,
                    userType = 'user',
                    platform = tmp_pc_platform,
                    userConfigKey = 'showDefault',
                    botHash = plugin_event.bot_info.hash,
                    default = False
                )
                if isMatchWordStart(tmp_reast_str, 'on', fullMatch = True):
                    # defaultshow on 命令
                    if current_show_default:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowDefaultAlreadyOn'], dictTValue)
                    else:
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'showDefault',
                            userConfigValue = True,
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_pc_id,
                            userType = 'user',
                            platform = tmp_pc_platform
                        )
                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                            userHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_pc_id,
                                userType = 'user',
                                platform = tmp_pc_platform
                            )
                        )
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowDefaultOn'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                elif isMatchWordStart(tmp_reast_str, 'off', fullMatch = True):
                    # defaultshow off 命令
                    if not current_show_default:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowDefaultAlreadyOff'], dictTValue)
                    else:
                        OlivaDiceCore.userConfig.setUserConfigByKey(
                            userConfigKey = 'showDefault',
                            userConfigValue = False,
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_pc_id,
                            userType = 'user',
                            platform = tmp_pc_platform
                        )
                        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                            userHash = OlivaDiceCore.userConfig.getUserHash(
                                userId = tmp_pc_id,
                                userType = 'user',
                                platform = tmp_pc_platform
                            )
                        )
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowDefaultOff'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                else:
                    # 切换模式
                    new_show_default = not current_show_default
                    OlivaDiceCore.userConfig.setUserConfigByKey(
                        userConfigKey = 'showDefault',
                        userConfigValue = new_show_default,
                        botHash = plugin_event.bot_info.hash,
                        userId = tmp_pc_id,
                        userType = 'user',
                        platform = tmp_pc_platform
                    )
                    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
                        userHash = OlivaDiceCore.userConfig.getUserHash(
                            userId = tmp_pc_id,
                            userType = 'user',
                            platform = tmp_pc_platform
                        )
                    )
                    if new_show_default:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowDefaultOn'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowDefaultOff'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
            elif isMatchWordStart(tmp_reast_str, ['clear', 'clr'], fullMatch = True):
                if is_at: return
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['clear', 'clr'])
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
                OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'rm'):
                if is_at: return
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
                # 获取模板信息
                tmp_pcCardRule = 'default'
                tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                if tmp_pcCardRule_new:
                    tmp_pcCardRule = tmp_pcCardRule_new
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_pcCardRule)
                synonyms = tmp_template.get('synonyms', {}) if tmp_template else {}
                # 获取所有skill
                all_skills = []
                if tmp_pc_name is not None:
                    skill_dict = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, tmp_hagID)
                    all_skills = [s.upper() for s in skill_dict.keys() if not s.startswith('__')]
                input_str = tmp_reast_str.strip().upper()
                if tmp_pc_name is None:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRmCardNone'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                elif not input_str:
                    replyMsgLazyHelpByEvent(plugin_event, 'st')
                    return
                else:
                    # 按空格分割输入字符串
                    input_parts = input_str.split()
                    removed_skills = []
                    failed_skills = []
                    seen_skills = set()
                    for part in input_parts:
                        remaining_str = part.upper()
                        matched_skills = []
                        current_unmatched = []
                        skill_mapping = {}
                        # 构建技能映射表
                        for skill in all_skills:
                            main_skill = None
                            for main_key in synonyms:
                                if skill in synonyms[main_key]:
                                    main_skill = main_key.upper()
                                    break
                            skill_mapping[skill] = main_skill if main_skill else skill
                        while remaining_str:
                            matched = False
                            max_len = 0
                            matched_skill = None
                            # 按长度从长到短排序匹配
                            for skill in sorted(all_skills, key=len, reverse=True):
                                skill_upper = skill.upper()
                                skill_len = len(skill_upper)
                                if skill_len > len(remaining_str):
                                    continue
                                if remaining_str.startswith(skill_upper):
                                    matched_skill = skill_mapping[skill]
                                    max_len = skill_len
                                    matched = True
                                    break
                            if matched:
                                if current_unmatched:
                                    failed_skills.append(''.join(current_unmatched))
                                    current_unmatched = []
                                # 检查是否已经添加过这个技能
                                if matched_skill not in seen_skills:
                                    matched_skills.append((matched_skill, max_len, True))
                                    seen_skills.add(matched_skill)
                                remaining_str = remaining_str[max_len:]
                            else:
                                current_unmatched.append(remaining_str[0])
                                remaining_str = remaining_str[1:]
                        if current_unmatched:
                            failed_skills.append(''.join(current_unmatched))
                        # 处理匹配到的技能
                        for skill, length, is_matched in matched_skills:
                            if is_matched:
                                removed_skills.append(skill)
                                OlivaDiceCore.pcCard.pcCardDataDelBySkillName(
                                    tmp_pcHash,
                                    skill,
                                    tmp_pc_name
                                )
                                tmp_enhanceList_new = []
                                tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                                    tmp_pcHash,
                                    tmp_pc_name,
                                    'enhanceList',
                                    []
                                )
                                for tmp_enhanceList_this in tmp_enhanceList:
                                    if skill != tmp_enhanceList_this.upper():
                                        tmp_enhanceList_new.append(tmp_enhanceList_this)
                                OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                                    tmp_pcHash,
                                    tmp_pc_name,
                                    'enhanceList',
                                    tmp_enhanceList_new
                                )
                                # 从all_skills中移除
                                if skill in all_skills:
                                    all_skills.remove(skill)
                    if removed_skills:
                        dictTValue['tLenSkillName'] = len(removed_skills)
                    if failed_skills:
                        dictTValue['tLenFailedSkills'] = len(failed_skills)

                    dictTValue['tPcSelection'] = tmp_pc_name
                    if removed_skills and failed_skills:
                        # 有成功有失败
                        dictTValue['tSkillName'] = '、'.join([f'[{skill}]' for skill in removed_skills])
                        dictTValue['tFailedSkills'] = '、'.join([f'[{skill}]' for skill in failed_skills])
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strPcRmPartialSuccess'], 
                            dictTValue
                        )
                    elif removed_skills:
                        # 有成功无失败
                        dictTValue['tSkillName'] = '、'.join([f'[{skill}]' for skill in removed_skills])
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strPcRm'], 
                            dictTValue
                        )
                    else:
                        # 无成功有失败
                        dictTValue['tFailedSkills'] = '、'.join([f'[{skill}]' for skill in failed_skills])
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strPcRmNone'], 
                            dictTValue
                        )
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                    if is_new_card:
                        OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
            elif isMatchWordStart(tmp_reast_str, 'temp'):
                if is_at: return
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
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
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
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'rule'):
                if is_at: return
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
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
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
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, ['note', 'rec']):
                if is_at: return
                flag_mode = 'note'
                keyName = 'noteRecord'
                is_remove = False
                if isMatchWordStart(tmp_reast_str, 'note'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'note')
                    flag_mode = 'note'
                    keyName = 'noteRecord'
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    if isMatchWordStart(tmp_reast_str, 'rm'):
                        is_remove = True
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rm')
                elif isMatchWordStart(tmp_reast_str, 'rec'):
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rec')
                    flag_mode = 'rec'
                    keyName = 'mappingRecord'
                    tmp_reast_str = skipSpaceStart(tmp_reast_str)
                    if isMatchWordStart(tmp_reast_str, 'rm'):
                        is_remove = True
                        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rm')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_reast_str_original = tmp_reast_str
                # 根据模式决定是否对字符串进行大写处理
                if flag_mode == 'rec':
                    tmp_reast_str = tmp_reast_str.upper()
                tmp_key = None
                tmp_value = None
                tmp_reast_str_list = tmp_reast_str.split(' ')
                tmp_reast_str_list = [tmp_reast_str_list_this for tmp_reast_str_list_this in tmp_reast_str_list if tmp_reast_str_list_this != '']
                # 使用原始字符串列表来提取值（保持原始大小写）
                tmp_reast_str_list_original = tmp_reast_str_original.split(' ')
                tmp_reast_str_list_original = [tmp_reast_str_list_this for tmp_reast_str_list_this in tmp_reast_str_list_original if tmp_reast_str_list_this != '']
                
                if len(tmp_reast_str_list) > 0:
                    tmp_key = tmp_reast_str_list[0]
                    tmp_key = OlivaDiceCore.pcCard.fixName(tmp_key)
                    # 如果是删除操作，不需要value
                    if is_remove:
                        if flag_mode == 'note':
                            tmp_value = None
                        elif flag_mode == 'rec':
                            tmp_value = None
                    else:
                        if flag_mode == 'note':
                            # note 模式：使用原始字符串保持大小写
                            if len(tmp_reast_str_list_original) > 1:
                                tmp_value = ' '.join(tmp_reast_str_list_original[1:])
                        elif flag_mode == 'rec':
                            # rec 模式：强制大写
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
                    enableFalse = True,
                    is_remove = is_remove
                )
                return
            elif isMatchWordStart(tmp_reast_str, 'blockrm'):
                if is_at: return
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'blockrm')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_block_name = tmp_reast_str.strip()
                if not tmp_block_name:
                    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
                    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
                    if tmp_pc_name is None:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRmCardNone'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        return
                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                    tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name or 'default')
                    pc_data = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
                    block_list = []
                    template_blocks = {}
                    # 处理模板定义的块
                    if 'skill' in tmp_template:
                        for block_name in tmp_template['skill']:
                            if isinstance(tmp_template['skill'][block_name], list):
                                has_skill = False
                                block_skills = []
                                for skill_name in tmp_template['skill'][block_name]:
                                    skill_core_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                        tmp_pcHash, skill_name, hagId=tmp_hagID)
                                    if skill_core_name in pc_data:
                                        has_skill = True
                                        block_skills.append(skill_core_name)

                                if has_skill:
                                    block_list.append(block_name)
                                    template_blocks[block_name] = block_skills
                    # 检查并添加有内容的固定块
                    mapping_record = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash, tmp_pc_name, 'mappingRecord', {})
                    if mapping_record:
                        block_list.append('映射')

                    note_record = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash, tmp_pc_name, 'noteRecord', {})
                    if note_record:
                        block_list.append('记录')
                    # 检查是否有"其它"内容
                    tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash, tmp_pc_name, 'enhanceList', [])
                    has_other = False
                    all_template_skills = set()
                    for block_skills in template_blocks.values():
                        all_template_skills.update(block_skills)
                    for skill_key in pc_data:
                        if skill_key.startswith('__') or skill_key == 'template':
                            continue
                        skill_core_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                            tmp_pcHash, skill_key, hagId=tmp_hagID)
                        if skill_core_name not in all_template_skills:
                            has_other = True
                            break
                    if has_other:
                        block_list.append('其它')
                    if block_list:
                        dictTValue['tBlockList'] = '\n'.join([f'- {block}' for block in block_list])
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcBlockList'], dictTValue)
                    else:
                        dictTValue['tBlockList'] = "无技能块"
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcBlockList'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
                if tmp_pc_name is None:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRmCardNone'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name or 'default')
                pc_data = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
                deleted = False
                tmp_block_name = tmp_block_name.strip()
                # 处理映射块
                if tmp_block_name == '映射':
                    mapping_record = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash, tmp_pc_name, 'mappingRecord', {})
                    if mapping_record:
                        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                            tmp_pcHash, tmp_pc_name, 'mappingRecord', {})
                        deleted = True
                # 处理记录块
                elif tmp_block_name == '记录':
                    note_record = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash, tmp_pc_name, 'noteRecord', {})
                    if note_record:
                        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                            tmp_pcHash, tmp_pc_name, 'noteRecord', {})
                        deleted = True
                        trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                # 处理其它块
                elif tmp_block_name in ['其它','其他']:
                    all_template_skills = set()
                    if 'skill' in tmp_template:
                        for block_name in tmp_template['skill']:
                            if isinstance(tmp_template['skill'][block_name], list):
                                for skill_name in tmp_template['skill'][block_name]:
                                    skill_core_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                        tmp_pcHash, skill_name, hagId=tmp_hagID)
                                    all_template_skills.add(skill_core_name)
                    other_skills = []
                    for skill_key in pc_data:
                        if skill_key.startswith('__') or skill_key == 'template':
                            continue
                        skill_core_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                            tmp_pcHash, skill_key, hagId=tmp_hagID)
                        if skill_core_name not in all_template_skills:
                            other_skills.append(skill_key)
                    if other_skills:
                        for skill_name in other_skills:
                            OlivaDiceCore.pcCard.pcCardDataDelBySkillName(
                                tmp_pcHash, skill_name, tmp_pc_name)
                        deleted = True
                # 处理模板定义的块
                elif 'skill' in tmp_template and tmp_block_name in tmp_template['skill']:
                    if isinstance(tmp_template['skill'][tmp_block_name], list):
                        skills_to_delete = []
                        for skill_name in tmp_template['skill'][tmp_block_name]:
                            skill_core_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                tmp_pcHash, skill_name, hagId=tmp_hagID)
                            if skill_core_name in pc_data:
                                skills_to_delete.append(skill_core_name)
                        if skills_to_delete:
                            for skill_name in skills_to_delete:
                                OlivaDiceCore.pcCard.pcCardDataDelBySkillName(
                                    tmp_pcHash, skill_name, tmp_pc_name)
                            deleted = True
                if deleted:
                    dictTValue['tBlockName'] = tmp_block_name
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcBlockRm'], dictTValue)
                else:
                    dictTValue['tBlockName'] = tmp_block_name
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcBlockRmNone'], dictTValue)
                is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                if is_new_card:
                    OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                replyMsg(plugin_event, tmp_reply_str)
                return
            elif isMatchWordStart(tmp_reast_str, 'export'):
                if is_at: return
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'export')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                tmp_pc_name = tmp_reast_str.strip()
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                # 没有指定人物卡，使用当前人物卡
                if not tmp_pc_name:
                    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                        tmp_pcHash,
                        tmp_hagID
                    )
                if not tmp_pc_name:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcExportCardNone'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                tmp_dict_pc_card = OlivaDiceCore.pcCard.pcCardDataGetUserAll(tmp_pcHash).get(tmp_pc_name, {})
                if not tmp_dict_pc_card:
                    dictTValue['tPcInputCard'] = tmp_pc_name
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strNoPcInputCard'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name or 'default')
                # 获取模板默认值
                default_skill_values = tmp_template.get('defaultSkillValue', {}) if tmp_template else {}
                primary_skills = set()
                if 'synonyms' in tmp_template:
                    primary_skills.update(tmp_template['synonyms'].keys())
                skill_pairs = []
                processed_skills = set()
                for skill_key in tmp_dict_pc_card:
                    if skill_key.startswith('__') or skill_key == 'template':
                        continue
                    # 跳过以数字结尾的技能名
                    if skill_key[-1].isdigit():
                        continue
                    skill_value = tmp_dict_pc_card[skill_key]
                    # 跳过值为0且与默认值相同的技能
                    if skill_value == 0:
                        default_value = default_skill_values.get(skill_key, 0)
                        if skill_value == default_value:
                            continue
                    # 主技能
                    if skill_key in primary_skills:
                        if skill_key not in processed_skills:
                            skill_pairs.append(f"{skill_key}{skill_value}")
                            processed_skills.add(skill_key)
                    # 别名处理
                    else:
                        is_alias = False
                        for main_key in primary_skills:
                            if skill_key in tmp_template['synonyms'].get(main_key, []):
                                if main_key not in processed_skills:
                                    skill_pairs.append(f"{main_key}{skill_value}")
                                    processed_skills.add(main_key)
                                is_alias = True
                                break
                        # 其它技能
                        if not is_alias and skill_key not in processed_skills:
                            skill_pairs.append(f"{skill_key}{skill_value}")
                            processed_skills.add(skill_key)
                export_lines = []
                # 添加技能导出
                if skill_pairs:
                    export_lines.append(f".st {tmp_pc_name}-" + "".join(skill_pairs))
                # 添加映射导出
                tmp_mappingRecord = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    pcHash = tmp_pcHash,
                    pcCardName = tmp_pc_name,
                    dataKey = 'mappingRecord',
                    resDefault = {}
                )
                for mapping_name, mapping_expr in tmp_mappingRecord.items():
                    export_lines.append(f".st &{mapping_name}={mapping_expr}")
                # 添加记录导出
                tmp_noteRecord = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    pcHash = tmp_pcHash,
                    pcCardName = tmp_pc_name,
                    dataKey = 'noteRecord',
                    resDefault = {}
                )
                for note_name, note_value in tmp_noteRecord.items():
                    export_lines.append(f".st note {note_name} {note_value}")
                if not export_lines:
                    dictTValue['tPcInputCard'] = tmp_pc_name
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcCardNoSkill'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                export_str = '\n'.join(export_lines)
                dictTValue['tPcInputCard'] = tmp_pc_name
                dictTValue['tExport'] = export_str
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcCardExport'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            tmp_reast_str_new = tmp_reast_str
            tmp_reast_str_new_2 = tmp_reast_str
            if len(tmp_reast_str_new) > 0:
                # 支持连续多个技能更新
                tmp_skill_updates = []
                reply_messages = []
                special_skills = []
                op_list = OlivaDiceCore.msgReplyModel.op_list_get()
                assign_op = '='
                is_pass = False
                # 检查是否需要跳过
                if not any(op in tmp_reast_str_new for op in op_list) or tmp_reast_str_new.startswith('&'):
                    is_pass = True
                # 检查是否是录卡格式（字符串-字符串）
                dash_pos = tmp_reast_str_new.find('-')
                if dash_pos > 0:
                    rest_after_dash = tmp_reast_str_new[dash_pos+1:].strip()
                    card_name = tmp_reast_str_new[:dash_pos].strip()
                    # 录卡格式判断 - 只有当后面跟着非数字、非运算符、非d且不是表达式时才跳过
                    if rest_after_dash and not (rest_after_dash[0].isdigit() or rest_after_dash[0] in op_list + [assign_op] or 
                                              (len(rest_after_dash) > 1 and rest_after_dash[0].upper() == 'D' and rest_after_dash[1].isdigit())):
                        is_pass = True
                        # 检查人物卡是否存在
                        tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
                        existing_cards = OlivaDiceCore.pcCard.pcCardDataGetUserAll(tmp_pcHash)
                        # 如果人物卡不存在或者是空的，才设置forced_is_new_card为True
                        if card_name not in existing_cards or not existing_cards[card_name]:
                            forced_is_new_card = True
                if is_pass:
                    pass
                else:
                    # 获取当前人物卡的所有技能名
                    tmp_pc_id = at_user_id if at_user_id else plugin_event.data.user_id
                    tmp_pc_platform = plugin_event.platform['platform']
                    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
                    is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                    if is_new_card:
                        OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                    pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
                    pc_skill_names = [s.upper() for s in pc_skills.keys() if not s.startswith('__')]
                    # 预处理字符串，在特定字母先查找技能名，找到技能名后添加空格
                    processed_str = tmp_reast_str_new
                    start_chars = {c.upper() for c in OlivaDiceCore.pcCardData.arrPcCardLetterStart}
                    sorted_skills = sorted(pc_skill_names, key=len, reverse=True)
                    i = 0
                    while i < len(processed_str):
                        char = processed_str[i].upper()
                        if char in start_chars:
                            for skill in sorted_skills:
                                if skill[0].upper() == char and processed_str[i:].upper().startswith(skill):
                                    if char == 'D' and len(skill) == 1 and i+1 < len(processed_str) and processed_str[i+1].isdigit():
                                        continue  # 跳过d后面跟着数字的情况
                                    # 在匹配的技能名前添加空格
                                    processed_str = processed_str[:i] + ' ' + processed_str[i:]
                                    i += len(skill) + 1
                                    break
                            else:
                                i += 1
                        else:
                            i += 1
                    current_pos = 0
                    while current_pos < len(processed_str):
                        # 查找技能名结束位置（遇到符号或数字）
                        skill_end_pos = -1
                        for i in range(current_pos, len(processed_str)):
                            if processed_str[i] in op_list + [assign_op] or processed_str[i].isdigit():
                                skill_end_pos = i
                                break
                        if skill_end_pos == -1:
                            break  # 没有找到符号或数字，结束解析
                        # 处理技能名和表达式
                        if processed_str[skill_end_pos].isdigit() or processed_str[skill_end_pos] in op_list:
                            # 检查是否是d后面跟着数字的情况
                            tmp_skill_name_part = processed_str[current_pos:skill_end_pos].strip()
                            if (tmp_skill_name_part.upper() == 'D' and 
                                skill_end_pos < len(processed_str) and 
                                processed_str[skill_end_pos].isdigit()):
                                current_pos = skill_end_pos  # 跳过这个d，不视为技能名
                                continue
                            # 查找完整的表达式
                            expr_end_pos = skill_end_pos
                            in_dice_expr = False
                            while expr_end_pos < len(processed_str):
                                char = processed_str[expr_end_pos]
                                if char.upper() == 'D':
                                    in_dice_expr = True
                                    expr_end_pos += 1
                                    continue
                                if char.isdigit() or (in_dice_expr and char in op_list) or char in op_list + [assign_op]:
                                    expr_end_pos += 1
                                else:
                                    break
                                
                            tmp_skill_name = processed_str[current_pos:skill_end_pos].strip()
                            tmp_skill_value = processed_str[skill_end_pos:expr_end_pos].strip()
                            # 自动补 = 如果没有运算符
                            if tmp_skill_value[0].isdigit() or tmp_skill_value[0].upper() == 'D':
                                tmp_skill_value = '=' + tmp_skill_value
                            if tmp_skill_name:
                                tmp_skill_updates.append([tmp_skill_name, tmp_skill_value])
                            current_pos = expr_end_pos
                        else:
                            current_pos = skill_end_pos + 1
                    # 对这些算式进行计算
                    for tmp_skill_name, tmp_skill_value in tmp_skill_updates:
                        if not tmp_skill_name:
                            continue
                        
                        tmp_skill_name = tmp_skill_name.strip()
                        # 移除技能名末尾的分隔符 = : ：
                        if tmp_skill_name and tmp_skill_name[-1] in ['=', ':', '：']:
                            tmp_skill_name = tmp_skill_name[:-1]
                        tmp_skill_name = OlivaDiceCore.pcCard.fixName(tmp_skill_name, flagMode = 'skillName')
                        if not OlivaDiceCore.pcCard.checkPcName(tmp_skill_name):
                            continue
                        
                        tmp_skill_name = tmp_skill_name.upper()
                        tmp_pc_id = at_user_id if at_user_id else plugin_event.data.user_id
                        tmp_pc_platform = plugin_event.platform['platform']
                        tmp_skill_value_old = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                            OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                            tmp_skill_name,
                            hagId=tmp_hagID
                        )
                        tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                            OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                            tmp_hagID
                        )
                        if tmp_pc_name_1:
                            dictTValue['tName'] = tmp_pc_name_1
                        # 添加特殊技能检测提示
                        tmp_pcCardRule = 'default'
                        if tmp_pc_name_1 is not None:
                            tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                                OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                                tmp_pc_name_1
                            )
                            if tmp_pcCardRule_new:
                                tmp_pcCardRule = tmp_pcCardRule_new
                        if tmp_pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial:
                            # 检查当前技能是否在特殊技能列表中
                            if tmp_skill_name in [skill for skill in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[tmp_pcCardRule]]:
                                special_skills.append(tmp_skill_name)
                        if tmp_skill_value:
                            # 处理直接赋值的情况
                            if tmp_skill_value.startswith('='):
                                tmp_skill_value_new = tmp_skill_value[1:].strip()
                                # 检查是否是骰子表达式或算式
                                if 'D' in tmp_skill_value_new.upper() or any(op in tmp_skill_value_new for op in op_list):
                                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                                        OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                                        dictTValue.get('tName', '')
                                    )
                                    tmp_template_customDefault = None
                                    if tmp_template_name:
                                        tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                                        if 'customDefault' in tmp_template:
                                            tmp_template_customDefault = tmp_template['customDefault']

                                    rd_para = OlivaDiceCore.onedice.RD(tmp_skill_value_new, tmp_template_customDefault)
                                    rd_para.roll()
                                    if rd_para.resError is None:
                                        tmp_original_str = tmp_skill_value_new
                                        tmp_skill_value_new = rd_para.resInt
                                        # 显示详细计算过程
                                        if "D" in tmp_original_str.upper():
                                            update_msg = f"[{tmp_skill_name}]: {tmp_skill_value_old} -> {tmp_skill_value_new} ({tmp_original_str}={rd_para.resDetail})"
                                        else:
                                            update_msg = f"[{tmp_skill_name}]: {tmp_skill_value_old} -> {tmp_skill_value_new} ({tmp_original_str})"
                                        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                            OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                                            tmp_skill_name,
                                            tmp_skill_value_new,
                                            dictTValue.get('tName', ''),
                                            hagId=tmp_hagID
                                        )
                                        reply_messages.append(update_msg)
                                    else:
                                        reply_messages.append(f"[{tmp_skill_name}]: 表达式错误 '{tmp_skill_value_new}'")
                                else:
                                    # 普通数字赋值
                                    if tmp_skill_value_new.isdigit():
                                        tmp_skill_value_new = int(tmp_skill_value_new)
                                        update_msg = f"[{tmp_skill_name}]: {tmp_skill_value_old} -> {tmp_skill_value_new}"
                                        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                            OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                                            tmp_skill_name,
                                            tmp_skill_value_new,
                                            dictTValue.get('tName', ''),
                                            hagId=tmp_hagID
                                        )
                                        reply_messages.append(update_msg)
                                    else:
                                        reply_messages.append(f"[{tmp_skill_name}]: 无效数值 '{tmp_skill_value_new}'")
                            else:
                                # 处理运算表达式
                                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                                    OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                                    dictTValue.get('tName', '')
                                )
                                tmp_template_customDefault = None
                                if tmp_template_name:
                                    tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                                    if 'customDefault' in tmp_template:
                                        tmp_template_customDefault = tmp_template['customDefault']
                                rd_para_str = str(tmp_skill_value_old) + tmp_skill_value
                                rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault)
                                rd_para.roll()
                                if rd_para.resError is None:
                                    tmp_skill_value_new = rd_para.resInt
                                    # 显示详细计算过程
                                    if 'D' in tmp_skill_value.upper():
                                        update_msg = f"[{tmp_skill_name}]: {tmp_skill_value_old}{tmp_skill_value}={rd_para.resDetail}={tmp_skill_value_new}"
                                    else:
                                        update_msg = f"[{tmp_skill_name}]: {tmp_skill_value_old}{tmp_skill_value}={tmp_skill_value_new}"
                                    OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                        OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                                        tmp_skill_name,
                                        tmp_skill_value_new,
                                        dictTValue.get('tName', ''),
                                        hagId=tmp_hagID
                                    )
                                    reply_messages.append(update_msg)
                                else:
                                    reply_messages.append(f"[{tmp_skill_name}]: 表达式错误 '{tmp_skill_value}'")
                        else:
                            # 不符合所有条件的直接记录
                            reply_messages.append(f"[{tmp_skill_name}]: {tmp_skill_value_old}")
                    if reply_messages:
                        if special_skills:
                            dictTValue['tSpecialSkills'] = '、'.join([f'[{skill}]' for skill in special_skills])
                            tmp_notice = OlivaDiceCore.msgCustomManager.formatReplySTR(
                                dictStrCustom['strPcSetSpecialSkills'], dictTValue
                            )
                        else:
                            tmp_notice = ''
                        if is_at:
                            dictTValue['tSkillUpdate'] = '\n'.join(reply_messages)
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                                dictStrCustom['strPcUpdateSkillValueAtOther'], dictTValue
                            )
                        else:
                            dictTValue['tSkillUpdate'] = '\n'.join(reply_messages)
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                                dictStrCustom['strPcUpdateSkillValue'], dictTValue
                            )
                        trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                        replyMsg(plugin_event, tmp_reply_str + tmp_notice)
                    return
                tmp_skill_name = None
                tmp_skill_value = None
            if len(tmp_reast_str) > 0:
                # 在这里判断映射，不在后面判断，防止录卡格式判断影响映射
                flag_is_mapping = False
                if tmp_reast_str[0] in ['&']:
                    flag_is_mapping = True
                special_skills = []
                tmp_reast_str_bak = tmp_reast_str
                if not flag_is_mapping:
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
                # 前面判断过映射了，这里不需要再判断了，并且通过 break 能跳出循环，不影响
                if flag_is_mapping:
                    # 支持 = : ： 三种分隔符
                    tmp_reast_str_list_0 = None
                    used_separator = None
                    for separator in ['=', ':', '：']:
                        if separator in tmp_reast_str:
                            tmp_reast_str_list_0 = tmp_reast_str.split(separator)
                            used_separator = separator
                            break
                    if tmp_reast_str_list_0 and len(tmp_reast_str_list_0) > 1:
                        tmp_skill_name = tmp_reast_str_list_0[0][1:].upper()
                        tmp_reast_str = used_separator.join(tmp_reast_str_list_0[1:])
                        # # 不进行表达式解析，故这里注释掉
                        # if len(tmp_reast_str) > 0:
                        #     [tmp_skill_value, tmp_reast_str] = getExpression(tmp_reast_str)
                        #     tmp_reast_str = skipSpaceStart(tmp_reast_str)
                        tmp_skill_value = tmp_reast_str
                        if len(tmp_reast_str) > 0:
                            tmp_skill_pair_list.append([tmp_skill_name, tmp_skill_value])
                        else:
                            tmp_skill_name_find = tmp_skill_name
                        break
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
                    # 先判断负数，再判断赋值
                    if tmp_skill_name[-1] == '-':
                        if not flag_is_mapping:
                            tmp_skill_name = tmp_skill_name[:-1]
                            tmp_skill_value = -int(tmp_skill_value)
                    if tmp_skill_name[-1] in ['=', ':', '：']:
                        if not flag_is_mapping:
                            tmp_skill_name = tmp_skill_name[:-1]
                    tmp_skill_name = OlivaDiceCore.pcCard.fixName(tmp_skill_name)
                    tmp_skill_name = tmp_skill_name.upper()
                    # 添加特殊技能检测提示
                    tmp_pcCardRule = 'default'
                    if tmp_pc_name_1 is not None:
                        tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                            OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                            tmp_pc_name_1
                        )
                        if tmp_pcCardRule_new:
                            tmp_pcCardRule = tmp_pcCardRule_new
                    if tmp_pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial:
                        if tmp_skill_name in [skill for skill in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[tmp_pcCardRule]]:
                            special_skills.append(tmp_skill_name)
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
                        if forced_is_new_card and forced_is_new_card_time == 0:
                            forced_is_new_card_time = 1
                            # 先创建新的人物卡
                            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
                            OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                                tmp_pcHash,
                                '__new',
                                0,
                                dictTValue['tName'],
                                hagId = tmp_hagID
                            )
                            OlivaDiceCore.pcCard.pcCardDataDelBySkillName(
                                tmp_pcHash,
                                '__new',
                                dictTValue['tName']
                            )
                            # 再更改模板
                            OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id, dictTValue['tName'])
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
                    if special_skills:
                        dictTValue['tSpecialSkills'] = '、'.join([f'[{skill}]' for skill in special_skills])
                        tmp_notice = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strPcSetSpecialSkills'], dictTValue
                        )
                    else:
                        tmp_notice = ''
                    if is_at:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetSkillValueAtOther'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetSkillValue'], dictTValue)
                    trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    replyMsg(plugin_event, tmp_reply_str + tmp_notice)
                    return
            else:
                tmp_pcCardRule = 'default'
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
                is_new_card = OlivaDiceCore.pcCard.isNewPcCard(plugin_event, tmp_pc_id)
                if is_new_card:
                    OlivaDiceCore.pcCard.setPcTemplateByGroupRule(plugin_event, tmp_pc_id)
                pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
                pc_skill_names = [s.upper() for s in pc_skills.keys() if not s.startswith('__')]
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
                tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                if tmp_pcCardRule_new:
                    tmp_pcCardRule = tmp_pcCardRule_new
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_pcCardRule)
                synonyms = tmp_template.get('synonyms', {}) if tmp_template else {}
                # 获取特殊技能并合并到普通技能列表
                special_skills = []
                if tmp_pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial:
                    special_skills = OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[tmp_pcCardRule]
                all_skills = pc_skill_names + special_skills
                if tmp_pc_name is None:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRmCardNone'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                elif not tmp_reast_str_new_2:
                    replyMsgLazyHelpByEvent(plugin_event, 'st')
                    return
                input_str = tmp_reast_str_new_2.strip().upper()
                # 按空格分割输入字符串
                input_parts = input_str.split()
                result_lines = []
                seen_skills = set() 
                for part in input_parts:
                    remaining_str = part.upper()
                    matched_skills = []
                    unmatched_groups = []
                    current_unmatched = []
                    skill_mapping = {}
                    # 构建技能映射表
                    for skill in all_skills:
                        main_skill = None
                        for main_key in synonyms:
                            if skill in synonyms[main_key]:
                                main_skill = main_key.upper()
                                break
                        skill_mapping[skill] = main_skill if main_skill else skill
                    while remaining_str:
                        matched = False
                        max_len = 0
                        matched_skill = None
                        # 按长度从长到短排序匹配
                        for skill in sorted(all_skills, key=len, reverse=True):
                            skill_upper = skill.upper()
                            skill_len = len(skill_upper)
                            if skill_len > len(remaining_str):
                                continue
                            if remaining_str.startswith(skill_upper):
                                matched_skill = skill_mapping[skill]
                                max_len = skill_len
                                matched = True
                                break
                        if matched:
                            if current_unmatched:
                                unmatched_groups.append(''.join(current_unmatched))
                                current_unmatched = []
                            # 检查是否已经添加过这个技能
                            if matched_skill not in seen_skills:
                                matched_skills.append((matched_skill, max_len, True))
                                seen_skills.add(matched_skill)
                            remaining_str = remaining_str[max_len:]
                        else:
                            current_unmatched.append(remaining_str[0])
                            remaining_str = remaining_str[1:]
                    if current_unmatched:
                        unmatched_groups.append(''.join(current_unmatched))
                    # 处理匹配到的技能
                    for skill, length, is_matched in matched_skills:
                        if is_matched:
                            if skill in special_skills and skill not in pc_skill_names:
                                skill_value = OlivaDiceCore.skillCheck.getSpecialSkill(
                                    skill,
                                    tmp_pcCardRule,
                                    pc_skills
                                )
                                if skill_value is None:
                                    skill_value = "0"
                            else:
                                skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                                    tmp_pcHash,
                                    skill,
                                    hagId = tmp_hagID
                                )
                            display_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                                tmp_pcHash,
                                skill,
                                flagShow=True,
                                hagId=tmp_hagID
                            )
                            result_lines.append(f"[{display_name}]: {skill_value}")
                    # 处理未匹配的部分
                    for group in unmatched_groups:
                        display_name = group.upper()
                        if display_name not in seen_skills:
                            skill_value = '0'
                            result_lines.append(f"[{display_name}]: {skill_value}")
                            seen_skills.add(display_name)
                dictTValue['tName'] = tmp_pc_name
                dictTValue['tSkillName'] = input_str
                dictTValue['tSkillValue'] = '\n'.join(result_lines)
                # 根据匹配到的技能数量选择不同的回复模板
                total_skills = len(result_lines)
                if total_skills == 1:
                    dictTValue['tSkillName'] = display_name
                    dictTValue['tSkillValue'] = skill_value
                    if is_at:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetSingleSkillValueAtOther'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetSingleSkillValue'], dictTValue)
                else:
                    if is_at:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetMultiSkillValueAtOther'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetMultiSkillValue'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            if not tmp_reply_str:
                tmp_reply_str = OlivaDiceCore.helpDoc.getHelp('st', plugin_event.bot_info.hash)
                replyMsg(plugin_event, tmp_reply_str)
                return
        elif isMatchWordStart(tmp_reast_str, 'set', isCommand = True):
            OlivaDiceCore.msgReplyModel.replySET_command(plugin_event, Proc, valDict)
        elif isMatchWordStart(tmp_reast_str, ['coc6','coc'], isCommand = True) \
        or (False and isMatchWordStart(tmp_reast_str, 'dnd', isCommand = True)):
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
                if tmp_roll_count_str.isdecimal():
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
                time_count = 0
                for tmp_res_list_this in tmp_res_list:
                    if time_count > 0:
                        tmp_reply_str_1 += '\n\n'
                    else:
                        tmp_reply_str_1 += '\n'
                    tmp_total_count_1 = 0
                    tmp_total_count_2 = 0
                    # 添加计数器用于换行
                    count = 0
                    total_skills = len(tmp_res_list_this)
                    for i, tmp_res_list_this_this in enumerate(tmp_res_list_this):
                        tmp_skill_name_this_1 = tmp_res_list_this_this
                        if tmp_res_list_this_this in tmp_pcCardTemplate['showName']:
                            tmp_skill_name_this_1 = tmp_pcCardTemplate['showName'][tmp_res_list_this_this]
                        tmp_reply_str_1 += '%s: %d  ' % (tmp_skill_name_this_1, tmp_res_list_this[tmp_res_list_this_this])
                        tmp_total_count_2 += tmp_res_list_this[tmp_res_list_this_this]
                        if tmp_res_list_this_this != 'LUC':
                            tmp_total_count_1 += tmp_res_list_this[tmp_res_list_this_this]
                        # 每三个属性后换行，最后一行不换
                        count += 1
                        if count % 3 == 0 and i < total_skills - 1:
                            tmp_reply_str_1 += '\n'
                    if tmp_pcCardTemplateName in ['COC7']:
                        # 计算HP
                        if 'CON' in tmp_res_list_this and 'SIZ' in tmp_res_list_this:
                            hp = (tmp_res_list_this['CON'] + tmp_res_list_this['SIZ']) // 10
                            tmp_reply_str_1 += f'\nHP: {hp}'
                        # 计算体格
                        build = OlivaDiceCore.skillCheck.getSpecialSkill('体格', tmp_pcCardTemplateName, tmp_res_list_this)
                        if build:
                            tmp_reply_str_1 += f'  体格: {build}'
                        # 计算DB
                        db = OlivaDiceCore.skillCheck.getSpecialSkill('DB', tmp_pcCardTemplateName, tmp_res_list_this)
                        if db:
                            tmp_reply_str_1 += f'  DB: {db}'
                        tmp_reply_str_1 += '\n共计: %d/%d  %.2f%%' % (tmp_total_count_1, tmp_total_count_2, 100 * tmp_total_count_1 / tmp_total_count_2)
                    elif tmp_pcCardTemplateName in ['COC6', 'DND5E']:
                        tmp_reply_str_1 += '\n共计: %d' % tmp_total_count_1
                    time_count += 1
                dictTValue['tPcInitResult'] = tmp_reply_str_1
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInit'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            else:
                dictTValue['tPcTempName'] = tmp_pcCardTemplateName
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitErrorRange'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
        elif isMatchWordStart(tmp_reast_str, 'dnd', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'dnd')
            tmp_pcCardTemplateName = 'DND5E'
            tmp_roll_count = 1
            tmp_roll_count_str = None
            tmp_res_list = []
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) > 0:
                [tmp_roll_count_str, tmp_reast_str] = getNumberPara(tmp_reast_str)
            if tmp_roll_count_str == '':
                tmp_roll_count_str = None
            if tmp_roll_count_str != None:
                if tmp_roll_count_str.isdecimal():
                    tmp_roll_count = int(tmp_roll_count_str)
            if tmp_roll_count > 0 and tmp_roll_count <= 10:
                tmp_res_list = []
                tmp_range_list = range(0, tmp_roll_count)
                for tmp_i in tmp_range_list:
                    tmp_res_list_this = []
                    tmp_sum = 0
                    for tmp_i_this in range(6):
                        rd_this = OlivaDiceCore.onedice.RD('4d6k3')
                        rd_this.roll()
                        if rd_this.resError is None:
                            tmp_res_list_this.append('%2d' % rd_this.resInt)
                            tmp_sum += rd_this.resInt
                    tmp_res_list.append([tmp_res_list_this, '%3d' % tmp_sum])
                dictTValue['tPcTempName'] = tmp_pcCardTemplateName
                dictTValue['tPcInitResult'] = '\n' + '\n'.join([
                    '[%s] : %s' % (', '.join(tmp_res_list_this[0]), tmp_res_list_this[1])
                    for tmp_res_list_this in tmp_res_list
                ])
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInit'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            else:
                dictTValue['tPcTempName'] = tmp_pcCardTemplateName
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitErrorRange'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
        elif isMatchWordStart(tmp_reast_str, 'sc', isCommand = True):
            is_at, at_user_id, tmp_reast_str = parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin)
            if is_at:
                if not at_user_id:
                    return
                dictTValue['tName'] = dictTValue['tUserName01']
            tmp_pc_id = at_user_id if at_user_id else plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'sc')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            if len(tmp_reast_str) <= 0:
                replyMsgLazyHelpByEvent(plugin_event, 'sc')
                return
            # 处理奖励骰和惩罚骰
            flag_bp_type = 0  # 0:无 1:奖励骰 2:惩罚骰
            flag_bp_count = 1  # 骰子数量
            if isMatchWordStart(tmp_reast_str, 'b'):
                flag_bp_type = 1
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'b')
                # 检查是否有数字指定骰子数量
                if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                    flag_bp_count = int(tmp_reast_str[0])
                    tmp_reast_str = tmp_reast_str[1:]
            elif isMatchWordStart(tmp_reast_str, 'p'):
                flag_bp_type = 2
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'p')
                # 检查是否有数字指定骰子数量
                if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                    flag_bp_count = int(tmp_reast_str[0])
                    tmp_reast_str = tmp_reast_str[1:]
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str_list = tmp_reast_str.split(' ')
            tmp_sancheck_para = None
            tmp_san_val = None
            if len(tmp_reast_str_list) >= 2:
                tmp_sancheck_para = tmp_reast_str_list[0]
                if tmp_reast_str_list[-1].isdecimal():
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
                # 构建骰子表达式
                rd_para_str = '1D100'
                if flag_bp_type == 1:
                    rd_para_str = f'B{flag_bp_count}'
                elif flag_bp_type == 2:
                    rd_para_str = f'P{flag_bp_count}'
                rd_para = OlivaDiceCore.onedice.RD(rd_para_str)
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
                    tmp_template_name = 'COC7'
                    tmp_template_rule_name = 'default'
                    if flag_groupTemplate != None:
                        tmp_template_name = flag_groupTemplate
                        if flag_groupTemplateRule != None:
                            tmp_template_rule_name = flag_groupTemplateRule
                    tmpSkillCheckType, _ = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                        dictRuleTempData,
                        OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name),
                        tmp_template_rule_name
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
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatSucceed'], dictTValue)
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
                        # 构建骰子详情显示
                        dice_detail = f"{rd_para_str}={tmp_rd_int}/{str(tmp_skill_value_old)}"
                        if rd_para.resDetail:
                            dice_detail = f"{rd_para_str}={rd_para.resDetail}={tmp_rd_int}/{str(tmp_skill_value_old)}"
                        dictTValue['tName'] = tmp_pc_name
                        dictTValue['tSkillValue'] = str(tmp_skill_value_old)
                        dictTValue['tSkillValueNew'] = str(tmp_skill_value)
                        dictTValue['tRollResult'] = dice_detail
                        if is_at:
                            if flag_GreatFailed:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheckGreatFailedAtOther'], dictTValue)
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheckAtOther'], dictTValue)
                        else:
                            if flag_GreatFailed:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheckGreatFailed'], dictTValue)
                            else:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheck'], dictTValue)
                        trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                    else:
                        dictTValue['tName'] = tmp_pc_name
                        dictTValue['tSkillValue'] = str(tmp_skill_value_old)
                        dictTValue['tRollResult'] = f"{rd_para_str}={tmp_rd_int}/{str(tmp_skill_value_old)}"
                        dictTValue['tRollSubResult'] = tmp_sancheck_para_final
                        if is_at:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheckErrorAtOther'], dictTValue)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSanCheckError'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
            else:
                replyMsgLazyHelpByEvent(plugin_event, 'sc')
        elif isMatchWordStart(tmp_reast_str, 'ri', isCommand = True):
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
        elif isMatchWordStart(tmp_reast_str, 'init', isCommand = True):
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
            elif isMatchWordStart(tmp_reast_str, ['clear', 'clr'], fullMatch = True):
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
        elif isMatchWordStart(tmp_reast_str, 'rav', isCommand = True):
            OlivaDiceCore.msgReplyModel.replyRAV_command(plugin_event, Proc, valDict)
        elif isMatchWordStart(tmp_reast_str, ['ra','rc'], isCommand = True):
            is_at, at_user_id, tmp_reast_str = parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin)
            if is_at:
                if not at_user_id:
                    return
                dictTValue['tName'] = dictTValue['tUserName01']
            tmp_pc_id = at_user_id if at_user_id else plugin_event.data.user_id
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
            if isMatchWordStart(tmp_reast_str, ['ra','rc']):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['ra','rc'])
            else:
                return
            flag_hide_roll = False
            if len(tmp_reast_str) > 0:
                if isMatchWordStart(tmp_reast_str, 'h'):
                    flag_hide_roll = True
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'h')
            if len(tmp_reast_str) > 2:
                tmp_reast_str_list_1 = tmp_reast_str.split('#')
                if len(tmp_reast_str_list_1) > 1:
                    if tmp_reast_str_list_1[0].isdecimal():
                        roll_times_count = int(tmp_reast_str_list_1[0])
                        if roll_times_count > 10:
                            roll_times_count = 10
                        tmp_reast_str = tmp_reast_str_list_1[1]
            # 处理奖励/惩罚骰（b/p）
            flag_bp_type = 0  # 0无 1奖励 2惩罚
            flag_bp_count = None
            if len(tmp_reast_str) > 0:
                if isMatchWordStart(tmp_reast_str, ['b','B']):
                    flag_bp_type = 1
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['b','B'])
                elif isMatchWordStart(tmp_reast_str, ['p','P']):
                    flag_bp_type = 2
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['p','P'])
                if flag_bp_type != 0 and len(tmp_reast_str) > 1:
                    if tmp_reast_str[0].isdecimal():
                        flag_bp_count = tmp_reast_str[0]
                        tmp_reast_str = tmp_reast_str[1:]
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_skill_name = None
            tmp_skill_value = None
            difficulty = None
            # 解析难度前缀（困难/极难/大成功）
            difficulty, tmp_reast_str = OlivaDiceCore.msgReplyModel.difficulty_analyze(tmp_reast_str)
            tmp_skill_value_str = None
            if tmp_reast_str:
                op_list = OlivaDiceCore.msgReplyModel.op_list_get()
                skill_end_pos = len(tmp_reast_str)
                for i, char in enumerate(tmp_reast_str):
                    if char in op_list or char.isdigit():
                        skill_end_pos = i
                        break
                tmp_skill_name = tmp_reast_str[:skill_end_pos].strip().upper() or None
                tmp_reast_str = tmp_reast_str[skill_end_pos:].strip()
                if not tmp_reast_str:
                    tmp_skill_name = tmp_skill_name.split()[0]
                    if tmp_skill_name:
                        tmp_skill_name = OlivaDiceCore.pcCard.fixName(tmp_skill_name, flagMode = 'skillName')
                    # 直接读取数值
                    tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                        tmp_skill_name,
                        hagId=tmp_hagID
                    )
                    tmp_skill_value_str = str(tmp_skill_value)
                else:
                    if tmp_skill_name:
                        tmp_skill_name = OlivaDiceCore.pcCard.fixName(tmp_skill_name, flagMode = 'skillName')
                    # 检查是否有运算符
                    if tmp_reast_str[0] in op_list:
                        # 带运算表达式
                        expr_end = 0
                        in_dice = False
                        for i, char in enumerate(tmp_reast_str):
                            if char.isspace():
                                expr_end = i
                                break
                            if char.upper() == 'D':
                                in_dice = True
                            if not (char.isdigit() or char in op_list or char.upper() == 'D'):
                                if not in_dice:
                                    expr_end = i
                                    break
                        expr_str = tmp_reast_str[:expr_end] if expr_end > 0 else tmp_reast_str
                        tmp_reast_str = tmp_reast_str[len(expr_str):].strip()
                        base_value = None
                        if tmp_reast_str and tmp_reast_str[0].isdigit():
                            [base_value, tmp_reast_str] = getNumberPara(tmp_reast_str)
                            base_value = int(base_value)
                        else:
                            base_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                                OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                                tmp_skill_name,
                                hagId=tmp_hagID
                            )
                        if base_value is not None:
                            full_expr = f"{base_value}{expr_str}"
                            rd_para = OlivaDiceCore.onedice.RD(full_expr)
                            rd_para.roll()
                            if rd_para.resError is None:
                                tmp_skill_value = rd_para.resInt
                                if "D" in full_expr.upper():
                                    tmp_skill_value_str = (
                                        f"{full_expr}={rd_para.resDetail}={tmp_skill_value}"
                                    )
                                else:
                                    tmp_skill_value_str = (
                                        f"{full_expr}={tmp_skill_value}"
                                    )
                    else:
                        # 指定数值
                        if tmp_reast_str[0].isdigit():
                            [tmp_skill_value, tmp_reast_str] = getNumberPara(tmp_reast_str)
                            tmp_skill_value = int(tmp_skill_value)
                            tmp_skill_value_str = str(tmp_skill_value)
            if tmp_skill_name and tmp_skill_value is None:
                tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                    OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                    tmp_skill_name,
                    hagId=tmp_hagID
                )
                if tmp_skill_value is not None:
                    tmp_skill_value_str = str(tmp_skill_value)
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                tmp_hagID
            )
            if tmp_pc_name_1:
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
                        dictRuleTempData = {
                            'roll': rd_para.resInt,
                            'skill': tmp_skill_value
                        }
                        OlivaDiceCore.onediceOverride.saveRDDataUser(
                            data = rd_para,
                            botHash = plugin_event.bot_info.hash,
                            userId = tmp_pc_id,
                            platform = tmp_pc_platform,
                            skillValue = tmp_skill_value
                        )
                        tmpSkillCheckType, tmpSkillThreshold = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                            dictRuleTempData,
                            tmp_Template,
                            tmp_TemplateRuleName,
                            difficulty_prefix=difficulty
                        )
                        dictTValue['tSkillValue'] = tmp_skill_value_str if not difficulty else f'{tmpSkillThreshold}({tmp_skill_value_str})'
                        if tmpSkillThreshold == None: dictTValue['tSkillValue'] = tmp_skill_value_str
                        dictTValue['tRollResult'] = '%s/%s' % (dictTValue['tRollResult'], dictTValue['tSkillValue'])
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgReplyModel.get_SkillCheckResult(tmpSkillCheckType, dictStrCustom, dictTValue)
                        if tmpSkillCheckType in [
                            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS,
                            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS,
                            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
                            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
                        ]:
                            flag_check_success = True
                        flag_need_reply = True
                else:
                    flag_begin = True
                    tmp_tSkillCheckReasult = ''
                    for i in range(roll_times_count):
                        rd_para = OlivaDiceCore.onedice.RD(rd_para_str)
                        rd_para.roll()
                        if rd_para.resError == None:
                            if flag_bp_type == 0:
                                tmp_tSkillCheckReasult += '%s=%d' % (rd_para_str, rd_para.resInt)
                            else:
                                tmp_tSkillCheckReasult += '%s=%s=%d' % (rd_para_str, rd_para.resDetail, rd_para.resInt)
                            dictRuleTempData = {
                                'roll': rd_para.resInt,
                                'skill': tmp_skill_value
                            }
                            tmpSkillCheckType, tmpSkillThreshold = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                                dictRuleTempData,
                                tmp_Template,
                                tmp_TemplateRuleName,
                                difficulty_prefix=difficulty
                            )
                            dictTValue['tSkillValue'] = tmp_skill_value_str if not difficulty else f'{tmpSkillThreshold}({tmp_skill_value_str})'
                            if tmpSkillThreshold == None: dictTValue['tSkillValue'] = tmp_skill_value_str
                            tmp_tSkillCheckReasult = '%s/%s ' % (tmp_tSkillCheckReasult, dictTValue['tSkillValue'])
                            tmp_tSkillCheckReasult += OlivaDiceCore.msgReplyModel.get_SkillCheckResult(tmpSkillCheckType, dictStrCustom, dictTValue)
                            if tmpSkillCheckType in [
                                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS,
                                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS,
                                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
                                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
                            ]:
                                flag_check_success = True
                            flag_need_reply = True
                            tmp_tSkillCheckReasult += '\n'
                        else:
                            flag_need_reply = False
                            break
                    dictTValue['tRollResult'] = ''
                    dictTValue['tSkillCheckReasult'] = tmp_tSkillCheckReasult.strip()
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
                        if flag_bp_type != 1:
                            if tmp_skill_name_core not in tmp_enhanceList and tmp_skill_name_core not in tmp_skipEnhance_list:
                                tmp_enhanceList.append(tmp_skill_name_core)
                        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                            tmp_pcHash,
                            tmp_pc_name_1,
                            'enhanceList',
                            tmp_enhanceList
                        )
                if flag_need_reply:
                    if is_at:
                        if tmp_skill_name:
                            dictTValue['tSkillName'] = tmp_skill_name if not difficulty else f'{tmp_skill_name}({difficulty})'
                            if tmpSkillThreshold == None: dictTValue['tSkillName'] = tmp_skill_name
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckWithSkillNameAtOther'], dictTValue)
                            tmp_reply_str_show = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHideShowWithSkillNameAtOther'], dictTValue)
                            if flag_hide_roll and flag_is_from_group:
                                dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHideWithSkillNameAtOther'], dictTValue)
                        else:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckAtOther'], dictTValue)
                            tmp_reply_str_show = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHideShowAtOther'], dictTValue)
                            if flag_hide_roll and flag_is_from_group:
                                dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHideAtOther'], dictTValue)
                        if flag_hide_roll and flag_is_from_group:
                            replyMsg(plugin_event, tmp_reply_str_show)
                            replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                        else:
                            replyMsg(plugin_event, tmp_reply_str)
                    else:
                        if tmp_skill_name:
                            dictTValue['tSkillName'] = tmp_skill_name if not difficulty else f'{tmp_skill_name}({difficulty})'
                            if tmpSkillThreshold == None: dictTValue['tSkillName'] = tmp_skill_name
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
        elif isMatchWordStart(tmp_reast_str, 'en', isCommand = True):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'en')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip()
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
            tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
            if tmp_pc_name is None:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceError'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            dictTValue['tName'] = tmp_pc_name
            tmp_pcCardRule = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name) or 'default'
            special_skills_for_rule = OlivaDiceCore.pcCardData.dictPcCardMappingSpecial.get(tmp_pcCardRule, [])
            # 内部函数：执行检定并返回原始结果
            def _perform_skill_enhancement(skill_list_to_enhance):
                results = {
                    'enhance_count': 0,
                    'succeed_count': 0,
                    'succeed_details': []
                }
                for skill_name in skill_list_to_enhance:
                    if skill_name in special_skills_for_rule: # 如果是特殊技能，直接跳过
                        continue
                    skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(tmp_pcHash, skill_name, hagId=tmp_hagID)
                    if skill_value is None or skill_value == 0:
                        continue
                    results['enhance_count'] += 1
                    rd_para_1 = OlivaDiceCore.onedice.RD('1D100')
                    rd_para_1.roll()
                    if rd_para_1.resError is None and (rd_para_1.resInt > skill_value or rd_para_1.resInt >= 96):
                        rd_para_str_2 = f'{skill_value}+1D10'
                        rd_para_2 = OlivaDiceCore.onedice.RD(rd_para_str_2)
                        rd_para_2.roll()
                        if rd_para_2.resError is None:
                            OlivaDiceCore.pcCard.pcCardDataSetBySkillName(tmp_pcHash, skill_name, rd_para_2.resInt, tmp_pc_name, hagId=tmp_hagID)
                            results['succeed_count'] += 1
                            results['succeed_details'].append([skill_name, skill_value, rd_para_2.resInt])
                return results
            # 无参数，使用自动成长
            if not tmp_reast_str:
                enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(tmp_pcHash, tmp_pc_name, 'enhanceList', [])
                enhanceList_filtered = [skill for skill in enhanceList if skill not in special_skills_for_rule]
                enhancement_results = _perform_skill_enhancement(enhanceList_filtered)
                dictTValue['tCheckedSkillList'] = '、'.join(f'[{skill}]' for skill in enhanceList_filtered)
                dictTValue['tSkillEnhanceCount'] = str(enhancement_results['enhance_count'])
                dictTValue['tSkillEnhanceSucceedCount'] = str(enhancement_results['succeed_count'])
                succeed_list_formatted = []
                for item in enhancement_results['succeed_details']:
                    display_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(tmp_pcHash, item[0], flagShow=True, hagId=tmp_hagID)
                    succeed_list_formatted.append(f'{display_name}:[{item[1]}+{item[2] - item[1]}]')
                dictTValue['tSkillEnhanceSucceedList'] = ('\n' + '、'.join(succeed_list_formatted)) if succeed_list_formatted else ''
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceAll'], dictTValue)
                OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(tmp_pcHash, tmp_pc_name, 'enhanceList', [skill for skill in enhanceList if skill in special_skills_for_rule])
                replyMsg(plugin_event, tmp_reply_str)
                return
            # 有参数，可能是单个技能或多个技能
            [tmp_skill_name, tmp_reast_str_single] = getToNumberPara(tmp_reast_str)
            tmp_reast_str_single = skipSpaceStart(tmp_reast_str_single)
            tmp_skill_value = None
            if tmp_reast_str_single:
                [tmp_skill_value_str, _] = getNumberPara(tmp_reast_str_single)
                if tmp_skill_value_str.isdigit():
                    tmp_skill_value = int(tmp_skill_value_str)
            # 如果成功解析出技能名和数值，则为指定的单技能成长（不保存）
            if tmp_skill_name and tmp_skill_value is not None:
                tmp_skill_name = tmp_skill_name.upper()
                rd_para_1 = OlivaDiceCore.onedice.RD('1D100')
                rd_para_1.roll()
                if rd_para_1.resError is None:
                    dictTValue['tSkillName'] = tmp_skill_name
                    dictTValue['tSkillValue'] = tmp_skill_value
                    dictTValue['tRollResult'] = f'1D100={rd_para_1.resInt}'
                    if rd_para_1.resInt > tmp_skill_value or rd_para_1.resInt >= 96:
                        rd_para_str_2 = f'{tmp_skill_value}+1D10'
                        rd_para_2 = OlivaDiceCore.onedice.RD(rd_para_str_2)
                        rd_para_2.roll()
                        if rd_para_2.resError is None:
                            dictTValue['tRollSubResult'] = f'{rd_para_str_2}={rd_para_2.resDetail}={rd_para_2.resInt}'
                            dictTValue['tSkillCheckReasult'] = f"{OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)}{OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceContent'], dictTValue)}"
                        else:
                             dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
                    else:
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceCheck'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            # 多技能或单个技能（从人物卡取值）成长模式
            pc_skills_data = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
            pc_skill_names = [s.upper() for s in pc_skills_data.keys() if not s.startswith('__')]
            tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_pcCardRule)
            synonyms = tmp_template.get('synonyms', {}) if tmp_template else {}
            special_skills = OlivaDiceCore.pcCardData.dictPcCardMappingSpecial.get(tmp_pcCardRule, [])
            all_skills_on_card = pc_skill_names + special_skills
            skill_mapping = {skill.upper(): skill.upper() for skill in all_skills_on_card}
            for main_key, syn_list in synonyms.items():
                for syn in syn_list:
                    skill_mapping[syn.upper()] = main_key.upper()
            skills_to_grow = []
            skipped_skills = []
            not_found_skills = []
            seen_skills = set()
            input_parts = tmp_reast_str.strip().upper().split()
            for part in input_parts:
                remaining_str = part
                current_unmatched_chars = []
                while remaining_str:
                    matched = False
                    for skill_len in range(len(remaining_str), 0, -1):
                        sub_str = remaining_str[:skill_len]
                        if sub_str in skill_mapping:
                            if current_unmatched_chars:
                                not_found_skills.append("".join(current_unmatched_chars))
                                current_unmatched_chars = []
                            mapped_skill = skill_mapping[sub_str]
                            if mapped_skill not in seen_skills:
                                seen_skills.add(mapped_skill)
                                display_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(tmp_pcHash, mapped_skill, flagShow=True, hagId=tmp_hagID)
                                is_special_not_on_card = mapped_skill in special_skills_for_rule and mapped_skill not in pc_skill_names
                                if mapped_skill in special_skills_for_rule: # 如果是特殊技能，直接跳过
                                    skill_value = 0
                                else:
                                    skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(tmp_pcHash, mapped_skill, hagId=tmp_hagID)
                                if is_special_not_on_card or skill_value is None or skill_value == 0:
                                    skipped_skills.append(display_name)
                                else:
                                    skills_to_grow.append(mapped_skill)
                            remaining_str = remaining_str[skill_len:]
                            matched = True
                            break
                    if not matched:
                        current_unmatched_chars.append(remaining_str[0])
                        remaining_str = remaining_str[1:]
                if current_unmatched_chars:
                    not_found_skills.append("".join(current_unmatched_chars))
            # 处理只输入了特殊技能或0值技能的或未找到对应的技能特殊情况
            if not skills_to_grow:
                if skipped_skills:
                    dictTValue['tSkippedSkillList'] = '、'.join(f'[{skill}]' for skill in skipped_skills)
                if not_found_skills:
                    if 'tSkippedSkillList' in dictTValue:
                        dictTValue['tSkippedSkillList'] += '、' + '、'.join(f'[{skill}]' for skill in not_found_skills)
                    else:
                        dictTValue['tSkippedSkillList'] = '、'.join(f'[{skill}]' for skill in not_found_skills)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceOnlySpecial'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            # 如果只有一个有效技能，且没有跳过或未找到的，则使用单技能成长回复
            if len(skills_to_grow) == 1 and not skipped_skills and not not_found_skills:
                tmp_skill_name = skills_to_grow[0]
                tmp_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(tmp_pcHash, tmp_skill_name, hagId=tmp_hagID)
                rd_para_1 = OlivaDiceCore.onedice.RD('1D100')
                rd_para_1.roll()
                if rd_para_1.resError is None:
                    dictTValue['tSkillName'] = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(tmp_pcHash, tmp_skill_name, flagShow=True, hagId=tmp_hagID)
                    dictTValue['tSkillValue'] = tmp_skill_value
                    dictTValue['tRollResult'] = f'1D100={rd_para_1.resInt}'
                    if rd_para_1.resInt > tmp_skill_value or rd_para_1.resInt >= 96:
                        rd_para_str_2 = f'{tmp_skill_value}+1D10'
                        rd_para_2 = OlivaDiceCore.onedice.RD(rd_para_str_2)
                        rd_para_2.roll()
                        if rd_para_2.resError is None:
                            OlivaDiceCore.pcCard.pcCardDataSetBySkillName(tmp_pcHash, tmp_skill_name, rd_para_2.resInt, tmp_pc_name, hagId=tmp_hagID)
                            dictTValue['tRollSubResult'] = f'{rd_para_str_2}={rd_para_2.resDetail}={rd_para_2.resInt}'
                            dictTValue['tSkillCheckReasult'] = f"{OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)}{OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceContent'], dictTValue)}"
                    else:
                        dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceCheck'], dictTValue)
                    enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(tmp_pcHash, tmp_pc_name, 'enhanceList', [])
                    if tmp_skill_name in enhanceList:
                        enhanceList.remove(tmp_skill_name)
                        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(tmp_pcHash, tmp_pc_name, 'enhanceList', enhanceList)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            # 多技能或混合结果，使用统一的汇总回复
            final_reply_parts = []
            if skills_to_grow:
                enhancement_results = _perform_skill_enhancement(skills_to_grow)
                checked_display_names = [OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(tmp_pcHash, s, flagShow=True, hagId=tmp_hagID) for s in skills_to_grow]
                dictTValue['tCheckedSkillList'] = '、'.join(f'[{skill}]' for skill in checked_display_names)
                dictTValue['tSkillEnhanceCount'] = str(enhancement_results['enhance_count'])
                dictTValue['tSkillEnhanceSucceedCount'] = str(enhancement_results['succeed_count'])
                succeed_list_formatted = []
                for item in enhancement_results['succeed_details']:
                    display_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(tmp_pcHash, item[0], flagShow=True, hagId=tmp_hagID)
                    succeed_list_formatted.append(f'{display_name}:[{item[1]}+{item[2] - item[1]}]')
                dictTValue['tSkillEnhanceSucceedList'] = ('\n' + '、'.join(succeed_list_formatted)) if succeed_list_formatted else ''
                final_reply_parts.append(OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceAll'], dictTValue))
            if skipped_skills:
                dictTValue['tSkippedSkillList'] = '、'.join(f'[{skill}]' for skill in skipped_skills)
                final_reply_parts.append(OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceSkipped'], dictTValue))
            if not_found_skills:
                dictTValue['tNotFoundSkillList'] = '、'.join(f'[{skill}]' for skill in not_found_skills)
                final_reply_parts.append(OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillEnhanceNotFound'], dictTValue))
            replyMsg(plugin_event, ''.join(final_reply_parts))
            return
        elif isMatchWordStart(tmp_reast_str, 'team', isCommand = True):
            if not flag_is_from_group:
                OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                    dictStrCustom['strForGroupOnly'], dictTValue
                ))
                return
            OlivaDiceCore.msgReplyModel.replyTEAM_command(plugin_event, Proc, valDict)
        #关闭该调试性质指令
        elif False and isMatchWordStart(tmp_reast_str, 'rrange', isCommand = True):
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
        elif isMatchWordStart(tmp_reast_str, 'rr', isCommand = True):
            OlivaDiceCore.msgReplyModel.replyRR_command(plugin_event, Proc, valDict)
        elif isMatchWordStart(tmp_reast_str, ['rx', 'r', 'ww', 'w', 'dxx', 'dx'], isCommand = True):
            tmp_pc_id = plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_reply_str = ''
            tmp_reply_str_show = ''
            flag_roll_mode = 'r'
            tmp_ruleMode = 'default'
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
                tmp_ruleMode = 'DX3'
            elif isMatchWordStart(tmp_reast_str, 'dx'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'dx')
                flag_roll_mode = 'dx'
                tmp_ruleMode = 'DX3'
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
                    if tmp_reast_str_list_1[0].isdecimal():
                        roll_times_count = int(tmp_reast_str_list_1[0])
                        if roll_times_count > 10:
                            roll_times_count = 10
                        tmp_reast_str = tmp_reast_str_list_1[1]
            tmp_rd_para_str = None
            tmp_rd_para_str_show = None
            if len(tmp_reast_str) > 0:
                if flag_roll_mode in ['rx']:
                    [tmp_rd_para_str, tmp_reast_str] = getExpression(tmp_reast_str, valueTable = None)
                    tmp_rd_para_str_show = tmp_rd_para_str
                else:
                    tmp_reast_str_old = tmp_reast_str
                    tmp_pcCardRule = 'default'
                    if flag_roll_mode in ['r']:
                        tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name_0)
                        if tmp_pcCardRule_new != None:
                            tmp_pcCardRule = tmp_pcCardRule_new
                    elif flag_roll_mode in ['ww', 'w']:
                        tmp_pcCardRule = 'WW'
                    elif flag_roll_mode in ['dx', 'dxx']:
                        tmp_pcCardRule = 'DX3'
                    [tmp_rd_para_str, tmp_reast_str] = getExpression(
                        tmp_reast_str_old,
                        valueTable = skill_valueTable,
                        pcCardRule = tmp_pcCardRule,
                        flagDynamic = True,
                        ruleMode = tmp_ruleMode
                    )
                    [tmp_rd_para_str_show, tmp_reast_str_2] = getExpression(
                        tmp_reast_str_old,
                        valueTable = skill_valueTable,
                        pcCardRule = tmp_pcCardRule,
                        flagDynamic = None,
                        ruleMode = tmp_ruleMode
                    )
                    if tmp_reast_str != tmp_reast_str_2:
                        tmp_rd_para_str_show = tmp_rd_para_str
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
                    if rd_para_str != tmp_rd_para_str:
                        tmp_rd_para_str_show = rd_para_str
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
            flag_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_pc_platform,
                userConfigKey = 'groupTemplate',
                botHash = plugin_event.bot_info.hash
            )
            if flag_groupTemplate != None:
                tmp_template_name = flag_groupTemplate
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
            # FATE规则时无视主骰设置
            if tmp_template_name and tmp_template_name.lower() in ['fate']:
                # FATE规则不使用主骰设置
                pass
            else:
                if rd_para_main_str != None and not flag_have_para and flag_roll_mode in ['r', 'rx']:
                    rd_para_str = rd_para_main_str
            # 确保 tmp_template_customDefault 是有效的字典
            if tmp_template_customDefault is None:
                tmp_template_customDefault = {}
            tmp_template_customDefault = copy.deepcopy(tmp_template_customDefault)
            # FATE规则时不修改D右值
            if tmp_template_name and tmp_template_name.lower() not in ['fate']:
                if type(rd_para_main_D_right) == int:
                    if type(tmp_template_customDefault) != dict:
                        tmp_template_customDefault = {}
                    if 'd' not in tmp_template_customDefault:
                        tmp_template_customDefault['d'] = {}
                    tmp_template_customDefault['d']['rightD'] = rd_para_main_D_right
            if roll_times_count == 1:
                rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault, valueTable = skill_valueTable)
                rd_para.ruleMode = tmp_ruleMode
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
                    if tmp_rd_para_str_show == None:
                        tmp_rd_para_str_show = rd_para_str
                    elif tmp_rd_para_str_show == '':
                        tmp_rd_para_str_show = rd_para_str
                    if flag_roll_mode in ['w', 'dxx']:
                        rd_para_str_new = tmp_rd_para_str_show
                        tmp_resDetail_short_str = OlivaDiceCore.onediceOverride.RDDataFormat(
                            data = rd_para.resDetailData,
                            mode = 'short'
                        )
                        if tmp_resDetail_short_str == None:
                            tmp_resDetail_short_str = ''
                        if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                            tmp_reply_str_1 = rd_para_str_new + '=' + (', '.join(
                                OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                            ))
                        elif len(str(rd_para.resInt)) > 100:
                            tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                        else:
                            tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)
                    elif flag_roll_mode in ['ww', 'dx']:
                        rd_para_str_new = tmp_rd_para_str_show
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
                                tmp_reply_str_1 = rd_para_str_new + '=' + (', '.join(
                                    OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                ))
                            elif len(str(rd_para.resInt)) > 100:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                            else:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_short_str) + '=' + str(rd_para.resInt)
                        else:
                            if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_str) + '=' + (', '.join(
                                    OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                ))
                            elif len(str(rd_para.resInt)) > 50:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_str) + '=' + str(rd_para.resInt)[:50] + '...的天文数字'
                            else:
                                tmp_reply_str_1 = rd_para_str_new + '=' + str(tmp_resDetail_str) + '=' + str(rd_para.resInt)
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
                            rd_para_str_new = tmp_rd_para_str_show
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
                    dictTValue['tRollPara'] = str(tmp_rd_para_str_show)
                    tmp_reply_str_1 = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_para.resError, dictStrCustom, dictTValue)
                    tmp_reply_str_1 += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollErrorHelp'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str_1)
                    return
                dictTValue['tRollResult'] = tmp_reply_str_1
            else:
                flag_begin = True
                tmp_reply_str_1 = ''
                tmp_reply_str_1_list = []
                rd_para_str_new = None
                flag_multiRollDetail = OlivaDiceCore.console.getConsoleSwitchByHash(
                    'multiRollDetail',
                    plugin_event.bot_info.hash
                )
                for i in range(roll_times_count):
                    rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault)
                    rd_para.ruleMode = tmp_ruleMode
                    rd_para.roll()
                    if rd_para.resError == None:
                        tmp_resDetail_str = ''
                        tmp_resDetail_short_str = ''
                        if tmp_rd_para_str_show == None:
                            tmp_rd_para_str_show = rd_para_str
                        elif tmp_rd_para_str_show == '':
                            tmp_rd_para_str_show = rd_para_str
                        if 1 == flag_multiRollDetail \
                        and flag_roll_mode in ['r', 'rx']:
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
                                rd_para_str_new = tmp_rd_para_str_show
                            if len(tmp_resDetail_str) == 0 or len(tmp_resDetail_str) > 150:
                                if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                                    tmp_reply_str_1 = ', '.join(
                                        OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                    )
                                elif len(str(tmp_resInt_str)) > 100:
                                    tmp_reply_str_1 = str(tmp_resInt_str)[:50] + '...的天文数字'
                                else:
                                    tmp_reply_str_1 = str(tmp_resInt_str)
                            else:
                                if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                                    tmp_reply_str_1 = str(tmp_resDetail_str) + '=' + (', '.join(
                                        OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                                    ))
                                elif len(str(tmp_resInt_str)) > 50:
                                    tmp_reply_str_1 = str(tmp_resDetail_str) + '=' + str(tmp_resInt_str)[:50] + '...的天文数字'
                                else:
                                    tmp_reply_str_1 = str(tmp_resDetail_str) + '=' + str(tmp_resInt_str)
                            tmp_reply_str_1_list.append(tmp_reply_str_1)
                        else:
                            if not flag_begin:
                                tmp_reply_str_1 += ', '
                            else:
                                flag_begin = False
                            if len(str(rd_para.resInt)) > 10:
                                tmp_reply_str_1 += str(rd_para.resInt)[:10] + '...'
                            else:
                                tmp_reply_str_1 += str(rd_para.resInt)
                    else:
                        dictTValue['tResult'] = str(rd_para.resError)
                        dictTValue['tRollPara'] = str(rd_para_str)
                        tmp_reply_str_1 = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_para.resError, dictStrCustom, dictTValue)
                        tmp_reply_str_1 += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollErrorHelp'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str_1)
                        return
                if 1 == flag_multiRollDetail \
                and flag_roll_mode in ['r', 'rx']:
                    tmp_reply_str_1 = '\n'.join(tmp_reply_str_1_list)
                    if rd_para_str_new == None:
                        rd_para_str_new = rd_para_str
                    elif rd_para_str_new == '':
                        rd_para_str_new = rd_para_str
                    dictTValue['tRollResult'] = rd_para_str_new + '= \n' + tmp_reply_str_1
                else:
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

def trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue):
    # 如果是私聊消息，直接返回不执行自动群名片更新
    if plugin_event.plugin_info['func_type'] == 'private_message':
        return
    
    auto_sn_enabled = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_pc_id,
        userType = 'user',
        platform = tmp_pc_platform,
        userConfigKey = 'autoSnEnabled',
        botHash = plugin_event.bot_info.hash,
        default = False
    )
    if not auto_sn_enabled:
        return
    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
    if not tmp_pc_name:
        return
    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
        tmp_pc_id,
        tmp_pc_platform
    )
    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
        tmp_pcHash,
        tmp_hagID
    )
    tmp_template_name = None
    tmp_template_rule_name = None
    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
        tmp_pcHash,
        tmp_pc_name
    )
    tmp_template_rule_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateRuleKey(
        tmp_pcHash,
        tmp_pc_name
    )
    if tmp_template_name == None:
        tmp_template_name = 'default'
    if tmp_template_rule_name == None:
        tmp_template_rule_name = 'default'
    tmp_pc_card_snTitle = None
    sn_title = None
    tmp_Record = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
        pcHash = tmp_pcHash,
        pcCardName = tmp_pc_name,
        dataKey = 'noteRecord',
        resDefault = {}
    )
    tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
    if 'snTitle' in tmp_template:
        tmp_pc_card_snTitle = tmp_template['snTitle']
        sn_title = tmp_pc_card_snTitle
    if '名片' in tmp_Record:
        sn_title = tmp_Record['名片']
    if not sn_title:
        sn_title = '{tName} hp{HP}/{HPMAX} san{SAN}/{SANMAX} dex{DEX}'
    sn_title = OlivaDiceCore.msgReplyModel.getNoteFormat(
        data = sn_title,
        pcHash = tmp_pcHash,
        hagID = tmp_hagID
    )
    plugin_event.set_group_card(
        group_id = plugin_event.data.group_id,
        user_id = tmp_pc_id,
        card = sn_title,
        host_id = plugin_event.data.host_id
    )

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

    # 敏感词检测
    message = OlivaDiceCore.censorAPI.doCensorReplaceOlivOSSafe(
        botHash = botHash,
        msg = message
    )

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

def pluginSend(plugin_event:OlivOS.API.Event, send_type, target_id, message:str, host_id = None):
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

    # 敏感词检测
    message = OlivaDiceCore.censorAPI.doCensorReplaceOlivOSSafe(
        botHash = botHash,
        msg = message
    )

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

def getExpression(
    data,
    reverse = False,
    valueTable = None,
    pcCardRule = None,
    flagDynamic:'bool|None' = False,
    ruleMode:str = 'default'
):
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
            if flag_not_hit and data[tmp_total_offset].isdecimal():
                flag_not_hit = False
            if flag_not_hit and not reverse:
                for idx in range(tmp_total_offset, len(data)):
                    if valueTable != None \
                    and data[tmp_total_offset:idx + 1].upper() in valueTable:
                        tmp_offset_len = idx - tmp_total_offset + 1
                        flag_not_hit = False
                        flag_value = True
                    elif pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial \
                    and data[tmp_total_offset:idx + 1].upper() in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[pcCardRule]:
                        tmp_offset_len = idx - tmp_total_offset + 1
                        flag_not_hit = False
                        flag_value = True
                if (not flag_not_hit) \
                and (data[tmp_total_offset:tmp_total_offset + tmp_offset_len] in OlivaDiceCore.onedice.dictOperationPriority \
                or (ruleMode in OlivaDiceCore.onedice.dictRuleOperationPriority \
                and data[tmp_total_offset:tmp_total_offset + tmp_offset_len] in OlivaDiceCore.onedice.dictRuleOperationPriority[ruleMode]) \
                or data[tmp_total_offset:tmp_total_offset + tmp_offset_len] in OlivaDiceCore.onedice.listOperationSub):
                    flag_value = False
            for range_this in reversed(range(1, OlivaDiceCore.onedice.lenOperationMax + 1)):
                if flag_not_hit \
                and tmp_total_offset + range_this <= len(data) \
                and (data[tmp_total_offset:tmp_total_offset + range_this] in OlivaDiceCore.onedice.dictOperationPriority \
                or (ruleMode in OlivaDiceCore.onedice.dictRuleOperationPriority \
                and data[tmp_total_offset:tmp_total_offset + range_this] in OlivaDiceCore.onedice.dictRuleOperationPriority[ruleMode])):
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
                # 在显示时处理格式转换
                tmp_display_str = tmp_output_str_reg
                # 普通变量
                for var_name in valueTable:
                    var_value = valueTable[var_name]
                    tmp_display_str = tmp_display_str.replace(
                        '{%s}' % var_name,
                        '%s(%s)' % (var_name, str(var_value))
                    )
                # special变量
                potential_vars = re.findall(r'\{([^}]+)\}', tmp_display_str)
                for var_name in potential_vars:
                    if OlivaDiceCore.skillCheck.isSpecialSkill(var_name, pcCardRule):
                        special_value = OlivaDiceCore.skillCheck.getSpecialSkill(var_name, pcCardRule, valueTable or {})
                        if special_value is not None:
                            tmp_display_str = tmp_display_str.replace(
                                '{%s}' % var_name,
                                '%s(%s)' % (var_name, str(special_value))
                            )
            
                tmp_output_str_1 = tmp_display_str
                if flagDynamic is True:
                    # 动态解析时仍使用原始格式
                    tmp_parse_str = tmp_output_str_reg
                    for i in range(100):
                        tmp_parse_str_old = tmp_parse_str
                        for value_this in valueTable:
                            if '{%s}' % value_this in tmp_parse_str:
                                raw_value = valueTable[value_this]
                                value_str = str(raw_value)
                                # 负数加括号
                                if isinstance(raw_value, int) and raw_value < 0:
                                    value_str = f"({value_str})"
                                tmp_parse_str = tmp_parse_str.replace(
                                    '{%s}' % value_this,
                                    '(%s)' % getExpression(
                                        data = value_str,
                                        reverse = reverse,
                                        valueTable = valueTable,
                                        pcCardRule = pcCardRule,
                                        flagDynamic = False
                                    )[0]
                                )
                        tmp_parse_str = OlivaDiceCore.skillCheck.getSpecialSkillReplace(
                            tmp_parse_str,
                            pcCardRule,
                            valueTable
                        )
                        if tmp_parse_str_old == tmp_parse_str:
                            break
                    tmp_output_str_1 = tmp_parse_str
                elif flagDynamic is False:
                    tmp_output_str_1 = OlivaDiceCore.skillCheck.getSpecialSkillReplace(
                        tmp_output_str_reg,
                        pcCardRule,
                        valueTable
                    )
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
            if data[tmp_total_offset].isdecimal():
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
            if data[tmp_total_offset].isdecimal():
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

def isMatchWordStart(data, key, ignoreCase=True, fullMatch=False, isCommand=False):
    tmp_output = False
    flag_skip = False
    tmp_data = data.strip()
    tmp_keys = [key] if isinstance(key, str) else key
    if isCommand:
        if 'replyContextFliter' in OlivaDiceCore.crossHook.dictHookList:
            for k in tmp_keys:
                if k in OlivaDiceCore.crossHook.dictHookList['replyContextFliter']:
                    tmp_output = False
                    flag_skip = True
                    break
    if not flag_skip:
        if ignoreCase:
            tmp_data = tmp_data.lower()
            tmp_keys = [k.lower() for k in tmp_keys]
        # 按长度从长到短排序
        tmp_keys_sorted = sorted(tmp_keys, key=lambda x: len(x), reverse=True)
        for tmp_key in tmp_keys_sorted:
            if not fullMatch and len(tmp_data) >= len(tmp_key):
                if tmp_data[:len(tmp_key)] == tmp_key:
                    tmp_output = True
                    break
            elif fullMatch and tmp_data == tmp_key:
                tmp_output = True
                break
    return tmp_output

def getMatchWordStartRight(data, key, ignoreCase=True):
    tmp_output_str = ''
    tmp_data = data
    tmp_keys = [key] if isinstance(key, str) else key
    if ignoreCase:
        tmp_data = tmp_data.lower()
        tmp_keys = [k.lower() for k in tmp_keys]
    # 按长度从长到短排序
    tmp_keys_sorted = sorted(tmp_keys, key=lambda x: len(x), reverse=True)
    for tmp_key in tmp_keys_sorted:
        if len(tmp_data) > len(tmp_key):
            if tmp_data[:len(tmp_key)] == tmp_key:
                tmp_output_str = data[len(tmp_key):]
                break
    return tmp_output_str

def isdigitSafe(data):
    if data in '0123456789':
        return True
    return False

def parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin):
    """
    解析消息中的@用户并检查权限
    返回: is_at, at_user_id, cleaned_message_str
    """
    flag_is_from_master = valDict['flag_is_from_master']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    at_user_id = None
    new_tmp_reast_str_parts = []
    is_at = False
    
    for part in tmp_reast_str_para.data:
        if isinstance(part, OlivOS.messageAPI.PARA.at):
            at_user_id = part.data['id']
            tmp_userName01 = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = at_user_id,
                userType = 'user',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash
            )
            plres = plugin_event.get_stranger_info(at_user_id)
            if plres['active']:
                dictTValue['tUserName01'] = plres['data']['name']
            else:
                dictTValue['tUserName01'] = tmp_userName01
            is_at = True
        else:
            if isinstance(part, OlivOS.messageAPI.PARA.text):
                new_tmp_reast_str_parts.append(part.data['text'])
    
    if is_at:
        # 检查发送者是否为管理员或群主
        if not (flag_is_from_group_admin or flag_is_from_master):
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strAtOtherPermissionDenied'], 
                dictTValue
            )
            replyMsg(plugin_event, tmp_reply_str)
            return (True, None, None)  # 权限不足
    
    # 返回解析结果
    cleaned_message = ''.join(new_tmp_reast_str_parts).strip()
    return is_at, at_user_id, cleaned_message

def to_half_width(res):
    """
    将字符串中的全角符号转换为半角符号
    """
    result = []
    for char in res:
        code = ord(char)
        # 全角空格
        if code == 0x3000:
            code = 0x0020
        # 全角字符（除空格外）
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        result.append(chr(code))
    return ''.join(result)
