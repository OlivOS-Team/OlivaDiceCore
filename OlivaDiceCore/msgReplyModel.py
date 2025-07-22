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
            tmp_userName01 = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = tmp_userID_1,
                userType = 'user',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash
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
                # 6: .rav 技能名1 数值1 @其他人
                
                # 先尝试提取所有数字
                numbers = []
                words = []
                is_rav = False
                for part in text_parts:
                    if part.isdigit():
                        numbers.append(int(part))
                    else:
                        words.append(part)

                # 处理第一个技能名
                if OlivaDiceCore.msgReply.isMatchWordStart(words[0], ['困难成功', '困难']):
                    difficulty_0 = '困难'
                    words[0] = OlivaDiceCore.msgReply.getMatchWordStartRight(words[0], ['困难成功', '困难']).strip()
                elif OlivaDiceCore.msgReply.isMatchWordStart(words[0], ['极难成功', '极限成功', '极难', '极限']):
                    difficulty_0 = '极难'
                    words[0] = OlivaDiceCore.msgReply.getMatchWordStartRight(words[0], ['极难成功', '极限成功', '极难', '极限']).strip()
                elif OlivaDiceCore.msgReply.isMatchWordStart(words[0], '大成功'):
                    difficulty_0 = '大成功'
                    words[0] = OlivaDiceCore.msgReply.getMatchWordStartRight(words[0], '大成功').strip()
                
                # 处理第二个技能名
                if len(words) > 1:
                    if OlivaDiceCore.msgReply.isMatchWordStart(words[1], ['困难成功', '困难']):
                        difficulty_1 = '困难'
                        words[1] = OlivaDiceCore.msgReply.getMatchWordStartRight(words[1], ['困难成功', '困难']).strip()
                    elif OlivaDiceCore.msgReply.isMatchWordStart(words[1], ['极难成功', '极限成功', '极难', '极限']):
                        difficulty_1 = '极难'
                        words[1] = OlivaDiceCore.msgReply.getMatchWordStartRight(words[1], ['极难成功', '极限成功', '极难', '极限']).strip()
                    elif OlivaDiceCore.msgReply.isMatchWordStart(words[1], '大成功'):
                        difficulty_1 = '大成功'
                        words[1] = OlivaDiceCore.msgReply.getMatchWordStartRight(words[1], '大成功').strip()

                # 根据数字数量决定解析方式
                if len(numbers) == 2:
                    # 格式1
                    if len(words) == 2:
                        tmp_skill_name_0 = words[0]
                        tmp_skill_value_0 = numbers[0]
                        tmp_skill_name_1 = words[1]
                        tmp_skill_value_1 = numbers[1]
                        is_rav = True
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
                            is_rav = True
                        elif num_pos == 2:
                            # 格式3
                            tmp_skill_name_0 = words[0]
                            tmp_skill_name_1 = words[1]
                            tmp_skill_value_1 = numbers[0]
                            is_rav = True
                    elif len(words) == 1:
                        # 格式6
                        tmp_skill_name_0 = words[0]
                        tmp_skill_name_1 = words[0]
                        tmp_skill_value_0 = numbers[0]
                        tmp_skill_value_1 = numbers[0]
                        is_rav = True
                else:
                    # 格式4或5
                    if len(words) == 2:
                        # 格式4
                        tmp_skill_name_0 = words[0]
                        tmp_skill_name_1 = words[1]
                        is_rav = True
                    elif len(words) == 1:
                        # 格式5
                        tmp_skill_name_0 = words[0]
                        tmp_skill_name_1 = words[0]
                        is_rav = True
            
            difficulty_1 = difficulty_0 if not difficulty_1 else difficulty_1
            
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

                tmp_pcHash_0 = OlivaDiceCore.pcCard.getPcHash(tmp_userID, tmp_platform)
                tmp_pcHash_1 = OlivaDiceCore.pcCard.getPcHash(tmp_userID_1, tmp_platform)

                # 如果未从命令中获取数值，则从角色卡中获取
                if tmp_skill_value_0 is None:
                    tmp_skill_value_0 = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                        tmp_pcHash_0, tmp_skill_name_0, hagId = tmp_hagID
                    )
                tmp_pc_name_0 = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash_0, tmp_hagID)

                if tmp_skill_value_1 is None:
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
                    res_1 = plugin_event.get_stranger_info(tmp_userID_1)
                    if res_1['active']:
                        dictTValue['tName01'] = res_1['data']['name']
                    else:
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

