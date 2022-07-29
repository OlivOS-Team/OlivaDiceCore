# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   helpDoc.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

import os
import json

def initHelpDoc(bot_info_dict):
    for bot_info_dict_this in bot_info_dict:
        OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this] = OlivaDiceCore.helpDocData.dictHelpDocTemp.copy()
        OlivaDiceCore.helpDocData.dictHelpDocDefault[bot_info_dict_this] = {}
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/extend')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/extend/helpdoc')
    customHelpDocDir = OlivaDiceCore.data.dataDirRoot + '/unity/extend/helpdoc'
    fileHelpDocList = os.listdir(customHelpDocDir)
    for fileHelpDocList_this in fileHelpDocList:
        customHelpDocFile = fileHelpDocList_this
        customHelpDocPath = customHelpDocDir + '/' + customHelpDocFile
        try:
            with open(customHelpDocPath, 'r', encoding = 'utf-8') as customHelpDocPath_f:
                obj_HelpDoc_this = json.loads(customHelpDocPath_f.read())
                for bot_info_dict_this in OlivaDiceCore.helpDocData.dictHelpDoc:
                    botHash = bot_info_dict_this
                    if 'helpdoc' in obj_HelpDoc_this:
                        OlivaDiceCore.helpDocData.dictHelpDoc[botHash].update(obj_HelpDoc_this['helpdoc'])
        except:
            continue
    for bot_info_dict_this in OlivaDiceCore.helpDocData.dictHelpDoc:
        botHash = bot_info_dict_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend')
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend/helpdoc')
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
        customHelpDocDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend/helpdoc'
        fileHelpDocList = os.listdir(customHelpDocDir)
        for fileHelpDocList_this in fileHelpDocList:
            customHelpDocFile = fileHelpDocList_this
            customHelpDocPath = customHelpDocDir + '/' + customHelpDocFile
            try:
                with open(customHelpDocPath, 'r', encoding = 'utf-8') as customHelpDocPath_f:
                    obj_HelpDoc_this = json.loads(customHelpDocPath_f.read())
                    if 'helpdoc' in obj_HelpDoc_this:
                        OlivaDiceCore.helpDocData.dictHelpDoc[botHash].update(obj_HelpDoc_this['helpdoc'])
            except:
                continue
        customHelpDocDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
        customHelpDocFile = 'helpdocDefault.json'
        customHelpDocPath = customHelpDocDir + '/' + customHelpDocFile
        try:
            with open(customHelpDocPath, 'r', encoding = 'utf-8') as customHelpDocPath_f:
                obj_HelpDoc_this = json.loads(customHelpDocPath_f.read())
                if type(obj_HelpDoc_this) == dict:
                    OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash].update(obj_HelpDoc_this)
                    OlivaDiceCore.helpDocData.dictHelpDoc[botHash].update(
                        OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash]
                    )
        except:
            pass

def setHelpDocByBotHash(botHash, helpdocKey, helpdocVal):
    if botHash not in OlivaDiceCore.helpDocData.dictHelpDocDefault:
        OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash] = {}
    if botHash not in OlivaDiceCore.helpDocData.dictHelpDoc:
        OlivaDiceCore.helpDocData.dictHelpDoc[botHash] = {}
    OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash][helpdocKey] = helpdocVal
    OlivaDiceCore.helpDocData.dictHelpDoc[botHash].update(
        OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash]
    )
    saveHelpDocByBotHash(botHash)

def delHelpDocByBotHash(botHash, helpdocKey):
    if botHash not in OlivaDiceCore.helpDocData.dictHelpDocDefault:
        OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash] = {}
    if botHash not in OlivaDiceCore.helpDocData.dictHelpDoc:
        OlivaDiceCore.helpDocData.dictHelpDoc[botHash] = {}
    if helpdocKey in OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash]:
        OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash].pop(helpdocKey)
    if helpdocKey in OlivaDiceCore.helpDocData.dictHelpDoc[botHash]:
        OlivaDiceCore.helpDocData.dictHelpDoc[botHash].pop(helpdocKey)
    saveHelpDocByBotHash(botHash)

def saveHelpDocByBotHash(botHash):
    if botHash in OlivaDiceCore.helpDocData.dictHelpDocDefault:
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
        try:
            customHelpDocDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
            customHelpDocFile = 'helpdocDefault.json'
            customHelpDocPath = customHelpDocDir + '/' + customHelpDocFile
            with open(customHelpDocPath, 'w', encoding = 'utf-8') as customHelpDocPath_f:
                customHelpDocPath_f.write(
                    json.dumps(
                        OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash],
                        ensure_ascii = False,
                        indent = 4
                    )
                )
        except:
            pass

