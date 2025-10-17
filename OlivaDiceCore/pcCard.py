# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   pcCard.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

import hashlib
import json
import os
import traceback
import sys

import copy

dictPcCardData = {
    'unity' : {}
}

dictPcCardSelection = {
    'unity' : {}
}

dictPcCardTemplate = {
    'unity' : {}
}

dictPcCardTemplateDefault = {
    'unity' : OlivaDiceCore.pcCardData.dictPcCardTemplateDefault.copy()
}

dictPcCardHiy = {
    'unity' : {}
}

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def dataPcCardTemplateDefaultInit():
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    OlivaDiceCore.pcCardData.dictPcCardTemplateDefault = copy.deepcopy(
        OlivaDiceCore.pcCardData.dictPcCardTemplateDefaultTemp
    )

    dataDirRoot_this = OlivaDiceCore.data.dataDirRoot
    releaseDir(dataDirRoot_this + '/unity')
    releaseDir(dataDirRoot_this + '/unity/extend')
    releaseDir(dataDirRoot_this + '/unity/extend/template')
    dataDir = dataDirRoot_this + '/unity/extend/template'
    dataPathList = os.listdir(dataDir)
    for dataName in dataPathList:
        dataPath = dataDir + '/' + dataName
        try:
            with open(dataPath, 'r', encoding = 'utf-8') as data_f:
                tmp_dictPcCardTemplatePatch = json.loads(data_f.read())
                for templateName in tmp_dictPcCardTemplatePatch:
                    if templateName not in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault:
                        OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[templateName] = copy.deepcopy(
                            OlivaDiceCore.pcCardData.dictPcCardTemplateModel
                        )
                    for templateModelName in tmp_dictPcCardTemplatePatch[templateName]:
                        if templateModelName not in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[templateName]:
                            OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[templateName][templateModelName] = tmp_dictPcCardTemplatePatch[templateName][templateModelName]
                        else:
                            if False:
                                # 此处等待后续实现特异化的补丁逻辑
                                pass
                            else:
                                OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[templateName][templateModelName] = tmp_dictPcCardTemplatePatch[templateName][templateModelName]
        except Exception as e:
            traceback.print_exc()
            dictTValue['tName'] = '全局'
            dictTValue['tInitDataName'] = dataName
            OlivaDiceCore.msgReply.globalLog(
                3,
                OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strInitTempDataError'], dictTValue),
                [
                    ('OlivaDice', 'default'),
                    ('Init', 'default')
                ]
            )

def dataPcCardTotalCount():
    total_count = 0
    for dictPcCardData_this in dictPcCardData:
        for dictPcCardData_hostkey_this in dictPcCardData[dictPcCardData_this]:
            total_count += 1
    return total_count

def dataPcCardSave(hostKey, pcHash):
    global dictPcCardData
    global dictPcCardSelection
    global dictPcCardTemplate
    global dictPcCardHiy
    dataDirRoot_this = OlivaDiceCore.data.dataDirRoot
    releaseDir(dataDirRoot_this)
    if hostKey in dictPcCardData:
        if pcHash in dictPcCardData[hostKey]:
            releaseDir(dataDirRoot_this + '/' + hostKey)
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard')
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/data')
            pcCardDataPath = dataDirRoot_this + '/' + hostKey + '/pcCard/data/' + pcHash
            with open(pcCardDataPath, 'w', encoding = 'utf-8') as pcCardDataPath_f:
                pcCardDataPath_f.write(json.dumps(dictPcCardData[hostKey][pcHash], ensure_ascii = False, indent = 4))
    if hostKey in dictPcCardSelection:
        if pcHash in dictPcCardSelection[hostKey]:
            releaseDir(dataDirRoot_this + '/' + hostKey)
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard')
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/selection')
            pcCardSelectionPath = dataDirRoot_this + '/' + hostKey + '/pcCard/selection/' + pcHash
            with open(pcCardSelectionPath, 'w', encoding = 'utf-8') as pcCardSelectionPath_f:
                pcCardSelectionPath_f.write(json.dumps(dictPcCardSelection[hostKey][pcHash], ensure_ascii = False, indent = 4))
    if hostKey in dictPcCardTemplate:
        if pcHash in dictPcCardTemplate[hostKey]:
            releaseDir(dataDirRoot_this + '/' + hostKey)
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard')
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/template')
            pcCardTemplatePath = dataDirRoot_this + '/' + hostKey + '/pcCard/template/' + pcHash
            with open(pcCardTemplatePath, 'w', encoding = 'utf-8') as dictPcCardTemplate_f:
                dictPcCardTemplate_f.write(json.dumps(dictPcCardTemplate[hostKey][pcHash], ensure_ascii = False, indent = 4))
    if hostKey in dictPcCardHiy:
        if pcHash in dictPcCardHiy[hostKey]:
            releaseDir(dataDirRoot_this + '/' + hostKey)
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard')
            releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/hiy')
            pcCardHiyPath = dataDirRoot_this + '/' + hostKey + '/pcCard/hiy/' + pcHash
            with open(pcCardHiyPath, 'w', encoding = 'utf-8') as pcCardHiyPath_f:
                pcCardHiyPath_f.write(json.dumps(dictPcCardHiy[hostKey][pcHash], ensure_ascii = False, indent = 4))

