# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReplyModel.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivaDiceCore
import OlivOS

import time
import hashlib
import re
import copy
import math

contextFeq = 0.1

def get_user_name(plugin_event, user_id):
    """
    获取用户名称
    """
    user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = user_id,
        userType = 'user',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'userName',
        botHash = plugin_event.bot_info.hash
    )
    # 没获取到再用api获取
    if user_name == None:
        plres = plugin_event.get_stranger_info(user_id)
        if plres['active']:
            user_name = plres['data']['name']
        else:
            user_name = f'用户{user_id}'
    return user_name

def op_list_get():
    return ['+', '-', '*', '/', '^']

def replyCONTEXT_fliter(tmp_reast_str):
    res = False
    if 'replyContextPrefixFliter' in OlivaDiceCore.crossHook.dictHookList:
        for key_this in OlivaDiceCore.crossHook.dictHookList['replyContextPrefixFliter']:
            if OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, key_this):
                res = True
    return res

def replyCONTEXT_regGet(plugin_event:OlivOS.API.Event, tmp_reast_str:str):
    res = False
    flagResult = False
    tmp_hagID = None
    tmp_bothash = plugin_event.bot_info.hash
    tmp_userID = plugin_event.data.user_id
    tmp_hash = contextRegHash([tmp_hagID, tmp_userID])
    if (
        tmp_bothash in OlivaDiceCore.crossHook.dictReplyContextReg
    ) and (
        tmp_hash in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash]
    ) and (
        'block' in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]
    ):
        if (
            'res' in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]
        ) and (
            OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]['res'] == None
        ):
            tmp_data_block = OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]['block']
            if type(tmp_data_block) == bool:
                res = OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]['block']
                flagResult = True
            elif type(tmp_data_block) == str:
                if tmp_data_block == 'allowCommand':
                    flag_is_command = False
                    [tmp_reast_str_tmp, flag_is_command] = OlivaDiceCore.msgReply.msgIsCommand(
                        tmp_reast_str,
                        OlivaDiceCore.crossHook.dictHookList['prefix']
                    )
                    if flag_is_command:
                        res = False
                        OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash].pop(tmp_hash)
                    else:
                        res = True
                        flagResult = True
                    time.sleep(contextFeq * 2)
                else:
                    res = True
            if flagResult:
                OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]['res'] = tmp_reast_str
        else:
            res = False
    return res

def contextRegHash(data:list):
    res = None
    hash_tmp = hashlib.new('md5')
    for data_this in data:
        if type(data_this) == str:
            hash_tmp.update(str(data_this).encode(encoding='UTF-8'))
    res = hash_tmp.hexdigest()
    return res

def replyCONTEXT_regWait(plugin_event:OlivOS.API.Event, flagBlock = True, hash:'str|None' = None):
    res = None
    tmp_hash = None
    tmp_bothash = plugin_event.bot_info.hash
    tmp_block = flagBlock
    if hash != None:
        tmp_hash = hash
    if tmp_bothash not in OlivaDiceCore.crossHook.dictReplyContextReg:
        OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash] = {}
    OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash] = {
        'hash': tmp_hash,
        'block': tmp_block,
        'res': None
    }
    feq = contextFeq
    count = 30 * int(1 / feq)
    while count > 0:
        count -= 1
        time.sleep(feq)
        if tmp_bothash in OlivaDiceCore.crossHook.dictReplyContextReg and tmp_hash in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash]:
            if 'res' in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash] and OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]['res'] != None:
                res = OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]['res']
                break
        else:
            break
    return res

def replySET_command(plugin_event, Proc, valDict):
    tmp_reast_str = valDict['tmp_reast_str']
    flag_is_from_master = valDict['flag_is_from_master']
    tmp_userID = valDict['tmp_userID']
    tmp_hagID = valDict['tmp_hagID']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    flag_is_from_group = valDict['flag_is_from_group']
    replyMsg = OlivaDiceCore.msgReply.replyMsg
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart

    tmp_user_platform = plugin_event.platform['platform']
    tmp_reply_str = None

    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'set')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    tmp_set_para = None
    tmp_set_D_right = None
    if tmp_reast_str == 'show':
        tmp_set_para = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = tmp_hagID,
            userType = 'group',
            platform = tmp_user_platform,
            userConfigKey = 'groupMainDice',
            botHash = plugin_event.bot_info.hash
        )
        if tmp_set_para != None:
            dictTValue['tResult'] = tmp_set_para
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowGroupMainDice'], dictTValue)
        else:
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShowGroupMainDiceNone'], dictTValue)
    elif isMatchWordStart(tmp_reast_str, 'coc', isCommand = True):
        if flag_is_from_group:
            tmp_user_platform = plugin_event.platform['platform']
            tmp_hag_id = tmp_hagID
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'coc')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip()
            tmp_switch_setcoc = None
            if tmp_reast_str.isdecimal():
                tmp_switch_setcoc = int(tmp_reast_str)
                if tmp_switch_setcoc not in [0, 1, 2, 3, 4, 5, 6, 7]:
                    tmp_switch_setcoc = None
            if tmp_switch_setcoc != None:
                tmp_templateName = 'COC7'
                tmp_templateRuleName = 'default'
                if tmp_switch_setcoc in [0, 1, 2, 3, 4, 5, 6]:
                    tmp_templateRuleName = 'C%s' % str(tmp_switch_setcoc)
                elif tmp_switch_setcoc == 7:
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
    elif isMatchWordStart(tmp_reast_str, 'rav', isCommand = True):
        if flag_is_from_group:
            tmp_user_platform = plugin_event.platform['platform']
            tmp_hag_id = tmp_hagID
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rav')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip()
            tmp_switch_setrav = None
            if tmp_reast_str.isdecimal():
                tmp_switch_setrav = int(tmp_reast_str)
                if tmp_switch_setrav not in [1, 2]:
                    tmp_switch_setrav = None
            if tmp_switch_setrav != None:
                tmp_ravRuleName = str(tmp_switch_setrav)
                OlivaDiceCore.userConfig.setUserConfigByKey(
                    userConfigKey = 'groupRavRule',
                    userConfigValue = tmp_ravRuleName,
                    botHash = plugin_event.bot_info.hash,
                    userId = tmp_hag_id,
                    userType = 'group',
                    platform = tmp_user_platform
                )
                dictTValue['tRavRuleName'] = tmp_ravRuleName
                if tmp_ravRuleName in OlivaDiceCore.msgCustom.dictSetRAVDetail:
                    dictTValue['tLazyResult'] = ':\n%s' % OlivaDiceCore.msgCustom.dictSetRAVDetail[tmp_ravRuleName]
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSetGroupRavRule'], dictTValue)
            else:
                OlivaDiceCore.userConfig.setUserConfigByKey(
                    userConfigKey = 'groupRavRule',
                    userConfigValue = None,
                    botHash = plugin_event.bot_info.hash,
                    userId = tmp_hag_id,
                    userType = 'group',
                    platform = tmp_user_platform
                )
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDelGroupRavRule'], dictTValue)
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
    elif isMatchWordStart(tmp_reast_str, 'dnd', fullMatch = True, isCommand = True):
        if flag_is_from_group:
            tmp_user_platform = plugin_event.platform['platform']
            tmp_hag_id = tmp_hagID
            tmp_switch_setcoc = None
            flag_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_hag_id,
                userType = 'group',
                platform = tmp_user_platform,
                userConfigKey = 'groupTemplate',
                botHash = plugin_event.bot_info.hash
            )
            flag_groupTemplateRule = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_hag_id,
                userType = 'group',
                platform = tmp_user_platform,
                userConfigKey = 'groupTemplateRule',
                botHash = plugin_event.bot_info.hash
            )
            if flag_groupTemplate not in ['DND5E']:
                tmp_templateName = 'DND5E'
                tmp_templateRuleName = 'default'
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
    elif isMatchWordStart(tmp_reast_str, ['temp','rule'], isCommand = True):
        if flag_is_from_group:
            flag_settemp_mode = 'settemp'
            tmp_templateName_input = 'default'
            tmp_templateRuleName_input = 'default'
            tmp_user_platform = plugin_event.platform['platform']
            tmp_hag_id = tmp_hagID
            if isMatchWordStart(tmp_reast_str, 'temp'):
                flag_settemp_mode = 'settemp'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'temp')
            elif isMatchWordStart(tmp_reast_str, 'rule'):
                flag_settemp_mode = 'setrule'
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'rule')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip()
            if flag_settemp_mode == 'settemp':
                tmp_templateName_input = tmp_reast_str
            elif flag_settemp_mode == 'setrule':
                flag_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hag_id,
                    userType = 'group',
                    platform = tmp_user_platform,
                    userConfigKey = 'groupTemplate',
                    botHash = plugin_event.bot_info.hash
                )
                if flag_groupTemplate != None:
                    tmp_templateName_input = flag_groupTemplate
                tmp_templateRuleName_input = tmp_reast_str
                if tmp_templateRuleName_input == '':
                    tmp_templateRuleName_input = 'default'
            if tmp_templateName_input == '' or OlivaDiceCore.pcCard.pcCardDataCheckTemplateKey(tmp_templateName_input, tmp_templateRuleName_input):
                if tmp_templateName_input != '':
                    tmp_templateName_input = OlivaDiceCore.pcCard.pcCardDataCheckTemplateKey(
                        tmp_templateName_input,
                        tmp_templateRuleName_input,
                        resMode = 'temp'
                    )
                    tmp_templateRuleName_input = OlivaDiceCore.pcCard.pcCardDataCheckTemplateKey(
                        tmp_templateName_input,
                        tmp_templateRuleName_input,
                        resMode = 'rule'
                    )
                    tmp_templateName = tmp_templateName_input
                    tmp_templateRuleName = tmp_templateRuleName_input
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
                if flag_settemp_mode == 'settemp':
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSetGroupTempError'], dictTValue)
                elif flag_settemp_mode == 'setrule':
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSetGroupTempRuleError'], dictTValue)
        else:
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strForGroupOnly'], dictTValue)
        replyMsg(plugin_event, tmp_reply_str)
        return
    else:
        if len(tmp_reast_str) > 0:
            if tmp_reast_str.isdigit():
                tmp_set_D_right = int(tmp_reast_str)
                tmp_set_para = '1D%d' % tmp_set_D_right
            else:
                tmp_set_para = tmp_reast_str
                tmp_set_para = tmp_set_para.upper()
                tmp_set_para_rd = OlivaDiceCore.onedice.RD(tmp_set_para)
                tmp_set_para_rd.roll()
                if tmp_set_para_rd.resError == None:
                    tmp_set_para_list = tmp_set_para.split('D')
                    if len(tmp_set_para_list) == 2:
                        if tmp_set_para_list[0].isdigit() and tmp_set_para_list[1].isdigit():
                            tmp_set_D_right = int(tmp_set_para_list[1])
                        elif tmp_set_para_list[0].isdigit() and tmp_set_para_list[1] == '':
                            tmp_set_D_right = 100
                            tmp_set_para = '%sD%d' % (
                                tmp_set_para_list[0],
                                tmp_set_D_right
                            )
                        elif tmp_set_para_list[0] == '' and tmp_set_para_list[1].isdigit():
                            tmp_set_D_right = int(tmp_set_para_list[1])
                            tmp_set_para = '1D%d' % (
                                tmp_set_D_right
                            )
                        elif tmp_set_para_list[0] == '' and tmp_set_para_list[1] == '':
                            tmp_set_D_right = 100
                            tmp_set_para = '1D%d' % (
                                tmp_set_D_right
                            )
                else:
                    tmp_set_para = None
        if tmp_set_para != None:
            OlivaDiceCore.userConfig.setUserConfigByKey(
                userConfigKey = 'groupMainDice',
                userConfigValue = tmp_set_para,
                botHash = plugin_event.bot_info.hash,
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_user_platform
            )
            OlivaDiceCore.userConfig.setUserConfigByKey(
                userConfigKey = 'groupMainDiceDRight',
                userConfigValue = tmp_set_D_right,
                botHash = plugin_event.bot_info.hash,
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_user_platform
            )
            dictTValue['tResult'] = tmp_set_para
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strSetGroupMainDice'], dictTValue)
        else:
            OlivaDiceCore.userConfig.setUserConfigByKey(
                userConfigKey = 'groupMainDice',
                userConfigValue = None,
                botHash = plugin_event.bot_info.hash,
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_user_platform
            )
            OlivaDiceCore.userConfig.setUserConfigByKey(
                userConfigKey = 'groupMainDiceDRight',
                userConfigValue = tmp_set_D_right,
                botHash = plugin_event.bot_info.hash,
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_user_platform
            )
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strDelGroupMainDice'], dictTValue)
        OlivaDiceCore.userConfig.writeUserConfigByUserHash(
            userHash = OlivaDiceCore.userConfig.getUserHash(
                userId = tmp_hagID,
                userType = 'group',
                platform = tmp_user_platform
            )
        )
    if tmp_reply_str not in ['', None]:
        replyMsg(plugin_event, tmp_reply_str)


