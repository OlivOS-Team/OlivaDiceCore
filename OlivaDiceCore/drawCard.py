# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   drawCard.py
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

def initDeck(bot_info_dict):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    obj_Deck_this_count_total_init = 0
    for bot_info_dict_this in bot_info_dict:
        OlivaDiceCore.drawCardData.dictDeck[bot_info_dict_this] = OlivaDiceCore.drawCardData.dictDeckTemp.copy()
        obj_Deck_this_count_total_init = len(OlivaDiceCore.drawCardData.dictDeck[bot_info_dict_this])
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/extend')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/extend/deckclassic')
    customDeckDir = OlivaDiceCore.data.dataDirRoot + '/unity/extend/deckclassic'
    fileDeckList = os.listdir(customDeckDir)
    obj_Deck_this = None
    obj_Deck_this_count = 0
    obj_Deck_this_count_total = 0
    dictTValue['tName'] = '全局'
    for fileDeckList_this in fileDeckList:
        customDeckFile = fileDeckList_this
        customDeckPath = customDeckDir + '/' + customDeckFile
        obj_Deck_this = None
        try:
            with open(customDeckPath, 'r', encoding = 'utf-8') as customDeckPath_f:
                obj_Deck_this = json.loads(customDeckPath_f.read())
        except:
            try:
                with open(customDeckPath, 'r', encoding = 'utf_8_sig') as customDeckPath_f:
                    obj_Deck_this = json.loads(customDeckPath_f.read())
            except:
                dictTValue['tInitDataName'] = customDeckFile
                OlivaDiceCore.msgReply.globalLog(
                    3,
                    dictStrConst['strInitDeckDataError'].format(**dictTValue),
                    [
                        ('OlivaDice', 'default'),
                        ('Init', 'default')
                    ]
                )
        if obj_Deck_this != None:
            for bot_info_dict_this in OlivaDiceCore.drawCardData.dictDeck:
                botHash = bot_info_dict_this
                OlivaDiceCore.drawCardData.dictDeck[botHash].update(obj_Deck_this)
        obj_Deck_this_count_total = len(OlivaDiceCore.drawCardData.dictDeck[botHash])
    dictTValue['tInitDataCount'] = str(obj_Deck_this_count_total - obj_Deck_this_count_total_init)
    dictTValue['tInitDataCount01'] = str(obj_Deck_this_count_total)
    OlivaDiceCore.msgReply.globalLog(
        2,
        dictStrConst['strInitDeckData'].format(**dictTValue),
        [
            ('OlivaDice', 'default'),
            ('Init', 'default')
        ]
    )
    for bot_info_dict_this in OlivaDiceCore.drawCardData.dictDeck:
        botHash = bot_info_dict_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend')
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend/deckclassic')
        customDeckDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend/deckclassic'
        dictTValue['tName'] = botHash
        if botHash in bot_info_dict:
            dictTValue['tName'] = '%s|%s' % (
                bot_info_dict[botHash].platform['platform'],
                str(bot_info_dict[botHash].id)
            )
        fileDeckList = os.listdir(customDeckDir)
        for fileDeckList_this in fileDeckList:
            customDeckFile = fileDeckList_this
            customDeckPath = customDeckDir + '/' + customDeckFile
            obj_Deck_this = None
            try:
                with open(customDeckPath, 'r', encoding = 'utf-8') as customDeckPath_f:
                    obj_Deck_this = json.loads(customDeckPath_f.read())
            except:
                try:
                    with open(customDeckPath, 'r', encoding = 'utf_8_sig') as customDeckPath_f:
                        obj_Deck_this = json.loads(customDeckPath_f.read())
                except:
                    dictTValue['tInitDataName'] = customDeckFile
                    OlivaDiceCore.msgReply.globalLog(
                        3,
                        dictStrConst['strInitDeckDataError'].format(**dictTValue),
                        [
                            ('OlivaDice', 'default'),
                            ('Init', 'default')
                        ]
                    )
            if obj_Deck_this != None:
                OlivaDiceCore.drawCardData.dictDeck[botHash].update(obj_Deck_this)
        obj_Deck_this_count = len(OlivaDiceCore.drawCardData.dictDeck[botHash])
        dictTValue['tInitDataCount'] = str(obj_Deck_this_count - obj_Deck_this_count_total)
        dictTValue['tInitDataCount01'] = str(obj_Deck_this_count)
        OlivaDiceCore.msgReply.globalLog(
            2,
            dictStrConst['strInitDeckData'].format(**dictTValue),
            [
                ('OlivaDice', 'default'),
                ('Init', 'default')
            ]
        )