def dataPcCardLoad(hostKey, pcHash):
    global dictPcCardData
    global dictPcCardSelection
    global dictPcCardTemplate
    global dictPcCardHiy
    dataDirRoot_this = OlivaDiceCore.data.dataDirRoot
    releaseDir(dataDirRoot_this)
    releaseDir(dataDirRoot_this + '/' + hostKey)
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard')
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/data')
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/selection')
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/template')
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/hiy')
    pcCardDataPath = dataDirRoot_this + '/' + hostKey + '/pcCard/data/' + pcHash
    pcCardSelectionPath = dataDirRoot_this + '/' + hostKey + '/pcCard/selection/' + pcHash
    pcCardTemplatePath = dataDirRoot_this + '/' + hostKey + '/pcCard/template/' + pcHash
    pcCardHiyPath = dataDirRoot_this + '/' + hostKey + '/pcCard/hiy/' + pcHash
    if hostKey not in dictPcCardData:
        dictPcCardData[hostKey] = {}
    if pcHash not in dictPcCardData[hostKey]:
        dictPcCardData[hostKey][pcHash] = {}
    if hostKey not in dictPcCardSelection:
        dictPcCardSelection[hostKey] = {}
    if pcHash not in dictPcCardSelection[hostKey]:
        dictPcCardSelection[hostKey][pcHash] = {}
    if hostKey not in dictPcCardTemplate:
        dictPcCardTemplate[hostKey] = {}
    if pcHash not in dictPcCardTemplate[hostKey]:
        dictPcCardTemplate[hostKey][pcHash] = {}
    if hostKey not in dictPcCardHiy:
        dictPcCardHiy[hostKey] = {}
    if pcHash not in dictPcCardHiy[hostKey]:
        dictPcCardHiy[hostKey][pcHash] = {}
    if os.path.exists(pcCardDataPath):
        with open(pcCardDataPath, 'r', encoding = 'utf-8') as pcCardDataPath_f:
            dictPcCardData[hostKey][pcHash] = jsonDataLoadSafe(pcCardDataPath_f, "人物卡", f"{hostKey}/{pcHash}")
    if os.path.exists(pcCardSelectionPath):
        with open(pcCardSelectionPath, 'r', encoding = 'utf-8') as pcCardSelectionPath_f:
            dictPcCardSelection[hostKey][pcHash] = jsonDataLoadSafe(pcCardSelectionPath_f, "人物卡", f"{hostKey}/{pcHash}")
    if os.path.exists(pcCardTemplatePath):
        with open(pcCardTemplatePath, 'r', encoding = 'utf-8') as pcCardTemplatePath_f:
            dictPcCardTemplate[hostKey][pcHash] = jsonDataLoadSafe(pcCardTemplatePath_f, "人物卡", f"{hostKey}/{pcHash}")
    if os.path.exists(pcCardHiyPath):
        with open(pcCardHiyPath, 'r', encoding = 'utf-8') as pcCardHiyPath_f:
            dictPcCardHiy[hostKey][pcHash] = jsonDataLoadSafe(pcCardHiyPath_f, "人物卡", f"{hostKey}/{pcHash}")

def jsonDataLoadSafe(data_f, dataType, dataName):
    tmp_userConfigData = {}
    try:
        tmp_userConfigData = json.loads(data_f.read())
    except Exception as e:
        tmp_log_str =  OlivaDiceCore.msgCustomManager.formatReplySTRConst(
            OlivaDiceCore.msgCustom.dictStrConst['strInitDataError'],
            {
                "tInitDataType": dataType,
                "tInitDataName": dataName,
                "tResult": str(e)
            }
        )
        OlivaDiceCore.msgReply.globalLog(3, tmp_log_str, [
            ('OlivaDice', 'default'),
            ('Init', 'default')
        ])
        tmp_userConfigData = {}
    return tmp_userConfigData

def dataPcCardLoadAll():
    dataDirRoot_this = OlivaDiceCore.data.dataDirRoot
    releaseDir(dataDirRoot_this)
    pcCardDataHostList = os.listdir(dataDirRoot_this)
    for pcCardDataHostList_this in pcCardDataHostList:
        hostKey = pcCardDataHostList_this
        releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard')
        releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/data')
        pcCardDataPCHashList = os.listdir(dataDirRoot_this + '/' + hostKey + '/pcCard/data')
        for pcCardDataPCHashList_this in pcCardDataPCHashList:
            pcHash = pcCardDataPCHashList_this
            dataPcCardLoad(hostKey, pcHash)

def dataPcCardTemplateInit():
    for temp_this in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault:
        if 'synonyms' in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[temp_this]:
            tmp_res = {}
            for key_this in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[temp_this]['synonyms']:
                tmp_res_res = [key_this.upper()]
                for res_this in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[temp_this]['synonyms'][key_this]:
                    if res_this.upper() not in tmp_res_res:
                        tmp_res_res.append(res_this.upper())
                tmp_res[key_this.upper()] = tmp_res_res
            OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[temp_this]['synonyms'] = tmp_res
    dictPcCardTemplateDefault['unity'] = OlivaDiceCore.pcCardData.dictPcCardTemplateDefault.copy()

def pcCardRebase(pcHash, pcCardName, hagId = None):
    lockList_key = 'lockList'
    pcCardNameOld = None
    dict_pcCardNameOld = {}
    dict_pcCardTemplateOld = {}
    dict_pcCardHiyOld = {}
    if pcHash not in dictPcCardSelection['unity']:
        dictPcCardSelection['unity'][pcHash] = {}
    pcCardNameOld = pcCardDataGetSelectionKey(pcHash, hagId)
    # 获取全局selection的旧名字
    pcCardNameOldGlobal = pcCardDataGetSelectionKey(pcHash)
    # 如果全局selection和当前selection的旧名字相同，也更新全局selection
    if pcCardNameOldGlobal == pcCardNameOld:
        pcCardDataSetSelectionKey(pcHash, pcCardName, forceSwitch = True)
    # 更新lockList中所有匹配旧名字的条目
    if lockList_key in dictPcCardSelection['unity'][pcHash]:
        for hagId_this in dictPcCardSelection['unity'][pcHash][lockList_key]:
            if pcCardNameOld == dictPcCardSelection['unity'][pcHash][lockList_key][hagId_this]:
                dictPcCardSelection['unity'][pcHash][lockList_key][hagId_this] = pcCardName
    if pcCardNameOld != None:
        if pcHash in dictPcCardData['unity']:
            if pcCardNameOld in dictPcCardData['unity'][pcHash]:
                dict_pcCardNameOld = dictPcCardData['unity'][pcHash][pcCardNameOld].copy()
                dictPcCardData['unity'][pcHash].pop(pcCardNameOld)
        else:
            dictPcCardData['unity'][pcHash] = {}
    else:
        dictPcCardData['unity'][pcHash] = {}
    dictPcCardData['unity'][pcHash][pcCardName] = dict_pcCardNameOld
    if pcCardNameOld != None:
        if pcHash in dictPcCardTemplate['unity']:
            if pcCardNameOld in dictPcCardTemplate['unity'][pcHash]:
                dict_pcCardTemplateOld = dictPcCardTemplate['unity'][pcHash][pcCardNameOld].copy()
                dictPcCardTemplate['unity'][pcHash].pop(pcCardNameOld)
        else:
            dictPcCardTemplate['unity'][pcHash] = {}
    else:
        dictPcCardTemplate['unity'][pcHash] = {}
    dictPcCardTemplate['unity'][pcHash][pcCardName] = dict_pcCardTemplateOld
    # 处理hiy统计数据的重命名
    if pcCardNameOld != None:
        if pcHash in dictPcCardHiy['unity']:
            if pcCardNameOld in dictPcCardHiy['unity'][pcHash]:
                dict_pcCardHiyOld = dictPcCardHiy['unity'][pcHash][pcCardNameOld].copy()
                dictPcCardHiy['unity'][pcHash].pop(pcCardNameOld)
        else:
            dictPcCardHiy['unity'][pcHash] = {}
    else:
        dictPcCardHiy['unity'][pcHash] = {}
    dictPcCardHiy['unity'][pcHash][pcCardName] = dict_pcCardHiyOld
    dataPcCardSave('unity', pcHash)
    return True