def getHelp(key_str, bot_hash):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustom
    tmp_reply_str = None
    tmp_recommend_list = []
    tmp_recommend_str = ''
    if bot_hash in OlivaDiceCore.msgCustom.dictStrCustomDict:
        dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[bot_hash]
    if bot_hash in OlivaDiceCore.helpDocData.dictHelpDoc:
        if key_str in OlivaDiceCore.helpDocData.dictHelpDoc[bot_hash]:
            tmp_tHelpDocResult = OlivaDiceCore.helpDocData.dictHelpDoc[bot_hash][key_str]
            if len(tmp_tHelpDocResult) > 1:
                if tmp_tHelpDocResult[0] == '&' and tmp_tHelpDocResult[1:] != key_str:
                    tmp_reply_str = getHelp(tmp_tHelpDocResult[1:], bot_hash)
                    return tmp_reply_str
            dictTValue['tHelpDocResult'] = OlivaDiceCore.helpDocData.dictHelpDoc[bot_hash][key_str]
            if key_str == 'default':
                tmp_reply_str = '%s\n%s' % (OlivaDiceCore.data.bot_info, dictTValue['tHelpDocResult'])
            else:
                tmp_reply_str = dictStrCustom['strHelpDoc'].format(**dictTValue)
            return tmp_reply_str
        else:
            tmp_recommend_list = getHelpRecommend(key_str, bot_hash)
            if type(tmp_recommend_list) == list:
                if len(tmp_recommend_list) > 0:
                    flag_is_begin = True
                    for tmp_recommend_list_this in tmp_recommend_list:
                        if not flag_is_begin:
                            tmp_recommend_str += '\n'
                        else:
                            flag_is_begin = False
                        tmp_recommend_str += '[.help %s]' % (tmp_recommend_list_this,)
                    dictTValue['tHelpDocResult'] = tmp_recommend_str
                    tmp_reply_str = dictStrCustom['strHelpDocRecommend'].format(**dictTValue)
                else:
                    tmp_reply_str = dictStrCustom['strHelpDocNotFound'].format(**dictTValue)
                return tmp_reply_str
    tmp_reply_str = dictStrCustom['strHelpDocNotFound'].format(**dictTValue)
    return tmp_reply_str

def getHelpRecommend(key_str:str, bot_hash:str):
    res = []
    tmp_RecommendRank_list = []
    if bot_hash in OlivaDiceCore.helpDocData.dictHelpDoc:
        for dictHelpDoc_this in OlivaDiceCore.helpDocData.dictHelpDoc[bot_hash]:
            tmp_RecommendRank_list.append([
                getRecommendRank(
                    key_str,
                    dictHelpDoc_this
                ),
                dictHelpDoc_this
            ])
        tmp_RecommendRank_list.sort(key = lambda x : x[0])
    tmp_for_list = range(min(8, len(tmp_RecommendRank_list)))
    for tmp_for_list_this in tmp_for_list:
        if tmp_RecommendRank_list[tmp_for_list_this][0] < 1000:
            if len(tmp_RecommendRank_list[tmp_for_list_this][1]) < 25:
                res.append(tmp_RecommendRank_list[tmp_for_list_this][1])
    return res

def getRecommendRank(word1_in:str, word2_in:str):
    iRank = 1
    find_flag = 1
    word1 = word1_in.lower()
    word2 = word2_in.lower()
    if len(word1) > len(word2):
        [word1, word2] = [word2, word1]
    word1_len = len(word1)
    word2_len = len(word2)

    if word2.find(word1) != -1:
        find_flag = 0

    #LCS
    dp1 = []
    dp1_first = [0]
    for word1_this in word1:
        dp1_first.append(0)
    dp1.append(dp1_first)
    for word2_this in word2:
        dp1.append([0] + [0] * word1_len)
    tmp_i_list = range(1, word1_len + 1)
    tmp_j_list = range(1, word2_len + 1)
    for i in tmp_i_list:
        for j in tmp_j_list:
            if word1[i - 1] == word2[j - 1]:
                dp1[j][i] = dp1[j - 1][i - 1] + 1
            else:
                dp1[j][i] = max(dp1[j - 1][i], dp1[j][i - 1])
    iRank_1 = dp1[word2_len][word1_len]

    #minDistance
    dp2 = []
    dp2_first = [0]
    tmp_counter = 1
    for word1_this in word1:
        dp2_first.append(tmp_counter)
        tmp_counter += 1
    dp2.append(dp2_first)
    tmp_counter = 1
    for word2_this in word2:
        dp2.append([tmp_counter] + [0] * word1_len)
        tmp_counter += 1
    tmp_i_list = range(1, word1_len + 1)
    tmp_j_list = range(1, word2_len + 1)
    for i in tmp_i_list:
        for j in tmp_j_list:
            if word1[i - 1] == word2[j - 1]:
                dp2[j][i] = dp2[j - 1][i - 1]
            else:
                dp2[j][i] = min(dp2[j - 1][i - 1], min(dp2[j - 1][i], dp2[j][i - 1])) + 1
    iRank_2 = dp2[word2_len][word1_len]

    iRank = (find_flag) * (word2_len * (word1_len - iRank_1) + iRank_2 + 1);
    iRank = int(int((iRank * iRank) / word1_len) / word2_len)

    if iRank >= word1_len * word2_len:
        iRank += 1000

    return iRank

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
