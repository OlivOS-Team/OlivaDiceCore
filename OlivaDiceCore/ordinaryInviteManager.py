# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   ordinaryInviteManager.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import hashlib

def unity_group_invite_request(plugin_event, Proc):
    flag_enable_default = 1
    flag_enable = 1
    flag_enable = OlivaDiceCore.console.getConsoleSwitchByHash('autoAcceptGroupAdd', 'unity')
    flag_enable = OlivaDiceCore.console.getConsoleSwitchByHash('autoAcceptGroupAdd', plugin_event.bot_info.hash)
    if flag_enable == None:
        flag_enable = flag_enable_default

    if flag_enable == 1:
        tmp_data = plugin_event.set_group_add_request(plugin_event.data.flag, 'invite', True, '')

    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    for bot_hash_this in [plugin_event.bot_info.hash]:
        if bot_hash_this in OlivaDiceCore.console.dictConsoleSwitch:
            if 'noticeGroupList' in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]:
                if type(OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['noticeGroupList']) == list:
                    for noticeGroupList_this in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['noticeGroupList']:
                        if type(noticeGroupList_this) == list and len(noticeGroupList_this) == 2:
                            dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                            dictTValue['tInvaterId'] = str(plugin_event.data.user_id)
                            dictTValue['tComment'] = plugin_event.data.comment
                            if flag_enable == 0:
                                dictTValue['tAcceptCommand'] = '.master accept %s' % (str(plugin_event.data.flag),)
                                dictTValue['tResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAddGroupNoticeIgnoreResult'], dictTValue)
                            elif flag_enable == 1:
                                dictTValue['tResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strAccept'], dictTValue)
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAddGroupNotice'], dictTValue)
                            OlivaDiceCore.msgReply.sendMsgByEvent(plugin_event, tmp_reply_str, noticeGroupList_this[0], 'group')

def unity_friend_add_request(plugin_event, Proc):
    flag_enable_default = 1
    flag_enable = 1
    flag_enable = OlivaDiceCore.console.getConsoleSwitchByHash('autoAcceptFriendAdd', 'unity')
    flag_enable = OlivaDiceCore.console.getConsoleSwitchByHash('autoAcceptFriendAdd', plugin_event.bot_info.hash)
    if flag_enable == None:
        flag_enable = flag_enable_default

    if flag_enable == 1:
        tmp_data = plugin_event.set_friend_add_request(plugin_event.data.flag, True, '')

    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    for bot_hash_this in [plugin_event.bot_info.hash]:
        if bot_hash_this in OlivaDiceCore.console.dictConsoleSwitch:
            if 'noticeGroupList' in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]:
                if type(OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['noticeGroupList']) == list:
                    for noticeGroupList_this in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['noticeGroupList']:
                        if type(noticeGroupList_this) == list and len(noticeGroupList_this) == 2:
                            dictTValue['tUserId'] = str(plugin_event.data.user_id)
                            dictTValue['tComment'] = plugin_event.data.comment
                            if flag_enable == 0:
                                dictTValue['tResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strIgnore'], dictTValue)
                            elif flag_enable == 1:
                                dictTValue['tResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strAccept'], dictTValue)
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBotAddFriendNotice'], dictTValue)
                            OlivaDiceCore.msgReply.sendMsgByEvent(plugin_event, tmp_reply_str, noticeGroupList_this[0], 'group')

def isInMasterList(bot_hash, user_hash):
    res = False
    for bot_hash_this in [bot_hash]:
        if bot_hash_this in OlivaDiceCore.console.dictConsoleSwitch:
            if 'masterList' in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]:
                if type(OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['masterList']) == list:
                    for masterList_this in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['masterList']:
                        if type(masterList_this) == list and len(masterList_this) == 2:
                            if OlivaDiceCore.userConfig.getUserHash(masterList_this[0], 'user', masterList_this[1]) == user_hash:
                                res = True
    return res


def unity_group_member_increase(plugin_event, Proc):
    replyMsg = OlivaDiceCore.msgReply.replyMsg
    tmp_hagID = str(plugin_event.data.group_id)
    fake_plugin_event = OlivaDiceCore.msgEvent.getReRxEvent_group_message(plugin_event, '[加群]')
    if fake_plugin_event.data.host_id != None:
        tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
    else:
        tmp_hagID = str(plugin_event.data.group_id)
    # 检查是否是机器人自己加入群聊
    new_member_id = plugin_event.data.user_id
    # 计算新成员的 bot hash
    hash_tmp = hashlib.new('md5')
    hash_tmp.update(str(new_member_id).encode(encoding='UTF-8'))
    hash_tmp.update(str(plugin_event.bot_info.platform['sdk']).encode(encoding='UTF-8'))
    hash_tmp.update(str(plugin_event.bot_info.platform['platform']).encode(encoding='UTF-8'))
    new_member_hash = hash_tmp.hexdigest()
    # 如果是机器人自己加入群聊
    if new_member_hash == plugin_event.bot_info.hash:
        record_bot_join = OlivaDiceCore.console.getConsoleSwitchByHash('recordBotJoinGroup', plugin_event.bot_info.hash)
        # 如果启用了记录,则记录时间
        if record_bot_join == 1:
            tmp_list_hit = []
            if fake_plugin_event.data.host_id != None:
                tmp_list_hit = [
                    [fake_plugin_event.data.host_id, 'host', plugin_event.platform['platform']],
                    ['%s|%s' % (str(fake_plugin_event.data.host_id), str(fake_plugin_event.data.group_id)), 'group', plugin_event.platform['platform']]
                ]
            else:
                tmp_list_hit = [
                    [fake_plugin_event.data.group_id, 'group', plugin_event.platform['platform']]
                ]
            # 记录机器人加群时间
            OlivaDiceCore.userConfig.releaseUnityMsgCount(tmp_list_hit, plugin_event.bot_info.hash)
        # 发送入群欢迎消息
        dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
        dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
        dictGValue = OlivaDiceCore.msgCustom.dictGValue
        dictTValue.update(dictGValue)
        hello_msg = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strHello'], dictTValue)
        replyMsg(fake_plugin_event, hello_msg)
        return
    # 如果不是机器人自己,则处理 welcome 消息
    reply_msg = OlivaDiceCore.userConfig.getUserConfigByKey(
        userConfigKey = 'welcomeMsg',
        botHash = plugin_event.bot_info.hash,
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform']
    )
    if reply_msg != None:
        # 支持 AT 新成员
        dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
        dictGValue = OlivaDiceCore.msgCustom.dictGValue
        dictTValue.update(dictGValue)
        at_para = OlivOS.messageAPI.PARA.at(str(new_member_id))
        at_str = at_para.get_string_by_key('CQ')
        dictTValue['tAtNewMember'] = at_str
        dictTValue['tNewMemberId'] = str(new_member_id)
        # 获取新成员名称
        new_member_name = OlivaDiceCore.msgReplyModel.get_user_name(plugin_event, new_member_id)
        dictTValue['tNewMemberName'] = new_member_name
        formatted_reply_msg = OlivaDiceCore.msgCustomManager.formatReplySTR(reply_msg, dictTValue)
        replyMsg(fake_plugin_event, formatted_reply_msg)