def pcCardDataSkillNameMapper(pcHash, skillName, flagShow = False, hagId = None):
    pcCardName = pcCardDataGetSelectionKey(pcHash, hagId)
    pcCardSynonyms_hit = str(skillName)
    res = str(skillName)
    pcCardTemplateName = 'default'
    tmp_pcCardSynonyms = {}
    if pcCardName != None:
        pcCardTemplateName = pcCardDataGetTemplateDataByKey(pcHash, pcCardName, 'template', 'default')
    # 解析模板映射
    pcCardTemplateName = pcCardDataResolveTemplateMapping(pcCardTemplateName)
    if 'synonyms' in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[pcCardTemplateName]:
        tmp_pcCardSynonyms = OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[pcCardTemplateName]['synonyms']
    for tmp_pcCardSynonyms_this in tmp_pcCardSynonyms:
        if str(skillName) in tmp_pcCardSynonyms[tmp_pcCardSynonyms_this]:
            pcCardSynonyms_hit = tmp_pcCardSynonyms_this
    res = pcCardSynonyms_hit
    if flagShow:
        if 'showName' in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[pcCardTemplateName]:
            if type(OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[pcCardTemplateName]['showName']) == dict:
                if pcCardSynonyms_hit in OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[pcCardTemplateName]['showName']:
                    res = OlivaDiceCore.pcCardData.dictPcCardTemplateDefault[pcCardTemplateName]['showName'][pcCardSynonyms_hit]
    return res

def pcCardDataSetBySkillName(pcHash, skillName, skillValue, pcCardName = 'default', hitList = None, forceMapping = False, hagId = None):
    if skillName == '':
        return
    tmp_hitList = hitList
    if tmp_hitList == None:
        tmp_hitList = []
    tmp_pc_card_name_key = pcCardName
    # 先确保卡片数据存在
    if pcHash in dictPcCardData['unity']:
        pass
    else:
        dictPcCardData['unity'][pcHash] = {}
    if tmp_pc_card_name_key not in dictPcCardData['unity'][pcHash]:
        dictPcCardData['unity'][pcHash][tmp_pc_card_name_key] = {}
    # 然后再处理 selection 和 lock
    locked_pc = pcCardDataGetSelectionKeyLock(pcHash, hagId)
    if locked_pc is not None:
        # 如果有锁定的人物卡,只更新lockList中的人物卡,不修改全局selection
        if pcCardName != locked_pc:
            pcCardDataSetSelectionKeyLock(pcHash, tmp_pc_card_name_key, hagId)
    else:
        # 如果没有锁定的人物卡,按原逻辑修改全局selection
        pcCardDataSetSelectionKey(pcHash, tmp_pc_card_name_key, forceSwitch = True)
    tmp_pc_card_synonyms = {}
    tmp_pc_card_mapping = {}
    tmp_pc_card_forceMapping = []
    tmp_pc_card_template_name = pcCardDataGetTemplateDataByKey(pcHash, pcCardName, 'template', 'default')
    tmp_pc_card_template = pcCardDataGetTemplateByKey(tmp_pc_card_template_name)
    if 'synonyms' in tmp_pc_card_template:
        tmp_pc_card_synonyms = tmp_pc_card_template['synonyms']
    if 'mapping' in tmp_pc_card_template:
        tmp_pc_card_mapping = tmp_pc_card_template['mapping']
    if 'skillConfig' in tmp_pc_card_template \
    and 'forceMapping' in tmp_pc_card_template['skillConfig'] \
    and type(tmp_pc_card_template['skillConfig']['forceMapping']) is list:
        tmp_pc_card_forceMapping = tmp_pc_card_template['skillConfig']['forceMapping']
    tmp_pc_card_synonyms_hit = [str(skillName)]
    for tmp_pc_card_synonyms_this in tmp_pc_card_synonyms:
        if str(skillName) in tmp_pc_card_synonyms[tmp_pc_card_synonyms_this]:
            tmp_pc_card_synonyms_hit = tmp_pc_card_synonyms[tmp_pc_card_synonyms_this]
    for tmp_pc_card_synonyms_hit_this in tmp_pc_card_synonyms_hit:
        if tmp_pc_card_synonyms_hit_this not in tmp_hitList:
            dictPcCardData['unity'][pcHash][tmp_pc_card_name_key][tmp_pc_card_synonyms_hit_this] = skillValue
            tmp_hitList.append(tmp_pc_card_synonyms_hit_this)
    for tmp_pc_card_mapping_hit_this in tmp_pc_card_mapping:
        if tmp_pc_card_mapping_hit_this not in tmp_hitList:
            tmp_forceMapping = False
            if tmp_pc_card_mapping_hit_this in tmp_pc_card_forceMapping:
                tmp_forceMapping = True
            if tmp_forceMapping or forceMapping or tmp_pc_card_mapping_hit_this not in dictPcCardData['unity'][pcHash][tmp_pc_card_name_key]:
                if type(tmp_pc_card_mapping[tmp_pc_card_mapping_hit_this]) == str:
                    tmp_template_customDefault = None
                    tmp_template_name = pcCardDataGetTemplateKey(pcHash, pcCardName)
                    if tmp_template_name != None:
                        tmp_template = pcCardDataGetTemplateByKey(tmp_template_name)
                        if 'customDefault' in tmp_template:
                            tmp_template_customDefault = tmp_template['customDefault']
                    tmp_skill_rd = OlivaDiceCore.onedice.RD(
                        tmp_pc_card_mapping[tmp_pc_card_mapping_hit_this],
                        tmp_template_customDefault,
                        valueTable = dictPcCardData['unity'][pcHash][tmp_pc_card_name_key]
                    )
                    tmp_skill_rd.roll()
                    if tmp_skill_rd.resError == None:
                        pcCardDataSetBySkillName(
                            pcHash,
                            tmp_pc_card_mapping_hit_this,
                            tmp_skill_rd.resInt,
                            tmp_pc_card_name_key,
                            hitList = tmp_hitList,
                            forceMapping = forceMapping,
                            hagId = hagId
                        )
    if hitList == None:
        dataPcCardSave('unity', pcHash)

