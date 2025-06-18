# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   skillCheck.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivaDiceCore

from enum import Enum
import traceback

class resultType(Enum):
    SKILLCHECK_NOPE = 0
    SKILLCHECK_SUCCESS = 1
    SKILLCHECK_FAIL = 2
    SKILLCHECK_GREAT_SUCCESS = 3
    SKILLCHECK_GREAT_FAIL = 4
    SKILLCHECK_HARD_SUCCESS = 5
    SKILLCHECK_EXTREME_HARD_SUCCESS = 6
    SKILLCHECK_FATE_01 = 7
    SKILLCHECK_FATE_02 = 8
    SKILLCHECK_FATE_03 = 9
    SKILLCHECK_FATE_04 = 10
    SKILLCHECK_FATE_05 = 11
    SKILLCHECK_FATE_06 = 12
    SKILLCHECK_FATE_07 = 13
    SKILLCHECK_FATE_08 = 14
    SKILLCHECK_FATE_09 = 15
    SKILLCHECK_FATE_10 = 16
    SKILLCHECK_FATE_11 = 17

dictSkillCheckResultRouter = {
    'success': resultType.SKILLCHECK_SUCCESS,
    'fail': resultType.SKILLCHECK_FAIL,
    'greatSuccess': resultType.SKILLCHECK_GREAT_SUCCESS,
    'greatFail': resultType.SKILLCHECK_GREAT_FAIL,
    'hardSuccess': resultType.SKILLCHECK_HARD_SUCCESS,
    'extremeHardSuccess': resultType.SKILLCHECK_EXTREME_HARD_SUCCESS,
    'fate01': resultType.SKILLCHECK_FATE_01,
    'fate02': resultType.SKILLCHECK_FATE_02,
    'fate03': resultType.SKILLCHECK_FATE_03,
    'fate04': resultType.SKILLCHECK_FATE_04,
    'fate05': resultType.SKILLCHECK_FATE_05,
    'fate06': resultType.SKILLCHECK_FATE_06,
    'fate07': resultType.SKILLCHECK_FATE_07,
    'fate08': resultType.SKILLCHECK_FATE_08,
    'fate09': resultType.SKILLCHECK_FATE_09,
    'fate10': resultType.SKILLCHECK_FATE_10,
    'fate11': resultType.SKILLCHECK_FATE_11
}

class ErrorType(Enum):
    UNKNOWN_ERROR = -1
    TEMPLATE_ERROR = -2

dictSkillCheckTemp = {
    'roll': 0,
    'skill': 0
}

