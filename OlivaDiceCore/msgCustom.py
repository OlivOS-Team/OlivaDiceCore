# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgCustom.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

dictStrCustomDict = {}

dictStrCustom = {
    'strHello': '欢迎使用本机器人! 请使用[.help]查看帮助',
    'strBot': '欢迎使用本机器人! 请使用[.help]查看帮助',
    'strBotExit': '即将退出本群',
    'strBotExitRemote': '收到远程控制, 即将退出本群',
    'strBotExitRemoteShow' : '即将远程退出群[{tGroupId}]',
    'strBotAddFriendNotice': '好友添加请求, 来自[{tUserId}]\n备注:{tComment}\n{tResult}',
    'strBotAddGroupNotice' : '群添加请求，来自群[{tGroupId}], 邀请者[{tInvaterId}]\n{tResult}',
    'strBotAddGroupNoticeIgnoreResult' : '已忽略\n请输入[{tAcceptCommand}]以远程接受请求',
    'strBotAddGroupRemoteAcceptShow' : '已远程接受请求[{tInvateFlag}]',
    'strAccept' : '已接受',
    'strIgnore' : '已忽略',
    'strReject' : '已驳回',
    'strBotOn' : '开启成功',
    'strBotAlreadyOn' : '已经处于开启状态',
    'strBotOff' : '关闭成功',
    'strBotAlreadyOff' : '已经处于关闭状态',
    'strHelpDoc' : '已为你找到以下以下条目:\n{tHelpDocResult}',
    'strHelpDocRecommend' : '已为你找到以下以下相似条目:\n{tHelpDocResult}',
    'strHelpDocNotFound' : '未找到匹配条目',
    'strDrawDeck' : '你抽到了:\n{tDrawDeckResult}',
    'strDrawDeckHideShow' : '[{tName}]进行了暗抽牌',
    'strDrawDeckNotFound' : '牌堆未找到',
    'strRoll' : '[{tName}]掷骰: {tRollResult}',
    'strRollWithReason' : '[{tName}]由于[{tRollReason}]掷骰: {tRollResult}',
    'strRollHide' : '于群[{tGroupId}]中[{tName}]掷骰: {tRollResult}',
    'strRollHideWithReason' : '于群[{tGroupId}]中[{tName}]由于[{tRollReason}]掷骰: {tRollResult}',
    'strRollHideShow' : '[{tName}]掷暗骰',
    'strRollHideShowWithReason' : '[{tName}]由于[{tRollReason}]掷暗骰',
    'strRollRange' : '表达式: {tRollPara}\n细节: {tRollResultDetail}\n结果: {tRollResultInt}\n范围: {tRollResultIntRange}',
    'strPcInit' : '[{tPcTempName}]人物卡作成:{tPcInitResult}',
    'strPcSetSkillValue' : '[{tName}]的人物卡已保存',
    'strPcGetSingleSkillValue' : '[{tName}]的[{tSkillName}]: {tSkillValue}',
    'strPcShow' : '人物卡[{tName}]:\n{tPcShow}',
    'strPcList' : '[{tName}]的人物卡:\n{tPcList}\n当前选择:{tPcSelection}',
    'strPcSet' : '人物卡已切换至[{tPcSelection}]',
    'strPcSetError' : '试图切入的人物卡不存在',
    'strPcDel' : '人物卡[{tPcSelection}]已删除',
    'strPcDelError' : '试图删除的人物卡不存在',
    'strPcTemp' : '人物卡[{tPcSelection}]套用模板[{tPcTempName}]',
    'strPcTempShow' : '人物卡[{tPcSelection}]:\n模板[{tPcTempName}]',
    'strPcTempError' : '试图套用的模板不存在，或是未设置人物卡',
    'strPcTempRule' : '人物卡[{tPcSelection}]套用模板[{tPcTempName}]的规则[{tPcTempRuleName}]',
    'strPcTempRuleShow' : '人物卡[{tPcSelection}]:\n模板[{tPcTempName}]\n规则[{tPcTempRuleName}]',
    'strPcTempRuleError' : '试图套用的模板规则不存在，或是未设置人物卡',
    'strPcRename' : '[{tPcSelection}]已重命名为[{tPcSelectionNew}]',
    'strPcSkillCheck' : '[{tName}]进行技能[{tSkillValue}]检定: {tRollResult} {tSkillCheckReasult}',
    'strPcSkillCheckHide' : '于群[{tGroupId}]中[{tName}]进行技能[{tSkillValue}]检定: {tRollResult} {tSkillCheckReasult}',
    'strPcSkillCheckHideShow' : '[{tName}]进行技能[{tSkillValue}]暗检定',
    'strPcSkillCheckWithSkillName' : '[{tName}]进行技能[{tSkillName}:{tSkillValue}]检定: {tRollResult} {tSkillCheckReasult}',
    'strPcSkillCheckHideWithSkillName' : '于群[{tGroupId}]中[{tName}]进行技能[{tSkillName}:{tSkillValue}]检定: {tRollResult} {tSkillCheckReasult}',
    'strPcSkillCheckHideShowWithSkillName' : '[{tName}]进行技能[{tSkillName}:{tSkillValue}]暗检定',
    'strSanCheck' : '[{tName}]进行理智检定[{tSkillValue}]:\n{tRollResult} {tSkillCheckReasult}\n理智减少{tRollSubResult}点,当前剩余[{tSkillValueNew}]点',
    'strSanCheckGreatFailed' : '[{tName}]进行理智检定[{tSkillValue}]:\n{tRollResult} {tSkillCheckReasult}\n理智减少{tRollSubResult}的最大值[{tRollSubResultIntMax}]点,当前剩余[{tSkillValueNew}]点',
    'strIntPositiveInfinite' : '正无穷大',
    'strIntNegativeInfinite' : '负无穷大',
    'strPcSkillCheckSucceed' : '成功',
    'strPcSkillCheckHardSucceed' : '困难成功',
    'strPcSkillCheckExtremeHardSucceed' : '极难成功',
    'strPcSkillCheckGreatSucceed' : '大成功',
    'strPcSkillCheckFailed' : '失败',
    'strPcSkillCheckGreatFailed' : '大失败',
    'strPcSkillCheckFate01' : '[-2 拙劣]',
    'strPcSkillCheckFate02' : '[-1 差劲]',
    'strPcSkillCheckFate03' : '[+0 二流]',
    'strPcSkillCheckFate04' : '[+1 一般]',
    'strPcSkillCheckFate05' : '[+2 尚可]',
    'strPcSkillCheckFate06' : '[+3 良好]',
    'strPcSkillCheckFate07' : '[+4 极佳]',
    'strPcSkillCheckFate08' : '[+5 卓越]',
    'strPcSkillCheckFate09' : '[+6 惊异]',
    'strPcSkillCheckFate10' : '[+7 史诗]',
    'strPcSkillCheckFate11' : '[+8 传奇]',
    'strPcSkillCheckNope' : '无事发生',
    'strPcSkillCheckError' : '发生错误'
}