def pcCardDataDelBySkillName(pcHash, skillName, pcCardName = 'default'):
    tmp_pc_card_name_key = pcCardName
    if pcHash in dictPcCardData['unity']:
        pass
    else:
        dictPcCardData['unity'][pcHash] = {}
    if tmp_pc_card_name_key not in dictPcCardData['unity'][pcHash]:
        dictPcCardData['unity'][pcHash][tmp_pc_card_name_key] = {}
    tmp_pc_card_synonyms = {}
    tmp_pc_card_synonyms_name = pcCardDataGetTemplateDataByKey(pcHash, pcCardName, 'template', 'default')
    tmp_pc_card_template = pcCardDataGetTemplateByKey(tmp_pc_card_synonyms_name)
    if 'synonyms' in tmp_pc_card_template:
        tmp_pc_card_synonyms = tmp_pc_card_template['synonyms']
    tmp_pc_card_synonyms_hit = [str(skillName)]
    for tmp_pc_card_synonyms_this in tmp_pc_card_synonyms:
        if str(skillName) in tmp_pc_card_synonyms[tmp_pc_card_synonyms_this]:
            tmp_pc_card_synonyms_hit = tmp_pc_card_synonyms[tmp_pc_card_synonyms_this]
    for tmp_pc_card_synonyms_hit_this in tmp_pc_card_synonyms_hit:
        if tmp_pc_card_synonyms_hit_this in dictPcCardData['unity'][pcHash][tmp_pc_card_name_key]:
            dictPcCardData['unity'][pcHash][tmp_pc_card_name_key].pop(tmp_pc_card_synonyms_hit_this)
    dataPcCardSave('unity', pcHash)

# 获取用户当前人物卡某技能
def pcCardDataGetBySkillName(pcHash, skillName, hagId = None):
    tmp_skill_value = 0
    skillName_src = pcCardDataSkillNameMapper(pcHash, skillName, flagShow = False, hagId = hagId)
    tmp_pc_card_name_key = 'default'
    tmp_pc_card_name_key_1 = pcCardDataGetSelectionKey(pcHash, hagId)
    if tmp_pc_card_name_key_1 != None:
        tmp_pc_card_name_key = tmp_pc_card_name_key_1
    else:
        return tmp_skill_value
    tmp_template_name = pcCardDataGetTemplateKey(pcHash, tmp_pc_card_name_key)
    tmp_template_defaultSkillValue = None
    if tmp_template_name == None:
        tmp_template_name = 'default'
    if tmp_template_name != None:
        tmp_template = pcCardDataGetTemplateByKey(tmp_template_name)
        if tmp_template != None:
            if 'defaultSkillValue' in tmp_template:
                tmp_template_defaultSkillValue = tmp_template['defaultSkillValue']
    if type(tmp_template_defaultSkillValue) == dict:
        if skillName_src in tmp_template_defaultSkillValue and type(tmp_template_defaultSkillValue[skillName_src]) == int:
            tmp_skill_value = tmp_template_defaultSkillValue[skillName_src]
    if pcHash not in dictPcCardData['unity']:
        return tmp_skill_value
    if tmp_pc_card_name_key not in dictPcCardData['unity'][pcHash]:
        return tmp_skill_value
    if str(skillName) in dictPcCardData['unity'][pcHash][tmp_pc_card_name_key]:
        tmp_skill_value = dictPcCardData['unity'][pcHash][tmp_pc_card_name_key][str(skillName)]
    else:
        pcCardDataSetBySkillName(
            pcHash = pcHash,
            skillName = skillName_src,
            skillValue = tmp_skill_value,
            pcCardName = tmp_pc_card_name_key,
            hagId = hagId
        )
    return tmp_skill_value

def pcCardDataGetSelectionKey(pcHash, hagId = None):
    selection_key = 'selection'
    lockList_key = 'lockList'
    tmp_pc_card_name_key = None
    if pcHash not in dictPcCardSelection['unity']:
        return tmp_pc_card_name_key
    if selection_key not in dictPcCardSelection['unity'][pcHash]:
        return tmp_pc_card_name_key
    else:
        tmp_pc_card_name_key = dictPcCardSelection['unity'][pcHash][selection_key]
    if lockList_key in dictPcCardSelection['unity'][pcHash]:
        if hagId != None:
            if hagId in dictPcCardSelection['unity'][pcHash][lockList_key]:
                tmp_pc_card_name_key = dictPcCardSelection['unity'][pcHash][lockList_key][hagId]
    return tmp_pc_card_name_key

def pcCardDataSetSelectionKey(pcHash, pcCardName, forceSwitch = False):
    selection_key = 'selection'
    tmp_pc_card_name_key = pcCardName
    tmp_card_dict = {}
    if pcHash in dictPcCardData['unity']:
        tmp_card_dict = dictPcCardData['unity'][pcHash]
    if forceSwitch or tmp_pc_card_name_key in tmp_card_dict:
        if pcHash not in dictPcCardSelection['unity']:
            dictPcCardSelection['unity'][pcHash] = {}
        dictPcCardSelection['unity'][pcHash][selection_key] = tmp_pc_card_name_key
        dataPcCardSave('unity', pcHash)
        return True
    else:
        return False