def getSkillCheckByTemplate(data, template = None, ruleKey = 'default', difficulty_prefix = None):
    global dictSkillCheckTemp
    global dictSkillCheckResultRouter
    selection_key = 'checkRules'
    tmp_data = dictSkillCheckTemp.copy()
    tmp_template_dict = None
    tmp_template_rule_dict = None
    #处理人物卡模板规则
    if template == None:
        tmp_template_dict = OlivaDiceCore.pcCardData.dictPcCardTemplateDefault['default'].copy()
    else:
        tmp_template_dict = template.copy()
    if selection_key in tmp_template_dict:
        if ruleKey in tmp_template_dict[selection_key]:
            if 'default' in tmp_template_dict[selection_key]:
                tmp_template_rule_dict = tmp_template_dict[selection_key]['default'].copy()
            else:
                tmp_template_rule_dict = {}
            tmp_template_rule_dict.update(tmp_template_dict[selection_key][ruleKey])
    #处理临时参数
    tmp_data.update(data)
    difficulty_mapping = {
        '困难': 'hardSuccess',
        '极难': 'extremeHardSuccess',
        '大成功': 'greatSuccess'
    }
    
    difficulty_order = [
        'greatSuccess',
        'extremeHardSuccess',
        'hardSuccess',
        'success'
    ]
    
    current_difficulty_key = difficulty_mapping.get(difficulty_prefix)
    threshold_value = None
    special_text = None
    
    temp_result_enum = resultType.SKILLCHECK_NOPE
    if type(tmp_template_rule_dict) == dict:
        original_check_list = tmp_template_rule_dict.get('checkList', [])
        modified_check_list = original_check_list.copy()
        if difficulty_prefix:
            if difficulty_prefix == '困难':
                modified_check_list = [x for x in modified_check_list if x not in ['success']]
            elif difficulty_prefix == '极难':
                modified_check_list = [x for x in modified_check_list if x not in ['success', 'hardSuccess']]
            elif difficulty_prefix == '大成功':
                modified_check_list = [x for x in modified_check_list if x not in ['success', 'hardSuccess', 'extremeHardSuccess']]
        
        # DeltaGreen规则的特殊处理
        if ruleKey == 'DeltaGreen' and difficulty_prefix in ['困难','极难','大成功']:
            special_text = '结果为1或小于技巧两骰相同'
        
        if not special_text and current_difficulty_key and current_difficulty_key in tmp_template_rule_dict:
            threshold_value = calculateThreshold(tmp_template_rule_dict[current_difficulty_key], tmp_data)
            if threshold_value == 0:
                if difficulty_prefix == '困难':
                    if 'extremeHardSuccess' in tmp_template_rule_dict:
                        threshold_value = calculateThreshold(tmp_template_rule_dict['extremeHardSuccess'], tmp_data)
                    if threshold_value == 0 and 'greatSuccess' in tmp_template_rule_dict:
                        threshold_value = calculateThreshold(tmp_template_rule_dict['greatSuccess'], tmp_data)
                elif difficulty_prefix == '极难':
                    if 'greatSuccess' in tmp_template_rule_dict:
                        threshold_value = calculateThreshold(tmp_template_rule_dict['greatSuccess'], tmp_data)
        
        if 'greatFail' in tmp_template_rule_dict:
            great_fail_result = culRule('.node', tmp_template_rule_dict['greatFail'], tmp_data)
            if great_fail_result == True:
                if special_text and difficulty_prefix == '大成功':
                    threshold_value = special_text
                return resultType.SKILLCHECK_GREAT_FAIL, threshold_value
        
        for difficulty in difficulty_order:
            if difficulty in modified_check_list and difficulty in tmp_template_rule_dict:
                temp_result = culRule('.node', tmp_template_rule_dict[difficulty], tmp_data)
                if temp_result == True:
                    temp_result_enum = dictSkillCheckResultRouter[difficulty]
                    break
        
        if temp_result_enum == resultType.SKILLCHECK_NOPE:
            if 'fail' in tmp_template_rule_dict:
                fail_result = culRule('.node', tmp_template_rule_dict['fail'], tmp_data)
                if fail_result == True:
                    temp_result_enum = resultType.SKILLCHECK_FAIL
        
        if temp_result_enum == resultType.SKILLCHECK_NOPE:
            for difficulty in original_check_list:
                if difficulty in tmp_template_rule_dict:
                    temp_result = culRule('.node', tmp_template_rule_dict[difficulty], tmp_data)
                    if temp_result == True:
                        temp_result_enum = resultType.SKILLCHECK_FAIL
                        break
                    
        if special_text:
            threshold_value = special_text
            
    return temp_result_enum, threshold_value

def calculateThreshold(ruleNode, tmp_data):
    threshold_data = tmp_data.copy()
    skill_value = tmp_data['skill']
    threshold = 0
    threshold_a = 0
    threshold_b = 0
    for i in range(skill_value, 0, -1):
        threshold_data['roll'] = i
        if culRule('.node', ruleNode, threshold_data):
            threshold_a = i
            break
    # dnd大成功显示兼1-5大成功显示
    for i in range(20, 0, -1):
        threshold_data['roll'] = i
        if culRule('.node', ruleNode, threshold_data):
            threshold_b = i
            break
    threshold = max(threshold_a, threshold_b)
    return threshold

