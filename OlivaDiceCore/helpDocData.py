# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   helpDocData.py
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

dictHelpDoc = {}

dictHelpDocTemp = {
    'default': '''若需要使本机器人退群,请使用[.bot exit]
输入[.bot on]/[.bot off]可以开关骰子功能
(如群内有多个骰子,请在@后追加指令)
[.help指令] 查看指令列表
[.help链接] 查看源码文档
有问题请联系(请优先加群)
青果核心用户群：661366095''',

    '指令': '''@后接指令可以指定单独响应，如@机器人.bot off
多数指令需要后接参数，请.help对应指令 获取详细信息，如.help bot
.bot exit 退群
.bot 版本信息
.bot on 启用指令
.bot off 停用指令
.coc COC7人物作成
.st 人物卡记录
.nn 设置人物卡名称
.r 掷骰
.ra 检定
.sc 理智检定''',

    '链接': '''查看源码: https://github.com/OlivOS-Team/OlivaDiceCore''',

    'st': '''.st [人物卡名]-[技能名][技能值][技能名][技能值]……    人物卡批量录入
.st list    显示人物卡列表
.st set [人物卡名]    切换人物卡
.st show    显示人物卡
.st temp [人物卡模版名]    切换人物卡模版
    默认可选：COC7，DND，FATE
.st rule [人物卡模版规则名]    切换人物卡规则
.st del [人物卡模版名]    删除人物卡''',

    'r': '''通用掷骰指令
.r [掷骰表达式] [理由]    掷骰子
.rh [掷骰表达式] [理由]    掷暗骰''',

    'ra': '''检定指令
.ra [技能名] [技能值]    技能检定
.rah [技能名] [技能值]    暗技能检定''',

    'sc': '''理智检定
.sc [成功表达式]/[失败表达式] [san值]   理智检定''',

    'nn': '''命名
.nn [新人物卡名]    重命名人物卡''',

    'coc': '''人物作成
.coc [数量]    COC7人物作成''',

    'draw': '''抽牌：.draw [牌堆名称]'''
}