def pcCardDataDelSelectionKey(pcHash, pcCardName, skipDel = False):
    global dictPcCardHiy
    selection_key = 'selection'
    lockList_key = 'lockList'
    tmp_pc_card_name_key = pcCardName
    tmp_card_dict = {}
    tmp_card_dict_2 = {}
    tmp_card_dict_3 = {}
    if pcHash in dictPcCardData['unity']:
        tmp_card_dict = dictPcCardData['unity'][pcHash]
    else:
        dictPcCardData['unity'][pcHash] = {}
    if pcHash in dictPcCardTemplate['unity']:
        tmp_card_dict_2 = dictPcCardTemplate['unity'][pcHash]
    else:
        dictPcCardTemplate['unity'][pcHash] = {}
    if pcHash in dictPcCardHiy['unity']:
        tmp_card_dict_3 = dictPcCardHiy['unity'][pcHash]
    else:
        dictPcCardHiy['unity'][pcHash] = {}
    if tmp_pc_card_name_key in tmp_card_dict:
        dictPcCardData['unity'][pcHash].pop(tmp_pc_card_name_key)
        if tmp_pc_card_name_key in tmp_card_dict_2:
            dictPcCardTemplate['unity'][pcHash].pop(tmp_pc_card_name_key)
        if tmp_pc_card_name_key in tmp_card_dict_3:
            dictPcCardHiy['unity'][pcHash].pop(tmp_pc_card_name_key)
        if pcHash not in dictPcCardSelection['unity']:
            dictPcCardSelection['unity'][pcHash] = {}
            return False
        if not skipDel:
            if selection_key in dictPcCardSelection['unity'][pcHash]:
                if tmp_pc_card_name_key == dictPcCardSelection['unity'][pcHash][selection_key]:
                    dictPcCardSelection['unity'][pcHash].pop(selection_key)
                    if len(dictPcCardData['unity'][pcHash].keys()) > 0:
                        tmp_card_dict_keys = list(dictPcCardData['unity'][pcHash].keys())
                        dictPcCardSelection['unity'][pcHash][selection_key] = tmp_card_dict_keys[0]
        if not skipDel:
            # 处理lockList: 如果被删除的卡被某个群锁定,则切换到其他卡但保持锁定状态
            if lockList_key in dictPcCardSelection['unity'][pcHash]:
                lockList_updates = {}
                lockList_deletes = []
                for hagId_this in dictPcCardSelection['unity'][pcHash][lockList_key]:
                    if pcCardName == dictPcCardSelection['unity'][pcHash][lockList_key][hagId_this]:
                        # 该群锁定的是被删除的卡,需要切换到其他卡
                        if len(dictPcCardData['unity'][pcHash].keys()) > 0:
                            # 还有其他人物卡,切换到第一个并保持锁定
                            tmp_card_dict_keys = list(dictPcCardData['unity'][pcHash].keys())
                            lockList_updates[hagId_this] = tmp_card_dict_keys[0]
                        else:
                            # 没有其他人物卡了,删除该群的锁定
                            lockList_deletes.append(hagId_this)
                # 应用更新
                for hagId_this, new_card in lockList_updates.items():
                    dictPcCardSelection['unity'][pcHash][lockList_key][hagId_this] = new_card
                # 应用删除
                for hagId_this in lockList_deletes:
                    dictPcCardSelection['unity'][pcHash][lockList_key].pop(hagId_this)
        dataPcCardSave('unity', pcHash)
        return True
    else:
        return False

def pcCardDataSetSelectionKeyLock(pcHash, pcCardName, hagID):
    lockList_key = 'lockList'
    tmp_pc_card_name_key = pcCardName
    tmp_card_dict = {}
    if pcHash in dictPcCardData['unity']:
        tmp_card_dict = dictPcCardData['unity'][pcHash]
    if tmp_pc_card_name_key in tmp_card_dict:
        if pcHash not in dictPcCardSelection['unity']:
            dictPcCardSelection['unity'][pcHash] = {}
        if lockList_key not in dictPcCardSelection['unity'][pcHash]:
            dictPcCardSelection['unity'][pcHash][lockList_key] = {}
        dictPcCardSelection['unity'][pcHash][lockList_key][hagID] = tmp_pc_card_name_key
        dataPcCardSave('unity', pcHash)
        return True
    else:
        return False

def pcCardDataGetSelectionKeyLock(pcHash, hagID):
    lockList_key = 'lockList'
    tmp_pc_card_name_key = None
    if pcHash in dictPcCardSelection['unity']:
        if lockList_key in dictPcCardSelection['unity'][pcHash]:
            if hagID in dictPcCardSelection['unity'][pcHash][lockList_key]:
                tmp_pc_card_name_key = dictPcCardSelection['unity'][pcHash][lockList_key][hagID]
    return tmp_pc_card_name_key

def pcCardDataDelSelectionKeyLock(pcHash, hagID):
    lockList_key = 'lockList'
    if pcHash in dictPcCardSelection['unity']:
        if lockList_key in dictPcCardSelection['unity'][pcHash]:
            if hagID in dictPcCardSelection['unity'][pcHash][lockList_key]:
                dictPcCardSelection['unity'][pcHash][lockList_key].pop(hagID)
                dataPcCardSave('unity', pcHash)

def pcCardDataResolveTemplateMapping(templateName):
    """
    解析模板映射，处理 tempMapping 字段的重定向
    """
    global dictPcCardTemplateDefault
    if templateName not in dictPcCardTemplateDefault['unity']:
        return None
    tmp_template = dictPcCardTemplateDefault['unity'][templateName]
    # 如果没有 tempMapping 字段，直接返回原名称
    if not tmp_template or 'tempMapping' not in tmp_template:
        return templateName
    # 有 tempMapping 字段，进行重定向解析
    redirect_count = 0
    max_redirects = 100
    visited_templates = set()
    current_name = templateName
    while tmp_template and 'tempMapping' in tmp_template:
        redirect_count += 1
        # 检查是否超过最大重定向次数
        if redirect_count > max_redirects:
            return None
        mapping_target = tmp_template['tempMapping']
        # 检测循环引用
        if mapping_target in visited_templates:
            return None
        # 记录已访问的模板
        visited_templates.add(current_name)
        # 检查目标模板是否存在
        if mapping_target not in dictPcCardTemplateDefault['unity']:
            return None
        # 切换到目标模板
        current_name = mapping_target
        tmp_template = dictPcCardTemplateDefault['unity'][mapping_target]
    return current_name

def pcCardDataGetTemplateByKey(templateName):
    global dictPcCardTemplateDefault
    resolved_name = pcCardDataResolveTemplateMapping(templateName)
    if resolved_name in dictPcCardTemplateDefault['unity']:
        return dictPcCardTemplateDefault['unity'][resolved_name]
    else:
        return None