def replyTEAM_command(plugin_event, Proc, valDict, flag_is_from_group_admin):
    tmp_reast_str = valDict['tmp_reast_str']
    flag_is_from_master = valDict['flag_is_from_master']
    tmp_hagID = valDict['tmp_hagID']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'team')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    
    if OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'show'):
        team_show(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'list'):
        team_list(plugin_event, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'rm'):
        team_remove(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                           flag_is_from_master, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'del'):
        team_delete(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                           flag_is_from_master, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['clear','clr']):
        team_clear(plugin_event, tmp_reast_str, tmp_hagID, flag_is_from_group_admin, 
                          flag_is_from_master, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'at'):
        team_at(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'set'):
        team_set(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['sort','arr']):
        team_sort(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'rename'):
        team_rename(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['st','pc']):
        team_st(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, ['ra','rc']):
        team_ra(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'sc'):
        team_sc(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)
    elif OlivaDiceCore.msgReply.isMatchWordStart(tmp_reast_str, 'help', fullMatch=True):
        OlivaDiceCore.msgReply.replyMsgLazyHelpByEvent(plugin_event, 'team')
    else:
        team_create(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom)

def team_create(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    team_name = None
    members = []
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
            plres = plugin_event.get_stranger_info(member_id)
            user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = member_id,
                userType = 'user',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash,
                default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
            )
            if plres['active'] and user_name == f'用户{member_id}':
                user_name = plres['data']['name']
            # 获取当前人物卡
            pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
            pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
            member_info.append(f"成员{index}: [{user_name}] - 人物卡: [{pc_name if pc_name else {user_name}}]")
            index += 1
    dictTValue['tTeamName'] = team_name
    dictTValue['tMemberCount'] = str(len(members))
    dictTValue['tMembers'] = '\n'.join(member_info)
    OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
        dictStrCustom['strTeamCreated'], dictTValue
    ))

def team_show(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'show')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
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
        plres = plugin_event.get_stranger_info(member_id)
        user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = member_id,
            userType = 'user',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'userName',
            botHash = plugin_event.bot_info.hash,
            default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
        )
        if plres['active'] and user_name == f'用户{member_id}':
            user_name = plres['data']['name']
        # 获取当前人物卡
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        member_info.append(f"成员{index}: [{user_name}] - 人物卡: [{pc_name if pc_name else {user_name}}]")
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
                flag_is_from_master, dictTValue, dictStrCustom):
    if not (flag_is_from_group_admin or flag_is_from_master):
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strNeedAdmin'], dictTValue
        ))
        return
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'rm')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    team_name = None
    members_to_remove = []
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
        plres = plugin_event.get_stranger_info(member_id)
        user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = member_id,
            userType = 'user',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'userName',
            botHash = plugin_event.bot_info.hash,
            default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
        )
        if plres['active'] and user_name == f'用户{member_id}':
            user_name = plres['data']['name']
        # 获取人物卡名
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        display_name = f"-> [{user_name}] - [{pc_name if pc_name else user_name}]"
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
            plres = plugin_event.get_stranger_info(member_id)
            user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = member_id,
                userType = 'user',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash,
                default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
            )
            if plres['active'] and user_name == f'用户{member_id}':
                user_name = plres['data']['name']
            # 获取当前人物卡
            pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
            pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
            member_info.append(f"成员{index}: [{user_name}] - 人物卡: [{pc_name if pc_name else {user_name}}]")
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
                flag_is_from_master, dictTValue, dictStrCustom):
    if not (flag_is_from_group_admin or flag_is_from_master):
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strNeedAdmin'], dictTValue
        ))
        return
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'del')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
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
               flag_is_from_master, dictTValue, dictStrCustom):
    if not (flag_is_from_group_admin or flag_is_from_master):
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strNeedAdmin'], dictTValue
        ))
        return
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, ['clear','clr'])
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
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

def team_at(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'at')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
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

