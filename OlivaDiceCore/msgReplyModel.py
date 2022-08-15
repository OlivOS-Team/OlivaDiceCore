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
        dictTValue['tRollResult'] = '%s=%s=%d' % (
            OlivaDiceCore.onediceOverride.getRDDataRawUser(
                botHash = plugin_event.bot_info.hash,
                userId = tmp_userID,
                platform = tmp_user_platform
            ),
            tmp_RDData_str,
            OlivaDiceCore.onediceOverride.getRDDataIntUser(
                botHash = plugin_event.bot_info.hash,
                userId = tmp_userID,
                platform = tmp_user_platform
            )
        )
        tmp_reply_str = dictStrCustom['strRollRecord'].format(**dictTValue)
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

def get_SkillCheckReasult(tmpSkillCheckType, dictStrCustom):
    res = dictStrCustom['strPcSkillCheckError']
    if tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS:
        res = dictStrCustom['strPcSkillCheckSucceed']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_HARD_SUCCESS:
        res = dictStrCustom['strPcSkillCheckHardSucceed']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_EXTREME_HARD_SUCCESS:
        res = dictStrCustom['strPcSkillCheckExtremeHardSucceed']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS:
        res = dictStrCustom['strPcSkillCheckGreatSucceed']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL:
        res = dictStrCustom['strPcSkillCheckFailed']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL:
        res = dictStrCustom['strPcSkillCheckGreatFailed']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_01:
        res = dictStrCustom['strPcSkillCheckFate01']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_02:
        res = dictStrCustom['strPcSkillCheckFate02']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_03:
        res = dictStrCustom['strPcSkillCheckFate03']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_04:
        res = dictStrCustom['strPcSkillCheckFate04']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_05:
        res = dictStrCustom['strPcSkillCheckFate05']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_06:
        res = dictStrCustom['strPcSkillCheckFate06']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_07:
        res = dictStrCustom['strPcSkillCheckFate07']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_08:
        res = dictStrCustom['strPcSkillCheckFate08']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_09:
        res = dictStrCustom['strPcSkillCheckFate09']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_10:
        res = dictStrCustom['strPcSkillCheckFate10']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FATE_11:
        res = dictStrCustom['strPcSkillCheckFate11']
    elif tmpSkillCheckType == OlivaDiceCore.skillCheck.resultType.SKILLCHECK_NOPE:
        res = dictStrCustom['strPcSkillCheckNope']
    else:
        res = dictStrCustom['strPcSkillCheckError']
    return res


def replyRAV_command(plugin_event, Proc, valDict):
    tmp_reast_str = valDict['tmp_reast_str']
    flag_is_from_master = valDict['flag_is_from_master']
    tmp_userID = valDict['tmp_userID']
    tmp_hagID = valDict['tmp_hagID']
    tmp_platform = valDict['tmp_platform']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    replyMsg = OlivaDiceCore.msgReply.replyMsg

    if tmp_hagID == None:
        return

    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'rav')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    tmp_reast_str = tmp_reast_str.rstrip(' ')
    tmp_skill_name = None
    tmp_skill_value_0 = None
    tmp_skill_value_1 = None
    tmp_userID_1 = None
    tmp_pc_name_0 = '用户'
    tmp_pc_name_1 = '用户'
    tmp_Template = None
    tmp_TemplateRuleName = 'default'
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    if len(tmp_reast_str_para.data) >= 2:
        if (
            type(tmp_reast_str_para.data[0]) == OlivOS.messageAPI.PARA.text
        ) and (
            type(tmp_reast_str_para.data[1]) == OlivOS.messageAPI.PARA.at
        ):
            tmp_skill_name = tmp_reast_str_para.data[0].data['text'].strip(' ')
            tmp_userID_1 = tmp_reast_str_para.data[1].data['id']
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
            tmp_pcHash_0 = OlivaDiceCore.pcCard.getPcHash(
                tmp_userID,
                tmp_platform
            )
            tmp_pcHash_1 = OlivaDiceCore.pcCard.getPcHash(
                tmp_userID_1,
                tmp_platform
            )
            tmp_skill_value_0 = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                tmp_pcHash_0,
                tmp_skill_name,
                hagId = tmp_hagID
            )
            tmp_pc_name_0 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash_0,
                tmp_hagID
            )
            tmp_skill_value_1 = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                tmp_pcHash_1,
                tmp_skill_name,
                hagId = tmp_hagID
            )
            tmp_pc_name_1 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash_1,
                tmp_hagID
            )
            if tmp_pc_name_0 != None:
                dictTValue['tName'] = tmp_pc_name_0
                tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(
                    tmp_pcHash_0,
                    tmp_pc_name_0
                )
                if flag_groupTemplate != None:
                    tmp_template_name = flag_groupTemplate
                if tmp_template_name != None:
                    tmp_Template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                tmp_template_rule_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateRuleKey(
                    tmp_pcHash_0,
                    tmp_pc_name_0
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
                    dictRuleTempData,
                    tmp_Template,
                    tmp_TemplateRuleName
                )
            rd_para_1 = OlivaDiceCore.onedice.RD(rd_para_str, tmp_customDefault)
            rd_para_1.roll()
            tmpSkillCheckType_1 = None
            dictRuleTempData_1 = {
                'roll': 0,
                'skill': tmp_skill_value_1
            }
            if rd_para_1.resError == None:
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
                    dictRuleTempData_1,
                    tmp_Template,
                    tmp_TemplateRuleName
                )
            flag_rav_type = 'x'
            if tmpSkillCheckType in dictSkillCheckRank and tmpSkillCheckType_1 in dictSkillCheckRank:
                dictTValue['tSkillCheckReasult'] = get_SkillCheckReasult(tmpSkillCheckType, dictStrCustom)
                dictTValue['tSkillCheckReasult01'] = get_SkillCheckReasult(tmpSkillCheckType_1, dictStrCustom)
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
            dictTValue['tSkillName'] = tmp_skill_name
            if flag_rav_type == '0':
                dictTValue['tRAVResult'] = dictStrCustom['strRAVResult01'].format(**dictTValue)
            elif flag_rav_type == '1':
                dictTValue['tRAVResult'] = dictStrCustom['strRAVResult02'].format(**dictTValue)
            elif flag_rav_type == '-':
                dictTValue['tRAVResult'] = dictStrCustom['strRAVResult03'].format(**dictTValue)
            tmp_reply_str = dictStrCustom['strRAVShow'].format(**dictTValue)
            replyMsg(plugin_event, tmp_reply_str)
    else:
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'rav')