def pcCardDataGetTemplateKey(pcHash, pcCardName):
    global dictPcCardTemplate
    selection_key = 'template'
    tmp_pc_template_name_key = None
    if pcHash not in dictPcCardTemplate['unity']:
        return tmp_pc_template_name_key
    if pcCardName not in dictPcCardTemplate['unity'][pcHash]:
        return tmp_pc_template_name_key
    if selection_key not in dictPcCardTemplate['unity'][pcHash][pcCardName]:
        return tmp_pc_template_name_key
    else:
        tmp_pc_template_name_key = dictPcCardTemplate['unity'][pcHash][pcCardName][selection_key]
    templateName_resolved = pcCardDataResolveTemplateMapping(tmp_pc_template_name_key)
    return templateName_resolved

def pcCardDataGetTemplateRuleKey(pcHash, pcCardName):
    global dictPcCardTemplate
    selection_key = 'checkRules'
    tmp_pc_template_name_key = None
    if pcHash not in dictPcCardTemplate['unity']:
        return tmp_pc_template_name_key
    if pcCardName not in dictPcCardTemplate['unity'][pcHash]:
        return tmp_pc_template_name_key
    if selection_key not in dictPcCardTemplate['unity'][pcHash][pcCardName]:
        return tmp_pc_template_name_key
    else:
        tmp_pc_template_name_key = dictPcCardTemplate['unity'][pcHash][pcCardName][selection_key]
    return tmp_pc_template_name_key

def pcCardDataSetTemplateKey(pcHash, pcCardName, templateName = 'default', ruleName = 'default'):
    selection_key = 'template'
    selection_key_2 = 'checkRules'
    tmp_pc_card_name_key = pcCardName
    templateName_core = None
    ruleName_core = None
    # 先解析模板映射
    templateName_resolved = pcCardDataResolveTemplateMapping(templateName)
    templateName_core = getKeyWithUpper(
        data = dictPcCardTemplateDefault['unity'],
        key = templateName_resolved
    )
    if templateName_core == None:
        return False
    if selection_key_2 not in dictPcCardTemplateDefault['unity'][templateName_core]:
        return False
    ruleName_core = getKeyWithUpper(
        data = dictPcCardTemplateDefault['unity'][templateName_core][selection_key_2],
        key = ruleName
    )
    if ruleName_core == None:
        return False
    tmp_card_dict = {}
    if pcHash in dictPcCardData['unity']:
        tmp_card_dict = dictPcCardData['unity'][pcHash]
    if tmp_pc_card_name_key in tmp_card_dict:
        if pcHash not in dictPcCardTemplate['unity']:
            dictPcCardTemplate['unity'][pcHash] = {}
        if tmp_pc_card_name_key not in dictPcCardTemplate['unity'][pcHash]:
            dictPcCardTemplate['unity'][pcHash][tmp_pc_card_name_key] = {}
        dictPcCardTemplate['unity'][pcHash][tmp_pc_card_name_key][selection_key] = templateName_core
        dictPcCardTemplate['unity'][pcHash][tmp_pc_card_name_key][selection_key_2] = ruleName_core
        dataPcCardSave('unity', pcHash)
        return True
    else:
        return False

def pcCardDataCheckTemplateKey(templateName = 'default', ruleName = 'default', resMode = 'flag'):
    res = None
    if resMode == 'flag':
        res = False
    elif resMode == 'temp':
        res = None
    elif resMode == 'rule':
        res = None
    selection_key = 'template'
    selection_key_2 = 'checkRules'
    # 先解析模板映射
    templateName_resolved = pcCardDataResolveTemplateMapping(templateName)
    templateName_core = getKeyWithUpper(
        data = dictPcCardTemplateDefault['unity'],
        key = templateName_resolved
    )
    if templateName_core == None:
        return res
    if templateName_core not in dictPcCardTemplateDefault['unity']:
        return res
    if selection_key_2 not in dictPcCardTemplateDefault['unity'][templateName_core]:
        return res
    ruleName_core = getKeyWithUpper(
        data = dictPcCardTemplateDefault['unity'][templateName_core][selection_key_2],
        key = ruleName
    )
    if ruleName_core == None:
        return res
    res = True
    if resMode == 'flag':
        res = True
    elif resMode == 'temp':
        res = templateName_core
    elif resMode == 'rule':
        res = ruleName_core
    return res

def setPcTemplateByGroupRule(plugin_event, tmp_pc_id = None, tmp_pc_name = None, set_flag = True):
    """
    根据传入参数设置人物卡模板
    """
    if not set_flag:
        return
    
    # 获取当前群规的模板
    group_template, group_rule = getGroupTemplateRule(plugin_event)
    if not group_template:
        return
    
    # 获取当前用户和群组信息
    if not tmp_pc_id:
        tmp_pc_id = plugin_event.data.user_id
    tmp_pc_platform = plugin_event.platform['platform']
    tmp_hagID = getHagIDFromMsg(plugin_event, OlivaDiceCore.data.global_Proc)
    
    # 获取人物卡哈希和当前选择的人物卡名
    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
    if not tmp_pc_name:
        tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
    
    if tmp_pc_name:
        # 设置人物卡模板
        OlivaDiceCore.pcCard.pcCardDataSetTemplateKey(
            tmp_pcHash,
            tmp_pc_name,
            group_template,
            group_rule
        )
        
def isNewPcCard(plugin_event, tmp_pc_id = None, external_flag = None):
    """
    判断人物卡是否为新卡
    """
    # 如果外部传入了标志，直接返回外部值
    if external_flag is not None:
        return external_flag
    
    # 获取当前用户和群组信息
    if not tmp_pc_id:
        tmp_pc_id = plugin_event.data.user_id
    tmp_pc_platform = plugin_event.platform['platform']
    tmp_hagID = getHagIDFromMsg(plugin_event, OlivaDiceCore.data.global_Proc)
    
    # 获取人物卡哈希和当前选择的人物卡数据
    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(tmp_pc_id, tmp_pc_platform)
    pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
    
    # 过滤掉系统字段，检查是否为空
    valid_skills = {k: v for k, v in pc_skills.items() 
                   if not k.startswith('__') and k != 'template'}
    
    # 如果没有任何有效技能，则为新卡
    return len(valid_skills) == 0