dictStrConst = {
    'strInitData' : '[{tInitDataCount}]条[{tInitDataType}]数据已加载',
    'strInitBakData' : '[{tInitDataCount}]条[{tInitDataType}]数据已备份',
    'strSaveData' : '[{tInitDataCount}]条[{tInitDataType}]数据已写入'
}

dictGValue = {
    'gBotName' : '我'
}

dictTValue = {
    'tName' : 'N/A',
    'tUserId' : 'N/A',
    'tGroupName' : '私聊',
    'tGroupId' : '私聊',
    'tInvaterName' : 'N/A',
    'tInvaterId' : 'N/A',
    'tInvateFlag' : 'N/A',
    'tComment' : 'N/A',
    'tResult' : 'N/A',
    'tAcceptCommand' : 'N/A',
    'tRollResult' : '',
    'tRollSubResult' : '',
    'tRollSubResultIntMax' : 'N/A',
    'tRollReason' : '',
    'tRollPara' : '',
    'tRollResultInt' : 'N/A',
    'tRollResultDetail' : 'N/A',
    'tRollResultIntRange' : 'N/A',
    'tSkillName' : '',
    'tSkillValue' : '',
    'tSkillValueNew' : '',
    'tSkillCheckReasult' : '',
    'tPcInitResult' : 'N/A',
    'tPcShow' : '',
    'tPcList' : '',
    'tPcSelection' : 'N/A',
    'tPcSelectionNew' : 'N/A',
    'tPcTempName' : '',
    'tPcTempRuleName' : '',
    'tInitDataCount' : '0',
    'tInitDataType': '未知',
    'tHelpDocResult': 'N/A',
    'tDrawDeckResult': 'N/A'
}