def replyRR_command(plugin_event, Proc, valDict):
    tmp_reast_str = valDict['tmp_reast_str']
    flag_is_from_master = valDict['flag_is_from_master']
    tmp_userID = valDict['tmp_userID']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    replyMsg = OlivaDiceCore.msgReply.replyMsg

    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'rr')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    tmp_reast_str = tmp_reast_str.rstrip(' ')
    flag_mode = '默认'
    tmp_user_platform = plugin_event.platform['platform']
    if len(tmp_reast_str) > 0:
        if not flag_is_from_master and tmp_reast_str in ['debug']:
            pass
        else:
            flag_mode = tmp_reast_str
    tmp_RDData_str = OlivaDiceCore.onediceOverride.RDDataFormat(
        data = OlivaDiceCore.onediceOverride.getRDDataUser(
            botHash = plugin_event.bot_info.hash,
            userId = tmp_userID,
            platform = tmp_user_platform
        ),
        mode = flag_mode
    )
    tmp_reply_str = None
    if tmp_RDData_str != None:
        dictTValue['tRollFormatType'] = flag_mode
        tmp_RDDataIntUser = OlivaDiceCore.onediceOverride.getRDDataIntUser(
            botHash = plugin_event.bot_info.hash,
            userId = tmp_userID,
            platform = tmp_user_platform
        )
        if type(tmp_RDDataIntUser) == int:
            tmp_RDDataIntUser = str(tmp_RDDataIntUser)
        elif type(tmp_RDDataIntUser) == str:
            tmp_RDDataIntUser = str(tmp_RDDataIntUser)
        elif type(tmp_RDDataIntUser) == list:
            tmp_RDDataIntUser = ', '.join([str(tmp_RDDataIntUser_this) for tmp_RDDataIntUser_this in tmp_RDDataIntUser])
        dictTValue['tRollResult'] = '%s=%s=%s' % (
            OlivaDiceCore.onediceOverride.getRDDataRawUser(
                botHash = plugin_event.bot_info.hash,
                userId = tmp_userID,
                platform = tmp_user_platform
            ),
            tmp_RDData_str,
            str(tmp_RDDataIntUser)
        )
        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollRecord'], dictTValue)
    if tmp_reply_str != None:
        replyMsg(plugin_event, tmp_reply_str)


dictSkillCheckRank = {
    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS: 5,
    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS: 4,
    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS: 3,
    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS: 2,
    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL: 1,
    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL: 0
}

def get_SkillCheckResult(tmpSkillCheckType, dictStrCustom, dictTValue, pcHash = None, pcCardName = None, user_id = None, skill_name = None, platform = None, botHash = None, hagId = None):
    res = dictStrCustom['strPcSkillCheckError']
    # 存储hiy统计数据
    if pcHash and pcCardName:
        hiy_key = None
        if tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS:
            hiy_key = '普通成功'
        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
            hiy_key = '困难成功'
        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
            hiy_key = '极难成功'
        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
            hiy_key = '大成功'
        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
            hiy_key = '失败'
        elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
            hiy_key = '大失败'
        
        if hiy_key:
            OlivaDiceCore.pcCard.pcCardDataSetHiyKey(pcHash, pcCardName, hiy_key, 1)
        
        # 记录技能检定结果到 logStatus
        if user_id and skill_name and platform and botHash and hagId:
            is_success = tmpSkillCheckType in [
                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS,
                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS,
                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
                OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
            ]
            record_skill_check_result(
                user_id, pcCardName, skill_name, is_success, platform, botHash, hagId
            )
    if tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckSucceed'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckHardSucceed'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckExtremeHardSucceed'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatSucceed'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFailed'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckGreatFailed'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_01:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate01'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_02:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate02'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_03:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate03'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_04:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate04'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_05:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate05'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_06:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate06'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_07:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate07'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_08:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate08'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_09:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate09'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_10:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate10'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_11:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckFate11'], dictTValue)
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckNope'], dictTValue)
    else:
        res = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSkillCheckError'], dictTValue)
    return res

def get_SkillCheckError(resError, dictStrCustom, dictTValue):
    if resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_GENERATE_FATAL:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError01'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_COMPLETE_FATAL:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError02'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_RAW_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError03'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_CHILD_PARA_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError04'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.INPUT_NODE_OPERATION_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError05'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_OPERATION_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError06'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_STACK_EMPTY:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError07'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_LEFT_VAL_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError08'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_RIGHT_VAL_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError09'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_SUB_VAL_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError10'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.NODE_EXTREME_VAL_INVALID:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError11'], dictTValue)
    elif resError == OlivaDiceCore.onedice.RD.resErrorType.UNKNOWN_REPLACE_FATAL:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollError12'], dictTValue)
    else:
        tmp_reply_str_1 = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollErrorUnknown'], dictTValue)
    return tmp_reply_str_1

def record_skill_check_result(user_id, pc_name, skill_name, is_success, platform, botHash, hagId):
    """
    记录技能检定结果到logStatus
    """
    try:
        # 获取logStatus
        log_status = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId=hagId,
            userType='group',
            platform=platform,
            userConfigKey='logStatus',
            botHash=botHash
        )
        
        if log_status is None:
            return
        
        # 获取当前活跃日志的UUID
        log_enable = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId=hagId,
            userType='group',
            platform=platform,
            userConfigKey='logEnable',
            botHash=botHash
        )
        
        if not log_enable:
            return
        
        log_active_name = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId=hagId,
            userType='group',
            platform=platform,
            userConfigKey='logActiveName',
            botHash=botHash
        )
        
        if not log_active_name:
            return
        
        log_name_dict = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId=hagId,
            userType='group',
            platform=platform,
            userConfigKey='logNameDict',
            botHash=botHash
        )
        
        if not log_name_dict or log_active_name not in log_name_dict:
            return
        
        log_uuid = log_name_dict[log_active_name]
        
        # 确保UUID条目存在
        if log_uuid not in log_status:
            log_status[log_uuid] = {}
        
        # 计算用户哈希
        user_hash = OlivaDiceCore.userConfig.getUserHash(user_id, 'user', platform)
        
        # 确保用户条目存在
        if user_hash not in log_status[log_uuid]:
            log_status[log_uuid][user_hash] = {
                'id': str(user_id),
                '人物卡': {}
            }
        
        # 确保人物卡条目存在
        if pc_name not in log_status[log_uuid][user_hash]['人物卡']:
            log_status[log_uuid][user_hash]['人物卡'][pc_name] = {
                '成功': {},
                '失败': {}
            }
        
        # 将技能名转换为主键名
        pc_hash = OlivaDiceCore.pcCard.getPcHash(user_id, platform)
        main_skill_name = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(pc_hash, skill_name, flagShow=False, hagId=hagId)
        
        # 记录结果
        result_key = '成功' if is_success else '失败'
        if main_skill_name not in log_status[log_uuid][user_hash]['人物卡'][pc_name][result_key]:
            log_status[log_uuid][user_hash]['人物卡'][pc_name][result_key][main_skill_name] = 0
        log_status[log_uuid][user_hash]['人物卡'][pc_name][result_key][main_skill_name] += 1
        
        # 更新logStatus
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userId=hagId,
            userType='group',
            platform=platform,
            userConfigKey='logStatus',
            userConfigValue=log_status,
            botHash=botHash
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()

def difficulty_analyze(res):
    difficulty = None
    if OlivaDiceCore.msgReply.isMatchWordStart(res, ['困难成功', '困难']):
        difficulty = '困难'
        res = OlivaDiceCore.msgReply.getMatchWordStartRight(res, ['困难成功', '困难']).strip()
    elif OlivaDiceCore.msgReply.isMatchWordStart(res, ['极难成功', '极限成功', '极难', '极限']):
        difficulty = '极难'
        res = OlivaDiceCore.msgReply.getMatchWordStartRight(res, ['极难成功', '极限成功', '极难', '极限']).strip()
    elif OlivaDiceCore.msgReply.isMatchWordStart(res, '大成功'):
        difficulty = '大成功'
        res = OlivaDiceCore.msgReply.getMatchWordStartRight(res, '大成功').strip()
    res = res.strip()
    return difficulty, res