def getGroupTemplateRule(plugin_event):
    """
    获取当前群聊的房规模板
    """
    tmp_hagID = getHagIDFromMsg(plugin_event, OlivaDiceCore.data.global_Proc)
    tmp_user_platform = plugin_event.platform['platform']
    
    if not tmp_hagID:
        return (None, None)
    
    # 获取群模板和规则
    group_template = OlivaDiceCore.userConfig.getUserConfigByKey(
        userConfigKey='groupTemplate',
        botHash=plugin_event.bot_info.hash,
        userId=tmp_hagID,
        userType='group',
        platform=tmp_user_platform,
    )
    
    group_rule = OlivaDiceCore.userConfig.getUserConfigByKey(
        userConfigKey='groupTemplateRule',
        botHash=plugin_event.bot_info.hash,
        userId=tmp_hagID,
        userType='group',
        platform=tmp_user_platform
    )
    
    return (group_template, group_rule)

def getHagIDFromMsg(plugin_event, Proc):
    """
    从消息中获取群组/频道ID
    """
    tmp_hagID = None
    flag_is_from_host = False
    flag_is_from_group = False
    
    if plugin_event.plugin_info['func_type'] == 'group_message':
        if plugin_event.data.host_id is not None:
            flag_is_from_host = True
        flag_is_from_group = True
    elif plugin_event.plugin_info['func_type'] == 'private_message':
        flag_is_from_group = False
    
    if flag_is_from_host and flag_is_from_group:
        tmp_hagID = f"{plugin_event.data.host_id}|{plugin_event.data.group_id}"
    elif flag_is_from_group:
        tmp_hagID = str(plugin_event.data.group_id)
    
    return tmp_hagID

def pcCardDataSetHiyKey(pcHash, pcCardName, hiyKey, value):
    '''
    设置人物卡骰点统计数据
    '''
    global dictPcCardHiy
    global dictPcCardData
    hostKey = 'unity'
    # 检查人物卡是否存在,只有存在时才记录hiy统计数据
    if hostKey not in dictPcCardData:
        return
    if pcHash not in dictPcCardData[hostKey]:
        return
    if pcCardName not in dictPcCardData[hostKey][pcHash]:
        return
    if hostKey not in dictPcCardHiy:
        dictPcCardHiy[hostKey] = {}
    if pcHash not in dictPcCardHiy[hostKey]:
        dictPcCardHiy[hostKey][pcHash] = {}
    if pcCardName not in dictPcCardHiy[hostKey][pcHash]:
        dictPcCardHiy[hostKey][pcHash][pcCardName] = {}
    if hiyKey not in dictPcCardHiy[hostKey][pcHash][pcCardName]:
        dictPcCardHiy[hostKey][pcHash][pcCardName][hiyKey] = 0
    
    dictPcCardHiy[hostKey][pcHash][pcCardName][hiyKey] += value
    dataPcCardSave(hostKey, pcHash)

def pcCardDataGetHiyKey(pcHash, pcCardName, hiyKey):
    '''
    获取人物卡骰点统计数据
    '''
    global dictPcCardHiy
    hostKey = 'unity'
    
    if hostKey not in dictPcCardHiy:
        return 0
    if pcHash not in dictPcCardHiy[hostKey]:
        return 0
    if pcCardName not in dictPcCardHiy[hostKey][pcHash]:
        return 0
    if hiyKey not in dictPcCardHiy[hostKey][pcHash][pcCardName]:
        return 0
    
    return dictPcCardHiy[hostKey][pcHash][pcCardName][hiyKey]

def pcCardDataGetAllHiyKeys(pcHash, pcCardName):
    '''
    获取人物卡所有骰点统计数据
    '''
    global dictPcCardHiy
    hostKey = 'unity'
    
    if hostKey not in dictPcCardHiy:
        return {}
    if pcHash not in dictPcCardHiy[hostKey]:
        return {}
    if pcCardName not in dictPcCardHiy[hostKey][pcHash]:
        return {}
    
    return dictPcCardHiy[hostKey][pcHash][pcCardName].copy()



#更通用的接口

def pcCardDataGetTemplateDataByKey(pcHash, pcCardName, dataKey, resDefault = None):
    global dictPcCardTemplate
    selection_key = dataKey
    tmp_pc_template_name_key = resDefault
    if pcHash not in dictPcCardTemplate['unity']:
        return tmp_pc_template_name_key
    if pcCardName not in dictPcCardTemplate['unity'][pcHash]:
        return tmp_pc_template_name_key
    if selection_key not in dictPcCardTemplate['unity'][pcHash][pcCardName]:
        return tmp_pc_template_name_key
    else:
        tmp_pc_template_name_key = dictPcCardTemplate['unity'][pcHash][pcCardName][selection_key]
    return tmp_pc_template_name_key

def pcCardDataSetTemplateDataByKey(pcHash, pcCardName, dataKey, dataContent):
    selection_key = dataKey
    tmp_pc_card_name_key = pcCardName
    tmp_card_dict = {}
    if pcHash in dictPcCardData['unity']:
        tmp_card_dict = dictPcCardData['unity'][pcHash]
    if tmp_pc_card_name_key in tmp_card_dict:
        if pcHash not in dictPcCardTemplate['unity']:
            dictPcCardTemplate['unity'][pcHash] = {}
        if tmp_pc_card_name_key not in dictPcCardTemplate['unity'][pcHash]:
            dictPcCardTemplate['unity'][pcHash][tmp_pc_card_name_key] = {}
        dictPcCardTemplate['unity'][pcHash][tmp_pc_card_name_key][selection_key] = dataContent
        dataPcCardSave('unity', pcHash)
        return True
    else:
        return False


def pcCardDataGetUserAll(pcHash):
    tmp_card_dict = {}
    if pcHash in dictPcCardData['unity']:
        tmp_card_dict = dictPcCardData['unity'][pcHash]
    return tmp_card_dict