def culRule(nodeKey, nodeData, tempData):
    temp_result = False
    if nodeData == None:
        temp_result = False
    elif type(nodeData) == int:
        temp_result = nodeData
    elif type(nodeData) == str:
        if len(nodeData) > 1:
            if nodeData[0] == '$':
                if nodeData[1:] in tempData:
                    temp_result = tempData[nodeData[1:]]
    elif type(nodeData) == dict:
        if nodeKey == '.node':
            for nodeData_this in nodeData:
                temp_result = culRule(nodeData_this, nodeData[nodeData_this], tempData)
        elif nodeKey == '.and':
            temp_result_1 = True
            for nodeData_this in nodeData:
                temp_result_2 = culRule(nodeData_this, nodeData[nodeData_this], tempData)
                if temp_result_2 == False:
                    temp_result_1 = False
            temp_result = temp_result_1
        elif nodeKey == '.or':
            temp_result_1 = False
            for nodeData_this in nodeData:
                temp_result_2 = culRule(nodeData_this, nodeData[nodeData_this], tempData)
                if temp_result_2 == True:
                    temp_result_1 = True
            temp_result = temp_result_1
    elif type(nodeData) == list:
        if nodeKey == '.node':
            for nodeData_this in nodeData:
                temp_result = culRule('.node', nodeData_this, tempData)
        elif nodeKey == '.and':
            temp_result_1 = True
            for nodeData_this in nodeData:
                temp_result_2 = culRule('.node', nodeData_this, tempData)
                if temp_result_2 == False:
                    temp_result_1 = False
            temp_result = temp_result_1
        elif nodeKey == '.or':
            temp_result_1 = False
            for nodeData_this in nodeData:
                temp_result_2 = culRule('.node', nodeData_this, tempData)
                if temp_result_2 == True:
                    temp_result_1 = True
            temp_result = temp_result_1
        elif nodeKey == '.==':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                if temp_result_2_1 == temp_result_2_2:
                    temp_result_1 = True
            temp_result = temp_result_1
        elif nodeKey == '.>':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                if temp_result_2_1 > temp_result_2_2:
                    temp_result_1 = True
            temp_result = temp_result_1
        elif nodeKey == '.<':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                if temp_result_2_1 < temp_result_2_2:
                    temp_result_1 = True
            temp_result = temp_result_1
        elif nodeKey == '.>=':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                if temp_result_2_1 >= temp_result_2_2:
                    temp_result_1 = True
            temp_result = temp_result_1
        elif nodeKey == '.<=':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                if temp_result_2_1 <= temp_result_2_2:
                    temp_result_1 = True
            temp_result = temp_result_1
        elif nodeKey == '.+':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                temp_result_1 = int(temp_result_2_1 + temp_result_2_2)
            temp_result = temp_result_1
        elif nodeKey == '.-':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                temp_result_1 = int(temp_result_2_1 - temp_result_2_2)
            temp_result = temp_result_1
        elif nodeKey == '.*':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                temp_result_1 = int(temp_result_2_1 * temp_result_2_2)
            temp_result = temp_result_1
        elif nodeKey == './':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                temp_result_1 = int(temp_result_2_1 / temp_result_2_2)
            temp_result = temp_result_1
        elif nodeKey == '.%':
            temp_result_1 = False
            if len(nodeData) >= 2:
                temp_result_2_1 = culRule('.node', nodeData[0], tempData)
                temp_result_2_2 = culRule('.node', nodeData[1], tempData)
                temp_result_1 = int(temp_result_2_1 % temp_result_2_2)
            temp_result = temp_result_1
    return temp_result

def isSpecialSkill(skillName:str, pcCardRule:str):
    res = False
    if pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial \
    and skillName in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[pcCardRule]:
        res = True
    return res

def getSpecialSkillReplace(srcPara:str, pcCardRule:str, pcCardData:dict):
    res = srcPara
    if pcCardRule in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial:
        for skill_this in OlivaDiceCore.pcCardData.dictPcCardMappingSpecial[pcCardRule]:
            res_this = getSpecialSkill(skill_this, pcCardRule, pcCardData)
            if type(res_this) is str:
                res = res.replace('{%s}' % skill_this, skill_this)
                res = res.replace('%s' % skill_this, res_this)
    return res

def getSpecialSkill(skillName:str, pcCardRule:str, pcCardData:dict):
    res = None
    if isSpecialSkill(skillName, pcCardRule):
        if skillName == '体格':
            if type(pcCardData) is dict \
            and 'STR' in pcCardData \
            and 'SIZ' in pcCardData:
                try:
                    tmp_sum = int(pcCardData['STR']) + int(pcCardData['SIZ'])
                    if tmp_sum <= 64:
                        res = -2
                    elif tmp_sum <= 84:
                        res = -1
                    elif tmp_sum <= 124:
                        res = 0
                    elif tmp_sum <= 164:
                        res = 1
                    elif tmp_sum <= 204:
                        res = 2
                    else:
                        res = int((tmp_sum - 205) / 80) + 2
                except:
                    res = None
            else:
                res = 0
        elif skillName == 'DB':
            """
            根据COC7th规则计算DB
            如果缺少任何属性或计算失败，返回0
            
            COC7th规则:
            STR+SIZ的和为左侧，DB为右侧
            2-64: -2
            65-84: -1
            85-124: 0
            125-164: +1d4
            165-204: +1d6
            205-284: +2d6
            285-364: +3d6
            365-444: +4d6
            之后每超过80，再加1d6
            """
            if type(pcCardData) is dict \
            and 'STR' in pcCardData \
            and 'SIZ' in pcCardData:
                try:
                    tmp_sum = int(pcCardData['STR']) + int(pcCardData['SIZ'])
                    if tmp_sum <= 64:
                        res = -2
                    elif tmp_sum <= 84:
                        res = -1
                    elif tmp_sum <= 124:
                        res = 0
                    elif tmp_sum <= 164:
                        res = '1D4'
                    elif tmp_sum <= 204:
                        res = '1D6'
                    else:
                        res = '%dD6' % (int((tmp_sum - 205) / 80) + 1)
                except:
                    res = None
            else:
                res = 0
    res = f'({res})' if type(res) in (int,) and res < 0 else res
    res = res if res == None else str(res)
    return res
