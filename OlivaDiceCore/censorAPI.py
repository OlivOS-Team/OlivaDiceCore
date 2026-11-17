r"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   censorAPI.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2022-2026, OlivOS-Team
@Desc      :   None
"""

import OlivOS
import OlivaDiceCore

import os
import codecs
import copy
import time
import json
import traceback

gCensorDFA = {}

gCensorList = {}
gCensorConfigList = {}
gCensorInfoList = {}

gCensorConfigListUnitTemplate = {'censorList': []}


def formatUTF8WithBOM(data: bytes):
    res = data
    if res[:3] == codecs.BOM_UTF8:
        res = res[3:]
    return res


def readListFromFile(path):
    res = []
    try:
        with open(path, 'rb') as path_f:
            path_fs = formatUTF8WithBOM(path_f.read()).decode('utf-8')
            res = path_fs.replace('\r\n', '\n').split('\n')
    except Exception:
        res = []
    return res


def readConfigListByHash(bot_hash):
    res = copy.deepcopy(gCensorConfigListUnitTemplate)
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console')
    fileDir = OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console'
    fileName = 'censor.json'
    path = fileDir + '/' + fileName
    try:
        with open(path, 'rb') as path_f:
            path_fs = formatUTF8WithBOM(path_f.read()).decode('utf-8')
            res = json.loads(path_fs)
    except Exception:
        res = copy.deepcopy(gCensorConfigListUnitTemplate)
    gCensorConfigList[bot_hash] = res


def reloadConfigList(bot_hash):
    # 从 console/censor.json 重新读入，覆盖内存里还没落盘的修改。
    # 文件不存在按空表；文件在但读不出来就抛错，不改内存。
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console')
    path = OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console/censor.json'
    if not os.path.isfile(path):
        return setConfigList(bot_hash, [])
    try:
        with open(path, 'rb') as path_f:
            raw = json.loads(formatUTF8WithBOM(path_f.read()).decode('utf-8'))
    except Exception as error:
        raise ValueError('读取敏感词文件失败: %s' % error)
    if not isinstance(raw, dict) or not isinstance(raw.get('censorList'), list):
        raise ValueError('敏感词文件格式不正确')
    return setConfigList(bot_hash, raw.get('censorList'))


def writeConfigListByHash(bot_hash):
    res = copy.deepcopy(gCensorConfigListUnitTemplate)
    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console')
    fileDir = OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/console'
    fileName = 'censor.json'
    path = fileDir + '/' + fileName
    if bot_hash in gCensorConfigList:
        res = gCensorConfigList[bot_hash]
    try:
        with open(path, 'w', encoding='utf-8') as path_f:
            path_fs = json.dumps(res, ensure_ascii=False, indent=4)
            path_f.write(path_fs)
    except Exception:
        pass


def addConfigList(bot_hash, setWord):
    if (
        bot_hash in gCensorConfigList
        and 'censorList' in gCensorConfigList[bot_hash]
        and type(gCensorConfigList[bot_hash]['censorList']) is list
    ):
        if setWord not in gCensorConfigList[bot_hash]['censorList']:
            gCensorConfigList[bot_hash]['censorList'].append(setWord)


censorWordMaxLen = 64


def normalizeCensorWord(word):
    # 单条词条清洗:去首尾空白、压掉换行与制表符、限制长度。
    # 清洗后为空或超长的返回 None,由调用方跳过。
    if not isinstance(word, str):
        return None
    text = word.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    if text == '' or len(text) > censorWordMaxLen:
        return None
    return text


def normalizeCensorWordList(word_list):
    # 批量清洗并保序去重,供导入与全量写入共用。
    if not isinstance(word_list, (list, tuple)):
        return []
    res = []
    seen = set()
    for word_this in word_list:
        text = normalizeCensorWord(word_this)
        if text is None or text in seen:
            continue
        seen.add(text)
        res.append(text)
    return res


def summarizeCensorAdds(existing, raw_lines):
    # 按行判定要添加的敏感词。空行跳过，不计入总数。
    # 返回可写入的词，以及失败行和原因，供界面逐条反馈。
    if not isinstance(existing, (list, tuple)):
        existing = []
    if not isinstance(raw_lines, (list, tuple)):
        raw_lines = []
    seen = set(existing)
    batch = set()
    accepted = []
    failures = []
    total = 0
    for index, raw in enumerate(raw_lines, 1):
        if not isinstance(raw, str) or raw.strip() == '':
            continue
        total += 1
        word = normalizeCensorWord(raw)
        if word is None:
            failures.append({
                'line': index,
                'text': raw.strip()[:32],
                'reason': '无效或超过 64 字',
            })
            continue
        if word in seen:
            failures.append({'line': index, 'text': word, 'reason': '已存在'})
            continue
        if word in batch:
            failures.append({'line': index, 'text': word, 'reason': '本次重复'})
            continue
        batch.add(word)
        accepted.append(word)
    return {
        'total': total,
        'success': len(accepted),
        'failed': len(failures),
        'failures': failures,
        'accepted': accepted,
    }


def setConfigList(bot_hash, word_list):
    # 全量替换某个账号的自定义敏感词表,返回实际写入的列表。
    res = normalizeCensorWordList(word_list)
    if bot_hash not in gCensorConfigList or type(gCensorConfigList[bot_hash]) is not dict:
        gCensorConfigList[bot_hash] = copy.deepcopy(gCensorConfigListUnitTemplate)
    gCensorConfigList[bot_hash]['censorList'] = res
    writeConfigListByHash(bot_hash)
    return list(res)


def getCensorFileList(bot_hash):
    # 词库文件里的词(只读)。unity 是全局目录,其余按账号目录。
    res = []
    for word_this in gCensorList.get(bot_hash, []):
        text = normalizeCensorWord(word_this)
        if text is not None:
            res.append(text)
    return res


def censorFileDir(bot_hash):
    return OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/censor'


def listCensorFiles(bot_hash):
    # 只读列出文本库文件。目录没有就当空，不创建、不改写。
    directory = censorFileDir(bot_hash)
    if not os.path.isdir(directory):
        return []
    try:
        names = sorted(os.listdir(directory))
    except OSError as error:
        raise ValueError('读取文本库失败: %s' % error)
    files = []
    for name in names:
        path = directory + '/' + name
        if not os.path.isfile(path):
            continue
        lines = readListFromFile(path)
        files.append({
            'name': name,
            'lines': lines,
            'count': len([line for line in lines if str(line).strip()]),
        })
    return files


def reloadCensorFiles(bot_hash):
    # 把当前范围的文本库重新读进内存。不写文件。读目录失败则保持原内存。
    directory = censorFileDir(bot_hash)
    if not os.path.isdir(directory):
        gCensorList[bot_hash] = []
        return []
    files = listCensorFiles(bot_hash)
    words = []
    for item in files:
        words.extend(item['lines'])
    gCensorList[bot_hash] = words
    return files


def getCensorSnapshot(bot_hash):
    # 敏感词管理页的数据快照:可编辑的自定义词 + 只读文本库文件。
    return {
        'config': list(getConfigList(bot_hash)),
        'fromFiles': getCensorFileList(bot_hash),
        'files': listCensorFiles(bot_hash),
    }


def rebuildCensorByHash(bot_hash):
    # 词表变更后重建匹配器。unity 是全局词表,所有账号都要重建。
    if bot_hash == 'unity':
        for target_hash in list(gCensorInfoList.keys()):
            initCensorByHash(target_hash)
        return
    initCensorByHash(bot_hash)


def getConfigList(bot_hash):
    res = []
    if (
        bot_hash in gCensorConfigList
        and 'censorList' in gCensorConfigList[bot_hash]
        and type(gCensorConfigList[bot_hash]['censorList']) is list
    ):
        res = gCensorConfigList[bot_hash]['censorList']
    return res


def delConfigList(bot_hash, setWord):
    if (
        bot_hash in gCensorConfigList
        and 'censorList' in gCensorConfigList[bot_hash]
        and type(gCensorConfigList[bot_hash]['censorList']) is list
    ):
        gCensorConfigList[bot_hash]['censorList']
        if setWord in gCensorConfigList[bot_hash]['censorList']:
            gCensorConfigList[bot_hash]['censorList'].remove(setWord)


def initCensor(bot_info_dict):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    releaseDir(OlivaDiceCore.data.dataDirRoot)
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity')
    releaseDir(OlivaDiceCore.data.dataDirRoot + '/unity/censor')
    fileDir = OlivaDiceCore.data.dataDirRoot + '/unity/censor'
    fileList = os.listdir(fileDir)
    censorList_unity = []
    dictTValue['tName'] = '全局'
    readConfigListByHash('unity')
    writeConfigListByHash('unity')
    for fileList_this in fileList:
        fileName = fileList_this
        filePath = fileDir + '/' + fileName
        censorList_unity += readListFromFile(filePath)
        gCensorList['unity'] = censorList_unity
    for bot_hash in bot_info_dict:
        dictTValue['tName'] = bot_hash
        if bot_hash in bot_info_dict:
            dictTValue['tName'] = '%s|%s' % (
                bot_info_dict[bot_hash].platform['platform'],
                str(bot_info_dict[bot_hash].id),
            )
        gCensorInfoList[bot_hash] = dictTValue['tName']
        censorList_this = []
        releaseDir(OlivaDiceCore.data.dataDirRoot)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash)
        releaseDir(OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/censor')
        fileDir = OlivaDiceCore.data.dataDirRoot + '/' + bot_hash + '/censor'
        fileList = os.listdir(fileDir)
        readConfigListByHash(bot_hash)
        writeConfigListByHash(bot_hash)
        for fileList_this in fileList:
            fileName = fileList_this
            filePath = fileDir + '/' + fileName
            censorList_this += readListFromFile(filePath)
        gCensorList[bot_hash] = censorList_this
        initCensorByHash(bot_hash)


def initCensorByHash(bot_hash):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    dictTValue['tName'] = bot_hash
    if bot_hash in gCensorInfoList:
        dictTValue['tName'] = gCensorInfoList[bot_hash]

    censorList_this = []
    for bot_hash_this in ['unity', bot_hash]:
        if bot_hash_this in gCensorList:
            censorList_this += gCensorList[bot_hash_this]
    for bot_hash_this in ['unity', bot_hash]:
        censorList_this += getConfigList(bot_hash_this)

    time_start = time.perf_counter()
    gCensorDFA[bot_hash] = OlivaDiceCore.censorDFA.DFA(censorList_this)
    time_end = time.perf_counter()
    dictTValue['tInitDataCount'] = str(len(censorList_this))
    dictTValue['tInitDataTimeCost'] = '%.2fms' % ((time_end - time_start) * 1000)
    OlivaDiceCore.msgReply.globalLog(
        2,
        OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strInitCensor'], dictTValue),
        [('OlivaDice', 'default'), ('Init', 'default')],
    )


def patchCensorByHash(bot_hash, patchList: list):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    dictTValue['tName'] = bot_hash
    if bot_hash in gCensorInfoList:
        dictTValue['tName'] = gCensorInfoList[bot_hash]

    time_start = time.perf_counter()
    if bot_hash in gCensorDFA:
        gCensorDFA[bot_hash].loadl(patchList)
    time_end = time.perf_counter()

    dictTValue['tInitDataCount'] = str(len(patchList))
    dictTValue['tInitDataTimeCost'] = '%.2fms' % ((time_end - time_start) * 1000)
    OlivaDiceCore.msgReply.globalLog(
        2,
        OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strPatchCensor'], dictTValue),
        [('OlivaDice', 'default'), ('Init', 'default')],
    )


def doCensorReplace(botHash: str, msg: str, replaceMark: str = '*', mode: str = OlivaDiceCore.censorDFA.maxMatchType):
    res = msg
    if botHash in gCensorDFA:
        res: str = gCensorDFA[botHash].doReplace(inData=msg, replaceMark=replaceMark, mode=mode)
    return res


def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# 外部调用的直接接口
def doCensorReplaceOlivOSSafe(botHash: str, msg: str):
    dictStrConst = OlivaDiceCore.msgCustom.dictStrConst
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustom
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    if botHash in OlivaDiceCore.msgCustom.dictStrCustomDict:
        dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[botHash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    msg_para = OlivOS.messageAPI.Message_templet('old_string', msg)

    censorMode = OlivaDiceCore.console.getConsoleSwitchByHash('censorMode', botHash)
    censorMatchMode = OlivaDiceCore.console.getConsoleSwitchByHash('censorMatchMode', botHash)

    censorMatchModeFlag = OlivaDiceCore.censorDFA.minMatchType
    if censorMatchMode == 1:
        censorMatchModeFlag = OlivaDiceCore.censorDFA.maxMatchType
    elif censorMatchMode == 0:
        censorMatchModeFlag = OlivaDiceCore.censorDFA.minMatchType

    res = ''
    try:
        if censorMode == 1:
            for msg_para_this in msg_para.data:
                if type(msg_para_this) is OlivOS.messageAPI.PARA.text:
                    res += OlivaDiceCore.censorAPI.doCensorReplace(
                        botHash=botHash,
                        replaceMark=OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strCensorReplace'], dictTValue
                        ),
                        mode=censorMatchModeFlag,
                        msg=msg_para_this.CQ(),
                    )
                else:
                    res += msg_para_this.CQ()
        else:  # elif censorMode == 0:
            res = msg
    except Exception as e:
        dictTValue['tResult'] = '%s\n%s' % (str(e), traceback.format_exc())
        OlivaDiceCore.msgReply.globalLog(
            4,
            OlivaDiceCore.msgCustomManager.formatReplySTRConst(dictStrConst['strRunCensorError'], dictTValue),
            [('OlivaDice', 'default'), ('Censor', 'default')],
        )
        res = msg

    return res
