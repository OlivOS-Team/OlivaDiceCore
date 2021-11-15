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
                                dictTValue['tResult'] = dictStrCustom['strBotAddGroupNoticeIgnoreResult'].format(**dictTValue)
                            elif flag_enable == 1:
                                dictTValue['tResult'] = dictStrCustom['strAccept'].format(**dictTValue)
                            tmp_reply_str = dictStrCustom['strBotAddGroupNotice'].format(**dictTValue)
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
                                dictTValue['tResult'] = dictStrCustom['strIgnore'].format(**dictTValue)
                            elif flag_enable == 1:
                                dictTValue['tResult'] = dictStrCustom['strAccept'].format(**dictTValue)
                            tmp_reply_str = dictStrCustom['strBotAddFriendNotice'].format(**dictTValue)
                            OlivaDiceCore.msgReply.sendMsgByEvent(plugin_event, tmp_reply_str, noticeGroupList_this[0], 'group')

def isInMasterList(bot_hash, user_hash):
    res = False
    for bot_hash_this in [bot_hash, 'unity']:
        if bot_hash_this in OlivaDiceCore.console.dictConsoleSwitch:
            if 'masterList' in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]:
                if type(OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['masterList']) == list:
                    for masterList_this in OlivaDiceCore.console.dictConsoleSwitch[bot_hash_this]['masterList']:
                        if type(masterList_this) == list and len(masterList_this) == 2:
                            if OlivaDiceCore.userConfig.getUserHash(masterList_this[0], 'user', masterList_this[1]) == user_hash:
                                res = True
    return res
