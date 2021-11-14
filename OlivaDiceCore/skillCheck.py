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

def getSkillCheckByTemplate(data, template = None, ruleKey = 'default'):
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
    #处理检定逻辑
    temp_result_enum = resultType.SKILLCHECK_NOPE
    if type(tmp_template_rule_dict) == dict:
        if 'checkList' in tmp_template_rule_dict:
            for dictSkillCheckResultRouter_this in tmp_template_rule_dict['checkList']:
                if dictSkillCheckResultRouter_this in dictSkillCheckResultRouter:
                    temp_result = False
                    if dictSkillCheckResultRouter_this in tmp_template_rule_dict:
                        temp_result = culRule('.node', tmp_template_rule_dict[dictSkillCheckResultRouter_this], tmp_data)
                    if temp_result == True:
                        temp_result_enum = dictSkillCheckResultRouter[dictSkillCheckResultRouter_this]
    return temp_result_enum


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