def team_set(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'set')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    team_name = tmp_reast_str.strip()
    team_config = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = plugin_event.platform['platform'],
        userConfigKey = 'teamConfig',
        botHash = plugin_event.bot_info.hash,
        default = {}
    )
    
    # 检查小队是否存在
    if team_name not in team_config:
        dictTValue['tTeamName'] = team_name
        OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
            dictStrCustom['strTeamNotFound'], dictTValue
        ))
        return
    
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

def team_sort(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
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
    # 按名称长度降序排序，优先匹配更长的名称
    sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
    team_name = None
    skill_name = None
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
        plres = plugin_event.get_stranger_info(member_id)
        user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = member_id,
            userType = 'user',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'userName',
            botHash = plugin_event.bot_info.hash,
            default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
        )
        if plres['active'] and user_name == f'用户{member_id}':
            user_name = plres['data']['name']
        
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
        line = f"{index}. [{member['name']}] - [{member['pc_name'] if member['pc_name'] else member['name']}]({skill_name}: {member['skill_value']})"
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
def team_st(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
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
    # 按名称长度降序排序，优先匹配更长的名称
    sorted_team_names = sorted(team_config.keys(), key=lambda x: -len(x))
    team_name = None
    skill_operations = None
    # 尝试匹配小队名称
    for candidate in sorted_team_names:
        if tmp_reast_str.startswith(candidate):
            team_name = candidate
            skill_operations = tmp_reast_str[len(candidate):].strip()
            break
    if team_name is None:
        if active_team is None:
            OlivaDiceCore.msgReply.replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                dictStrCustom['strNoActiveTeam'], dictTValue
            ))
            return
        team_name = active_team
        skill_operations = tmp_reast_str.strip()
    if not skill_operations:
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
        for skill_name in pc_skills:
            if not skill_name.startswith('__'):
                # 移除技能名中的数字
                clean_skill_name = re.sub(r'\d+', '', skill_name).upper()
                all_pc_skill_names.add(clean_skill_name)
    # 预处理字符串，在特定字母先查找技能名，找到技能名后添加空格
    processed_skill_ops = skill_operations
    for start_char in OlivaDiceCore.pcCardData.arrPcCardLetterStart:
        i = 0
        while i < len(processed_skill_ops):
            if processed_skill_ops[i].lower() == start_char.lower():
                max_len = 0
                for skill in sorted(all_pc_skill_names, key = len, reverse = True):
                    if skill.startswith(start_char.upper()) and processed_skill_ops[i:].upper().startswith(skill):
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
    op_list = ['+', '-', '*', '/']
    skill_updates = []
    # 分割技能操作
    current_pos = 0
    while current_pos < len(processed_skill_ops):
        # 查找技能名结束位置（遇到操作符）
        skill_end_pos = -1
        for i in range(current_pos, len(processed_skill_ops)):
            if processed_skill_ops[i] in op_list:
                skill_end_pos = i
                break
        if skill_end_pos == -1:
            break
        skill_name = processed_skill_ops[current_pos:skill_end_pos].strip()
        if not skill_name:
            current_pos = skill_end_pos + 1
            continue
        op = processed_skill_ops[skill_end_pos]
        rest_str = processed_skill_ops[skill_end_pos+1:]
        # 提取表达式
        expr_end_pos = 0
        in_dice_expr = False
        for i in range(len(rest_str)):
            char = rest_str[i]
            if char.upper() == 'D':
                in_dice_expr = True
            if char.isdigit() or (in_dice_expr and char in op_list) or char.upper() == 'D':
                expr_end_pos = i + 1
            else:
                if i > 0:
                    expr_end_pos = i
                break
        if expr_end_pos == 0 and len(rest_str) > 0:
            expr_end_pos = 1
        expr_str = rest_str[:expr_end_pos]
        current_pos = skill_end_pos + expr_end_pos + 1
        if skill_name and expr_str:
            # 移除技能名中的数字
            clean_skill_name = re.sub(r'\d+', '', skill_name).upper()
            skill_updates.append((clean_skill_name, op, expr_str))
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
                if 'D' in expr_str.upper():
                    member_results.append(f"[{skill_name}]: {current_value}{op}{expr_str}={rd_para.resDetail}={new_value}")
                else:
                    member_results.append(f"[{skill_name}]: {current_value}{op}{expr_str}={new_value}")
            else:
                member_results.append(f"{skill_name}: 表达式错误 '{op}{expr_str}'")
            OlivaDiceCore.msgReply.trigger_auto_sn_update(plugin_event, tmp_pc_id, tmp_pc_platform, tmp_hagID, dictTValue)
        plres = plugin_event.get_stranger_info(member_id)
        user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = tmp_pc_id,
            userType = 'user',
            platform = tmp_pc_platform,
            userConfigKey = 'userName',
            botHash = plugin_event.bot_info.hash,
            default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
        )
        if plres['active'] and user_name == f'用户{member_id}':
            user_name = plres['data']['name']
        if member_results:
            results.append(f"-> [{user_name}] - [{tmp_pc_name}]:\n" + '\n'.join(member_results))
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