def replyRAV_command(plugin_event, Proc, valDict):
    tmp_reast_str = valDict['tmp_reast_str']
    flag_is_from_master = valDict['flag_is_from_master']
    tmp_userID = valDict['tmp_userID']
    tmp_hagID = valDict['tmp_hagID']
    tmp_platform = valDict['tmp_platform']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    dictTValue['tUserName'] = plugin_event.data.sender['name']
    dictTValue['tUserName01'] = "对方"
    replyMsg = OlivaDiceCore.msgReply.replyMsg

    if tmp_hagID == None:
        return

    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'rav')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    tmp_reast_str = tmp_reast_str.rstrip(' ')
    tmp_skill_name_0 = None
    tmp_skill_name_1 = None
    tmp_skill_value_0 = None
    tmp_skill_value_1 = None
    difficulty_0 = None
    difficulty_1 = None
    tmp_userID_1 = None
    tmp_pc_name_0 = '用户'
    tmp_pc_name_1 = '用户'
    tmp_Template = None
    tmp_TemplateRuleName = 'default'
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    
    if len(tmp_reast_str_para.data) >= 2:
        if type(tmp_reast_str_para.data[-1]) == OlivOS.messageAPI.PARA.at:
            tmp_userID_1 = tmp_reast_str_para.data[-1].data['id']
            tmp_userName01 = get_user_name(plugin_event, tmp_userID_1)
            dictTValue['tUserName01'] = tmp_userName01
            # 提取所有文本部分并拼接
            text_parts = []
            for item in tmp_reast_str_para.data:
                if isinstance(item, OlivOS.messageAPI.PARA.text):
                    text_parts.append(item.data['text'].strip())
            full_text_str = ' '.join(filter(None, text_parts))
            is_rav = False
            skills = []
            values = []
            # 解析技能和数值
            remaining_str = full_text_str
            while remaining_str:
                # 提取直到数字或空格的技能名部分
                skill_part, rest = OlivaDiceCore.msgReply.getToNumberPara(remaining_str)
                skill_part = skill_part.strip()
                if skill_part:
                    skills.append(skill_part)
                # 提取数字部分
                value_part, rest = OlivaDiceCore.msgReply.getNumberPara(rest)
                value_part = value_part.strip()
                if value_part:
                    values.append(int(value_part))
                remaining_str = rest.strip()
            # 解析难度
            difficulties = [None, None]
            for i, skill in enumerate(skills):
                if i >= 2: break
                difficulties[i], skills[i] = difficulty_analyze(skill)
            difficulty_0 = difficulties[0]
            difficulty_1 = difficulties[1] if difficulties[1] is not None else difficulties[0]
            # 进行分配技能和数值
            num_skills = len(skills)
            num_values = len(values)
            if num_skills == 1:
                # .rav 技能名1 @B -> A和B都用技能1，数值待查
                # .rav 技能名1 50 @B -> A用技能1 50，B用技能1 待查
                # .rav 技能名1 50 60 @B -> A用技能1 50，B用技能1 60
                tmp_skill_name_0 = skills[0]
                tmp_skill_name_1 = skills[0]
                if num_values == 1:
                    tmp_skill_value_0 = values[0]
                elif num_values >= 2:
                    tmp_skill_value_0 = values[0]
                    tmp_skill_value_1 = values[1]
                is_rav = True
            elif num_skills >= 2:
                # .rav 技能名1 技能名2 @B -> A用技能1，B用技能2，数值待查
                # .rav 技能名1 50 技能名2 @B -> A用技能1 50，B用技能2 待查
                # .rav 技能名1 50 技能名2 60 @B -> A用技能1 50，B用技能2 60
                tmp_skill_name_0 = skills[0]
                tmp_skill_name_1 = skills[1]
                if num_values == 1:
                    value_as_str = str(values[0])
                    # 如果技能名2的文本部分以数值结尾，则将其分配给技能2
                    if full_text_str.strip().endswith(value_as_str):
                        tmp_skill_value_1 = values[0]
                    else:
                        tmp_skill_value_0 = values[0]
                elif num_values >= 2:
                    tmp_skill_value_0 = values[0]
                    tmp_skill_value_1 = values[1]
                is_rav = True
            if is_rav:
                flag_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_platform,
                    userConfigKey = 'groupTemplate',
                    botHash = plugin_event.bot_info.hash
                )
                flag_groupTemplateRule = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_platform,
                    userConfigKey = 'groupTemplateRule',
                    botHash = plugin_event.bot_info.hash
                )
                flag_groupRavRule = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = tmp_platform,
                    userConfigKey = 'groupRavRule',
                    botHash = plugin_event.bot_info.hash
                )
                # 默认使用规则1（官方规则）
                if flag_groupRavRule is None:
                    flag_groupRavRule = '1'

                tmp_pcHash_0 = OlivaDiceCore.pcCard.getPcHash(tmp_userID, tmp_platform)
                tmp_pcHash_1 = OlivaDiceCore.pcCard.getPcHash(tmp_userID_1, tmp_platform)
                # 修正技能名
                if tmp_skill_name_0 is not None:
                    tmp_skill_name_0 = OlivaDiceCore.pcCard.fixName(tmp_skill_name_0, flagMode='skillName')
                if tmp_skill_name_1 is not None:
                    tmp_skill_name_1 = OlivaDiceCore.pcCard.fixName(tmp_skill_name_1, flagMode='skillName')
                # 如果未从命令中获取数值，则从角色卡中获取
                if tmp_skill_value_0 is None and tmp_skill_name_0 is not None:
                    tmp_skill_value_0 = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        tmp_pcHash_0, tmp_skill_name_0, hagId = tmp_hagID
                    )
                tmp_pc_name_0 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash_0, tmp_hagID)

                if tmp_skill_value_1 is None and tmp_skill_name_1 is not None:
                    tmp_skill_value_1 = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        tmp_pcHash_1, tmp_skill_name_1, hagId = tmp_hagID
                    )
                tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash_1, tmp_hagID)

                if tmp_pc_name_0 != None:
                    dictTValue['tName'] = tmp_pc_name_0
                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash_0, tmp_pc_name_0)
                    if flag_groupTemplate != None:
                        tmp_template_name = flag_groupTemplate
                    if tmp_template_name != None:
                        tmp_Template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                    tmp_template_rule_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateRuleKey(
                        tmp_pcHash_0, tmp_pc_name_0
                    )
                    if flag_groupTemplateRule != None:
                        tmp_template_rule_name = flag_groupTemplateRule
                    if tmp_template_rule_name != None:
                        tmp_TemplateRuleName = tmp_template_rule_name

                if tmp_pc_name_1 != None:
                    dictTValue['tName01'] = tmp_pc_name_1

                rd_para_str = '1D100'
                tmp_customDefault = None
                if tmp_Template != None:
                    if 'mainDice' in tmp_Template:
                        rd_para_str = tmp_Template['mainDice']
                    if 'customDefault' in tmp_Template:
                        tmp_customDefault = tmp_Template['customDefault']

                rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_customDefault)
                rd_para.roll()
                tmpSkillCheckType = None
                dictRuleTempData = {
                    'roll': 0,
                    'skill': tmp_skill_value_0
                }
                if rd_para.resError == None:
                    if rd_para.resDetail == None or rd_para.resDetail == '':
                        dictTValue['tRollResult'] = '%s=%d' % (rd_para_str, rd_para.resInt)
                    else:
                        dictTValue['tRollResult'] = '%s=%s=%d' % (rd_para_str, rd_para.resDetail, rd_para.resInt)
                    dictRuleTempData = {
                        'roll': rd_para.resInt,
                        'skill': tmp_skill_value_0
                    }
                    tmpSkillCheckType, tmpSkillThreshold = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                        dictRuleTempData, tmp_Template, tmp_TemplateRuleName, difficulty_0
                    )
                    dictTValue['tSkillValue'] = str(tmp_skill_value_0) if not difficulty_0 else f'{tmpSkillThreshold}({str(tmp_skill_value_0)})'
                rd_para_1 = OlivaDiceCore.onedice.RD(rd_para_str, tmp_customDefault)
                rd_para_1.roll()
                tmpSkillCheckType_1 = None
                dictRuleTempData_1 = {
                    'roll': 0,
                    'skill': tmp_skill_value_1
                }
                if rd_para_1.resError == None:
                    if rd_para_1.resDetail == None or rd_para_1.resDetail == '':
                        dictTValue['tRollResult01'] = '%s=%d' % (rd_para_str, rd_para_1.resInt)
                    else:
                        dictTValue['tRollResult01'] = '%s=%s=%d' % (rd_para_str, rd_para_1.resDetail, rd_para_1.resInt)
                    dictRuleTempData_1 = {
                        'roll': rd_para_1.resInt,
                        'skill': tmp_skill_value_1
                    }
                    tmpSkillCheckType_1, tmpSkillThreshold_1 = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                        dictRuleTempData_1, tmp_Template, tmp_TemplateRuleName, difficulty_1
                    )
                    dictTValue['tSkillValue01'] = str(tmp_skill_value_1) if not difficulty_1 else f'{tmpSkillThreshold_1}({str(tmp_skill_value_1)})'
                flag_rav_type = 'x'
                if tmpSkillCheckType in dictSkillCheckRank and tmpSkillCheckType_1 in dictSkillCheckRank:
                    dictTValue['tSkillCheckReasult'] = get_SkillCheckResult(
                        tmpSkillCheckType, dictStrCustom, dictTValue,
                        pcHash=tmp_pcHash_0, pcCardName=tmp_pc_name_0,
                        user_id=tmp_userID, skill_name=tmp_skill_name_0,
                        platform=tmp_platform, botHash=plugin_event.bot_info.hash, hagId=tmp_hagID
                    )
                    dictTValue['tSkillCheckReasult01'] = get_SkillCheckResult(
                        tmpSkillCheckType_1, dictStrCustom, dictTValue,
                        pcHash=tmp_pcHash_1, pcCardName=tmp_pc_name_1,
                        user_id=tmp_userID_1, skill_name=tmp_skill_name_1,
                        platform=tmp_platform, botHash=plugin_event.bot_info.hash, hagId=tmp_hagID
                    )
                    if dictSkillCheckRank[tmpSkillCheckType] > dictSkillCheckRank[tmpSkillCheckType_1]:
                        flag_rav_type = '0'
                    elif dictSkillCheckRank[tmpSkillCheckType] < dictSkillCheckRank[tmpSkillCheckType_1]:
                        flag_rav_type = '1'
                    elif dictSkillCheckRank[tmpSkillCheckType] == dictSkillCheckRank[tmpSkillCheckType_1]:
                        # 难度相同时，根据规则判断
                        if flag_groupRavRule == '1':
                            # 规则1：官方规则 - 比较属性值，不比较骰点
                            if dictRuleTempData['skill'] > dictRuleTempData_1['skill']:
                                flag_rav_type = '0'
                            elif dictRuleTempData['skill'] < dictRuleTempData_1['skill']:
                                flag_rav_type = '1'
                            else:
                                # 属性值相同直接平局
                                flag_rav_type = '-'
                        else:
                            # 规则2：现行规则 - 先比较骰点，再比较属性值
                            if dictRuleTempData['roll'] < dictRuleTempData_1['roll']:
                                flag_rav_type = '0'
                            elif dictRuleTempData['roll'] > dictRuleTempData_1['roll']:
                                flag_rav_type = '1'
                            elif dictRuleTempData['roll'] == dictRuleTempData_1['roll']:
                                if dictRuleTempData['skill'] > dictRuleTempData_1['skill']:
                                    flag_rav_type = '0'
                                elif dictRuleTempData['skill'] < dictRuleTempData_1['skill']:
                                    flag_rav_type = '1'
                                elif dictRuleTempData['skill'] == dictRuleTempData_1['skill']:
                                    flag_rav_type = '-'
                if flag_rav_type == '0' and tmpSkillCheckType in [
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS,
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS,
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
                ]:
                    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_userID, tmp_platform)
                    tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name_0,
                        'enhanceList',
                        []
                    )
                    tmp_skipEnhance_list = []
                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name_0)
                    if tmp_template_name is not None:
                        tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                        if 'skillConfig' in tmp_template and 'skipEnhance' in tmp_template['skillConfig']:
                            if isinstance(tmp_template['skillConfig']['skipEnhance'], list):
                                tmp_skipEnhance_list = tmp_template['skillConfig']['skipEnhance']
                    if (tmp_skill_name_0.upper() not in tmp_enhanceList and 
                        tmp_skill_name_0.upper() not in tmp_skipEnhance_list):
                        tmp_enhanceList.append(tmp_skill_name_0.upper())
                        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                            tmp_pcHash,
                            tmp_pc_name_0,
                            'enhanceList',
                            tmp_enhanceList
                        )
                elif flag_rav_type == '1' and tmpSkillCheckType_1 in [
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS,
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS,
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
                    OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
                ]:
                    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_userID_1, tmp_platform)
                    tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        tmp_pcHash,
                        tmp_pc_name_1,
                        'enhanceList',
                        []
                    )
                    tmp_skipEnhance_list = []
                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name_1)
                    if tmp_template_name is not None:
                        tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                        if 'skillConfig' in tmp_template and 'skipEnhance' in tmp_template['skillConfig']:
                            if isinstance(tmp_template['skillConfig']['skipEnhance'], list):
                                tmp_skipEnhance_list = tmp_template['skillConfig']['skipEnhance']
                    if (tmp_skill_name_1.upper() not in tmp_enhanceList and 
                        tmp_skill_name_1.upper() not in tmp_skipEnhance_list):
                        tmp_enhanceList.append(tmp_skill_name_1.upper())
                        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                            tmp_pcHash,
                            tmp_pc_name_1,
                            'enhanceList',
                            tmp_enhanceList
                        )
                if tmp_pc_name_1 == None:
                    dictTValue['tName01'] = tmp_userName01
                dictTValue['tSkillName'] = tmp_skill_name_0 if not difficulty_0 else f'{tmp_skill_name_0}({difficulty_0})'
                dictTValue['tSkillName01'] = tmp_skill_name_1 if not difficulty_1 else f'{tmp_skill_name_1}({difficulty_1})'
                if flag_rav_type == '0':
                    dictTValue['tRAVResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRAVResult01'], dictTValue)
                elif flag_rav_type == '1':
                    dictTValue['tRAVResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRAVResult02'], dictTValue)
                elif flag_rav_type == '-':
                    dictTValue['tRAVResult'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRAVResult03'], dictTValue)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRAVShow'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            else:
                OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'rav')
    else:
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'rav')

def setPcNoteOrRecData(
    plugin_event,
    tmp_pc_id,
    tmp_pc_platform,
    tmp_hagID,
    dictTValue,
    dictStrCustom,
    keyName,
    tmp_key,
    tmp_value,
    flag_mode,
    enableFalse:bool = True,
    is_remove:bool = False
):
    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
        tmp_pc_id,
        tmp_pc_platform
    )
    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
        tmp_pcHash,
        tmp_hagID
    )
    if tmp_pc_name == None:
        tmp_pc_name = dictTValue['tName']
        tmp_pc_name = OlivaDiceCore.pcCard.fixName(tmp_pc_name)
        if not OlivaDiceCore.pcCard.checkPcName(tmp_pc_name):
            tmp_pc_name = '用户'
        if not OlivaDiceCore.pcCard.pcCardRebase(
            tmp_pcHash,
            tmp_pc_name,
            tmp_hagID
        ):
            return
    dictTValue['tName'] = tmp_pc_name
    tmp_mappingRecord = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
        pcHash = tmp_pcHash,
        pcCardName = tmp_pc_name,
        dataKey = keyName,
        resDefault = {}
    )
    
    # 处理删除操作
    if is_remove and tmp_key is not None:
        if tmp_key in tmp_mappingRecord:
            del tmp_mappingRecord[tmp_key]
            OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                pcHash = tmp_pcHash,
                pcCardName = tmp_pc_name,
                dataKey = keyName,
                dataContent = tmp_mappingRecord
            )
            if enableFalse:
                if flag_mode == 'rec':
                    dictTValue['tSkillName'] = tmp_key
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRecRm'], dictTValue)
                    OlivaDiceCore.msgReply.trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                else:
                    dictTValue['tSkillName'] = tmp_key
                    OlivaDiceCore.msgReply.trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcNoteRm'], dictTValue)
                    OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
        else:
            if enableFalse:
                if flag_mode == 'rec':
                    dictTValue['tSkillName'] = tmp_key
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcRecError'], dictTValue)
                    OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                else:
                    dictTValue['tSkillName'] = tmp_key
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcNoteError'], dictTValue)
                    OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
        return
    
    if tmp_key != None and tmp_value != None:
        # # 删除 rec 的合规检测
        # if flag_mode == 'rec':
        #     tmp_rd = OlivaDiceCore.onedice.RD(tmp_value)
        #     tmp_rd.roll()
        #     if tmp_rd.resError != None:
        #         if enableFalse:
        #             dictTValue['tResult'] = tmp_value
        #             tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetMapValueError'], dictTValue)
        #             OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
        #         return
        # 添加特殊技能检测
        tmp_pcCardRule = 'default'
        if tmp_pc_name is not None:
            tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform),
                tmp_pc_name
            )
            if tmp_pcCardRule_new:
                tmp_pcCardRule = tmp_pcCardRule_new
        
        special_skills = []
        if tmp_pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial:
            if tmp_key.upper() in [skill.upper() for skill in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[tmp_pcCardRule]]:
                special_skills.append(tmp_key)
        tmp_mappingRecord[tmp_key] = tmp_value
        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
            pcHash = tmp_pcHash,
            pcCardName = tmp_pc_name,
            dataKey = keyName,
            dataContent = tmp_mappingRecord
        )
        # 如果有特殊技能，添加提示
        if special_skills:
            dictTValue['tSpecialSkills'] = '、'.join([f'[{skill}]' for skill in special_skills])
            tmp_notice = OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strPcSetSpecialSkills'], dictTValue
            )
        else:
            tmp_notice = ''
        if enableFalse:
            OlivaDiceCore.msgReply.trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetSkillValue'], dictTValue)
            OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str + tmp_notice)
    elif tmp_key != None and tmp_value == None:
        if tmp_key in tmp_mappingRecord:
            tmp_value = tmp_mappingRecord[tmp_key]
            if enableFalse:
                dictTValue['tSkillName'] = tmp_key
                dictTValue['tSkillValue'] = tmp_value
                OlivaDiceCore.msgReply.trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcGetSingleSkillValue'], dictTValue)
                OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)

