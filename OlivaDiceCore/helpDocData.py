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
[.help更新] 查看更新日志
有问题请联系(请优先加群)
青果核心用户群：661366095''',

    '更新': '''[OlivaDiceCore]
3.0.7: 属性增量
3.0.6: 心跳系统
3.0.5: 固化版本
3.0.4: 细化指令
3.0.3: 优化控制流
3.0.2: 对接频道
3.0.1: 审核模式
3.0.0: 基础版本实现''',

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
.sc 理智检定
.ti/li 临时/总结症状
.name 随机名称''',

    '链接': '''查看源码: https://github.com/OlivOS-Team/OlivaDiceCore
OneDice标准: https://github.com/OlivOS-Team/onedice
OlivOS项目: https://github.com/OlivOS-Team/OlivOS''',

    'dismiss': '''dismiss [dɪsˈmɪs]
vt.	不予考虑; 摒弃; 对…不屑一提; 去除，消除，摒除(思想、感情等); 解雇; 免职; 开除;
[例句]
He dismissed the dismiss as worthless.
他认为dismiss毫无用处。
[其他]
第三人称单数：dismisses
现在分词：dismissing
过去式：dismissed
过去分词：dismissed

若需要使本机器人退群,请使用[.bot exit]''',

    'bot': '''@后接指令可以指定单独响应，如@机器人.bot off
.bot exit 退群
.bot 版本信息
.bot on 启用指令
.bot off 停用指令''',

    'st': '''.st [人物卡名]-[技能名][技能值][技能名][技能值]……    人物卡批量录入
.st list    显示人物卡列表
.st set [人物卡名]    切换人物卡
.st show    显示人物卡
.st temp [人物卡模版名]    切换人物卡模版
    默认可选：COC7，DND5E，FATE
.st rule [人物卡模版规则名]    切换人物卡规则
更多请使用[.help 人物卡模板]进行查看
.st del [人物卡名]    删除人物卡''',

    'r': '''通用掷骰指令
.r [掷骰表达式] [理由]    掷骰子
.rh [掷骰表达式] [理由]    掷暗骰
.r[次数]#[掷骰表达式] [理由]    多轮掷骰
表达式支持OneDice标准:
https://github.com/OlivOS-Team/onedice''',

    'ra': '''检定指令
.ra [技能名] [技能值]    技能检定
.rah [技能名] [技能值]    暗技能检定
.ra[次数]#[技能名] [技能值]    多轮检定
.ra(b/p)[技能名] [技能值]    奖惩检定''',


    'sc': '''理智检定
.sc [成功表达式]/[失败表达式] [san值]   理智检定''',

    '疯狂症状': '''疯狂症状：
.ti 临时疯狂症状
.li 总结疯狂症状''',

    'nn': '''命名
.nn [新人物卡名]    重命名人物卡
当与已有其它人物卡重名时，将覆盖旧卡''',

    'coc': '''人物作成
.coc [数量]    COC7人物作成''',

    'draw': '''抽牌:
.draw [牌堆名称]  抽牌堆
.drawh [牌堆名称]  暗抽牌堆''',

    '人物卡模板': '''1、为自己的人物卡指定COC模版（目前可选为COC7，DND5E，FATE）
指令: [.st temp COC7]
2、为自己的人物卡指定COC模版下的规则
指令: [.st rule C2]

其中[COC7]可选参数如下：
[default]
等同C3
[C0]
出1大成功
不满50出96 - 100大失败，满50出100大失败
[C1]
不满50出1大成功，满50出1 - 5大成功
不满50出96 - 100大失败，满50出100大失败
[C2]
出1 - 5且 <= 成功率大成功
出100或出96 - 99且 > 成功率大失败
[C3]
出1 - 5大成功
出96 - 100大失败
[C4]
出1 - 5且 <= 十分之一大成功
不满50出 >= 96 + 十分之一大失败，满50出100大失败
[C5]
出1 - 2且 < 五分之一大成功
不满50出96 - 100大失败，满50出99 - 100大失败
[DeltaGreen]
绿色三角洲规则书''',


    'name': '''随机姓名：
.name (cn/jp/en/enzh)
    后接cn/jp/en/enzh则限定生成中文/日文/英文/英文中译名''',


    'rc': '&ra',
    'ti': '&疯狂症状',
    'li': '&疯狂症状',
    'help': '&default',
    '帮助': '&default',
    '掷骰': '&r',
    '检定': '&ra',
    '理智检定': '&sc',
    '命名': '&nn',
    '人物卡': '&st',
    '车卡coc': '&coc'
}