# 获取某用户当前人物卡技能表
def pcCardDataGetByPcName(pcHash, hagId = None):
    tmp_skill_list = {}
    tmp_pc_card_name_key = 'default'
    tmp_pc_card_name_key_1 = pcCardDataGetSelectionKey(pcHash, hagId)
    if tmp_pc_card_name_key_1 != None:
        tmp_pc_card_name_key = tmp_pc_card_name_key_1
    else:
        return tmp_skill_list
    if pcHash in dictPcCardData['unity']:
        if tmp_pc_card_name_key in dictPcCardData['unity'][pcHash]:
            tmp_skill_list = dictPcCardData['unity'][pcHash][tmp_pc_card_name_key]
    tmp_template_name = pcCardDataGetTemplateKey(pcHash, tmp_pc_card_name_key)
    tmp_template_defaultSkillValue = None
    if tmp_template_name == None:
        tmp_template_name = 'default'
    if tmp_template_name != None:
        tmp_template = pcCardDataGetTemplateByKey(tmp_template_name)
        if tmp_template != None:
            if 'defaultSkillValue' in tmp_template:
                tmp_template_defaultSkillValue = tmp_template['defaultSkillValue']
    if type(tmp_template_defaultSkillValue) == dict:
        for skillName_src in tmp_template_defaultSkillValue:
            if type(tmp_template_defaultSkillValue[skillName_src]) == int:
                if skillName_src not in tmp_skill_list:
                    tmp_skill_value = tmp_template_defaultSkillValue[skillName_src]
                    pcCardDataSetBySkillName(
                        pcHash = pcHash,
                        skillName = skillName_src,
                        skillValue = tmp_skill_value,
                        pcCardName = tmp_pc_card_name_key,
                        hagId = hagId
                    )
    return tmp_skill_list

def fixName(data:str, flagMode = 'default'):
    res = data
    list_origin = [
        '!', '@', '#', '$', '%', '^', '&', '*',
        '(', ')', '{', '}', '[', ']', '-', '=',
        '+', '/', '\\', '*', ':', ';', '\'', '\"',
        ',', '.', '?', '~', '`', '|', ' ',
        '\r\n', '\r', '\n'
    ]
    for list_origin_this in list_origin:
        res = res.replace(list_origin_this, '_')
    return res

def checkPcName(data):
    res = True
    if len(data) > 50:
        res = False
    if '\n' in data:
        res = False
    return res

def getPcHash(pcId, platform):
    hash_tmp = hashlib.new('md5')
    hash_tmp.update(str(pcId).encode(encoding='UTF-8'))
    hash_tmp.update(str(platform).encode(encoding='UTF-8'))
    return hash_tmp.hexdigest()

def getKeyWithUpper(data, key):
    res = None
    if key is None:
        return res
    for key_this in data:
        if key.upper() == key_this.upper():
            res = key_this
            break
    return res

# 外部调用接口

def getPcSkillAPI(pcHash, skillName, hagId, defaultName = '人物卡'):
    res = None
    if getPcNameAPI(pcHash, hagId, defaultName) != None:
        res = pcCardDataGetBySkillName(pcHash, skillName, hagId)
    return res

def setPcSkillAPI(pcHash, skillName, skillValue, hagId, defaultName = '人物卡'):
    res = False
    tmp_pcCardNameKey = getPcNameAPI(pcHash, hagId, defaultName)
    if tmp_pcCardNameKey != None:
        res = pcCardDataSetBySkillName(
            pcHash = pcHash,
            skillName = skillName,
            skillValue = skillValue,
            pcCardName = tmp_pcCardNameKey,
            hitList = None,
            forceMapping = False,
            hagId = hagId
        )
    return res

## 保证至少有一个目标人物卡
def getPcNameAPI(pcHash, hagId, defaultName = '人物卡'):
    res = None
    tmp_pcCardNameKey = pcCardDataGetSelectionKey(pcHash, hagId)
    if tmp_pcCardNameKey == None:
        tmp_pcCardNameKey = defaultName
        tmp_pcCardNameKey = OlivaDiceCore.pcCard.fixName(tmp_pcCardNameKey)
        if not OlivaDiceCore.pcCard.checkPcName(tmp_pcCardNameKey):
            tmp_pcCardNameKey = '人物卡'
        if not OlivaDiceCore.pcCard.pcCardRebase(
            pcHash,
            tmp_pcCardNameKey,
            hagId
        ):
            return res
    res = tmp_pcCardNameKey
    return res

## 保证指定的目标人物卡一定存在
def getPcNameForceAPI(pcHash, hagId, pcName = '人物卡'):
    res = None
    tmp_pcCardNameKey = pcCardDataGetSelectionKey(pcHash, hagId)
    if tmp_pcCardNameKey != pcName:
        tmp_pcCardNameKey = pcName
        tmp_pcCardNameKey = OlivaDiceCore.pcCard.fixName(tmp_pcCardNameKey)
        if not OlivaDiceCore.pcCard.checkPcName(tmp_pcCardNameKey):
            tmp_pcCardNameKey = '人物卡'
        OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
            pcHash,
            '__new',
            0,
            tmp_pcCardNameKey,
            hagId = hagId
        )
        OlivaDiceCore.pcCard.pcCardDataDelBySkillName(
            pcHash,
            '__new',
            tmp_pcCardNameKey
        )
    res = tmp_pcCardNameKey
    return res

def setPcSwitchAPI(pcHash, hagId, switchName = '人物卡'):
    res = False
    if getPcNameForceAPI(pcHash, hagId, switchName) != None:
        # 检查是否有锁定的人物卡
        if OlivaDiceCore.pcCard.pcCardDataGetSelectionKeyLock(
            pcHash,
            hagId
        ) == None:
            # 没有锁定,修改全局selection
            res = OlivaDiceCore.pcCard.pcCardDataSetSelectionKey(
                pcHash,
                switchName
            )
        else:
            # 有锁定,只修改lockList中的人物卡
            res = OlivaDiceCore.pcCard.pcCardDataSetSelectionKeyLock(
                pcHash,
                switchName,
                hagId
            )
        res = True
    return res

def setPcLockAPI(pcHash, hagId, setFlag:bool, pcName = '人物卡'):
    res = False
    tmp_pcName = getPcNameAPI(pcHash, hagId, pcName)
    if tmp_pcName != None:
        if OlivaDiceCore.pcCard.pcCardDataGetSelectionKeyLock(
            pcHash,
            hagId
        ) == None:
            if setFlag == True:
                OlivaDiceCore.pcCard.pcCardDataSetSelectionKeyLock(
                    pcHash,
                    tmp_pcName,
                    hagId
                )
        else:
            if setFlag == False:
                OlivaDiceCore.pcCard.pcCardDataDelSelectionKeyLock(
                    pcHash,
                    hagId
                )
        res = True
    return res