# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   data.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import sys
import platform
import os
import uuid

import OlivOS

OlivaDiceCore_name = 'OlivaDice核心模块'
OlivaDiceCore_ver = '3.3.11'
OlivaDiceCore_svn = 1061
OlivaDiceCore_ver_short = '%s(%s)' % (str(OlivaDiceCore_ver), str(OlivaDiceCore_svn))

exce_path = os.getcwd()

global_Proc = None

bot_info_Ver = '%s(%s)' % (str(OlivaDiceCore_ver), str(OlivaDiceCore_svn))

bot_info_basic = 'OlivaDice By lunzhiPenxil Ver.%s' % bot_info_Ver

bot_info_basic_short = 'OlivaDice Ver.%s' % bot_info_Ver

bot_info = '%s [Python %s For OlivOS %s]' % (bot_info_basic, str(platform.python_version()), OlivOS.infoAPI.OlivOS_Version)

bot_version_short = 'OlivaDice %s' % bot_info_Ver

bot_version_short_header = 'OlivaDice/%s' % str(OlivaDiceCore_ver)

bot_summary = bot_info_basic + '\n'
bot_summary += 'Python ' + str(sys.version) + '\n'
bot_summary += str(platform.machine()) + '\n'
bot_summary += str(platform.processor()) + '\n'
bot_summary += str(os.name) + ':' + str(platform.platform())

bot_content = {
    'masterKey': str(uuid.uuid4())
}

dataDirRoot = './plugin/data/OlivaDice'

defaultOlivaDicePulseUrl = 'https://api.dice.center/dicestatusup/'