def replyRI_command(
    plugin_event,
    tmp_reast_str,
    tmp_pc_id,
    tmp_pc_platform,
    tmp_hagID,
    dictTValue,
    dictStrCustom,
    flag_reply = True
):
    # 支持多种分隔符: 逗号、分号、空格
    # 首先将所有分隔符统一替换为逗号
    tmp_reast_str_normalized = tmp_reast_str.replace('；', ',').replace(';', ',')
    # 对于空格分隔，需要更谨慎处理，避免破坏表达式内部的空格
    # 使用正则表达式来智能分割
    tmp_reast_str_list = re.split(r'[,;；]|\s{2,}', tmp_reast_str_normalized)
    
    result_list = []
    count = 1
    
    for tmp_reast_str_list_this in tmp_reast_str_list:
        tmp_reast_str_list_this = tmp_reast_str_list_this.strip(' ')
        if not tmp_reast_str_list_this:
            continue
        
        # 检查是否是批量生成格式: 5#敌人+3 或 1D3黄色敌人
        batch_match = re.match(r'^(\d+)#(.+)$', tmp_reast_str_list_this)
        dice_batch_match = re.match(r'^(\d+[dD]\d+)(.+)$', tmp_reast_str_list_this)
        
        if batch_match:
            # 批量生成模式: 5#敌人+3
            batch_count = int(batch_match.group(1))
            batch_content = batch_match.group(2).strip()
            # 传入 count 作为起始序号，并获取实际添加的数量
            process_batch_init(
                plugin_event, batch_count, batch_content, tmp_pc_id, 
                tmp_pc_platform, tmp_hagID, dictTValue, dictStrCustom, 
                result_list, count
            )
            # 批量添加只算1个条目（整体显示）
            count += 1
        elif dice_batch_match:
            # 骰子批量生成模式: 1D3黄色敌人
            dice_expr = dice_batch_match.group(1)
            batch_content = dice_batch_match.group(2).strip()
            
            # 投骰决定数量
            tmp_dice_rd = OlivaDiceCore.onedice.RD(dice_expr)
            tmp_dice_rd.roll()
            if tmp_dice_rd.resError == None:
                batch_count = tmp_dice_rd.resInt
                process_batch_init(
                    plugin_event, batch_count, batch_content, tmp_pc_id, 
                    tmp_pc_platform, tmp_hagID, dictTValue, dictStrCustom, 
                    result_list, count
                )
                # 批量添加只算1个条目（整体显示）
                count += 1
        else:
            # 普通单个处理
            added = process_single_init(
                plugin_event, tmp_reast_str_list_this, tmp_pc_id, 
                tmp_pc_platform, tmp_hagID, dictTValue, dictStrCustom, 
                result_list, count
            )
            if added:
                count += 1
            
    if flag_reply:
        dictTValue['tResult'] = '\n'.join(result_list)
        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitSet'], dictTValue)
        OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)


def process_batch_init(
    plugin_event, batch_count, batch_content, tmp_pc_id, 
    tmp_pc_platform, tmp_hagID, dictTValue, dictStrCustom, 
    result_list, start_count
):
    """处理批量先攻录入，返回实际添加的数量"""
    # 解析批量内容: 敌人+3 或 敌人-1
    # 支持: 名称+修正值 或 名称 (默认+0)
    advantage_mode = None
    tmp_value_modifier = '+0'
    tmp_base_name = batch_content
    
    # 检查是否有优势/劣势
    if batch_content.startswith('优势'):
        advantage_mode = 'advantage'
        batch_content = batch_content[2:].strip()
    elif batch_content.startswith('劣势'):
        advantage_mode = 'disadvantage'
        batch_content = batch_content[2:].strip()
    
    # 提取修正值
    modifier_match = re.search(r'([+\-*/^]\d+)$', batch_content)
    if modifier_match:
        tmp_value_modifier = modifier_match.group(1)
        tmp_base_name = batch_content[:modifier_match.start()].strip()
    else:
        tmp_base_name = batch_content.strip()
    
    # 生成字母序号: a, b, c, ... z, aa, ab, ... zz, aaa, aab, ...
    def get_letter_suffix(index):
        """
        将数字索引转换为字母序号
        0 -> a, 1 -> b, ..., 25 -> z
        26 -> aa, 27 -> ab, ..., 51 -> az
        52 -> ba, 53 -> bb, ..., 701 -> zz
        702 -> aaa, 703 -> aab, ...
        """
        letters = 'abcdefghijklmnopqrstuvwxyz'
        result = ''
        
        # 确定需要几位字母
        if index < 26:
            # 单字母: a-z
            return letters[index]
        elif index < 26 + 26 * 26:
            # 双字母: aa-zz
            index -= 26
            return letters[index // 26] + letters[index % 26]
        else:
            # 三字母及以上: aaa-zzz...
            index -= (26 + 26 * 26)
            # 计算需要的位数
            base = 26 * 26 * 26
            digits = 3
            while index >= base:
                index -= base
                digits += 1
                base *= 26
            
            # 转换为对应位数的字母
            for _ in range(digits):
                result = letters[index % 26] + result
                index //= 26
            return result
    
    result_values = []
    added_count = 0
    
    for i in range(batch_count):
        letter = get_letter_suffix(i)
        tmp_name = f"{tmp_base_name}{letter}"
        
        # 构建骰子表达式 - 使用 kh/kl
        if advantage_mode == 'advantage':
            # 优势: 投两次取高
            tmp_value = f'2D20kh{tmp_value_modifier}'
        elif advantage_mode == 'disadvantage':
            # 劣势: 投两次取低
            tmp_value = f'2D20kl{tmp_value_modifier}'
        else:
            # 普通投掷
            tmp_value = f'1D20{tmp_value_modifier}'
        
        # 投骰
        tmp_value_rd = OlivaDiceCore.onedice.RD(tmp_value)
        tmp_value_rd.roll()
        
        if tmp_value_rd.resError == None:
            tmp_value_final = tmp_value_rd.resInt
            result_values.append(tmp_value_final)
            
            # 保存到先攻列表
            setUserConfigForInit(
                tmp_hagID = tmp_hagID,
                tmp_pc_platform = tmp_pc_platform,
                bot_hash = plugin_event.bot_info.hash,
                config_key = 'groupInitList',
                init_name = tmp_name,
                init_value = tmp_value_final
            )
            setUserConfigForInit(
                tmp_hagID = tmp_hagID,
                tmp_pc_platform = tmp_pc_platform,
                bot_hash = plugin_event.bot_info.hash,
                config_key = 'groupInitParaList',
                init_name = tmp_name,
                init_value = tmp_value
            )
            setUserConfigForInit(
                tmp_hagID = tmp_hagID,
                tmp_pc_platform = tmp_pc_platform,
                bot_hash = plugin_event.bot_info.hash,
                config_key = 'groupInitUserList',
                init_name = tmp_name,
                init_value = {
                    'userId': tmp_pc_id,
                    'platform': tmp_pc_platform
                }
            )
            added_count += 1
    
    # 添加到结果列表 (批量显示)
    if result_values:
        dictTValue['tId'] = str(start_count)
        # 获取最后一个元素的字母后缀
        last_letter = get_letter_suffix(batch_count - 1)
        dictTValue['tSubName'] = f"{tmp_base_name}a_{last_letter}"
        dictTValue['tSubResult'] = f"{tmp_value_modifier}=({','.join(map(str, result_values))})"
        result_list.append(
            OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitShowNode'], dictTValue)
        )
    
    return added_count


def process_single_init(
    plugin_event, tmp_reast_str_list_this, tmp_pc_id, 
    tmp_pc_platform, tmp_hagID, dictTValue, dictStrCustom, 
    result_list, count
):
    """处理单个先攻录入，返回是否成功添加"""
    tmp_value = '0'
    tmp_name = None
    flag_para_mode = '-'
    advantage_mode = None
    
    # 检查是否有优势/劣势关键词
    if tmp_reast_str_list_this.startswith('优势'):
        advantage_mode = 'advantage'
        tmp_reast_str_list_this = tmp_reast_str_list_this[2:].strip()
    elif tmp_reast_str_list_this.startswith('劣势'):
        advantage_mode = 'disadvantage'
        tmp_reast_str_list_this = tmp_reast_str_list_this[2:].strip()
    
    if len(tmp_reast_str_list_this) > 0:
        if len(tmp_reast_str_list_this) > 1 and tmp_reast_str_list_this[0] in ['+', '-', '*', '/', '^']:
            flag_para_mode = '1'
            tmp_value = '0'
            tmp_op = tmp_reast_str_list_this[0]
            [tmp_value, tmp_reast_str_list_this] = OlivaDiceCore.msgReply.getNumberPara(tmp_reast_str_list_this[1:])
            
            # 应用优势/劣势 - 使用 kh/kl
            if advantage_mode == 'advantage':
                tmp_value = '2D20kh%s%s' % (tmp_op, tmp_value)
            elif advantage_mode == 'disadvantage':
                tmp_value = '2D20kl%s%s' % (tmp_op, tmp_value)
            else:
                tmp_value = '1D20%s%s' % (tmp_op, tmp_value)
            
            tmp_reast_str_list_this = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str_list_this)
        elif len(tmp_reast_str_list_this) > 1 and tmp_reast_str_list_this[0] in ['=']:
            flag_para_mode = '2'
            [tmp_value, tmp_reast_str_list_this] = OlivaDiceCore.msgReply.getExpression(tmp_reast_str_list_this[1:])
            tmp_reast_str_list_this = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str_list_this)
        elif tmp_reast_str_list_this[0].isdigit():
            flag_para_mode = '3'
            tmp_value = '0'
            [tmp_value, tmp_reast_str_list_this] = OlivaDiceCore.msgReply.getNumberPara(tmp_reast_str_list_this)
            tmp_reast_str_list_this = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str_list_this)
        else:
            # 检查是否是 "名称+修正值" 或 "名称-修正值" 的格式（如: 龙+8）
            modifier_match = re.match(r'^(.+?)([+\-]\d+)$', tmp_reast_str_list_this)
            if modifier_match:
                # 提取名称和修正值
                tmp_name = modifier_match.group(1).strip()
                modifier = modifier_match.group(2)
                flag_para_mode = '4'
                tmp_op = modifier[0]
                tmp_value = modifier[1:]
                
                # 应用优势/劣势
                if advantage_mode == 'advantage':
                    tmp_value = '2D20kh%s%s' % (tmp_op, tmp_value)
                elif advantage_mode == 'disadvantage':
                    tmp_value = '2D20kl%s%s' % (tmp_op, tmp_value)
                else:
                    tmp_value = '1D20%s%s' % (tmp_op, tmp_value)
                
                tmp_reast_str_list_this = ''  # 名称已经提取
        
        tmp_reast_str_list_this = tmp_reast_str_list_this.strip(' ')
        if tmp_reast_str_list_this == '':
            # 如果 tmp_name 还没有赋值（即 flag_para_mode != '4'），则使用角色卡
            if tmp_name is None:
                OlivaDiceCore.msgReplyModel.setPcNoteOrRecData(
                    plugin_event = plugin_event,
                    tmp_pc_id = tmp_pc_id,
                    tmp_pc_platform = tmp_pc_platform,
                    tmp_hagID = tmp_hagID,
                    dictTValue = dictTValue,
                    dictStrCustom = dictStrCustom,
                    keyName = 'mappingRecord',
                    tmp_key = '先攻',
                    tmp_value = tmp_value,
                    flag_mode = 'rec',
                    enableFalse = False
                )
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                    tmp_pcHash,
                    tmp_hagID
                )
                tmp_name = tmp_pc_name
        else:
            tmp_name = tmp_reast_str_list_this
            tmp_name = OlivaDiceCore.pcCard.fixName(tmp_name)
            if not OlivaDiceCore.pcCard.checkPcName(tmp_name):
                tmp_name = None
    
    tmp_value_final = None
    display_detail = None
    
    if tmp_value:
        # 使用 onedice 直接处理 kh/kl
        tmp_value_rd = OlivaDiceCore.onedice.RD(tmp_value)
        tmp_value_rd.roll()
        if tmp_value_rd.resError == None:
            tmp_value_final = tmp_value_rd.resInt
            # 获取详细的投掷过程字符串
            if tmp_value_rd.resDetail != None:
                display_detail = tmp_value_rd.resDetail
    
    if tmp_name != None and tmp_value_final != None:
        setUserConfigForInit(
            tmp_hagID = tmp_hagID,
            tmp_pc_platform = tmp_pc_platform,
            bot_hash = plugin_event.bot_info.hash,
            config_key = 'groupInitList',
            init_name = tmp_name,
            init_value = tmp_value_final
        )
        setUserConfigForInit(
            tmp_hagID = tmp_hagID,
            tmp_pc_platform = tmp_pc_platform,
            bot_hash = plugin_event.bot_info.hash,
            config_key = 'groupInitParaList',
            init_name = tmp_name,
            init_value = tmp_value
        )
        setUserConfigForInit(
            tmp_hagID = tmp_hagID,
            tmp_pc_platform = tmp_pc_platform,
            bot_hash = plugin_event.bot_info.hash,
            config_key = 'groupInitUserList',
            init_name = tmp_name,
            init_value = {
                'userId': tmp_pc_id,
                'platform': tmp_pc_platform
            }
        )
        
        # 格式化结果显示 - 使用 onedice 的详细结果
        if display_detail:
            display_value = f"{display_detail}={tmp_value_final}"
        else:
            display_value = f"{tmp_value}={tmp_value_final}"
        
        dictTValue['tId'] = str(count)
        dictTValue['tSubName'] = tmp_name
        dictTValue['tSubResult'] = display_value
        result_list.append(
            OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitShowNode'], dictTValue)
        )
        return True
    
    return False

def setUserConfigForInit(
    tmp_hagID,
    tmp_pc_platform,
    bot_hash,
    config_key,
    init_name,
    init_value
):
    tmp_groupHash = OlivaDiceCore.userConfig.getUserHash(
        userId = tmp_hagID,
        userType = 'group',
        platform = tmp_pc_platform
    )
    tmp_groupInitList_list = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = tmp_pc_platform,
        userConfigKey = config_key,
        botHash = bot_hash
    )
    if tmp_groupInitList_list == None:
        tmp_groupInitList_list = {}
    tmp_groupInitList_list[init_name] = init_value
    OlivaDiceCore.userConfig.setUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = tmp_pc_platform,
        userConfigKey = config_key,
        userConfigValue = tmp_groupInitList_list,
        botHash = bot_hash
    )
    OlivaDiceCore.userConfig.writeUserConfigByUserHash(
        userHash = tmp_groupHash
    )

