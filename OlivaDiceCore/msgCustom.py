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

dictStrCustomUpdateDict = {}

dictStrCustom = {
    'strBotName': 'Bot',
    'strSetStr': '回复词[{tStrName}]已更新',
    'strBecomeMaster': '口令正确，[{tName}]已成为Master',
    'strCantBecomeMaster': '无Master权限且口令错误，拒绝认证',
    'strMasterConsoleShow': '[{tConsoleKey}]当前为[{tConsoleValue}]',
    'strMasterConsoleShowList': '[{tConsoleKey}]当前为:\n{tConsoleValue}',
    'strMasterConsoleSet': '[{tName}]已将[{tConsoleKey}]设置为[{tConsoleValue}]',
    'strMasterConsoleAppend': '[{tName}]已修改[{tConsoleKey}]条目',
    'strMasterConsoleSetInvalid': '非法的配置值',
    'strMasterConsoleNotFound': '无法访问的配置项',
    'strNeedMaster': '需要Master权限',
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
    'strBotNotUnderHost' : '无所属主频道',
    'strBotHostLocalOn' : '本主频道开启成功',
    'strBotAlreadyHostLocalOn' : '本主频道已经处于开启状态',
    'strBotHostLocalOff' : '本主频道关闭成功',
    'strBotAlreadyHostLocalOff' : '本主频道已经处于关闭状态',
    'strBotHostOn' : '本主频道进入默认开启模式',
    'strBotAlreadyHostOn' : '本主频道已经处于默认开启模式',
    'strBotHostOff' : '本主频道进入默认关闭模式',
    'strBotAlreadyHostOff' : '本主频道已经处于默认关闭模式',
    'strHelpDoc' : '已为你找到以下以下条目:\n{tHelpDocResult}',
    'strHelpDocRecommend' : '已为你找到以下以下相似条目:\n{tHelpDocResult}',
    'strHelpDocNotFound' : '未找到匹配条目',
    'strDrawTi' : '[{tName}]疯狂发作-临时症状:\n{tResult}',
    'strDrawLi' : '[{tName}]疯狂发作-总结症状:\n{tResult}',
    'strDrawName' : '[{tName}]的随机名称:\n{tResult}',
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
    'strPcUpdateSkillValue' : '[{tName}]的人物卡已更新:\n[{tSkillName}]: {tSkillUpdate}',
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
    'strPcSkillEnhanceCheck' : '[{tName}]进行技能[{tSkillName}:{tSkillValue}]成长检定: {tRollResult} {tSkillCheckReasult}',
    'strPcSkillEnhanceContent' : '\n该技能发生了增长: {tRollSubResult}',
    'strPcSkillEnhanceAll' : '[{tName}]进行技能自动成长检定:\n共有[{tSkillEnhanceCount}]个技能进行了检定，其中成功[{tSkillEnhanceSucceedCount}]个: {tSkillEnhanceSucceedList}',
    'strPcSkillEnhanceError' : '未设置人物卡，无法进行自动成长检定',
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
    'strPcSkillCheckNope' : '需要解释',
    'strPcSkillCheckError' : '发生错误'
}

dictStrConst = {
    'strToBeMaster' : '请使用[{tInitMasterKey}]指令以获取Master权限',
    'strInitData' : '[{tInitDataCount}]条[{tInitDataType}]数据已加载',
    'strInitBakData' : '[{tInitDataCount}]条[{tInitDataType}]数据已备份',
    'strSaveData' : '[{tInitDataCount}]条[{tInitDataType}]数据已写入'
}

dictGValue = {
    'gBotName' : '我'
}

dictTValue = {
    'tName' : 'N/A',
    'tStrName' : 'N/A',
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
    'tSkillUpdate' : 'N/A',
    'tPcInitResult' : 'N/A',
    'tPcShow' : '',
    'tPcList' : '',
    'tPcSelection' : 'N/A',
    'tPcSelectionNew' : 'N/A',
    'tPcTempName' : '',
    'tPcTempRuleName' : '',
    'tSkillEnhanceCount' : 'N/A',
    'tSkillEnhanceSucceedCount' : 'N/A',
    'tSkillEnhanceSucceedList' : 'N/A',
    'tInitDataCount' : '0',
    'tInitMasterKey': '不可用',
    'tInitDataType': '未知',
    'tHelpDocResult': 'N/A',
    'tDrawDeckResult': 'N/A',
    'tConsoleKey': 'N/A',
    'tConsoleValue': 'N/A'
}
