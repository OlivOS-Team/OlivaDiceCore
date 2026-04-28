# -*- encoding: utf-8 -*-
r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   helpDoc.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2026, OlivOS-Team
@Desc      :   None
"""

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
            with open(customHelpDocPath, 'r', encoding='utf-8') as customHelpDocPath_f:
                obj_HelpDoc_this = json.loads(customHelpDocPath_f.read())
                for bot_info_dict_this in OlivaDiceCore.helpDocData.dictHelpDoc:
                    botHash = bot_info_dict_this
                    if 'helpdoc' in obj_HelpDoc_this:
                        OlivaDiceCore.helpDocData.dictHelpDoc[botHash].update(obj_HelpDoc_this['helpdoc'])
        except Exception:
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
                with open(customHelpDocPath, 'r', encoding='utf-8') as customHelpDocPath_f:
                    obj_HelpDoc_this = json.loads(customHelpDocPath_f.read())
                    if 'helpdoc' in obj_HelpDoc_this:
                        OlivaDiceCore.helpDocData.dictHelpDoc[botHash].update(obj_HelpDoc_this['helpdoc'])
            except Exception:
                continue
        customHelpDocDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
        customHelpDocFile = 'helpdocDefault.json'
        customHelpDocPath = customHelpDocDir + '/' + customHelpDocFile
        try:
            with open(customHelpDocPath, 'r', encoding='utf-8') as customHelpDocPath_f:
                obj_HelpDoc_this = json.loads(customHelpDocPath_f.read())
                if type(obj_HelpDoc_this) is dict:
                    OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash].update(obj_HelpDoc_this)
                    OlivaDiceCore.helpDocData.dictHelpDoc[botHash].update(
                        OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash]
                    )
        except Exception:
            pass


def setHelpDocByBotHash(botHash, helpdocKey, helpdocVal):
    # 应用重定向逻辑
    redirected_bot_hash = OlivaDiceCore.userConfig.getRedirectedBotHash(botHash)

    if redirected_bot_hash not in OlivaDiceCore.helpDocData.dictHelpDocDefault:
        OlivaDiceCore.helpDocData.dictHelpDocDefault[redirected_bot_hash] = {}
    if redirected_bot_hash not in OlivaDiceCore.helpDocData.dictHelpDoc:
        OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash] = {}
    OlivaDiceCore.helpDocData.dictHelpDocDefault[redirected_bot_hash][helpdocKey] = helpdocVal
    OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash].update(
        OlivaDiceCore.helpDocData.dictHelpDocDefault[redirected_bot_hash]
    )
    saveHelpDocByBotHash(redirected_bot_hash)


def delHelpDocByBotHash(botHash, helpdocKey):
    # 应用重定向逻辑
    redirected_bot_hash = OlivaDiceCore.userConfig.getRedirectedBotHash(botHash)

    if redirected_bot_hash not in OlivaDiceCore.helpDocData.dictHelpDocDefault:
        OlivaDiceCore.helpDocData.dictHelpDocDefault[redirected_bot_hash] = {}
    if redirected_bot_hash not in OlivaDiceCore.helpDocData.dictHelpDoc:
        OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash] = {}
    if helpdocKey in OlivaDiceCore.helpDocData.dictHelpDocDefault[redirected_bot_hash]:
        OlivaDiceCore.helpDocData.dictHelpDocDefault[redirected_bot_hash].pop(helpdocKey)
    if helpdocKey in OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash]:
        OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash].pop(helpdocKey)
    saveHelpDocByBotHash(redirected_bot_hash)


def saveHelpDocByBotHash(botHash):
    if botHash in OlivaDiceCore.helpDocData.dictHelpDocDefault:
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console')
        try:
            customHelpDocDir = OlivaDiceCore.data.dataDirRoot + '/' + botHash + '/console'
            customHelpDocFile = 'helpdocDefault.json'
            customHelpDocPath = customHelpDocDir + '/' + customHelpDocFile
            with open(customHelpDocPath, 'w', encoding='utf-8') as customHelpDocPath_f:
                customHelpDocPath_f.write(
                    json.dumps(OlivaDiceCore.helpDocData.dictHelpDocDefault[botHash], ensure_ascii=False, indent=4)
                )
        except Exception:
            pass


# plugin_event 为 None 时仅返回回复内容，否则接管回复流程
def getHelp(key_str, bot_hash, plugin_event=None):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustom
    tmp_reply_str = None
    tmp_recommend_list = []
    tmp_recommend_str = ''
    key_str_new = key_str

    if plugin_event is not None:
        dictTValue['tUserName'] = plugin_event.data.sender['name']
    # 应用重定向逻辑（仅用于帮助文档数据）
    redirected_bot_hash = OlivaDiceCore.userConfig.getRedirectedBotHash(bot_hash)

    if bot_hash in OlivaDiceCore.msgCustom.dictStrCustomDict:
        dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[bot_hash]
    if redirected_bot_hash in OlivaDiceCore.helpDocData.dictHelpDoc:
        while True:
            # 以下划线开头的键值只能被帮助文档内部引用，无法直接精确匹配搜索
            if (
                not key_str_new.startswith('_')
                and key_str_new in OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash]
            ):
                tmp_tHelpDocResult = OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash][key_str_new]
                if len(tmp_tHelpDocResult) > 1:
                    if tmp_tHelpDocResult[0] == '&' and tmp_tHelpDocResult[1:] != key_str_new:
                        tmp_reply_str = getHelp(tmp_tHelpDocResult[1:], bot_hash, plugin_event)
                        return tmp_reply_str
                dictTValue['tHelpDocResult'] = OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash][key_str_new]
                if key_str_new == 'default':
                    bot_info_str = OlivaDiceCore.data.bot_info
                    if type(plugin_event) is OlivOS.API.Event:
                        dictTValue['tAdapter'] = OlivaDiceCore.msgCustomManager.loadAdapterType(plugin_event.bot_info)
                        bot_info_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            OlivaDiceCore.data.bot_info_auto, dictTValue
                        )
                    tmp_reply_str = '%s\n%s' % (bot_info_str, dictTValue['tHelpDocResult'])
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                        dictStrCustom['strHelpDoc'], dictTValue
                    )
                for count_index in range(100):
                    tmp_reply_str_old = tmp_reply_str
                    tmp_reply_str = formatSTRReplace(
                        tmp_reply_str, OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash]
                    )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(tmp_reply_str, dictTValue)
                    if tmp_reply_str_old == tmp_reply_str:
                        break
                return tmp_reply_str
            else:
                flag_need_loop = False
                tmp_recommend_list = getHelpRecommend(key_str_new, bot_hash)
                if type(tmp_recommend_list) is list:
                    if len(tmp_recommend_list) > 0:
                        flag_is_begin = True
                        tmp_count = 0
                        for tmp_recommend_list_this in tmp_recommend_list:
                            if not flag_is_begin:
                                tmp_recommend_str += '\n'
                            else:
                                flag_is_begin = False
                            tmp_recommend_str += '%d. %s' % (tmp_count + 1, tmp_recommend_list_this)
                            tmp_count += 1
                        if plugin_event is not None:
                            tmp_recommend_str += '\n请输入序号以查看对应选项'
                        dictTValue['tHelpDocResult'] = tmp_recommend_str
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strHelpDocRecommend'], dictTValue
                        )
                        flag_need_loop = True
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strHelpDocNotFound'], dictTValue
                        )
                    if plugin_event is None:
                        return tmp_reply_str
                    else:
                        if flag_need_loop:
                            OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
                            tmp_select: 'str|None' = OlivaDiceCore.msgReplyModel.replyCONTEXT_regWait(
                                plugin_event=plugin_event,
                                flagBlock='allowCommand',
                                hash=OlivaDiceCore.msgReplyModel.contextRegHash([None, plugin_event.data.user_id]),
                            )
                            if type(tmp_select) is str and tmp_select.isdigit():
                                tmp_select = int(tmp_select) - 1
                                if tmp_select >= 0 and tmp_select < len(tmp_recommend_list):
                                    key_str_new = tmp_recommend_list[tmp_select]
                                else:
                                    flag_need_loop = False
                            elif tmp_select is None:
                                return None
                            else:
                                flag_need_loop = False
                        if not flag_need_loop:
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                                dictStrCustom['strHelpDocNotFound'], dictTValue
                            )
                            return tmp_reply_str
                        else:
                            continue
            if plugin_event is None:
                break
    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strHelpDocNotFound'], dictTValue)
    if plugin_event is None:
        return tmp_reply_str


def getHelpRecommend(key_str: str, bot_hash: str):
    res = []
    tmp_RecommendRank_list = []

    helpRecommendGate = OlivaDiceCore.console.getConsoleSwitchByHash('helpRecommendGate', bot_hash)
    if helpRecommendGate is None:
        helpRecommendGate = 25

    # 应用重定向逻辑
    redirected_bot_hash = OlivaDiceCore.userConfig.getRedirectedBotHash(bot_hash)

    if redirected_bot_hash in OlivaDiceCore.helpDocData.dictHelpDoc:
        for dictHelpDoc_this in OlivaDiceCore.helpDocData.dictHelpDoc[redirected_bot_hash]:
            # 以下划线开头的键值只能被帮助文档内部引用，不参与模糊搜索
            if type(dictHelpDoc_this) is str and dictHelpDoc_this.startswith('_'):
                continue
            tmp_RecommendRank_list.append([getRecommendRank(key_str, dictHelpDoc_this), dictHelpDoc_this])
        tmp_RecommendRank_list.sort(key=lambda x: x[0])
    tmp_for_list = range(min(8, len(tmp_RecommendRank_list)))
    for tmp_for_list_this in tmp_for_list:
        if tmp_RecommendRank_list[tmp_for_list_this][0] < 1000:
            if len(tmp_RecommendRank_list[tmp_for_list_this][1]) < helpRecommendGate:
                res.append(tmp_RecommendRank_list[tmp_for_list_this][1])
    return res


def getRecommendRank(word1_in: str, word2_in: str, gate_rank: int = 1000, rate: float = 1.0):
    word1 = word1_in.lower()
    word2 = word2_in.lower()

    # 空字符串处理
    if not word1 or not word2:
        return gate_rank + 1

    # 保证 word1 为较短的字符串（提高 DP 效率），原始逻辑会自动交换
    if len(word1) > len(word2):
        word1, word2 = word2, word1

    len1 = len(word1)
    len2 = len(word2)

    # 子串快速匹配（此时 len1 <= len2）
    if word2.find(word1) != -1:
        return 0   # 完全匹配时原始逻辑计算后也是 0

    # 滚动数组：prev_lcs 上一行 LCS，prev_ed 上一行编辑距离
    prev_lcs = [0] * (len1 + 1)
    prev_ed = list(range(len1 + 1))   # 第一行：空字符串 -> word1 的编辑距离

    for j in range(1, len2 + 1):
        ch2 = word2[j - 1]
        cur_lcs = [0] * (len1 + 1)
        cur_ed = [0] * (len1 + 1)
        cur_ed[0] = j   # 第一列：空字符串 -> word2 前缀的编辑距离

        for i in range(1, len1 + 1):
            if word1[i - 1] == ch2:
                cur_lcs[i] = prev_lcs[i - 1] + 1
                cur_ed[i] = prev_ed[i - 1]
            else:
                cur_lcs[i] = max(prev_lcs[i], cur_lcs[i - 1])
                cur_ed[i] = min(prev_ed[i - 1], prev_ed[i], cur_ed[i - 1]) + 1

        prev_lcs = cur_lcs
        prev_ed = cur_ed

    iRank_1 = prev_lcs[len1]   # LCS 长度
    iRank_2 = prev_ed[len1]    # 编辑距离

    # 原始计算公式（此时 find_flag = 1，因为未子串匹配）
    iRank = len2 * (len1 - iRank_1) + iRank_2 + 1
    iRank = (iRank * iRank) // len1 // len2

    # 阈值判断（使用 rate 和 gate_rank，原始 rate=1.0）
    if iRank >= int(len1 * len2 * rate):
        iRank += gate_rank

    return iRank


def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# 用状态机实现高宽容度的变量引用
# 替代Python内置Format
def formatSTRReplace(data: str, valDict: dict):
    raw = data
    res = ''
    reg_res = ''
    reg_key = ''
    flagType = 'str'
    for i in raw:
        if flagType == 'str':
            if i == '{':
                flagType = 'left'
            else:
                reg_res += i
                flagType = 'str'
        elif flagType == 'left':
            if i == '}':
                reg_key = ''
                flagType = 'right'
            else:
                reg_key = i
                flagType = 'key'
        elif flagType == 'key':
            if i == '}':
                flag_hit = False
                # 变量表替换
                if not flag_hit and reg_key in valDict and type(valDict[reg_key] is str):
                    reg_res += str(valDict[reg_key])
                    flag_hit = True
                # 缺省确保原样返回
                if not flag_hit:
                    reg_res += '{%s}' % reg_key
                flagType = 'right'
            else:
                reg_key += i
                flagType = 'key'
        elif flagType == 'right':
            reg_key = ''
            if i == '{':
                flagType = 'left'
            else:
                reg_res += i
                flagType = 'str'
    if flagType == 'key':
        reg_res += '{%s' % reg_key
    res = reg_res
    return res


# 通用模糊搜索和选择函数
# 参数：
#   key_str: 搜索关键词
#   item_list: 待搜索的项目列表
#   bot_hash: bot哈希值（用于获取阈值配置）
#   plugin_event: 事件对象（如果为None则不等待用户选择，仅返回搜索结果）
#   strRecommendKey: 找到相似项时使用的消息模板键名（如 'strPcSetRecommend', 'strTeamSetRecommend'）
#   dictStrCustom: 自定义回复字符串字典
#   dictTValue: 模板值字典
# 返回值：
#   如果 plugin_event 为 None，返回搜索结果列表
#   如果 plugin_event 不为 None，返回用户选择的项目，或 None（用户未选择/超时/取消）
def fuzzySearchAndSelect(
    key_str: str,
    item_list: list,
    bot_hash: str,
    plugin_event=None,
    strRecommendKey: str = 'strSearchRecommend',
    strErrorKey: str = None,
    dictStrCustom=None,
    dictTValue=None,
):
    """
    使用与 helpDoc 相同的模糊搜索算法，对任意列表进行模糊搜索，
    并可选择性地等待用户输入数字选择结果
    strErrorKey: 未找到匹配或用户超时/取消时的错误消息模板键
    """
    if dictStrCustom is None:
        dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustom
    if dictTValue is None:
        dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    helpRecommendGate = OlivaDiceCore.console.getConsoleSwitchByHash('helpRecommendGate', bot_hash)
    if helpRecommendGate is None:
        helpRecommendGate = 25
    # 对每个项目计算相似度
    tmp_RecommendRank_list = []
    for item in item_list:
        tmp_RecommendRank_list.append([getRecommendRank(key_str, str(item)), item])
    # 按相似度排序
    tmp_RecommendRank_list.sort(key=lambda x: x[0])
    # 获取前8个最相似的项目
    res = []
    tmp_for_list = range(min(8, len(tmp_RecommendRank_list)))
    for tmp_for_list_this in tmp_for_list:
        if tmp_RecommendRank_list[tmp_for_list_this][0] < 1000:
            if len(str(tmp_RecommendRank_list[tmp_for_list_this][1])) < helpRecommendGate:
                res.append(tmp_RecommendRank_list[tmp_for_list_this][1])
    # 如果没有提供 plugin_event，直接返回搜索结果
    if plugin_event is None:
        return res
    flag_need_loop = False
    tmp_reply_str = None
    if len(res) > 0:
        # 构建推荐列表字符串（与 getHelp 相同逻辑）
        tmp_recommend_str = ''
        flag_is_begin = True
        tmp_count = 0
        for tmp_recommend_list_this in res:
            if not flag_is_begin:
                tmp_recommend_str += '\n'
            else:
                flag_is_begin = False
            tmp_recommend_str += '%d. %s' % (tmp_count + 1, tmp_recommend_list_this)
            tmp_count += 1
        dictTValue['tSearchResult'] = tmp_recommend_str
        # 使用指定的消息模板
        if strRecommendKey in dictStrCustom:
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom[strRecommendKey], dictTValue)
        flag_need_loop = True
    else:
        # 没有搜索结果
        if strErrorKey is not None and strErrorKey in dictStrCustom:
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom[strErrorKey], dictTValue)
    # 按照 getHelp 的逻辑处理等待和选择
    if flag_need_loop:
        OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
        tmp_select: 'str|None' = OlivaDiceCore.msgReplyModel.replyCONTEXT_regWait(
            plugin_event=plugin_event,
            flagBlock='allowCommand',
            hash=OlivaDiceCore.msgReplyModel.contextRegHash([None, plugin_event.data.user_id]),
        )
        if type(tmp_select) is str and tmp_select.isdigit():
            tmp_select = int(tmp_select) - 1
            if tmp_select >= 0 and tmp_select < len(res):
                # 返回用户选择的项目
                return res[tmp_select]
            else:
                flag_need_loop = False
        elif tmp_select is None:
            return None
        elif tmp_select is False:
            return None
        else:
            flag_need_loop = False
    if not flag_need_loop:
        if strErrorKey is not None and strErrorKey in dictStrCustom:
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom[strErrorKey], dictTValue)
            OlivaDiceCore.msgReply.replyMsg(plugin_event, tmp_reply_str)
        return None
    return None