def getNoteFormat(
    data:str,
    pcHash:str,
    hagID
):
    res = data
    tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pcHash, hagID)
    if tmp_pc_name != None:
        res = res.replace(
            '{tName}',
            '%s' % tmp_pc_name
        )
    tmp_dict_pc_card = OlivaDiceCore.pcCard.pcCardDataGetByPcName(
        pcHash,
        hagId = hagID
    )
    for skill_name in tmp_dict_pc_card:
        res = res.replace(
            '{%s}' % skill_name,
            '%d' % tmp_dict_pc_card[skill_name]
        )
    tmp_value = 99
    if '克苏鲁神话' in tmp_dict_pc_card:
        tmp_value = 99 - tmp_dict_pc_card['克苏鲁神话']
    res = res.replace(
        '{SANMAX}',
        '%d' % (tmp_value)
    )
    return res

'''
team指令部分
'''
# Team成员信息格式化辅助函数
def format_team_member_display(user_name, pc_name, dictStrCustom, template_key='strTeamMemberFormat', **kwargs):
    """格式化团队成员显示信息的通用函数"""
    display_pc_name = pc_name if pc_name else user_name
    format_dict = {
        'tUserName': user_name,
        'tPcName': display_pc_name,
        **kwargs
    }
    return OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom.get(template_key, '[{tUserName}] - [{tPcName}]'), 
        format_dict
    )

def replyTEAM_command(plugin_event, Proc, valDict):
    tmp_reast_str = valDict['tmp_reast_str']
    flag_is_from_master = valDict['flag_is_from_master']
    flag_is_from_group_admin = valDict['flag_is_from_group_admin']
    tmp_hagID = valDict['tmp_hagID']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'team')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    # 解析 team 名字
    team_name = None
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId=tmp_hagID,
        userType='group',
        platform=plugin_event.platform['platform'],
        userConfigKey='teamConfig',
        botHash=plugin_event.bot_info.hash,
        default={}
    )
    # 按名称长度降序排序，优先匹配更长的名称
    sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
    for candidate in sorted_team_names:
        if tmp_reast_str.startswith(candidate):
            team_name = candidate
            tmp_reast_str = tmp_reast_str[len(candidate):].strip()
            break
    if OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'show'):
        team_show(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'list'):
        team_list(plugin_event, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'rm'):
        team_remove(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                           flag_is_from_master, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'del'):
        team_delete(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                           flag_is_from_master, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['clear','clr']):
        team_clear(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                          flag_is_from_master, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['at','call']):
        team_at(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'set'):
        team_set(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['sort','arr']):
        team_sort(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'rename'):
        team_rename(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['st','pc']):
        team_st(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['ra','rc']):
        team_ra(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'sc'):
        team_sc(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'r'):
        team_r(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'help', fullMatch=True):
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'team')
    else:
        team_create(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name)

def team_create(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    members = []
    if not team_name:
        # 解析小队名称
        if len(tmp_reast_str_para.data) > 0 and isinstance(tmp_reast_str_para.data[0], OlivOS.messageAPI.PARA.text):
            team_name = tmp_reast_str_para.data[0].data['text'].strip()
            if team_name == '':
                team_name = None
    # 解析成员
    for part in tmp_reast_str_para.data:
        if isinstance(part, OlivOS.messageAPI.PARA.at):
            members.append(part.data['id'])
    if team_name is None and not members:
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'team')
        return   
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    # 处理默认小队名称
    if team_name is None:
        if active_team is None:
            team_name = 'default'
        else:
            team_name = active_team
    # 创建或更新小队
    if team_name not in team_config:
        team_config[team_name] = {
            'members': list(set(members)),
            'created': int(time.time())
        }
        # 设置新小队为活跃小队
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userConfigKey = 'activeTeam',
            userConfigValue = team_name,
            botHash = plugin_event.bot_info.hash,
            userId = tmp_hagID,
            userType = 'group',
            platform = plugin_event.platform['platform']
        )
    else:
        # 更新现有小队
        existing_members = set(team_config[team_name]['members'])
        new_members = set(members)
        team_config[team_name]['members'] = list(existing_members | new_members)
    OlivaDiceCore.userConfig.setUserConfigByKey(
        userConfigKey = 'teamConfig',
        userConfigValue = team_config,
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
    # 获取成员信息
    members = team_config[team_name]['members']
    member_info = []
    index = 1
    if not members:
        dictTValue['tTeamName'] = team_name
        tmp_empty_msg = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strTeamEmpty'], dictTValue)
        member_info.append(tmp_empty_msg)
    else:
        for member_id in members:
            # 获取用户名称
            user_name = get_user_name(plugin_event, member_id)
            # 获取当前人物卡
            pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
            pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
            member_display = format_team_member_display(
                user_name, pc_name, dictStrCustom, 'strTeamMemberFormatWithIndex', tIndex=f"{index}"
            )
            member_info.append(member_display)
            index += 1
    dictTValue['tTeamName'] = team_name
    dictTValue['tMemberCount'] = str(len(members))
    dictTValue['tMembers'] = '\n'.join(member_info)
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamCreated'], dictTValue
    ))

def team_show(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'show')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    if not team_name:
        team_name = tmp_reast_str.strip()
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    if not team_name:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    # 检查小队是否存在
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    # 获取成员信息
    members = team_config[team_name]['members']
    if not members:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        ))
        return
    member_info = []
    index = 1
    for member_id in members:
        # 获取用户名称
        user_name = get_user_name(plugin_event, member_id)
        # 获取当前人物卡
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        member_display = format_team_member_display(
            user_name, pc_name, dictStrCustom, 'strTeamMemberFormatWithIndex', tIndex=f"{index}"
        )
        member_info.append(member_display)
        index += 1
    dictTValue['tTeamName'] = team_name
    dictTValue['tMemberCount'] = str(len(members))
    dictTValue['tMembers'] = '\n'.join(member_info)
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamShow'], dictTValue
    ))

def team_list(plugin_event, tmp_hagID, dictTValue, dictStrCustom):
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    # 构建小队列表
    team_list = []
    for team_name, team_data in team_config.items():
        member_count = len(team_data['members'])
        active_indicator = " (活跃)" if team_name == active_team else ""
        team_list.append(f"{team_name}{active_indicator} - {member_count}名成员")
    if not team_list:
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strNoTeams'], dictTValue
        ))
        return
    dictTValue['tTeamCount'] = str(len(team_list))
    dictTValue['tTeamList'] = '\n'.join(team_list)
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamList'], dictTValue
    ))

def team_remove(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                flag_is_from_master, dictTValue, dictStrCustom, team_name):
    # if not (flag_is_from_group_admin or flag_is_from_master):
    #     OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
    #         dictStrCustom['strNeedAdmin'], dictTValue
    #     ))
    #     return
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'rm')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    members_to_remove = []
    if not team_name:
        # 解析小队名称
        if len(tmp_reast_str_para.data) > 0 and isinstance(tmp_reast_str_para.data[0], OlivOS.messageAPI.PARA.text):
            team_name = tmp_reast_str_para.data[0].data['text'].strip()
            if team_name == '':
                team_name = None
    # 解析要移除的成员
    for part in tmp_reast_str_para.data:
        if isinstance(part, OlivOS.messageAPI.PARA.at):
            members_to_remove.append(part.data['id'])
    if team_name is None and not members_to_remove:
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'team')
        return
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    # 确定小队名称
    if team_name is None:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    # 移除成员
    current_members = set(team_config[team_name]['members'])
    removed_members = []
    if not current_members:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        ))
        return
    for member_id in members_to_remove:
        if member_id in current_members:
            current_members.remove(member_id)
            removed_members.append(member_id)
    team_config[team_name]['members'] = list(current_members)
    OlivaDiceCore.userConfig.setUserConfigByKey(
        userConfigKey = 'teamConfig',
        userConfigValue = team_config,
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
    if not removed_members:
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strNoMembersRemoved'], dictTValue
        ))
        return
    removed_names = []
    for member_id in removed_members:
        # 获取用户名称
        user_name = get_user_name(plugin_event, member_id)
        # 获取人物卡名
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        display_name = format_team_member_display(user_name, pc_name, dictStrCustom, 'strTeamSkillUpdateMemberFormat').replace('->', '').replace(':', '')
        removed_names.append(display_name)
    # 获取成员信息
    members = team_config[team_name]['members']
    member_info = []
    index = 1
    if not members:
        dictTValue['tTeamName'] = team_name
        tmp_empty_msg = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strTeamEmpty'], dictTValue)
        member_info.append(tmp_empty_msg)
    else:
        for member_id in members:
            # 获取用户名称
            user_name = get_user_name(plugin_event, member_id)
            # 获取当前人物卡
            pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
            pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
            member_display = format_team_member_display(
                user_name, pc_name, dictStrCustom, 'strTeamMemberFormatWithIndex', tIndex=f"{index}"
            )
            member_info.append(member_display)
            index += 1
    dictTValue['tTeamName'] = team_name
    dictTValue['tRemovedCount'] = str(len(removed_members))
    dictTValue['tRemovedMembers'] = '\n'.join(removed_names)
    dictTValue['tMemberCount'] = str(len(members))
    dictTValue['tMembers'] = '\n'.join(member_info)
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strMembersRemoved'], dictTValue
    ))

def team_delete(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                flag_is_from_master, dictTValue, dictStrCustom, team_name):
    # if not (flag_is_from_group_admin or flag_is_from_master):
    #     OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
    #         dictStrCustom['strNeedAdmin'], dictTValue
    #     ))
    #     return
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'del')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    if not team_name:
        team_name = tmp_reast_str.strip()
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    # 确定小队名称
    if team_name == '':
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    
    # 删除小队
    del team_config[team_name]
    # 处理活跃小队
    if active_team == team_name:
        if team_config:
            # 设置第一个小队为活跃小队
            new_active_team = list(team_config.keys())[0]
            OlivaDiceCore.userConfig.setUserConfigByKey(
                userConfigKey = 'activeTeam',
                userConfigValue=new_active_team,
                botHash = plugin_event.bot_info.hash,
                userId = tmp_hagID,
                userType = 'group',
                platform = plugin_event.platform['platform']
            )
        else:
            # 没有其他小队，清除活跃小队
            OlivaDiceCore.userConfig.setUserConfigByKey(
                userConfigKey = 'activeTeam',
                userConfigValue=None,
                botHash = plugin_event.bot_info.hash,
                userId = tmp_hagID,
                userType = 'group',
                platform = plugin_event.platform['platform']
            )
    # 保存配置
    OlivaDiceCore.userConfig.setUserConfigByKey(
        userConfigKey = 'teamConfig',
        userConfigValue = team_config,
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
    dictTValue['tTeamName'] = team_name
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamDeleted'], dictTValue
    ))

def team_clear(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
               flag_is_from_master, dictTValue, dictStrCustom, team_name):
    # if not (flag_is_from_group_admin or flag_is_from_master):
    #     OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
    #         dictStrCustom['strNeedAdmin'], dictTValue
    #     ))
    #     return
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, ['clear','clr'])
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    if not team_name:
        team_name = tmp_reast_str.strip()
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    # 确定小队名称
    if team_name == '':
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    # 清除成员
    team_config[team_name]['members'] = []
    OlivaDiceCore.userConfig.setUserConfigByKey(
        userConfigKey = 'teamConfig',
        userConfigValue = team_config,
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
    dictTValue['tTeamName'] = team_name
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamCleared'], dictTValue
    ))

def team_at(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, ['at','call'])
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    if not team_name:
        team_name = tmp_reast_str.strip()
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    
    # 确定小队名称
    if team_name == '':
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    
    # 检查小队是否存在
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strTeamNotFound'], dictTValue
            ))
        return
    members = team_config[team_name]['members']
    if not members:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        ))
        return
    
    # at实现
    at_members_str = ""
    for member_id in members:
        at_para = OlivOS.messageAPI.PARA.at(str(member_id))
        at_str = at_para.get_string_by_key('CQ')
        at_members_str += at_str
    dictTValue['tTeamName'] = team_name
    dictTValue['tAtMembers'] = at_members_str
    reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamAt'], dictTValue
    )
    OlivaDiceCore.msgReply.replyMsg(plugin_event, reply_str)

def team_set(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'set')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    if not team_name:
        team_name = tmp_reast_str.strip()
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    
    # 首先尝试直接切换
    if team_name in team_config:
        # 设置活跃小队
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userConfigKey = 'activeTeam',
            userConfigValue = team_name,
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
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamSetActive'], dictTValue
        ))
    else:
        # 如果直接切换失败，尝试模糊搜索
        team_list = list(team_config.keys())
        if len(team_list) > 0:
            dictTValue['tUserName'] = plugin_event.data.sender['name']
            dictTValue['tTeamName'] = team_name
            selected_team_name = OlivaDiceCore.helpDoc.fuzzySearchAndSelect(
                key_str = team_name,
                item_list = team_list,
                bot_hash = plugin_event.bot_info.hash,
                plugin_event = plugin_event,
                strRecommendKey = 'strTeamSetRecommend',
                strErrorKey = 'strTeamNotFound',
                dictStrCustom = dictStrCustom,
                dictTValue = dictTValue
            )
            # 如果用户选择了某个小队，切换到该小队
            if selected_team_name is not None:
                OlivaDiceCore.userConfig.setUserConfigByKey(
                    userConfigKey = 'activeTeam',
                    userConfigValue = selected_team_name,
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
                dictTValue['tTeamName'] = selected_team_name
                OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                    dictStrCustom['strTeamSetActive'], dictTValue
                ))
        else:
            # 如果没有任何小队，显示错误
            dictTValue['tTeamName'] = team_name
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strTeamNotFound'], dictTValue
            ))


