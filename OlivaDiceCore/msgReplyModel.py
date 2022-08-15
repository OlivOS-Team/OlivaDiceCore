# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReplyModel.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivaDiceCore
import OlivOS

def replyRR_command(plugin_event, Proc, valDict):
    tmp_reast_str = valDict['tmp_reast_str']
    flag_is_from_master = valDict['flag_is_from_master']
    tmp_userID = valDict['tmp_userID']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    replyMsg = OlivaDiceCore.msgReply.replyMsg

    tmp_reast_str = OlivaDiceCore.msgReply.getMatchWordStartRight(tmp_reast_str, 'rr')
    tmp_reast_str = OlivaDiceCore.msgReply.skipSpaceStart(tmp_reast_str)
    tmp_reast_str = tmp_reast_str.rstrip(' ')
    flag_mode = '默认'
    tmp_user_platform = plugin_event.platform['platform']
    if len(tmp_reast_str) > 0:
        if not flag_is_from_master and tmp_reast_str in ['debug']:
            pass
        else:
            flag_mode = tmp_reast_str
    tmp_RDData_str = OlivaDiceCore.onediceOverride.RDDataFormat(
        data = OlivaDiceCore.onediceOverride.getRDDataUser(
            botHash = plugin_event.bot_info.hash,
            userId = tmp_userID,
            platform = tmp_user_platform
        ),
        mode = flag_mode
    )
    tmp_reply_str = None
    if tmp_RDData_str != None:
        dictTValue['tRollFormatType'] = flag_mode
        dictTValue['tRollResult'] = '%s=%s=%d' % (
            OlivaDiceCore.onediceOverride.getRDDataRawUser(
                botHash = plugin_event.bot_info.hash,
                userId = tmp_userID,
                platform = tmp_user_platform
            ),
            tmp_RDData_str,
            OlivaDiceCore.onediceOverride.getRDDataIntUser(
                botHash = plugin_event.bot_info.hash,
                userId = tmp_userID,
                platform = tmp_user_platform
            )
        )
        tmp_reply_str = dictStrCustom['strRollRecord'].format(**dictTValue)
    if tmp_reply_str != None:
        replyMsg(plugin_event, tmp_reply_str)
