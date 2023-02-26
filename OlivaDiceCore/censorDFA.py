'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   censorDFA.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2022-2023, lunzhiPenxil
@Desc      :   一个基于DFA算法实现的高性能敏感词解析库
'''

import copy
import json

defautDFANode = {
    '_is_end': True
}

def loadListFromFile(path):
    res = []
    try:
        with open(path, 'r', encoding = 'utf-8') as fileObj:
            res = fileObj.read().replace('\r\n', '\n').split('\n')
    except:
        res = []
    return res

minMatchType = 'MIN'  # 最小匹配规则
maxMatchType = 'MAX'  # 最大匹配规则

class DFA(object):
    def __init__(self, textList:list):
        self.data = {}
        self._initDFAFromList(textList)

    def _initDFAFromList(self, textList:list):
        self.data = copy.deepcopy(defautDFANode)
        self.loadl(textList)
        return self.data

    def loadl(self, textList:list):
        for textThis in textList:
            res_this = self.data
            for textThis_i in textThis:
                if '_is_end' in res_this:
                    res_this.pop('_is_end')
                res_this.setdefault(textThis_i, copy.deepcopy(defautDFANode))
                res_this = res_this[textThis_i]
            res_this['_is_break'] = True
        return self.data

    def dumpf(self, path:str, indent = None):
        DFAObj = self.data
        with open(path, 'w', encoding = 'utf-8') as fileObj:
            fileObj.write(json.dumps(DFAObj, ensure_ascii = False, indent = indent))

    def dumps(self, indent = None):
        DFAObj = self.data
        return json.dumps(DFAObj, ensure_ascii = False, indent = indent)

    def _findByOffset(self, rawData:str, offset:int):
        res = []
        DFAData = self.data
        matchData = ''
        for i in range(offset, len(rawData)):
            flagIsBreak = False
            if DFAData.get('_is_break') is True:
                flagIsBreak = True
                res.append(matchData)
            if DFAData.get('_is_end') is True:
                if not flagIsBreak:
                    res.append(matchData)
                break
            if rawData[i] in DFAData:
                matchData += rawData[i]
                DFAData = DFAData[rawData[i]]
            else:
                break
        return res

    def find(self, rawData:str, mode = maxMatchType):
        res = []
        rawDataNew = rawData + '\0'
        for i in range(len(rawDataNew)):
            res_this = self._findByOffset(rawDataNew, i)
            for res_this_this in res_this:
                if res_this_this not in res and len(res_this_this) > 0:
                    res.append(res_this_this)
        flagReverse = mode == maxMatchType
        res.sort(
            key = lambda x: len(x),
            reverse = flagReverse
        )
        return res

    def doReplace(self, inData:str, replaceMark:str = '*', mode = maxMatchType):
        res = inData
        matchList = self.find(inData, mode)
        for matchList_this in matchList:
            res = res.replace(matchList_this, replaceMark * len(matchList_this))
        return res