def team_sort(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, ['sort','arr'])
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)

    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    skill_name = tmp_reast_str.strip()
    if not team_name:
        # 按名称长度降序排序，优先匹配更长的名称
        sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
        # 尝试匹配小队名称
        for candidate in sorted_team_names:
            if tmp_reast_str.startswith(candidate):
                team_name = candidate
                skill_name = tmp_reast_str[len(candidate):].strip()
                break
    if team_name is None:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
        skill_name = tmp_reast_str.strip()
    if not team_name and not skill_name:
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'team')
        return
    if not skill_name:
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamSortNeedSkill'], dictTValue
        ))
        return
    skill_name = skill_name.upper()
    members = team_config[team_name]['members']
    if not members:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        ))
        return
    # 收集成员信息并获取技能值
    member_info_list = []
    for original_index, member_id in enumerate(members):
        user_name = get_user_name(plugin_event, member_id)
        
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        skill_value = 0
        if pc_name:
            skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                pc_hash, skill_name, hagId = tmp_hagID
            )
            if skill_value is None:
                skill_value = 0
        member_info_list.append({
            'id': member_id,
            'name': user_name,
            'pc_name': pc_name,
            'skill_value': skill_value,
            'original_index': original_index
        })
    # 按技能值降序排序
    member_info_list.sort(key=lambda x: (-x['skill_value'], x['original_index']))
    result_lines = []
    for index, member in enumerate(member_info_list, 1):
        line = format_team_member_display(
            member['name'], 
            member['pc_name'], 
            dictStrCustom, 
            'strTeamSortMemberFormat',
            tIndex=index,
            tSkillName=skill_name,
            tSkillValue=member['skill_value']
        )
        result_lines.append(line)
    dictTValue['tTeamName'] = team_name
    dictTValue['tSkillName'] = skill_name
    dictTValue['tSortResult'] = '\n'.join(result_lines)
    reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamSortResult'], dictTValue
    )
    OlivaDiceCore.msgReply.replyMsg(plugin_event, reply_str)

def team_rename(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'rename')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    old_name = None
    new_name = None
    # 检查是否包含 '/' 分隔符
    if '/' in tmp_reast_str:
        # 新名字/旧名字
        parts = tmp_reast_str.split('/', 1)
        new_name = parts[0].strip()
        old_name = parts[1].strip()
    else:
        # 新名字（重命名活跃小队）
        new_name = tmp_reast_str.strip()
        old_name = active_team
    if not new_name:
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamRenameNeedNewName'], dictTValue
        ))
        return
    if not old_name:
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strNoActiveTeam'], dictTValue
        ))
        return
    # 检查旧小队是否存在
    if old_name not in team_config:
        dictTValue['tTeamName'] = old_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    # 检查新名称是否已存在
    if new_name in team_config:
        dictTValue['tTeamName'] = new_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNameExists'], dictTValue
        ))
        return
    team_config[new_name] = team_config.pop(old_name)
    # 更新活跃小队
    if active_team == old_name:
        OlivaDiceCore.userConfig.setUserConfigByKey(
            userConfigKey = 'activeTeam',
            userConfigValue=new_name,
            botHash = plugin_event.bot_info.hash,
            userId = tmp_hagID,
            userType = 'group',
            platform = plugin_event.platform['platform']
        )
    OlivaDiceCore.userConfig.setUserConfigByKey(
        userConfigKey = 'teamConfig',
        userConfigValue = team_config,
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
    dictTValue['tOldTeamName'] = old_name
    dictTValue['tNewTeamName'] = new_name
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamRenamed'], dictTValue
    ))

def team_st(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, ['st','pc'])
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    skill_name = tmp_reast_str.strip()
    if not team_name:
        # 按名称长度降序排序，优先匹配更长的名称
        sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
        # 尝试匹配小队名称
        for candidate in sorted_team_names:
            if tmp_reast_str.startswith(candidate):
                team_name = candidate
                skill_name = tmp_reast_str[len(candidate):].strip()
                break
    if team_name is None:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
        skill_name = tmp_reast_str.strip()
    if not skill_name:
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'team')
        return
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    # 获取所有成员的技能列表并去重
    all_pc_skill_names = set()
    for member_id in team_config[team_name]['members']:
        tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId = tmp_hagID)
        for tmp_skill_name in pc_skills:
            if not tmp_skill_name.startswith('__'):
                # 移除技能名中的数字
                clean_skill_name = re.sub(r'\d+', '', tmp_skill_name).upper()
                all_pc_skill_names.add(clean_skill_name)
    # 预处理字符串，在特定字母先查找技能名，找到技能名后添加空格
    processed_skill_ops = skill_name
    for start_char in OlivaDiceCore.pcCardData.arrPcCardLetterStart:
        i = 0
        while i < len(processed_skill_ops):
            if processed_skill_ops[i].lower() == start_char.lower():
                max_len = 0
                for skill in sorted(all_pc_skill_names, key = len, reverse = True):
                    if skill.startswith(start_char.upper()) and processed_skill_ops[i:].upper().startswith(skill):
                        # 特殊处理以d开头的技能名
                        if start_char.upper() == 'D' and len(skill) == 1 and i+1 < len(processed_skill_ops) and processed_skill_ops[i+1].isdigit():
                            i += 1
                            break
                        if len(skill) > max_len:
                            max_len = len(skill)
                            break
                if max_len > 0:
                    # 在匹配的技能名前添加空格
                    processed_skill_ops = processed_skill_ops[:i] + ' ' + processed_skill_ops[i:]
                    i += max_len + 1
                else:
                    i += 1
            else:
                i += 1
    # 解析多项技能操作
    op_list = op_list_get()
    assignment_symbols = ['=', ':', '：']  # 赋值符号
    all_op_list = op_list + assignment_symbols  # 所有操作符
    skill_updates = []
    # 分割技能操作
    current_pos = 0
    while current_pos < len(processed_skill_ops):
        # 查找技能名结束位置（遇到操作符或数字）
        skill_end_pos = -1
        for i in range(current_pos, len(processed_skill_ops)):
            # 如果遇到操作符或数字
            if processed_skill_ops[i] in all_op_list or processed_skill_ops[i].isdigit():
                skill_end_pos = i
                break
        if skill_end_pos == -1:
            break
        
        # 处理技能名和表达式
        if processed_skill_ops[skill_end_pos].isdigit() or processed_skill_ops[skill_end_pos] in all_op_list:
            # 检查是否是d后面跟着数字的情况
            tmp_skill_name_part = processed_skill_ops[current_pos:skill_end_pos].strip()
            if (tmp_skill_name_part.upper() == 'D' and 
                skill_end_pos < len(processed_skill_ops) and 
                processed_skill_ops[skill_end_pos].isdigit()):
                current_pos = skill_end_pos  # 跳过这个d，不视为技能名
                continue
            # 查找完整的表达式
            expr_end_pos = skill_end_pos
            in_dice_expr = False
            op = ''
            # 如果是赋值符号(= : ：)，记录并跳过它
            if processed_skill_ops[skill_end_pos] in assignment_symbols:
                op = ''
                expr_end_pos += 1
            elif processed_skill_ops[skill_end_pos] in op_list:
                op = processed_skill_ops[skill_end_pos]
                expr_end_pos += 1
            else:
                op = ''
            # 继续提取表达式的数值部分
            while expr_end_pos < len(processed_skill_ops):
                char = processed_skill_ops[expr_end_pos]
                if char.upper() == 'D':
                    in_dice_expr = True
                    expr_end_pos += 1
                    continue
                if char.isdigit() or (in_dice_expr and char in op_list) or char in op_list:
                    expr_end_pos += 1
                else:
                    break
            
            skill_name = processed_skill_ops[current_pos:skill_end_pos].strip()
            
            # 根据操作符确定表达式的起始位置
            if processed_skill_ops[skill_end_pos] in all_op_list:
                # 如果是操作符,表达式从操作符后面开始(已经在上面 expr_end_pos += 1 跳过了)
                expr_str = processed_skill_ops[skill_end_pos + 1:expr_end_pos].strip()
            else:
                # 如果直接是数字,表达式从当前位置开始
                expr_str = processed_skill_ops[skill_end_pos:expr_end_pos].strip()
            
            if skill_name and expr_str:
                skill_name = OlivaDiceCore.pcCard.fixName(skill_name, flagMode = 'skillName')
                # 移除技能名中的数字
                clean_skill_name = re.sub(r'\d+', '', skill_name).upper()
                skill_updates.append((clean_skill_name, op, expr_str))
            current_pos = expr_end_pos
        else:
            current_pos = skill_end_pos + 1
    if not skill_updates:
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'team')
        return
    
    members = team_config[team_name]['members']
    results = []
    special_skills = []
    # 处理每个成员
    for member_id in members:
        tmp_pc_id = member_id
        tmp_pc_platform = plugin_event.platform['platform']
        tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
        tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
        if not tmp_pc_name:
            # 如果没有人物卡，使用默认名称
            tmp_pc_name = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_pc_id,
                userType = 'user',
                platform = tmp_pc_platform,
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash,
                default=f"用户{member_id}"
            )
        member_results = []
        for skill_name, op, expr_str in skill_updates:
            # 获取当前技能值
            current_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                tmp_pcHash, skill_name, hagId = tmp_hagID
            )
            if current_value is None:
                current_value = 0
            # 处理表达式
            # 如果 op 为空字符串（直接赋值），直接使用 expr_str；否则使用 current_value + op + expr_str
            if op == '':
                rd_para_str = expr_str
            else:
                rd_para_str = str(current_value) + op + expr_str
            tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                tmp_pcHash, tmp_pc_name
            )
            tmp_template_customDefault = None
            if tmp_template_name:
                tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                if 'customDefault' in tmp_template:
                    tmp_template_customDefault = tmp_template['customDefault']
            rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault)
            rd_para.roll()
            if rd_para.resError is None:
                new_value = rd_para.resInt
                OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                    tmp_pcHash, skill_name, new_value, tmp_pc_name, hagId = tmp_hagID
                )
                # 检查是否为特殊技能
                tmp_pcCardRule = 'default'
                if tmp_pc_name is not None:
                    tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                    if tmp_pcCardRule_new:
                        tmp_pcCardRule = tmp_pcCardRule_new
                if tmp_pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial:
                    if skill_name in [skill for skill in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[tmp_pcCardRule]]:
                        special_skills.append(skill_name)
                # 构建计算过程字符串
                if op != '':
                    calculation_detail = f"{current_value}{op}{expr_str}"
                else:
                    calculation_detail = expr_str    
                # 判断是否显示详细计算过程
                has_calc_in_expr = False
                if len(expr_str) > 1:
                    for i, char in enumerate(expr_str):
                        if char in op_list and i > 0:
                            has_calc_in_expr = True
                            break
                if op != '' or 'D' in expr_str.upper() or has_calc_in_expr:
                    if 'D' in expr_str.upper():
                        # 包含骰子表达式，显示骰子结果
                        detail_str = f"{calculation_detail}={rd_para.resDetail}"
                        if len(detail_str) > 50:
                            skill_update_detail = f"{current_value} -> {new_value} ({calculation_detail}={new_value})"
                        else:
                            skill_update_detail = f"{current_value} -> {new_value} ({calculation_detail}={rd_para.resDetail})"
                    else:
                        # 普通计算表达式
                        skill_update_detail = f"{current_value} -> {new_value} ({calculation_detail})"
                else:
                    # 直接赋值
                    skill_update_detail = f"{current_value} -> {new_value}"
                member_results.append(OlivaDiceCore.msgCustomManager.formatReplySTR(
                    dictStrCustom.get('strTeamSkillUpdateResultFormat', '{tSkillName}: {tDetail}'),
                    {'tSkillName': skill_name, 'tOldValue': current_value, 'tNewValue': new_value, 'tDetail': skill_update_detail}
                ))
            else:
                member_results.append(f"{skill_name}: 表达式错误 '{op}{expr_str}'")
        # 检查是否修改了SAN或克苏鲁神话技能，如果是则更新神话淬炼状态
        modified_skills = [skill_name for skill_name, op, expr_str in skill_updates]
        if 'SAN' in modified_skills or '克苏鲁神话' in modified_skills:
            OlivaDiceCore.pcCard.checkMythicHardening(tmp_pcHash, tmp_pc_name, tmp_hagID)
        OlivaDiceCore.msgReply.trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
        user_name = get_user_name(plugin_event, member_id)
        if member_results:
            member_header = format_team_member_display(user_name, tmp_pc_name, dictStrCustom, 'strTeamSkillUpdateMemberFormat')
            results.append(member_header + ':\n' + '\n'.join(member_results))
    dictTValue['tTeamName'] = team_name
    dictTValue['tResults'] = '\n'.join(results)
    # 特殊技能提示
    if special_skills:
        dictTValue['tSpecialSkills'] = '、'.join([f'[{skill}]' for skill in set(special_skills)])
        special_notice = OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strPcSetSpecialSkills'], dictTValue
        )
    else:
        special_notice = ''
    reply_msg = OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamSkillUpdate'], dictTValue
    ) + special_notice
    OlivaDiceCore.msgReply.replyMsg(plugin_event, reply_msg)