def getDrawDeck(key_str, bot_hash, count = 1):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustom
    tmp_reply_str = None
    if bot_hash in OlivaDiceCore.msgCustom.dictStrCustomDict:
        dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[bot_hash]
    if bot_hash in OlivaDiceCore.drawCardData.dictDeck:
        if key_str in OlivaDiceCore.drawCardData.dictDeck[bot_hash]:
            if count >= 1 and count <= 10:
                tmp_for_list = range(count)
                tmp_card_list = []
                for tmp_for_list_this in tmp_for_list:
                    tmp_draw_str = draw(key_str, bot_hash)
                    if tmp_draw_str != None and type(tmp_draw_str) == str:
                        tmp_card_list.append(tmp_draw_str)
                dictTValue['tDrawDeckResult'] = '\n'.join(tmp_card_list)
                tmp_reply_str = dictStrCustom['strDrawDeck'].format(**dictTValue)
                return tmp_reply_str
    tmp_recommend_list = getDeckRecommend(key_str, bot_hash)
    if type(tmp_recommend_list) == list:
        if len(tmp_recommend_list) > 0:
            tmp_recommend_str = '\n'.join(
                ['[.draw %s]' % tmp_recommend_list_this for tmp_recommend_list_this in tmp_recommend_list]
            )
            dictTValue['tDrawDeckResult'] = tmp_recommend_str
            tmp_reply_str = dictStrCustom['strDrawDeckRecommend'].format(**dictTValue)
        else:
            tmp_reply_str = dictStrCustom['strDrawDeckNotFound'].format(**dictTValue)
    return tmp_reply_str

def getDeckRecommend(key_str:str, bot_hash:str):
    res = []
    tmp_RecommendRank_list = []
    if bot_hash in OlivaDiceCore.drawCardData.dictDeck:
        for dictDeck_this in OlivaDiceCore.drawCardData.dictDeck[bot_hash]:
            tmp_RecommendRank_list.append([
                OlivaDiceCore.helpDoc.getRecommendRank(
                    key_str,
                    dictDeck_this
                ),
                dictDeck_this
            ])
        tmp_RecommendRank_list.sort(key = lambda x : x[0])
    tmp_count_max = min(8, len(tmp_RecommendRank_list))
    count = 0
    while count < tmp_count_max:
        if tmp_RecommendRank_list[count][0] < 1000:
            if len(tmp_RecommendRank_list[count][1]) < 25:
                if len(tmp_RecommendRank_list[count][1]) > 0 and tmp_RecommendRank_list[count][1][0] != '_':
                    res.append(tmp_RecommendRank_list[count][1])
        count += 1
    return res

