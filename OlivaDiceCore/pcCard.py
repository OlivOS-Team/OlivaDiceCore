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

def dataPcCardLoad(hostKey, pcHash):
    global dictPcCardData
    global dictPcCardSelection
    global dictPcCardTemplate
    dataDirRoot_this = OlivaDiceCore.data.dataDirRoot
    releaseDir(dataDirRoot_this)
    releaseDir(dataDirRoot_this + '/' + hostKey)
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard')
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/data')
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/selection')
    releaseDir(dataDirRoot_this + '/' + hostKey + '/pcCard/template')
    pcCardDataPath = dataDirRoot_this + '/' + hostKey + '/pcCard/data/' + pcHash
    pcCardSelectionPath = dataDirRoot_this + '/' + hostKey + '/pcCard/selection/' + pcHash
    pcCardTemplatePath = dataDirRoot_this + '/' + hostKey + '/pcCard/template/' + pcHash
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
    if os.path.exists(pcCardDataPath):
        with open(pcCardDataPath, 'r', encoding = 'utf-8') as pcCardDataPath_f:
            dictPcCardData[hostKey][pcHash] = jsonDataLoadSafe(pcCardDataPath_f, "人物卡", f"{hostKey}/{pcHash}")
    if os.path.exists(pcCardSelectionPath):
        with open(pcCardSelectionPath, 'r', encoding = 'utf-8') as pcCardSelectionPath_f:
            dictPcCardSelection[hostKey][pcHash] = jsonDataLoadSafe(pcCardSelectionPath_f, "人物卡", f"{hostKey}/{pcHash}")
    if os.path.exists(pcCardTemplatePath):
        with open(pcCardTemplatePath, 'r', encoding = 'utf-8') as pcCardTemplatePath_f:
            dictPcCardTemplate[hostKey][pcHash] = jsonDataLoadSafe(pcCardTemplatePath_f, "人物卡", f"{hostKey}/{pcHash}")

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
    if pcHash not in dictPcCardSelection['unity']:
        dictPcCardSelection['unity'][pcHash] = {}
    pcCardNameOld = pcCardDataGetSelectionKey(pcHash, hagId)
    if None == pcCardDataGetSelectionKeyLock(pcHash, hagId):
        pcCardDataSetSelectionKey(pcHash, pcCardName, forceSwitch = True)
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
    if pcCardName != pcCardDataGetSelectionKeyLock(pcHash, hagId):
        pcCardDataSetSelectionKey(pcHash, tmp_pc_card_name_key, forceSwitch = True)
    if pcHash in dictPcCardData['unity']:
        pass
    else:
        dictPcCardData['unity'][pcHash] = {}
    if tmp_pc_card_name_key not in dictPcCardData['unity'][pcHash]:
        dictPcCardData['unity'][pcHash][tmp_pc_card_name_key] = {}
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
    selection_key = 'selection'
    lockList_key = 'lockList'
    tmp_pc_card_name_key = pcCardName
    tmp_card_dict = {}
    tmp_card_dict_2 = {}
    if pcHash in dictPcCardData['unity']:
        tmp_card_dict = dictPcCardData['unity'][pcHash]
    else:
        dictPcCardData['unity'][pcHash] = {}
    if pcHash in dictPcCardTemplate['unity']:
        tmp_card_dict_2 = dictPcCardTemplate['unity'][pcHash]
    else:
        dictPcCardTemplate['unity'][pcHash] = {}
    if tmp_pc_card_name_key in tmp_card_dict:
        dictPcCardData['unity'][pcHash].pop(tmp_pc_card_name_key)
        if tmp_pc_card_name_key in tmp_card_dict_2:
            dictPcCardTemplate['unity'][pcHash].pop(tmp_pc_card_name_key)
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
            lockList_dict_new = {}
            if lockList_key in dictPcCardSelection['unity'][pcHash]:
                for hagId_this in dictPcCardSelection['unity'][pcHash][lockList_key]:
                    if pcCardName != dictPcCardSelection['unity'][pcHash][lockList_key][hagId_this]:
                        lockList_dict_new[hagId_this] = dictPcCardSelection['unity'][pcHash][lockList_key][hagId_this]
                dictPcCardSelection['unity'][pcHash][lockList_key] = lockList_dict_new
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

def pcCardDataGetTemplateByKey(templateName):
    global dictPcCardTemplateDefault
    tmp_template = None
    if templateName in dictPcCardTemplateDefault['unity']:
        tmp_template = dictPcCardTemplateDefault['unity'][templateName]
    return tmp_template

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
    return tmp_pc_template_name_key

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
    templateName_core = getKeyWithUpper(
        data = dictPcCardTemplateDefault['unity'],
        key = templateName
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
    templateName_core = getKeyWithUpper(
        data = dictPcCardTemplateDefault['unity'],
        key = templateName
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
        if OlivaDiceCore.pcCard.pcCardDataGetSelectionKeyLock(
            pcHash,
            hagId
        ) == None:
            res = OlivaDiceCore.pcCard.pcCardDataSetSelectionKey(
                pcHash,
                switchName
            )
        else:
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

def getDBValue(pcHash, hagID=None):
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
    try:
        pc_data = OlivaDiceCore.pcCard.pcCardDataGetByPcName(pcHash, hagId=hagID)
        str_val = int(pc_data.get('STR'))
        siz_val = int(pc_data.get('SIZ'))
        power_size = str_val + siz_val
        if power_size <= 64:
            return '-2'
        elif power_size <= 84:
            return '-1'
        elif power_size <= 124:
            return '0'
        elif power_size <= 164:
            return '1d4'
        elif power_size <= 204:
            return '1d6'
        elif power_size <= 284:
            return '2d6'
        elif power_size <= 364:
            return '3d6'
        elif power_size <= 444:
            return '4d6'
        else:
            additional_dice = (power_size - 445) // 80 + 1
            return f'{4 + additional_dice}d6'
    except:
        return '0'