def team_ra(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, ['ra','rc'])
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    skill_expr = tmp_reast_str
    if not team_name:
        # 按名称长度降序排序，优先匹配更长的名称
        sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
        for candidate in sorted_team_names:
            if tmp_reast_str.startswith(candidate):
                team_name = candidate
                skill_expr = tmp_reast_str[len(candidate):].strip()
                break
    # 如果没有匹配到小队名称，使用活跃小队
    if team_name is None:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strTeamNotFound'], dictTValue
            ))
        return
    skill_name = None
    expr_str = None
    fixed_skill_value = None
    difficulty = None
    bp_type = 0  # 0:无, 1:奖励骰, 2:惩罚骰
    bp_count = None
    # 处理奖励/惩罚骰
    if skill_expr.startswith(('b','B')):
        bp_type = 1
        skill_expr = skill_expr[1:]
        bp_digits = ''
        while skill_expr and skill_expr[0].isdigit():
            bp_digits += skill_expr[0]
            skill_expr = skill_expr[1:]
        bp_count = int(bp_digits) if bp_digits else 1
    elif skill_expr.startswith(('p','P')):
        bp_type = 2
        skill_expr = skill_expr[1:]
        bp_digits = ''
        while skill_expr and skill_expr[0].isdigit():
            bp_digits += skill_expr[0]
            skill_expr = skill_expr[1:]
        bp_count = int(bp_digits) if bp_digits else 1
    skill_expr = OlivaDiceCore.msgReply.skipSpaceStart(skill_expr)
    # 检查是否没有指定技能
    if skill_expr == '' or skill_expr is None:
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamCheckResultNone'], dictTValue
        ))
        return
    # 解析难度前缀
    difficulty, skill_expr = difficulty_analyze(skill_expr)
    # 解析技能名和表达式
    if skill_expr:
        op_list = op_list_get()
        pos = len(skill_expr)
        for i, char in enumerate(skill_expr):
            if char in op_list or char.isdigit():
                pos = i
                break
        skill_name = skill_expr[:pos].strip().upper() or None
        if skill_name:
            skill_name = OlivaDiceCore.pcCard.fixName(skill_name, flagMode = 'skillName')
        skill_expr = skill_expr[pos:].strip()
        if skill_expr:
            if skill_expr[0] in op_list:
                expr_end = 0
                in_dice = False
                for i, char in enumerate(skill_expr):
                    if char.isspace():
                        expr_end = i
                        break
                    if char.upper() == 'D':
                        in_dice = True
                    if not (char.isdigit() or char in op_list or char.upper() == 'D'):
                        if not in_dice:
                            expr_end = i
                            break
                expr_str = skill_expr[:expr_end] if expr_end > 0 else skill_expr
                skill_expr = skill_expr[len(expr_str):].strip()
            elif skill_expr[0].isdigit():
                [num_str, skill_expr] = OlivaDiceCore.msgReply.getNumberPara(skill_expr)
                if num_str.isdigit():
                    fixed_skill_value = int(num_str)
                skill_expr = OlivaDiceCore.msgReply.skipSpaceStart(skill_expr)
        if skill_expr:
            [num_str, skill_expr] = OlivaDiceCore.msgReply.getNumberPara(skill_expr)
            if num_str.isdigit():
                fixed_skill_value = int(num_str)
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
    # 获取小队成员
    members = team_config[team_name]['members']
    if not members:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        ))
        return
    # 为每个成员进行检定
    results = []
    for member_id in members:
        user_name = get_user_name(plugin_event, member_id)
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        display_name = format_team_member_display(user_name, pc_name, dictStrCustom, 'strTeamMemberFormat')
        # 获取基础技能值
        base_skill_value = None
        if skill_name:
            skill_name_upper = skill_name.upper()
            base_skill_value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                pc_hash, skill_name_upper, hagId = tmp_hagID
            )
            if base_skill_value is None and pc_name:
                pc_data = OlivaDiceCore.pcCard.pcCardDataGetByPcName(pc_hash, hagId = tmp_hagID)
                if pc_data and skill_name_upper in pc_data:
                    base_skill_value = pc_data[skill_name_upper]
        # 默认值处理
        try:
            base_skill_value = int(base_skill_value) if base_skill_value is not None else 0
        except (ValueError, TypeError):
            base_skill_value = 0
        current_skill_value = base_skill_value
        expr_result_str = str(base_skill_value)
        if expr_str:
            try:
                # 如果有固定值，基于固定值计算表达式
                calc_base = fixed_skill_value if fixed_skill_value is not None else base_skill_value
                rd_para = OlivaDiceCore.onedice.RD(f"{calc_base}{expr_str}")
                rd_para.roll()
                if not rd_para.resError:
                    current_skill_value = rd_para.resInt
                    # 构建表达式详情
                    if "D" in expr_str.upper():
                        expr_result_str = f"{calc_base}{expr_str}={rd_para.resDetail}={current_skill_value}"
                    else:
                        expr_result_str = f"{calc_base}{expr_str}={current_skill_value}"
            except:
                pass
        # 没有表达式但有固定值时使用固定值
        elif fixed_skill_value is not None:
            current_skill_value = fixed_skill_value
            expr_result_str = f"{fixed_skill_value}"
        # 构建骰子表达式
        rd_para_str = '1D100'
        if bp_type == 1:
            rd_para_str = 'B'
        elif bp_type == 2:
            rd_para_str = 'P'
        if bp_count is not None:
            rd_para_str += str(bp_count)
        # 获取模板配置
        template_name = flag_groupTemplate or 'default'
        template_rule_name = flag_groupTemplateRule or 'default'
        template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(template_name)
        custom_default = None
        if template and 'customDefault' in template:
            custom_default = template['customDefault']
        rd_para = OlivaDiceCore.onedice.RD(rd_para_str, custom_default)
        rd_para.roll()
        if rd_para.resError is not None:
            # 检定出错
            result_str = get_SkillCheckError(rd_para.resError, dictStrCustom, dictTValue)
            results.append({
                'name': display_name,
                'result_str': result_str,
                'success_level': -1,
                'roll_value': 0,
                'skill_value': 0
            })
            continue
        roll_value = rd_para.resInt
        skill_check_data = {
            'roll': roll_value,
            'skill': current_skill_value
        }
        skill_check_type, skill_threshold = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
            skill_check_data, template, template_rule_name, difficulty
        )
        # 构建骰子详情
        dice_detail = f"{rd_para_str}={roll_value}"
        if rd_para.resDetail:
            dice_detail = f"{rd_para_str}={rd_para.resDetail}={roll_value}"
        skill_value_str = expr_result_str
        if difficulty:
            skill_value_str = f"{skill_threshold}({expr_result_str})"
        
        # 使用模板构造结果字符串
        skill_check_result = get_SkillCheckResult(
            skill_check_type, dictStrCustom, dictTValue, pc_hash, pc_name,
            user_id=member_id, skill_name=skill_name,
            platform=plugin_event.platform['platform'], botHash=plugin_event.bot_info.hash, hagId=tmp_hagID
        )
        if skill_name:
            result_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom.get('strTeamCheckMemberFormat', '{tDisplayName}({tSkillName}: {tSkillValue}): {tDiceDetail}/{tSkillValue} {tResult}'),
                {
                    'tDisplayName': display_name,
                    'tSkillName': skill_name,
                    'tSkillValue': skill_value_str,
                    'tDiceDetail': dice_detail,
                    'tResult': skill_check_result
                }
            )
        else:
            result_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom.get('strTeamCheckMemberFormatNoSkill', '{tDisplayName}: {tDiceDetail}/{tSkillValue} {tResult}'),
                {
                    'tDisplayName': display_name,
                    'tSkillValue': skill_value_str,
                    'tDiceDetail': dice_detail,
                    'tResult': skill_check_result
                }
            )
        # 处理enhanceList
        if skill_check_type in [
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
        ]:
            if pc_name and skill_name and bp_type != 1:
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
                tmp_enhanceList = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    tmp_pcHash,
                    pc_name,
                    'enhanceList',
                    []
                )
                tmp_skipEnhance_list = []
                if template_name:
                    tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(template_name)
                    if 'skillConfig' in tmp_template and 'skipEnhance' in tmp_template['skillConfig']:
                        if isinstance(tmp_template['skillConfig']['skipEnhance'], list):
                            tmp_skipEnhance_list = tmp_template['skillConfig']['skipEnhance']
                tmp_skill_name_core = OlivaDiceCore.pcCard.pcCardDataSkillNameMapper(
                    tmp_pcHash,
                    skill_name,
                    hagId = tmp_hagID
                )
                if (tmp_skill_name_core not in tmp_enhanceList and 
                    tmp_skill_name_core not in tmp_skipEnhance_list):
                    tmp_enhanceList.append(tmp_skill_name_core)
                    OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
                        tmp_pcHash,
                        pc_name,
                        'enhanceList',
                        tmp_enhanceList
                    )
        # 记录结果
        success_level = 0
        if skill_check_type in [
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS
        ]:
            success_level = 1
        results.append({
            'name': display_name,
            'result_str': result_str,
            'success_level': success_level,
            'roll_value': roll_value,
            'skill_value': current_skill_value
        })
    # 没有结果
    if not results:
        reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        )
        OlivaDiceCore.msgReply.replyMsg(plugin_event, reply_str)
        return
    # 排序结果：先按成功等级(成功在上)，再按roll值(小在上)，最后按技能值(大在上)
    results.sort(key=lambda x: (
        -x['success_level'],  # 成功在上
        x['roll_value'],     # roll值小在上
        -x['skill_value']    # 技能值大在上
    ))
    if not dictTValue['tSkillName']:
        if skill_name:
            dictTValue['tSkillName'] = skill_name
        else:
            dictTValue['tSkillName'] = str(results[0]['skill_value'])
    # 构建最终输出
    result_lines = []
    for i, result in enumerate(results, 1):
        result_lines.append(f"{i}. {result['result_str']}")
    dictTValue['tTeamName'] = team_name
    dictTValue['tResult'] = '\n'.join(result_lines)
    reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamCheckResult'], dictTValue
    )
    OlivaDiceCore.msgReply.replyMsg(plugin_event, reply_str)