def team_ra(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
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
    team_name = None
    skill_expr = tmp_reast_str
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

    # 解析难度前缀
    if OlivaDiceCore.msgReply.isMatchWordStart(skill_expr, ['困难成功', '困难']):
        difficulty = '困难'
        skill_expr = OlivaDiceCore.msgReply.getMatchWordStartRight(skill_expr, ['困难成功', '困难']).strip()
    elif OlivaDiceCore.msgReply.isMatchWordStart(skill_expr, ['极难成功', '极限成功', '极难', '极限']):
        difficulty = '极难'
        skill_expr = OlivaDiceCore.msgReply.getMatchWordStartRight(skill_expr, ['极难成功', '极限成功', '极难', '极限']).strip()
    elif OlivaDiceCore.msgReply.isMatchWordStart(skill_expr, '大成功'):
        difficulty = '大成功'
        skill_expr = OlivaDiceCore.msgReply.getMatchWordStartRight(skill_expr, '大成功').strip()
    skill_expr = OlivaDiceCore.msgReply.skipSpaceStart(skill_expr)
    # 解析技能名和表达式
    if skill_expr:
        op_list = ['+', '-', '*', '/']
        pos = len(skill_expr)
        for i, char in enumerate(skill_expr):
            if char in op_list or char.isdigit():
                pos = i
                break
        skill_name = skill_expr[:pos].strip().upper() or None
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
        plres = plugin_event.get_stranger_info(member_id)
        user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = member_id,
            userType = 'user',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'userName',
            botHash = plugin_event.bot_info.hash,
            default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
        )
        if plres['active'] and user_name == f'用户{member_id}':
            user_name = plres['data']['name']
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        display_name = f"[{user_name}] - [{pc_name if pc_name else user_name}]"
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
        result_str = f"{display_name}"
        if skill_name:
            result_str += f"({skill_name}: {skill_value_str}): {dice_detail}/{skill_value_str} "
        else:
            result_str += f": {dice_detail}/{skill_value_str} "
        result_str += get_SkillCheckResult(skill_check_type, dictStrCustom, dictTValue)
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
def team_sc(plugin_event, tmp_reast_str, tmp_hagID, dictTValue, dictStrCustom):
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
    team_name = None
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
        plres = plugin_event.get_stranger_info(member_id)
        user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
            userId = member_id,
            userType = 'user',
            platform = plugin_event.platform['platform'],
            userConfigKey = 'userName',
            botHash = plugin_event.bot_info.hash,
            default = plres['data']['name'] if plres['active'] else f"用户{member_id}"
        )
        if plres['active'] and user_name == f'用户{member_id}':
            user_name = plres['data']['name']
        pc_hash = OlivaDiceCore.pcCard.getPcHash(member_id, plugin_event.platform['platform'])
        pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, tmp_hagID)
        # 构建显示名称
        display_name = f"[{user_name}] - [{pc_name if pc_name else user_name}]"
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
        result_str = f"{display_name}(SAN:{current_san}): {dice_detail}/{current_san}"
        result_str += f"\nSAN: {current_san} -> {new_san}(损失{san_success if roll_value < current_san else san_fail}={san_loss}点)"
        result_str += get_SkillCheckResult(skill_check_type, dictStrCustom, dictTValue)
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
    
