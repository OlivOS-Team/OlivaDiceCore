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
    for bot_info_dict_this in bot_info_dict:
        OlivaDiceCore.drawCardData.dictDeck[bot_info_dict_this] = OlivaDiceCore.drawCardData.dictDeckTemp.copy()
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/extend')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/extend/deckclassic')
    customDeckDir = OlivaDiceCore.data.dataDirRoot + '/unity/extend/deckclassic'
    fileDeckList = os.listdir(customDeckDir)
    for fileDeckList_this in fileDeckList:
        customDeckFile = fileDeckList_this
        customDeckPath = customDeckDir + '/' + customDeckFile
        try:
            with open(customDeckPath, 'r', encoding = 'utf-8') as customDeckPath_f:
                obj_Deck_this = json.loads(customDeckPath_f.read())
                for bot_info_dict_this in OlivaDiceCore.drawCardData.dictDeck:
                    botHash = bot_info_dict_this
                    OlivaDiceCore.drawCardData.dictDeck[botHash].update(obj_Deck_this)
        except:
            continue
    for bot_info_dict_this in OlivaDiceCore.drawCardData.dictDeck:
        botHash = bot_info_dict_this
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend')
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend/deckclassic')
        customDeckDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/extend/deckclassic'
        fileDeckList = os.listdir(customDeckDir)
        for fileDeckList_this in fileDeckList:
            customDeckFile = fileDeckList_this
            customDeckPath = customDeckDir + '/' + customDeckFile
            try:
                with open(customDeckPath, 'r', encoding = 'utf-8') as customDeckPath_f:
                    obj_Deck_this = json.loads(customDeckPath_f.read())
                    OlivaDiceCore.drawCardData.dictDeck[botHash].update(obj_Deck_this)
            except:
                continue

def getDrawDeck(key_str, bot_hash):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustom
    tmp_reply_str = None
    if bot_hash in OlivaDiceCore.msgCustom.dictStrCustomDict:
        dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[bot_hash]
    if bot_hash in OlivaDiceCore.drawCardData.dictDeck:
        if key_str in OlivaDiceCore.drawCardData.dictDeck[bot_hash]:
            tmp_draw_str = draw(key_str, bot_hash)
            if tmp_draw_str != None and type(tmp_draw_str) == str:
                dictTValue['tDrawDeckResult'] = tmp_draw_str
                tmp_reply_str = dictStrCustom['strDrawDeck'].format(**dictTValue)
                return tmp_reply_str
    tmp_reply_str = dictStrCustom['strDrawDeckNotFound'].format(**dictTValue)
    return tmp_reply_str

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