def team_sc(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'sc')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    # 处理奖励骰和惩罚骰
    flag_bp_type = 0  # 0:无 1:奖励骰 2:惩罚骰
    flag_bp_count = 1  # 骰子数量
    if OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'b'):
        flag_bp_type = 1
        tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'b')
        # 检查是否有数字指定骰子数量
        if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
            flag_bp_count = int(tmp_reast_str[0])
            tmp_reast_str = tmp_reast_str[1:]
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'p'):
        flag_bp_type = 2
        tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'p')
        # 检查是否有数字指定骰子数量
        if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
            flag_bp_count = int(tmp_reast_str[0])
            tmp_reast_str = tmp_reast_str[1:]
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'activeTeam',
        botHash = plugin_event.bot_info.hash
    )
    # 解析小队名称
    if not team_name:
        # 按名称长度降序排序，优先匹配更长的名称
        sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
        for candidate in sorted_team_names:
            if tmp_reast_str.startswith(candidate):
                team_name = candidate
                tmp_reast_str = tmp_reast_str[len(candidate):].strip()
                break
    # 如果没有匹配到小队名称，使用活跃小队
    if team_name is None:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    # 检查小队是否存在
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    # 解析成功/失败参数
    san_success = '0'
    san_fail = '0'
    if len(tmp_reast_str) > 0:
        san_parts = tmp_reast_str.split('/')
        if len(san_parts) >= 2:
            san_success = san_parts[0].strip() or '0'
            san_fail = '/'.join(san_parts[1:]).strip() or '0'
        elif len(san_parts) == 1:
            san_success = '0'
            san_fail = san_parts[0].strip() or '0'
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
    # 获取小队成员
    members = team_config[team_name]['members']
    if not members:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        ))
        return
    # 构建骰子表达式
    rd_para_str = '1D100'
    if flag_bp_type == 1:
        rd_para_str = f'B{flag_bp_count}'
    elif flag_bp_type == 2:
        rd_para_str = f'P{flag_bp_count}'
    # 为每个成员进行sc检定
    results = []
    for member_id in members:
        tmp_pc_platform = plugin_event.platform['platform']
        # 获取用户信息
        user_name = get_user_name(plugin_event, member_id)
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        # 构建显示名称
        display_name = format_team_member_display(user_name, pc_name, dictStrCustom, 'strTeamMemberFormat')
        current_san = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
            pc_hash, 'SAN', hagId = tmp_hagID
        )
        if current_san is None:
            current_san = 0
        rd_para = OlivaDiceCore.onedice.RD(rd_para_str)
        rd_para.roll()
        if rd_para.resError is not None:
            # 检定出错
            result_str = get_SkillCheckError(rd_para.resError, dictStrCustom, dictTValue)
            results.append({
                'name': display_name,
                'result_str': result_str,
                'success_level': -1,
                'roll_value': 0,
                'san_value': current_san,
                'san_loss': 0,
                'new_san': current_san
            })
            continue
        roll_value = rd_para.resInt
        skill_check_data = {
            'roll': roll_value,
            'skill': current_san
        }
        # 获取检定结果
        template_name = flag_groupTemplate or 'COC7'
        template_rule_name = flag_groupTemplateRule or 'default'
        template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(template_name)
        skill_check_type, _ = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
            skill_check_data, template, template_rule_name
        )
        # 预先计算成功和失败表达式
        success_rd = OlivaDiceCore.onedice.RD(san_success)
        success_rd.roll()
        fail_rd = OlivaDiceCore.onedice.RD(san_fail)
        fail_rd.roll()
        success_error = success_rd.resError is not None
        fail_error = fail_rd.resError is not None
        if success_error or fail_error:
            error_str = ""
            if success_error and roll_value < current_san:
                dictTValue['tRollPara'] = san_success
                error_str += f"左式错误: {get_SkillCheckError(success_rd.resError, dictStrCustom, dictTValue)}"
            if fail_error and roll_value > current_san:
                dictTValue['tRollPara'] = san_fail
                error_str += f"右式错误: {get_SkillCheckError(fail_rd.resError, dictStrCustom, dictTValue)}"
            # 构建骰子详情
            dice_detail = f"{rd_para_str}={roll_value}"
            if rd_para.resDetail:
                dice_detail = f"{rd_para_str}={rd_para.resDetail}={roll_value}"
            result_str = f"{display_name}(SAN:{current_san}): {dice_detail}/{current_san}"
            result_str += f"\n{error_str}"
            results.append({
                'name': display_name,
                'result_str': result_str,
                'success_level': -1,
                'roll_value': roll_value,
                'san_value': current_san,
                'san_loss': 0,
                'new_san': current_san
            })
            continue
        san_loss = 0
        # 困难，极难转换成普通成功
        if skill_check_type in [
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS
        ]:
            skill_check_type = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS
        
        if skill_check_type == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
            if success_rd.resError is None:
                san_loss = success_rd.resInt
        elif skill_check_type == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS:
            if success_rd.resError is None:
                san_loss = success_rd.resInt
        elif skill_check_type == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
            if fail_rd.resError is None:
                san_loss = fail_rd.resInt
        elif skill_check_type == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
            if fail_rd.resError is None:
                san_loss = fail_rd.resIntMax
        # 保存原始损失值
        original_san_loss = san_loss
        # 检查神话淬炼状态
        is_mh_enabled = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = tmp_hagID,
            userType = 'group',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'mythicHardeningEnable',
            botHash = plugin_event.bot_info.hash
        )
        OlivaDiceCore.pcCard.checkMythicHardening(pc_hash, pc_name, tmp_hagID)
        is_mythic_hardened = OlivaDiceCore.pcCard.getMythicHardeningStatus(pc_hash, pc_name)
        if is_mh_enabled and is_mythic_hardened and san_loss > 0:
            san_loss = math.ceil(san_loss / 2.0)
        # 更新SAN值
        new_san = max(0, current_san - san_loss)
        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
            pc_hash, 'SAN', new_san, pc_name, hagId = tmp_hagID
        )
        OlivaDiceCore.msgReply.trigger_auto_sn_update(plugin_event, member_id, tmp_pc_platform, tmp_hagID, dictTValue)
        # 构建骰子详情
        dice_detail = f"{rd_para_str}={roll_value}"
        if rd_para.resDetail:
            dice_detail = f"{rd_para_str}={rd_para.resDetail}={roll_value}"
        
        # 计算损失参数
        san_loss_expr = san_success if roll_value < current_san else san_fail
        skill_check_result = get_SkillCheckResult(
            skill_check_type, dictStrCustom, dictTValue, pc_hash, pc_name,
            user_id=member_id, skill_name='SAN',
            platform=tmp_pc_platform, botHash=plugin_event.bot_info.hash, hagId=tmp_hagID
        )
        
        # 使用模板构造结果字符串
        result_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom.get('strTeamSCMemberFormat', '{tDisplayName}(SAN:{tCurrentSan}): {tDiceDetail}/{tCurrentSan}\nSAN: {tCurrentSan} -> {tNewSan}(损失{tSanLoss}点)'),
            {
                'tDisplayName': display_name,
                'tCurrentSan': current_san,
                'tDiceDetail': dice_detail,
                'tNewSan': new_san,
                'tSanLoss': san_loss,
                'tSanLossExpr': san_loss_expr
            }
        ) + skill_check_result
        # 添加神话淬炼提示
        if is_mh_enabled and is_mythic_hardened and original_san_loss > 0 and san_loss != original_san_loss:
            mh_dict = {
                'tOriginalLoss': str(original_san_loss),
                'tActualLoss': str(san_loss)
            }
            result_str += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strMHEffect'], mh_dict)
        success_level = 0
        if skill_check_type in [
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS,
            OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS
        ]:
            success_level = 1
        results.append({
            'name': display_name,
            'result_str': result_str,
            'success_level': success_level,
            'roll_value': roll_value,
            'san_value': current_san,
            'san_loss': san_loss,
            'new_san': new_san
        })
    # 排序结果：先按成功等级(成功在上)，再按roll值(小在上)，最后按SAN值(大在上)
    results.sort(key=lambda x: (
        -x['success_level'],  # 成功在上
        x['roll_value'],     # roll值小在上
        -x['san_value']      # SAN值大在上
    ))
    result_lines = []
    for i, result in enumerate(results, 1):
        result_lines.append(f"{i}. {result['result_str']}")
    dictTValue['tTeamName'] = team_name
    dictTValue['tResult'] = '\n'.join(result_lines)
    reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamSCResult'], dictTValue
    )
    OlivaDiceCore.msgReply.replyMsg(plugin_event, reply_str)

def team_r(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom, team_name):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'r')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    # 获取团队配置
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId=tmp_hagID,
        userType='group',
        platform=plugin_event.platform['platform'],
        userConfigKey='teamConfig',
        botHash=plugin_event.bot_info.hash,
        default={}
    )
    active_team = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId=tmp_hagID,
        userType='group',
        platform=plugin_event.platform['platform'],
        userConfigKey='activeTeam',
        botHash=plugin_event.bot_info.hash
    )
    # 解析团队名称
    if not team_name:
        sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
        for candidate in sorted_team_names:
            if tmp_reast_str.startswith(candidate):
                team_name = candidate
                tmp_reast_str = tmp_reast_str[len(candidate):].strip()
                break
    # 如果没有匹配到团队名称，使用活跃团队
    if team_name is None:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
    # 检查团队是否存在
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    # 获取团队成员
    members = team_config[team_name]['members']
    if not members:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamEmpty'], dictTValue
        ))
        return
    # 获取模板配置
    flag_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId=tmp_hagID,
        userType='group',
        platform=plugin_event.platform['platform'],
        userConfigKey='groupTemplate',
        botHash=plugin_event.bot_info.hash
    )
    rd_reason_str = None
    tmp_reast_str = tmp_reast_str.upper()
    # 为每个团队成员执行骰
    roll_results = []
    for member_id in members:
        user_name = get_user_name(plugin_event, member_id)
        # 获取角色卡信息
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        display_name = format_team_member_display(user_name, pc_name, dictStrCustom, 'strTeamMemberFormat')
        skill_valueTable = OlivaDiceCore.pcCard.pcCardDataGetByPcName(pc_hash, hagId=tmp_hagID).copy()
        if pc_name is not None:
            skill_valueTable.update(
                OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    pcHash=pc_hash,
                    pcCardName=pc_name,
                    dataKey='mappingRecord',
                    resDefault={}
                )
            )
        rd_para_str = '1D100'
        tmp_rd_para_str = None
        tmp_rd_para_str_show = None
        if len(tmp_reast_str) > 0:
            # 获取角色卡规则
            tmp_pcCardRule = 'default'
            if pc_name is not None:
                tmp_pcCardRule = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(pc_hash, pc_name) or 'default'
            # 解析表达式
            [tmp_rd_para_str, tmp_reast_str_remain] = OlivaDiceCore.msgReply.getExpression(
                tmp_reast_str,
                valueTable=skill_valueTable,
                pcCardRule=tmp_pcCardRule,
                flagDynamic=True,
                ruleMode='default'
            )
            [tmp_rd_para_str_show, _] = OlivaDiceCore.msgReply.getExpression(
                tmp_reast_str,
                valueTable=skill_valueTable,
                pcCardRule=tmp_pcCardRule,
                flagDynamic=None,
                ruleMode='default'
            )
            if tmp_rd_para_str is not None and tmp_rd_para_str != '':
                rd_para_str = tmp_rd_para_str
            # 剩余部分作为原因
            tmp_reast_str_remain = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str_remain)
            if len(tmp_reast_str_remain) > 0:
                rd_reason_str = tmp_reast_str_remain
        # 使用解析后的骰子表达式
        current_rd_para_str = rd_para_str
        current_rd_para_str_show = tmp_rd_para_str_show if not tmp_rd_para_str_show else rd_para_str
        tmp_template_customDefault = None
        if flag_groupTemplate is not None:
            tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(flag_groupTemplate)
            if 'customDefault' in tmp_template:
                tmp_template_customDefault = tmp_template['customDefault']
            if 'mainDice' in tmp_template and tmp_rd_para_str is None:
                current_rd_para_str = tmp_template['mainDice']
                current_rd_para_str_show = current_rd_para_str
        # 获取群组主骰配置
        rd_para_main_str = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId=tmp_hagID,
            userType='group',
            platform=plugin_event.platform['platform'],
            userConfigKey='groupMainDice',
            botHash=plugin_event.bot_info.hash
        )
        rd_para_main_D_right = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId=tmp_hagID,
            userType='group',
            platform=plugin_event.platform['platform'],
            userConfigKey='groupMainDiceDRight',
            botHash=plugin_event.bot_info.hash
        )
        if rd_para_main_str is not None and tmp_rd_para_str is None:
            current_rd_para_str = rd_para_main_str
            current_rd_para_str_show = current_rd_para_str
        tmp_template_customDefault = copy.deepcopy(tmp_template_customDefault)
        if isinstance(rd_para_main_D_right, int):
            if not isinstance(tmp_template_customDefault, dict):
                tmp_template_customDefault = {}
                if 'd' not in tmp_template_customDefault:
                    tmp_template_customDefault['d'] = {}
            tmp_template_customDefault['d']['rightD'] = rd_para_main_D_right
        # 掷骰
        rd_para = OlivaDiceCore.onedice.RD(current_rd_para_str, tmp_template_customDefault, valueTable=skill_valueTable)
        rd_para.ruleMode = 'default'
        rd_para.roll()
        OlivaDiceCore.onediceOverride.saveRDDataUser(
            data=rd_para,
            botHash=plugin_event.bot_info.hash,
            userId=member_id,
            platform=plugin_event.platform['platform']
        )
        if rd_para.resError is None:
            if not current_rd_para_str_show:
                current_rd_para_str_show = current_rd_para_str
            if not any(op in current_rd_para_str_show for op in ['+','-','*','/','^']) and current_rd_para_str.endswith("D"):
                current_rd_para_str_show += str(rd_para_main_D_right)
            tmp_resDetail_str = OlivaDiceCore.onediceOverride.RDDataFormat(
                data=rd_para.resDetailData,
                mode='default'
            )
            tmp_resInt_str = str(rd_para.resInt)
            if tmp_resDetail_str is None or tmp_resDetail_str == tmp_resInt_str:
                tmp_resDetail_str = ''
            if len(tmp_resDetail_str) == 0 or len(tmp_resDetail_str) > 150:
                if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                    roll_result = f"{current_rd_para_str_show}=" + ', '.join(
                        OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                    )
                elif len(tmp_resInt_str) > 100:
                    roll_result = f"{current_rd_para_str_show}={tmp_resInt_str[:50]}...的天文数字"
                else:
                    roll_result = f"{current_rd_para_str_show}={tmp_resInt_str}"
            else:
                if rd_para.resMetaTupleEnable and len(rd_para.resMetaTuple) > 1:
                    roll_result = f"{current_rd_para_str_show}={tmp_resDetail_str}=" + ', '.join(
                        OlivaDiceCore.onediceOverride.getRDResultFromList(rd_para.resMetaTuple)
                    )
                elif len(tmp_resInt_str) > 50:
                    roll_result = f"{current_rd_para_str_show}={tmp_resDetail_str}={tmp_resInt_str[:50]}...的天文数字"
                else:
                    roll_result = f"{current_rd_para_str_show}={tmp_resDetail_str}={tmp_resInt_str}"
            roll_results.append({
                'display_name': display_name,
                'user_name': user_name,
                'pc_name': pc_name,
                'roll_result': roll_result,
                'roll_value': rd_para.resInt
            })
        else:
            dictTValue['tResult'] = str(rd_para.resError)
            dictTValue['tRollPara'] = str(current_rd_para_str_show)
            roll_result = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_para.resError, dictStrCustom, dictTValue)
            roll_result += OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRollErrorHelp'], dictTValue)
            roll_results.append({
                'display_name': display_name,
                'user_name': user_name,
                'pc_name': pc_name,
                'roll_result': roll_result,
                'roll_value': "ERROR"
            })
    # 排序结果
    roll_results.sort(key=lambda x: (
        1 if isinstance(x['roll_value'], str) else 0, 
        -x['roll_value'] if not isinstance(x['roll_value'], str) else 0
    ))
    sorted_results = []
    for i, result in enumerate(roll_results, 1):
        member_roll_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom.get('strTeamRollMemberFormat', '[{tUserName}] - [{tPcName}]: {tRollResult}'),
            {
                'tUserName': result['user_name'],
                'tPcName': result['pc_name'] if result['pc_name'] else result['user_name'],
                'tRollResult': result['roll_result'],
                'tRollDetail': result['roll_result'].split('=')[0] if '=' in result['roll_result'] else result['roll_result']
            }
        )
        sorted_results.append(f"{i}. {member_roll_str}")
    dictTValue['tTeamName'] = team_name
    dictTValue['tRollResult'] = '\n'.join(sorted_results)
    if rd_reason_str:
        dictTValue['tReason'] = rd_reason_str
        reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamRollWithReason'], dictTValue
        )
    else:
        reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamRoll'], dictTValue
        )
    OlivaDiceCore.msgReply.replyMsg(plugin_event, reply_str)