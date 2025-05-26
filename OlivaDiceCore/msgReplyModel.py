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

contextFeq = 0.1

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
    replyMsg = OlivaDiceCore.msgReply.replyMsg

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

def get_SkillCheckResult(tmpSkillCheckType, dictStrCustom, dictTValue):
    res = dictStrCustom['strPcSkillCheckError']
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
    tmp_userID_1 = None
    tmp_pc_name_0 = '用户'
    tmp_pc_name_1 = '用户'
    tmp_Template = None
    tmp_TemplateRuleName = 'default'
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    
    if len(tmp_reast_str_para.data) >= 2:
        if type(tmp_reast_str_para.data[-1]) == OlivOS.messageAPI.PARA.at:
            tmp_userID_1 = tmp_reast_str_para.data[-1].data['id']
            tmp_userName01 = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId=tmp_userID_1,
                userType='user',
                platform=plugin_event.platform['platform'],
                userConfigKey='userName',
                botHash=plugin_event.bot_info.hash
            )
            plres_1 = plugin_event.get_stranger_info(tmp_userID_1)
            if plres_1['active']:
                dictTValue['tUserName01'] = plres_1['data']['name']
            else:
                dictTValue['tUserName01'] = tmp_userName01
            
            # 收集所有文本部分
            text_parts = []
            for item in tmp_reast_str_para.data:
                if type(item) == OlivOS.messageAPI.PARA.text:
                    text_parts.extend(item.data['text'].strip().split())
            
            # 解析技能名和数值
            if len(text_parts) > 0:
                # 支持以下格式:
                # 1. .rav 技能名1 数值1 技能名2 数值1 @其他人
                # 2. .rav 技能名1 数值1 技能名2 @其他人
                # 3. .rav 技能名1 技能名2 数值2 @其他人
                # 4. .rav 技能名1 技能名2 @其他人
                # 5. .rav 技能名1 @其他人
                
                # 先尝试提取所有数字
                numbers = []
                words = []
                for part in text_parts:
                    if part.isdigit():
                        numbers.append(int(part))
                    else:
                        words.append(part)
                
                # 根据数字数量决定解析方式
                if len(numbers) == 2:
                    # 格式1
                    if len(words) == 2:
                        tmp_skill_name_0 = words[0]
                        tmp_skill_value_0 = numbers[0]
                        tmp_skill_name_1 = words[1]
                        tmp_skill_value_1 = numbers[1]
                elif len(numbers) == 1:
                    # 格式2、3或6
                    if len(words) == 2:
                        # 检查数字位置
                        num_pos = text_parts.index(str(numbers[0]))
                        if num_pos == 1:
                            # 格式2
                            tmp_skill_name_0 = words[0]
                            tmp_skill_value_0 = numbers[0]
                            tmp_skill_name_1 = words[1]
                        elif num_pos == 2:
                            # 格式3
                            tmp_skill_name_0 = words[0]
                            tmp_skill_name_1 = words[1]
                            tmp_skill_value_1 = numbers[0]
                    elif len(words) == 1:
                        # 格式6
                        tmp_skill_name_0 = words[0]
                        tmp_skill_name_1 = words[0]
                        tmp_skill_value_0 = numbers[0]
                else:
                    # 格式4或5
                    if len(words) == 2:
                        # 格式4
                        tmp_skill_name_0 = words[0]
                        tmp_skill_name_1 = words[1]
                    elif len(words) == 1:
                        # 格式5
                        tmp_skill_name_0 = words[0]
                        tmp_skill_name_1 = words[0]
            
            flag_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId=tmp_hagID,
                userType='group',
                platform=tmp_platform,
                userConfigKey='groupTemplate',
                botHash=plugin_event.bot_info.hash
            )
            flag_groupTemplateRule = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId=tmp_hagID,
                userType='group',
                platform=tmp_platform,
                userConfigKey='groupTemplateRule',
                botHash=plugin_event.bot_info.hash
            )
            
            tmp_pcHash_0 = OlivaDiceCore.pcCard.getPcHash(tmp_userID, tmp_platform)
            tmp_pcHash_1 = OlivaDiceCore.pcCard.getPcHash(tmp_userID_1, tmp_platform)
            
            # 如果未从命令中获取数值，则从角色卡中获取
            if tmp_skill_value_0 is None:
                tmp_skill_value_0 = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                    tmp_pcHash_0, tmp_skill_name_0, hagId=tmp_hagID
                )
            tmp_pc_name_0 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash_0, tmp_hagID)
            
            if tmp_skill_value_1 is None:
                tmp_skill_value_1 = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                    tmp_pcHash_1, tmp_skill_name_1, hagId=tmp_hagID
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
                dictTValue['tSkillValue'] = str(tmp_skill_value_0)
                dictRuleTempData = {
                    'roll': rd_para.resInt,
                    'skill': tmp_skill_value_0
                }
                tmpSkillCheckType = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                    dictRuleTempData, tmp_Template, tmp_TemplateRuleName
                )
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
                dictTValue['tSkillValue01'] = str(tmp_skill_value_1)
                dictRuleTempData_1 = {
                    'roll': rd_para_1.resInt,
                    'skill': tmp_skill_value_1
                }
                tmpSkillCheckType_1 = OlivaDiceCore.skillCheck.getSkillCheckByTemplate(
                    dictRuleTempData_1, tmp_Template, tmp_TemplateRuleName
                )
            flag_rav_type = 'x'
            if tmpSkillCheckType in dictSkillCheckRank and tmpSkillCheckType_1 in dictSkillCheckRank:
                dictTValue['tSkillCheckReasult'] = get_SkillCheckResult(tmpSkillCheckType, dictStrCustom, dictTValue)
                dictTValue['tSkillCheckReasult01'] = get_SkillCheckResult(tmpSkillCheckType_1, dictStrCustom, dictTValue)
                if dictSkillCheckRank[tmpSkillCheckType] > dictSkillCheckRank[tmpSkillCheckType_1]:
                    flag_rav_type = '0'
                elif dictSkillCheckRank[tmpSkillCheckType] < dictSkillCheckRank[tmpSkillCheckType_1]:
                    flag_rav_type = '1'
                elif dictSkillCheckRank[tmpSkillCheckType] == dictSkillCheckRank[tmpSkillCheckType_1]:
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
            if tmp_pc_name_1 == None:
                res_1 = plugin_event.get_stranger_info(tmp_userID_1)
                if res_1['active']:
                    dictTValue['tName01'] = res_1['data']['name']
                else:
                    dictTValue['tName01'] = tmp_userName01
            dictTValue['tSkillName'] = tmp_skill_name_0
            dictTValue['tSkillName01'] = tmp_skill_name_1
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
    enableFalse:bool = True
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
    if tmp_key != None and tmp_value != None:
        if flag_mode == 'rec':
            tmp_rd = OlivaDiceCore.onedice.RD(tmp_value)
            tmp_rd.roll()
            if tmp_rd.resError != None:
                if enableFalse:
                    dictTValue['tResult'] = tmp_value
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetMapValueError'], dictTValue)
                    OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                return
        tmp_mappingRecord[tmp_key] = tmp_value
        OlivaDiceCore.pcCard.pcCardDataSetTemplateDataByKey(
            pcHash = tmp_pcHash,
            pcCardName = tmp_pc_name,
            dataKey = keyName,
            dataContent = tmp_mappingRecord
        )
        if enableFalse:
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcSetSkillValue'], dictTValue)
            OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
    elif tmp_key != None and tmp_value == None:
        if tmp_key in tmp_mappingRecord:
            tmp_value = tmp_mappingRecord[tmp_key]
            if enableFalse:
                dictTValue['tSkillName'] = tmp_key
                dictTValue['tSkillValue'] = tmp_value
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
    tmp_reast_str_list = tmp_reast_str.split(',')
    result_list = []
    count = 1
    flagLazy = False
    for tmp_reast_str_list_this in tmp_reast_str_list:
        tmp_value = '0'
        tmp_name = None
        flag_para_mode = '-'
        tmp_reast_str_list_this = tmp_reast_str_list_this.strip(' ')
        if len(tmp_reast_str_list_this) > 0:
            if len(tmp_reast_str_list_this) > 1 and tmp_reast_str_list_this[0] in ['+', '-', '*', '/', '^']:
                flag_para_mode = '1'
                tmp_value = '0'
                tmp_op = tmp_reast_str_list_this[0]
                [tmp_value, tmp_reast_str_list_this] = OlivaDiceCore.msgReply.getNumberPara(tmp_reast_str_list_this[1:])
                tmp_value = '1D20%s%s' % (tmp_op, tmp_value)
                tmp_reast_str_list_this = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str_list_this)
            elif len(tmp_reast_str_list_this) > 1 and tmp_reast_str_list_this[0] in ['=']:
                flag_para_mode = '2'
                tmp_value = '1D20'
                [tmp_value, tmp_reast_str_list_this] = OlivaDiceCore.msgReply.getExpression(tmp_reast_str_list_this[1:])
                tmp_reast_str_list_this = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str_list_this)
            elif tmp_reast_str_list_this[0].isdigit():
                flag_para_mode = '3'
                tmp_value = '0'
                [tmp_value, tmp_reast_str_list_this] = OlivaDiceCore.msgReply.getNumberPara(tmp_reast_str_list_this)
                tmp_reast_str_list_this = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str_list_this)
            tmp_reast_str_list_this = tmp_reast_str_list_this.strip(' ')
            if tmp_reast_str_list_this == '':
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
        elif not flagLazy:
            flagLazy = True
            tmp_value = None
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                tmp_pc_id,
                tmp_pc_platform
            )
            tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash,
                tmp_hagID
            )
            if tmp_pc_name != None:
                tmp_value_dict = OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                    pcHash = tmp_pcHash,
                    pcCardName = tmp_pc_name,
                    dataKey = 'mappingRecord',
                    resDefault = {}
                )
                if '先攻' in tmp_value_dict:
                    tmp_value = tmp_value_dict['先攻']
            tmp_name = tmp_pc_name
        tmp_value_final = None
        tmp_value_rd = OlivaDiceCore.onedice.RD(tmp_value)
        tmp_value_rd.roll()
        if tmp_value_rd.resError == None:
            tmp_value_final = tmp_value_rd.resInt
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
            dictTValue['tId'] = str(count)
            dictTValue['tSubName'] = tmp_name
            dictTValue['tSubResult'] = '%s=%d' % (tmp_value, tmp_value_final)
            result_list.append(
                OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitShowNode'], dictTValue)
            )
            count += 1
    if flag_reply:
        dictTValue['tResult'] = '\n'.join(result_list)
        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strPcInitSet'], dictTValue)
        OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)

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
        hagId = pcHash
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