def draw(key_str, bot_hash, flag_need_give_back = True, mark_dict = None):
    tmp_reply_str = None
    tmp_deck_this = []
    tmp_deck_this_len = 1
    tmp_deck_this_hit = 0
    if bot_hash in OlivaDiceCore.drawCardData.dictDeck:
        if key_str in OlivaDiceCore.drawCardData.dictDeck[bot_hash]:
            if mark_dict == None:
                tmp_mark_dict = {}
            else:
                tmp_mark_dict = mark_dict
            if key_str in tmp_mark_dict:
                if len(tmp_mark_dict[key_str]) <= 0:
                    tmp_mark_dict[key_str] = initCloneDeckList(OlivaDiceCore.drawCardData.dictDeck[bot_hash][key_str])
            else:
                tmp_mark_dict[key_str] = initCloneDeckList(OlivaDiceCore.drawCardData.dictDeck[bot_hash][key_str])
            tmp_deck_this = tmp_mark_dict[key_str]
            if type(tmp_deck_this) == list:
                tmp_deck_this_len = len(tmp_deck_this)
                if tmp_deck_this_len > 0:
                    tmp_deck_this_hit = OlivaDiceCore.onedice.RD.random(None, 0, tmp_deck_this_len - 1)
                    tmp_reply_str = tmp_deck_this[tmp_deck_this_hit]
                    if not flag_need_give_back:
                        tmp_deck_this.pop(tmp_deck_this_hit)
                    flag_need_roll = True
                    tmp_mark_left = -1
                    tmp_mark_right = -1
                    tmp_base_offset = 0
                    tmp_reply_str_2 = tmp_reply_str
                    tmp_reply_str = ''
                    while flag_need_roll:
                        tmp_reply_str_1 = None
                        tmp_mark_left = tmp_reply_str_2.find('{', tmp_base_offset)
                        flag_need_give_back_2 = False
                        if tmp_mark_left != -1:
                            tmp_mark_right = tmp_reply_str_2.find('}', tmp_mark_left)
                        if tmp_mark_left != -1 and tmp_mark_right != -1:
                            tmp_reply_str += tmp_reply_str_2[tmp_base_offset:tmp_mark_left]
                            if tmp_mark_right - tmp_mark_left > 2:
                                if tmp_reply_str_2[tmp_mark_left + 1] == '%':
                                    tmp_reply_str_1 = tmp_reply_str_2[tmp_mark_left + 2:tmp_mark_right]
                                    flag_need_give_back_2 = True
                                else:
                                    tmp_reply_str_1 = tmp_reply_str_2[tmp_mark_left + 1:tmp_mark_right]
                            else:
                                tmp_reply_str_1 = tmp_reply_str_2[tmp_mark_left + 1:tmp_mark_right]
                            tmp_reply_str_1 = draw(tmp_reply_str_1, bot_hash, flag_need_give_back_2, tmp_mark_dict)
                            if tmp_reply_str_1 != None:
                                tmp_reply_str += tmp_reply_str_1
                            else:
                                tmp_reply_str += tmp_reply_str_2[tmp_mark_left:tmp_mark_right + 1]
                            tmp_base_offset = tmp_mark_right + 1
                        else:
                            tmp_reply_str += tmp_reply_str_2[tmp_base_offset:]
                            flag_need_roll = False
                        tmp_mark_left = -1
                        tmp_mark_right = -1
                    flag_need_roll = True
                    tmp_mark_left = -1
                    tmp_mark_right = -1
                    tmp_base_offset = 0
                    tmp_reply_str_2 = tmp_reply_str
                    tmp_reply_str = ''
                    while flag_need_roll:
                        tmp_reply_str_1 = None
                        tmp_mark_left = tmp_reply_str_2.find('[', tmp_base_offset)
                        flag_need_give_back_2 = False
                        if tmp_mark_left != -1:
                            tmp_mark_right = tmp_reply_str_2.find(']', tmp_mark_left)
                        if tmp_mark_left != -1 and tmp_mark_right != -1:
                            tmp_reply_str += tmp_reply_str_2[tmp_base_offset:tmp_mark_left]
                            tmp_reply_str_1 = tmp_reply_str_2[tmp_mark_left + 1:tmp_mark_right]
                            tmp_rd = OlivaDiceCore.onedice.RD(tmp_reply_str_1)
                            tmp_rd.roll()
                            if tmp_rd.resError == None:
                                tmp_reply_str += str(tmp_rd.resInt)
                            else:
                                tmp_reply_str += tmp_reply_str_2[tmp_mark_left:tmp_mark_right + 1]
                            tmp_base_offset = tmp_mark_right + 1
                        else:
                            tmp_reply_str += tmp_reply_str_2[tmp_base_offset:]
                            flag_need_roll = False
                        tmp_mark_left = -1
                        tmp_mark_right = -1
    return tmp_reply_str

def initCloneDeckList(src_deck):
    res_deck = []
    for src_deck_this in src_deck:
        tmp_mark_left = -1
        tmp_mark_right = -1
        tmp_reply_str_1 = None
        tmp_reply_str_2 = src_deck_this
        if len(tmp_reply_str_2) > 4:
            if tmp_reply_str_2[:2] == '::':
                tmp_mark_left = 0
            if tmp_mark_left != -1:
                tmp_mark_right = tmp_reply_str_2.find('::', 2)
        if tmp_mark_left != -1 and tmp_mark_right != -1:
            tmp_reply_str_1 = tmp_reply_str_2[tmp_mark_left + 2:tmp_mark_right]
            if len(tmp_reply_str_1) > 3 and tmp_reply_str_1[0] == '[' and tmp_reply_str_1[-1] == ']':
                tmp_reply_str_1 = tmp_reply_str_1[1:-1]
                tmp_rd = OlivaDiceCore.onedice.RD(tmp_reply_str_1)
                tmp_rd.roll()
                if tmp_rd.resError == None:
                    if tmp_rd.resInt > 0:
                        if tmp_mark_right + 2 < len(tmp_reply_str_2):
                            res_deck += [tmp_reply_str_2[tmp_mark_right + 2:]] * tmp_rd.resInt
                else:
                    res_deck += [src_deck_this]
            elif tmp_reply_str_1.isdigit():
                if tmp_mark_right + 2 < len(tmp_reply_str_2):
                    res_deck += [tmp_reply_str_2[tmp_mark_right + 2:]] * int(tmp_reply_str_1)
                else:
                    res_deck += [src_deck_this]
            else:
                res_deck += [src_deck_this]
        else:
            res_deck += [src_deck_this]
    return res_deck

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
