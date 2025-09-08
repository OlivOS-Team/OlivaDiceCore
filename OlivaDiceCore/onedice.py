# -*- encoding: utf-8 -*-
'''
   ____  _   ____________  ________________
  / __ \/ | / / ____/ __ \/  _/ ____/ ____/
 / / / /  |/ / __/ / / / // // /   / __/   
/ /_/ / /|  / /___/ /_/ // // /___/ /___   
\____/_/ |_/_____/_____/___/\____/_____/   

@File      :   main.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

from enum import Enum
import random
import traceback

pypi_version = '1.0.7'

dictOperationPriority = {
    '[' : None,
    ']' : None,
    ',' : None,
    '(' : None,
    ')' : None,
    '<' : 1,
    '>' : 1,
    '&' : 2,
    '|' : 2,
    '+' : 3,
    '-' : 3,
    '*' : 4,
    'x' : 4,
    'X' : 4,
    '/' : 4,
    '^' : 5,
    'sp' : 6,
    'SP' : 6,
    'kl' : 6,
    'KL' : 6,
    'kh' : 6,
    'KH' : 6,
    'dl' : 6,
    'DL' : 6,
    'dh' : 6,
    'DH' : 6,
    'min' : 6,
    'MIN' : 6,
    'max' : 6,
    'MAX' : 6,
    'lp' : 6,
    'LP' : 6,
    'tp' : 6,
    'TP' : 6,
    'df' : 7,
    'DF' : 7,
    'd' : 7,
    'D' : 7,
    'a' : 7,
    'A' : 7,
    'c' : 7,
    'C' : 7,
    'f' : 7,
    'F' : 7,
    'b' : 7,
    'B' : 7,
    'p' : 7,
    'P' : 7,
    '?' : 8,
    '$t' : 9,
    '$T' : 9
}

dictOperationMapping = {
    'df' : 'f'
}

dictRuleOperationPriority = {}

dictRuleOperationMapping = {}

listOperationSub = [
    'm',
    'M',
    'k',
    'K',
    'q',
    'Q',
    'b',
    'B',
    'p',
    'P',
    ':',
    '=',
    'i'
]

lenOperationMax = 3

'''
朴素栈实现
'''
class Stack(object):
    def __init__(self, initList = None):
        if initList == None:
            self.data = []
        else:
            self.data = initList

    def push(self, data):
        self.data.append(data)

    def pushList(self, data):
        self.data.extend(data)

    def pop(self):
        if self.data:
            return self.data.pop()

    def peek(self):
        if self.data:
            return self.data[-1]

    def is_empty(self):
        return not bool(self.data)

    def size(self):
        return len(self.data)

    def popTo(self, but):
        res = []
        while self.size() > 0 and self.peek() != but:
            res.append(self.pop())
        if self.size() > 0:
            self.pop()
        return res

'''
语法树栈实现，继承自朴素栈
'''
class calNodeStack(Stack):
    def popTo(self, but, priority = 0, saveBut = False):
        res = []
        while self.size() > 0 and self.peek().data != but:
            if self.peek().getPriority() != None:
                if self.peek().getPriority() < priority:
                    break
            res.append(self.pop())
        if self.size() > 0:
            if self.peek().data == but and not saveBut:
                self.pop()
        return res

'''
语法树节点结构体
'''
class calNode(object):
    def __init__(self):
        self.data = None
        self.type = None

    class nodeType(Enum):
        NUMBER = 0
        OPERATION = 1
        TUPLE = 2
        MAX = 3

    def __str__(self):
        return '<calNode \'%s\' %s>' % (self.data, self.type)

    def isNumber(self):
        if self.type == self.nodeType.NUMBER:
            return True
        else:
            return False

    def isOperation(self):
        if self.type == self.nodeType.OPERATION:
            return True
        else:
            return False

    def isTuple(self):
        if self.type == self.nodeType.TUPLE:
            return True
        else:
            return False

    def getPriority(self):
        return

    def inOperation(self):
        return

'''
语法树数字节点结构体
'''
class calNumberNode(calNode):
    def __init__(self, data):
        calNode.__init__(self)
        self.data = data
        self.type = self.nodeType.NUMBER
        self.num = 0

    def getInt(self):
        if self.data.isdigit():
            return int(self.data)
        else:
            return 0

    def appendInt(self, data):
        if str(data).isdigit():
            self.data += str(data)
        return calNumberNode(self.data)

'''
语法树多元组节点结构体
'''
class calTupleNode(calNode):
    def __init__(self, data):
        calNode.__init__(self)
        self.data = data
        self.type = self.nodeType.TUPLE
        self.num = 0

'''
语法树运算符节点结构体
'''
class calOperationNode(calNode):
    def __init__(
        self,
        data,
        customDefault = None,
        ruleMode = 'default'
    ):
        calNode.__init__(self)
        self.data = data.lower()
        self.type = self.nodeType.OPERATION
        self.vals = {}
        self.valsDefault = {}
        self.valLeftDefault = None
        self.valRightDefault = None
        self.valStarterLeftDefault = None
        self.valEnderRightDefault = None
        self.priority = None
        self.dictOperationPriority = dictOperationPriority
        self.dictRuleOperationPriority = dictRuleOperationPriority
        self.customDefault = customDefault
        self.ruleMode = ruleMode
        self.initOperation()

    def initOperation(self):
        if self.inOperation():
            self.getPriority()
        if self.data == '-':
            self.valStarterLeftDefault = 0
        elif self.data == 'd':
            self.valLeftDefault = 1
            self.valRightDefault = 100
            self.vals['k'] = None
            self.vals['q'] = None
            self.vals['p'] = None
            self.vals['b'] = None
            self.vals['a'] = None
            self.valsDefault['p'] = 1
            self.valsDefault['b'] = 1
        elif self.data == 'a':
            self.vals['k'] = 8
            self.vals['q'] = None
            self.vals['m'] = 10
        elif self.data == 'c':
            self.vals['m'] = 10
        elif self.data == 'b':
            self.valLeftDefault = 1
            self.valRightDefault = 1
        elif self.data == 'p':
            self.valLeftDefault = 1
            self.valRightDefault = 1
        elif self.data == 'f':
            self.valLeftDefault = 4
            self.valRightDefault = 3
        elif self.data == '?':
            self.valRightDefault = 0
            self.vals[':'] = None
        elif self.data == 's':
            self.valRightDefault = 1
        elif self.data == 'kh':
            self.valRightDefault = 1
        elif self.data == 'kl':
            self.valRightDefault = 1
        elif self.data == 'dh':
            self.valRightDefault = 1
        elif self.data == 'dl':
            self.valRightDefault = 1
        elif self.data == 'tp':
            self.valRightDefault = 0
        elif self.data == '$t':
            self.valLeftDefault = 1
            self.vals['='] = None
        if self.customDefault != None:
            if self.data in self.customDefault:
                if 'leftD' in self.customDefault[self.data]:
                    self.valLeftDefault = self.customDefault[self.data]['leftD']
                if 'rightD' in self.customDefault[self.data]:
                    self.valRightDefault = self.customDefault[self.data]['rightD']
                if 'sub' in self.customDefault[self.data]:
                    for val_this in self.vals:
                        if val_this in self.customDefault[self.data]['sub']:
                            self.vals[val_this] = self.customDefault[self.data]['sub'][val_this]
                if 'subD' in self.customDefault[self.data]:
                    for val_this in self.valsDefault:
                        if val_this in self.customDefault[self.data]['subD']:
                            self.valsDefault[val_this] = self.customDefault[self.data]['subD'][val_this]

    def getPriority(self):
        if self.data in self.dictOperationPriority:
            self.priority = self.dictOperationPriority[self.data]
        elif self.ruleMode in self.dictRuleOperationPriority \
        and self.data in self.dictRuleOperationPriority[self.ruleMode]:
            self.priority = self.dictRuleOperationPriority[self.ruleMode][self.data]
        return self.priority

    def inOperation(self):
        res = False
        if self.data in self.dictOperationPriority:
            res = True
        elif self.ruleMode in self.dictRuleOperationPriority \
        and self.data in self.dictRuleOperationPriority[self.ruleMode]:
            res = True
        return res

class RD(object):
    def __init__(
        self,
        initData,
        customDefault = None,
        valueTable = None,
        ruleMode = 'default'
    ):
        self.originDataRaw = initData
        self.originData = initData.lower()
        self.calTree = calNodeStack([])
        self.resInt = None
        self.resIntMin = None
        self.resIntMax = None
        self.resIntMinType = None
        self.resIntMaxType = None
        self.resDetail = None
        self.resDetailData = []
        self.resMetaTuple = []
        self.resMetaTupleEnable = False
        self.resError = None
        self.dictOperationPriority = dictOperationPriority
        self.dictRuleOperationPriority = dictRuleOperationPriority
        self.customDefault = customDefault
        self.valueTable = valueTable
        self.ruleMode = ruleMode

    def roll(self):
        try:
            if type(self.valueTable) == dict:
                self.__replace()
        except Exception as e:
            traceback.print_exc()
            if self.resError == None:
                self.resError = self.resErrorType.UNKNOWN_REPLACE_FATAL
        if self.resError != None:
            return
        try:
            self.__getCalTree()
        except Exception as e:
            traceback.print_exc()
            if self.resError == None:
                self.resError = self.resErrorType.UNKNOWN_GENERATE_FATAL
        if self.resError != None:
            return
        try:
            resRecursiveObj = self.__calculate()
        except Exception as e:
            traceback.print_exc()
            if self.resError == None:
                self.resError = self.resErrorType.UNKNOWN_COMPLETE_FATAL
        if self.resError != None:
            return
        else:
            self.resInt = resRecursiveObj.resInt
            self.resIntMin = resRecursiveObj.resIntMin
            self.resIntMax = resRecursiveObj.resIntMax
            self.resIntMinType = resRecursiveObj.resIntMinType
            self.resIntMaxType = resRecursiveObj.resIntMaxType
            self.resDetail = resRecursiveObj.resDetail
            self.resDetailData = resRecursiveObj.resDetailData
            self.resMetaTupleEnable = resRecursiveObj.resMetaTupleEnable
            if not self.resMetaTupleEnable:
                self.resMetaTupleEnable = self.check_metaTuple(resRecursiveObj.resMetaTuple)
            self.resMetaTuple = self.get_from_metaTuple(resRecursiveObj.resMetaTuple)
        return

    class resErrorType(Enum):
        UNKNOWN_GENERATE_FATAL = -1
        UNKNOWN_COMPLETE_FATAL = -2
        INPUT_RAW_INVALID = -3
        INPUT_CHILD_PARA_INVALID = -4
        INPUT_NODE_OPERATION_INVALID = -5
        NODE_OPERATION_INVALID = -6
        NODE_STACK_EMPTY = -7
        NODE_LEFT_VAL_INVALID = -8
        NODE_RIGHT_VAL_INVALID = -9
        NODE_SUB_VAL_INVALID = -10
        NODE_EXTREME_VAL_INVALID = -11
        UNKNOWN_REPLACE_FATAL = -12

    class resExtremeType(Enum):
        INT_LIMITED = 0
        INT_POSITIVE_INFINITE = 1
        INT_NEGATIVE_INFINITE = -1

    class resRecursive(object):
        def __init__(self, resInt = 0, resDetail = ''):
            self.resInt = resInt
            self.resIntMin = 0
            self.resIntMax = 0
            self.resIntMinType = RD.resExtremeType.INT_LIMITED
            self.resIntMaxType = RD.resExtremeType.INT_LIMITED
            self.resDetail = resDetail
            self.resDetailData = []
            self.resMetaTuple = []
            self.resMetaTupleEnable = False

    def getPriority(self, data):
        res = None
        if data in self.dictOperationPriority:
            res = self.dictOperationPriority[data]
        elif self.ruleMode in self.dictRuleOperationPriority \
        and data in self.dictRuleOperationPriority[self.ruleMode]:
            res = self.dictRuleOperationPriority[self.ruleMode][data]
        return res

    def inOperation(self, data):
        res = False
        if data in self.dictOperationPriority:
            res = True
        elif self.ruleMode in self.dictRuleOperationPriority \
        and data in self.dictRuleOperationPriority[self.ruleMode]:
            res = True
        return res

    '''
    该方法实现自定义随机数生成函数，可通过继承后重写来完成随机数算法的修改
    '''
    def random(self, nMin, nMax):
        return random.randint(nMin, nMax)

    '''
    该方法用状态机实现高宽容度的变量引用
    '''
    def __replace(self):
        raw = self.originData
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
                    if reg_key.upper() in self.valueTable:
                        reg_res += str(self.valueTable[reg_key.upper()])
                    else:
                        reg_res += '{%s}' % reg_key.upper()
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
            reg_res += '{%s' % reg_key.upper()
        res = reg_res
        self.originData = res
        return

    '''
    该方法实现基于表达式生成语法树
    '''
    def __getCalTree(self):
        tmp_data = self.originData
        tmp_res = calNodeStack()
        tmp_data_this = ''
        op_stack = calNodeStack()
        len_data = len(tmp_data)
        it_offset = 0
        flag_old_number = False
        flag_left_as_number = False
        count_child_para = 0
        while it_offset < len_data:
            flag_is_op_val = False
            tmp_offset = 1
            for lenOperation_this in reversed(range(1, 1 + lenOperationMax)):
                if it_offset + lenOperation_this > len(tmp_data):
                    continue
                tmp_data_this = tmp_data[it_offset:it_offset + lenOperation_this]
                tmp_op_peek_this = op_stack.peek()
                if lenOperation_this == 1 and tmp_op_peek_this != None:
                    if tmp_op_peek_this.getPriority() != None:
                        if tmp_data_this in tmp_op_peek_this.vals:
                            flag_is_op_val = True
                if lenOperation_this == 1 and tmp_data_this.isdigit():
                    tmp2_data_this = calNumberNode(tmp_data_this)
                    if flag_old_number:
                        tmp2_data_this = tmp_res.pop().appendInt(tmp_data_this)
                    tmp_res.push(tmp2_data_this)
                    flag_old_number = True
                    flag_left_as_number = True
                    tmp_offset = 1
                elif lenOperation_this == 1 and tmp_data_this == '[':
                    tmp_tuple_len = 2
                    tmp_tuple_deep = 1
                    tmp_tuple_para = ''
                    tmp_tuple_data = []
                    while it_offset + tmp_tuple_len <= len(tmp_data):
                        if tmp_data[it_offset + tmp_tuple_len - 1] == '[':
                            tmp_tuple_deep += 1
                            if tmp_tuple_deep > 1:
                                tmp_tuple_para += tmp_data[it_offset + tmp_tuple_len - 1]
                        elif tmp_data[it_offset + tmp_tuple_len - 1] == ']':
                            if tmp_tuple_deep > 1:
                                tmp_tuple_para += tmp_data[it_offset + tmp_tuple_len - 1]
                            elif tmp_tuple_deep == 1 and tmp_tuple_para != '':
                                tmp_tuple_data.append(tmp_tuple_para)
                                tmp_tuple_para = ''
                            tmp_tuple_deep -= 1
                            if tmp_tuple_deep == 0:
                                break
                        elif tmp_data[it_offset + tmp_tuple_len - 1] == ' ':
                            if tmp_tuple_deep > 1:
                                tmp_tuple_para += tmp_data[it_offset + tmp_tuple_len - 1]
                        elif tmp_data[it_offset + tmp_tuple_len - 1] == ',':
                            if tmp_tuple_deep > 1:
                                tmp_tuple_para += tmp_data[it_offset + tmp_tuple_len - 1]
                            elif tmp_tuple_deep == 1 and tmp_tuple_para != '':
                                tmp_tuple_data.append(tmp_tuple_para)
                                tmp_tuple_para = ''
                        else:
                            tmp_tuple_para += tmp_data[it_offset + tmp_tuple_len - 1]
                        tmp_tuple_len += 1
                    if tmp_tuple_deep != 0:
                        self.resError = self.resErrorType.INPUT_RAW_INVALID
                        break
                    tmp_res.push(calTupleNode(tmp_tuple_data))
                    flag_old_number = False
                    flag_left_as_number = True
                    tmp_offset = tmp_tuple_len
                elif lenOperation_this == 1 and flag_is_op_val and op_stack.size() > 0:
                    tmp_op_peek_this = op_stack.peek()
                    if tmp_op_peek_this != None:
                        if not flag_left_as_number:
                            if tmp_op_peek_this.valRightDefault != None:
                                tmp_res.push(calNumberNode(str(tmp_op_peek_this.valRightDefault)))
                                flag_left_as_number = True
                            else:
                                self.resError = self.resErrorType.INPUT_RAW_INVALID
                                break
                        if tmp_data_this in tmp_op_peek_this.vals:
                            if it_offset < len(tmp_data) - 1:
                                if tmp_data[it_offset + 1].isdigit():
                                    tmp_number_offset = 0
                                    tmp_number = None
                                    while True:
                                        tmp_number_offset += 1
                                        tmp_total_offset = it_offset + tmp_number_offset + 1
                                        if tmp_total_offset <= len(tmp_data):
                                            tmp_val_data_this = tmp_data[it_offset + 1 : tmp_total_offset]
                                        else:
                                            tmp_number_offset -= 1
                                            break
                                        if tmp_val_data_this.isdigit():
                                            tmp_number = int(tmp_val_data_this)
                                        else:
                                            tmp_number_offset -= 1
                                            break
                                    if tmp_number != None:
                                        op_stack.pop()
                                        tmp_op_peek_this.vals[tmp_data_this] = tmp_number
                                        op_stack.push(tmp_op_peek_this)
                                    else:
                                        self.resError = self.resErrorType.INPUT_RAW_INVALID
                                        break
                                    tmp_offset = 1 + tmp_number_offset
                                elif tmp_data[it_offset + 1] == '(':
                                    count_child_para_2 = 1
                                    tmp_number_offset = 0
                                    while count_child_para_2 > 0:
                                        tmp_number_offset += 1
                                        tmp_total_offset = it_offset + tmp_number_offset + 1
                                        if tmp_total_offset >= len(tmp_data):
                                            tmp_number_offset -= 1
                                            break
                                        if tmp_data[tmp_total_offset] == '(':
                                            count_child_para_2 += 1
                                        elif tmp_data[tmp_total_offset] == ')':
                                            count_child_para_2 -= 1
                                    if count_child_para_2 == 0:
                                        tmp_rd_child_para = RD(
                                            tmp_data[it_offset + 1 : it_offset + 1 + tmp_number_offset + 1],
                                            customDefault = self.customDefault,
                                            valueTable = self.valueTable
                                        )
                                        tmp_rd_child_para.roll()
                                        if tmp_rd_child_para.resError == None:
                                            op_stack.pop()
                                            tmp_op_peek_this.vals[tmp_data_this] = tmp_rd_child_para.resInt
                                            op_stack.push(tmp_op_peek_this)
                                        else:
                                            self.resError = tmp_rd_child_para.resError
                                            break
                                    else:
                                        self.resError = self.resErrorType.INPUT_RAW_INVALID
                                        break
                                    tmp_offset = 1 + tmp_number_offset + 1
                                elif tmp_data_this in tmp_op_peek_this.valsDefault:
                                    op_stack.pop()
                                    tmp_op_peek_this.vals[tmp_data_this] = tmp_op_peek_this.valsDefault[tmp_data_this]
                                    op_stack.push(tmp_op_peek_this)
                                else:
                                    self.resError = self.resErrorType.INPUT_RAW_INVALID
                                    break
                            elif tmp_data_this in tmp_op_peek_this.valsDefault:
                                op_stack.pop()
                                tmp_op_peek_this.vals[tmp_data_this] = tmp_op_peek_this.valsDefault[tmp_data_this]
                                op_stack.push(tmp_op_peek_this)
                            else:
                                self.resError = self.resErrorType.INPUT_RAW_INVALID
                                break
                        else:
                            self.resError = self.resErrorType.INPUT_RAW_INVALID
                            break
                    else:
                        self.resError = self.resErrorType.INPUT_RAW_INVALID
                        break
                elif self.inOperation(tmp_data_this):
                    if self.getPriority(tmp_data_this) != None:
                        tmp_op_peek_this = op_stack.peek()
                        tmp_data_this_real = tmp_data_this
                        if tmp_data_this.lower() in dictOperationMapping:
                            tmp_data_this_real = dictOperationMapping[tmp_data_this.lower()]
                        elif self.ruleMode in dictRuleOperationMapping \
                        and tmp_data_this.lower() in dictRuleOperationMapping[self.ruleMode]:
                            tmp_data_this_real = dictRuleOperationMapping[self.ruleMode][tmp_data_this.lower()]
                        tmp_calOperationNode_this = calOperationNode(
                            data = tmp_data_this_real,
                            customDefault = self.customDefault,
                            ruleMode = self.ruleMode
                        )
                        if not flag_left_as_number:
                            if tmp_op_peek_this == None:
                                if tmp_calOperationNode_this.valStarterLeftDefault != None:
                                    tmp_res.push(calNumberNode(str(tmp_calOperationNode_this.valStarterLeftDefault)))
                                    flag_left_as_number = True
                                elif tmp_calOperationNode_this.valLeftDefault != None:
                                    tmp_res.push(calNumberNode(str(tmp_calOperationNode_this.valLeftDefault)))
                                    flag_left_as_number = True
                                else:
                                    self.resError = self.resErrorType.INPUT_RAW_INVALID
                                    break
                            elif tmp_op_peek_this.data == '(':
                                if tmp_calOperationNode_this.valStarterLeftDefault != None:
                                    tmp_res.push(calNumberNode(str(tmp_calOperationNode_this.valStarterLeftDefault)))
                                    flag_left_as_number = True
                                elif tmp_calOperationNode_this.valLeftDefault != None:
                                    tmp_res.push(calNumberNode(str(tmp_calOperationNode_this.valLeftDefault)))
                                    flag_left_as_number = True
                                else:
                                    self.resError = self.resErrorType.INPUT_RAW_INVALID
                                    break
                            elif tmp_op_peek_this.getPriority() == None:
                                if tmp_calOperationNode_this.valLeftDefault != None:
                                    tmp_res.push(calNumberNode(str(tmp_calOperationNode_this.valLeftDefault)))
                                    flag_left_as_number = True
                                else:
                                    self.resError = self.resErrorType.INPUT_RAW_INVALID
                                    break
                            elif tmp_op_peek_this.valRightDefault != None:
                                tmp_res.push(calNumberNode(str(tmp_op_peek_this.valRightDefault)))
                                flag_left_as_number = True
                            elif tmp_calOperationNode_this.valLeftDefault != None:
                                tmp_res.push(calNumberNode(str(tmp_calOperationNode_this.valLeftDefault)))
                                flag_left_as_number = True
                            else:
                                self.resError = self.resErrorType.INPUT_RAW_INVALID
                                break
                        if tmp_op_peek_this != None:
                            if tmp_op_peek_this.getPriority() == None:
                                pass
                            elif self.getPriority(tmp_data_this_real) <= tmp_op_peek_this.getPriority():
                                tmp_res.pushList(op_stack.popTo('(', self.getPriority(tmp_data_this_real), True))
                        op_stack.push(calOperationNode(
                            data = tmp_data_this_real,
                            customDefault = self.customDefault,
                            ruleMode = self.ruleMode
                        ))
                        flag_old_number = False
                        flag_left_as_number = False
                        tmp_offset = lenOperation_this
                    elif tmp_data_this == '(':
                        op_stack.push(calOperationNode(
                            data = tmp_data_this,
                            customDefault = self.customDefault,
                            ruleMode = self.ruleMode
                        ))
                        count_child_para += 1
                        flag_old_number = False
                        flag_left_as_number = False
                        tmp_offset = 1
                    elif tmp_data_this == ')':
                        if not flag_left_as_number:
                            tmp_op_peek_this = op_stack.peek()
                            if tmp_op_peek_this != None:
                                if tmp_op_peek_this.valRightDefault != None:
                                    tmp_res.push(calNumberNode(str(tmp_op_peek_this.valRightDefault)))
                                    flag_left_as_number = True
                                else:
                                    self.resError = self.resErrorType.INPUT_RAW_INVALID
                                    break
                            else:
                                self.resError = self.resErrorType.INPUT_RAW_INVALID
                                break
                        tmp_res.pushList(op_stack.popTo('('))
                        count_child_para -= 1
                        flag_old_number = False
                        flag_left_as_number = True
                        tmp_offset = 1
                    elif lenOperation_this == 1:
                        self.resError = self.resErrorType.INPUT_NODE_OPERATION_INVALID
                    break
                elif lenOperation_this == 1:
                    self.resError = self.resErrorType.INPUT_RAW_INVALID
                    break
                if lenOperation_this == 1 and count_child_para < 0:
                    self.resError = self.resErrorType.INPUT_CHILD_PARA_INVALID
                    break
            if self.resError != None:
                return
            it_offset += tmp_offset
        if not flag_left_as_number:
            tmp_op_peek_this = op_stack.peek()
            if tmp_op_peek_this.valRightDefault != None:
                tmp_res.push(calNumberNode(str(tmp_op_peek_this.valRightDefault)))
                flag_left_as_number = True
            else:
                self.resError = self.resErrorType.INPUT_RAW_INVALID
                return
        while op_stack.size() > 0:
            tmp_res.pushList(op_stack.popTo('('))
        if count_child_para != 0:
            self.resError = self.resErrorType.INPUT_CHILD_PARA_INVALID
        self.calTree = tmp_res
        return

    '''
    该方法实现基于语法树完成递归计算
    '''
    def __calculate(self, rootPriority = 0, forkSideRight = True, rootData = None):
        resNoneTemplate = self.resRecursive()
        if self.calTree.size() <= 0:
            self.resError = self.resErrorType.NODE_STACK_EMPTY
            return resNoneTemplate
        if self.calTree.size() > 0:
            tmp_node_this = None
            tmp_node_this_output = 0
            tmp_node_this_output_Max = 0
            tmp_node_this_output_Min = 0
            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
            tmp_node_this_output_str = ''
            tmp_node_this_output_data = {}
            tmp_node_this_output_data_final = []
            tmp_node_this_output_meta_tuple = []
            tmp_node_this_output_meta_tuple_enable = False
            if self.calTree.peek().isNumber():
                tmp_node_this = self.calTree.pop()
                tmp_node_this_output = tmp_node_this.getInt()
                tmp_node_this_output_Max = tmp_node_this.getInt()
                tmp_node_this_output_Min = tmp_node_this.getInt()
                tmp_node_this_output_str = str(tmp_node_this_output)
                tmp_node_this_output_data_final = [tmp_node_this_output]
                tmp_node_this_output_meta_tuple = [tmp_node_this_output]
            elif self.calTree.peek().isTuple():
                tmp_node_this = self.calTree.pop()
                tmp_node_this_output = 0
                tmp_node_this_output_Max = 0
                tmp_node_this_output_Min = 0
                if len(tmp_node_this.data) > 0 and rootData not in ['kh', 'kl', 'lp']:
                    tmp_metaTuple_res = self.get_from_metaTuple(tmp_node_this.data)
                    if len(tmp_metaTuple_res) > 0:
                        tmp_node_this_output = tmp_metaTuple_res[-1]
                        tmp_node_this_output_Max = tmp_node_this_output
                        tmp_node_this_output_Min = tmp_node_this_output
                tmp_node_this_output_str = '[%s]' % ','.join([str(data_this) for data_this in tmp_node_this.data])
                tmp_node_this_output_data_final = [{'op': '[', 'v': tmp_node_this.data}]
                tmp_node_this_output_meta_tuple = tmp_node_this.data
                tmp_node_this_output_meta_tuple_enable = True
            elif self.calTree.peek().isOperation():
                tmp_node_this = self.calTree.pop()
                tmp_priority_this = tmp_node_this.getPriority()
                if tmp_priority_this == None:
                    tmp_priority_this = 0
                tmp_main_val_right_obj = self.__calculate(tmp_priority_this, True, tmp_node_this.data)
                if self.resError != None:
                    return resNoneTemplate
                tmp_main_val_left_obj = self.__calculate(tmp_priority_this, False, tmp_node_this.data)
                if self.resError != None:
                    return resNoneTemplate
                tmp_main_val_right = [tmp_main_val_right_obj.resInt, tmp_main_val_right_obj.resDetail]
                tmp_main_val_right_data = tmp_main_val_right_obj.resDetailData
                tmp_main_val_left = [tmp_main_val_left_obj.resInt, tmp_main_val_left_obj.resDetail]
                tmp_main_val_left_data = tmp_main_val_left_obj.resDetailData
                if tmp_node_this.data == '>':
                    if tmp_main_val_left[0] > tmp_main_val_right[0]:
                        tmp_node_this_output = 1
                    else:
                        tmp_node_this_output = 0
                    tmp_node_this_output_Min = 0
                    tmp_node_this_output_Max = 1
                    tmp_node_this_output_str = '%s>%s' % (
                        str(tmp_main_val_left[1]),
                        str(tmp_main_val_right[1])
                    )
                    tmp_node_this_output_data_final = tmp_main_val_left_data + [{'op': '>'}] + tmp_main_val_right_data
                    if tmp_priority_this < rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                elif tmp_node_this.data == '<':
                    if tmp_main_val_left[0] < tmp_main_val_right[0]:
                        tmp_node_this_output = 1
                    else:
                        tmp_node_this_output = 0
                    tmp_node_this_output_Min = 0
                    tmp_node_this_output_Max = 1
                    tmp_node_this_output_str = '%s<%s' % (
                        str(tmp_main_val_left[1]),
                        str(tmp_main_val_right[1])
                    )
                    tmp_node_this_output_data_final = tmp_main_val_left_data + [{'op': '<'}] + tmp_main_val_right_data
                    if tmp_priority_this < rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                elif tmp_node_this.data == '&':
                    tmp_node_this_output = tmp_main_val_left[0] & tmp_main_val_right[0]
                    tmp_node_this_output_Min = str(tmp_node_this_output)
                    tmp_node_this_output_Max = str(tmp_node_this_output)
                    tmp_node_this_output_str = '{%s&%s}[%s&%s](%s)' % (
                        tmp_main_val_left[1],
                        tmp_main_val_right[1],
                        tmp_main_val_left[0],
                        tmp_main_val_right[0],
                        str(tmp_node_this_output)
                    )
                    tmp_node_this_output_data_final = [{
                        'key': {
                            'op': '&',
                            'l': tmp_main_val_left[0],
                            'r': tmp_main_val_right[0],
                            'v': tmp_node_this.vals
                        },
                        'result': [
                            [tmp_main_val_left_data, tmp_main_val_right_data],
                            [tmp_main_val_left[0], tmp_main_val_right[0]],
                            [tmp_node_this_output]
                        ]
                    }]
                elif tmp_node_this.data == '|':
                    tmp_node_this_output = tmp_main_val_left[0] | tmp_main_val_right[0]
                    tmp_node_this_output_Min = str(tmp_node_this_output)
                    tmp_node_this_output_Max = str(tmp_node_this_output)
                    tmp_node_this_output_str = '{%s|%s}[%s|%s](%s)' % (
                        tmp_main_val_left[1],
                        tmp_main_val_right[1],
                        tmp_main_val_left[0],
                        tmp_main_val_right[0],
                        str(tmp_node_this_output)
                    )
                    tmp_node_this_output_data_final = [{
                        'key': {
                            'op': '|',
                            'l': tmp_main_val_left[0],
                            'r': tmp_main_val_right[0],
                            'v': tmp_node_this.vals
                        },
                        'result': [
                            [tmp_main_val_left_data, tmp_main_val_right_data],
                            [tmp_main_val_left[0], tmp_main_val_right[0]],
                            [tmp_node_this_output]
                        ]
                    }]
                elif tmp_node_this.data == '+':
                    tmp_node_this_output = tmp_main_val_left[0] + tmp_main_val_right[0]
                    if boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax + tmp_main_val_right_obj.resIntMax
                    elif boolByListOr([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                    else:
                        self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                        return resNoneTemplate
                    if boolByListAnd([
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_Min = tmp_main_val_left_obj.resIntMin + tmp_main_val_right_obj.resIntMin
                    elif boolByListOr([
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    else:
                        self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                        return resNoneTemplate
                    tmp_node_this_output_str = tmp_main_val_left[1] + '+' + tmp_main_val_right[1]
                    tmp_node_this_output_data_final = tmp_main_val_left_data + [{'op': '+'}] + tmp_main_val_right_data
                    if tmp_priority_this < rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    # 多元组处理
                    tmp_node_this_left_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_node_this_right_resMetaTuple_raw = tmp_main_val_right_obj.resMetaTuple
                    tmp_node_this_left_resMetaTuple = self.get_from_metaTuple(tmp_node_this_left_resMetaTuple_raw)
                    tmp_node_this_right_resMetaTuple = self.get_from_metaTuple(tmp_node_this_right_resMetaTuple_raw)
                    tmp_node_this_resMetaTuple = [tmp_node_this_output]
                    if len(tmp_node_this_left_resMetaTuple) > 1 and not len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(tmp_node_this_resMetaTuple_this + tmp_main_val_right[0]) for tmp_node_this_resMetaTuple_this in tmp_node_this_left_resMetaTuple]
                    elif not len(tmp_node_this_left_resMetaTuple) > 1 and len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(tmp_node_this_resMetaTuple_this + tmp_main_val_left[0]) for tmp_node_this_resMetaTuple_this in tmp_node_this_right_resMetaTuple]
                    tmp_node_this_output_meta_tuple = tmp_node_this_resMetaTuple
                elif tmp_node_this.data == '-':
                    tmp_node_this_output = tmp_main_val_left[0] - tmp_main_val_right[0]
                    if boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax - tmp_main_val_right_obj.resIntMin
                    elif boolByListOr([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                    else:
                        self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                        return resNoneTemplate
                    if boolByListAnd([
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_Min = tmp_main_val_left_obj.resIntMin - tmp_main_val_right_obj.resIntMax
                    elif boolByListOr([
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE
                    ]):
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    else:
                        self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                        return resNoneTemplate
                    tmp_node_this_output_str = tmp_main_val_left[1] + '-' + tmp_main_val_right[1]
                    tmp_node_this_output_data_final = tmp_main_val_left_data + [{'op': '-'}] + tmp_main_val_right_data
                    if tmp_priority_this < rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    # 多元组处理
                    tmp_node_this_left_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_node_this_right_resMetaTuple_raw = tmp_main_val_right_obj.resMetaTuple
                    tmp_node_this_left_resMetaTuple = self.get_from_metaTuple(tmp_node_this_left_resMetaTuple_raw)
                    tmp_node_this_right_resMetaTuple = self.get_from_metaTuple(tmp_node_this_right_resMetaTuple_raw)
                    tmp_node_this_resMetaTuple = [tmp_node_this_output]
                    if len(tmp_node_this_left_resMetaTuple) > 1 and not len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(tmp_node_this_resMetaTuple_this - tmp_main_val_right[0]) for tmp_node_this_resMetaTuple_this in tmp_node_this_left_resMetaTuple]
                    elif not len(tmp_node_this_left_resMetaTuple) > 1 and len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(tmp_node_this_resMetaTuple_this - tmp_main_val_left[0]) for tmp_node_this_resMetaTuple_this in tmp_node_this_right_resMetaTuple]
                    tmp_node_this_output_meta_tuple = tmp_node_this_resMetaTuple
                elif tmp_node_this.data == '*' or tmp_node_this.data == 'x':
                    tmp_node_this_output = tmp_main_val_left[0] * tmp_main_val_right[0]
                    tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_Extremum_1 = 0
                    tmp_node_this_output_Extremum_2 = 0
                    tmp_node_this_output_Extremum_3 = 0
                    tmp_node_this_output_Extremum_4 = 0
                    ##############################################
                    if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                        if tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                            tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_POSITIVE_INFINITE
                        elif tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                            if tmp_main_val_right_obj.resIntMax > 0:
                                tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_POSITIVE_INFINITE
                            elif tmp_main_val_right_obj.resIntMax < 0:
                                tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_1 = 0
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                        if tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE:
                            tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                            if tmp_main_val_right_obj.resIntMax > 0:
                                tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_POSITIVE_INFINITE
                            elif tmp_main_val_right_obj.resIntMax < 0:
                                tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_2 = 0
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                    elif tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                        if tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                            if tmp_main_val_left_obj.resIntMin > 0:
                                tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_POSITIVE_INFINITE
                            elif tmp_main_val_left_obj.resIntMin < 0:
                                tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_1 = 0
                        elif tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                            tmp_node_this_output_ExtremumType_1 = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Extremum_1 = tmp_main_val_left_obj.resIntMax * tmp_main_val_right_obj.resIntMax
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                        if tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE:
                            if tmp_main_val_left_obj.resIntMin > 0:
                                tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            elif tmp_main_val_left_obj.resIntMin < 0:
                                tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_POSITIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_2 = 0
                        elif tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                            tmp_node_this_output_ExtremumType_2 = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Extremum_2 = tmp_main_val_left_obj.resIntMax * tmp_main_val_right_obj.resIntMin
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                    else:
                        self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                        return resNoneTemplate
                    ##############################################
                    if tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE:
                        if tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                            tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                            if tmp_main_val_right_obj.resIntMax > 0:
                                tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            elif tmp_main_val_right_obj.resIntMax < 0:
                                tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_POSITIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_3 = 0
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                        if tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE:
                            tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_POSITIVE_INFINITE
                        elif tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                            if tmp_main_val_right_obj.resIntMin > 0:
                                tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            elif tmp_main_val_right_obj.resIntMin < 0:
                                tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_POSITIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_4 = 0
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                    elif tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                        if tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                            if tmp_main_val_left_obj.resIntMin > 0:
                                tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_POSITIVE_INFINITE
                            elif tmp_main_val_left_obj.resIntMin < 0:
                                tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_3 = 0
                        elif tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                            tmp_node_this_output_ExtremumType_3 = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Extremum_3 = tmp_main_val_left_obj.resIntMin * tmp_main_val_right_obj.resIntMax
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                        if tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE:
                            if tmp_main_val_left_obj.resIntMin > 0:
                                tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_NEGATIVE_INFINITE
                            elif tmp_main_val_left_obj.resIntMin < 0:
                                tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_POSITIVE_INFINITE
                            else:
                                tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Extremum_4 = 0
                        elif tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                            tmp_node_this_output_ExtremumType_4 = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Extremum_4 = tmp_main_val_left_obj.resIntMin * tmp_main_val_right_obj.resIntMin
                        else:
                            self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                            return resNoneTemplate
                    ##############################################
                    else:
                        self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                        return resNoneTemplate
                    ##############################################
                    if boolByListOr([
                        tmp_node_this_output_ExtremumType_1 == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_node_this_output_ExtremumType_2 == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_node_this_output_ExtremumType_3 == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_node_this_output_ExtremumType_4 == self.resExtremeType.INT_POSITIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                    else:
                        flag_is_INT_LIMITED = False
                        tmp_Extremum = 0
                        if tmp_node_this_output_ExtremumType_1 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_1 > tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_1
                            flag_is_INT_LIMITED = True
                        if tmp_node_this_output_ExtremumType_2 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_2 > tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_2
                            flag_is_INT_LIMITED = True
                        if tmp_node_this_output_ExtremumType_3 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_3 > tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_3
                            flag_is_INT_LIMITED = True
                        if tmp_node_this_output_ExtremumType_4 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_4 > tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_4
                            flag_is_INT_LIMITED = True
                        if flag_is_INT_LIMITED:
                            tmp_node_this_output_Max = tmp_Extremum
                    if boolByListOr([
                        tmp_node_this_output_ExtremumType_1 == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_node_this_output_ExtremumType_2 == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_node_this_output_ExtremumType_3 == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_node_this_output_ExtremumType_4 == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    else:
                        flag_is_INT_LIMITED = False
                        tmp_Extremum = 0
                        if tmp_node_this_output_ExtremumType_1 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_1 < tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_1
                            flag_is_INT_LIMITED = True
                        if tmp_node_this_output_ExtremumType_2 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_2 < tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_2
                            flag_is_INT_LIMITED = True
                        if tmp_node_this_output_ExtremumType_3 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_3 < tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_3
                            flag_is_INT_LIMITED = True
                        if tmp_node_this_output_ExtremumType_4 == self.resExtremeType.INT_LIMITED:
                            if not flag_is_INT_LIMITED or tmp_node_this_output_Extremum_4 < tmp_Extremum:
                                tmp_Extremum = tmp_node_this_output_Extremum_4
                            flag_is_INT_LIMITED = True
                        if flag_is_INT_LIMITED:
                            tmp_node_this_output_Min = tmp_Extremum
                    tmp_node_this_output_str = tmp_main_val_left[1] + '*' + tmp_main_val_right[1]
                    tmp_node_this_output_data_final = tmp_main_val_left_data + [{'op': '*'}] + tmp_main_val_right_data
                    if tmp_priority_this < rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    elif forkSideRight and tmp_priority_this == rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    # 多元组处理
                    tmp_node_this_left_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_node_this_right_resMetaTuple_raw = tmp_main_val_right_obj.resMetaTuple
                    tmp_node_this_left_resMetaTuple = self.get_from_metaTuple(tmp_node_this_left_resMetaTuple_raw)
                    tmp_node_this_right_resMetaTuple = self.get_from_metaTuple(tmp_node_this_right_resMetaTuple_raw)
                    tmp_node_this_resMetaTuple = [tmp_node_this_output]
                    if len(tmp_node_this_left_resMetaTuple) > 1 and not len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(tmp_node_this_resMetaTuple_this * tmp_main_val_right[0]) for tmp_node_this_resMetaTuple_this in tmp_node_this_left_resMetaTuple]
                    elif not len(tmp_node_this_left_resMetaTuple) > 1 and len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(tmp_node_this_resMetaTuple_this * tmp_main_val_left[0]) for tmp_node_this_resMetaTuple_this in tmp_node_this_right_resMetaTuple]
                    tmp_node_this_output_meta_tuple = tmp_node_this_resMetaTuple
                elif tmp_node_this.data == '/':
                    if tmp_main_val_right[0] == 0:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    tmp_node_this_output = int(tmp_main_val_left[0] / tmp_main_val_right[0])
                    ##############################################
                    if boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        if tmp_main_val_right_obj.resIntMin > 0:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = min(
                                int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMin),
                                0
                            )
                        elif boolByListAnd([
                            tmp_main_val_right_obj.resIntMin == 0,
                            tmp_main_val_left_obj.resIntMin >= 0
                        ]):
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        else:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        if tmp_main_val_right_obj.resIntMin > 0:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = max(
                                int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMin),
                                0
                            )
                        elif boolByListAnd([
                            tmp_main_val_right_obj.resIntMin == 0,
                            tmp_main_val_left_obj.resIntMax <= 0
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 0
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        if tmp_main_val_right_obj.resIntMin > 0:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = max(
                                int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMin),
                                0
                            )
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = min(
                                int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMin),
                                0
                            )
                        if tmp_main_val_right_obj.resIntMin == 0:
                            if tmp_main_val_left_obj.resIntMax <= 0:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            if tmp_main_val_left_obj.resIntMin >= 0:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        if tmp_main_val_right_obj.resIntMax < 0:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = max(
                                int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMax),
                                0
                            )
                        elif boolByListAnd([
                            tmp_main_val_right_obj.resIntMax == 0,
                            tmp_main_val_left_obj.resIntMin >= 0
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 0
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        if tmp_main_val_right_obj.resIntMax < 0:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = min(
                                int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMax),
                                0
                            )
                        elif boolByListAnd([
                            tmp_main_val_right_obj.resIntMax == 0,
                            tmp_main_val_left_obj.resIntMax <= 0
                        ]):
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        else:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        if tmp_main_val_right_obj.resIntMax < 0:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = max(
                                int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMax),
                                0
                            )
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = min(
                                int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMax),
                                0
                            )
                        if tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_left_obj.resIntMax <= 0:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                            if tmp_main_val_left_obj.resIntMin >= 0:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        if tmp_main_val_right_obj.resIntMin > 0:
                            if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = max(
                                    int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMin),
                                    int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMax)
                                )
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            if tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = min(
                                    int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMin),
                                    int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMax)
                                )
                            else:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif tmp_main_val_right_obj.resIntMin == 0:
                            if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                                if tmp_main_val_left_obj.resIntMax > 0:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                else:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Max = int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMax)
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            if tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                                if tmp_main_val_left_obj.resIntMin < 0:
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                                else:
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Min = int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMax)
                            else:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif tmp_main_val_right_obj.resIntMax < 0:
                            if tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = max(
                                    int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMax),
                                    int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMin)
                                )
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = min(
                                    int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMax),
                                    int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMin)
                                )
                            else:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED:
                                if tmp_main_val_left_obj.resIntMin < 0:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                else:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Max = int(tmp_main_val_left_obj.resIntMin / tmp_main_val_right_obj.resIntMin)
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                                if tmp_main_val_left_obj.resIntMax > 0:
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                                else:
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Min = int(tmp_main_val_left_obj.resIntMax / tmp_main_val_right_obj.resIntMin)
                            else:
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    else:
                        self.resError = self.resErrorType.NODE_EXTREME_VAL_INVALID
                        return resNoneTemplate
                    ##############################################
                    tmp_node_this_output_str = tmp_main_val_left[1] + '/' + tmp_main_val_right[1]
                    tmp_node_this_output_data_final = tmp_main_val_left_data + [{'op': '/'}] + tmp_main_val_right_data
                    if tmp_priority_this < rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    elif forkSideRight and tmp_priority_this == rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    # 多元组处理
                    tmp_node_this_left_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_node_this_right_resMetaTuple_raw = tmp_main_val_right_obj.resMetaTuple
                    tmp_node_this_left_resMetaTuple = self.get_from_metaTuple(tmp_node_this_left_resMetaTuple_raw)
                    tmp_node_this_right_resMetaTuple = self.get_from_metaTuple(tmp_node_this_right_resMetaTuple_raw)
                    tmp_node_this_resMetaTuple = [tmp_node_this_output]
                    if len(tmp_node_this_left_resMetaTuple) > 1 and not len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(int(tmp_node_this_resMetaTuple_this / tmp_main_val_right[0])) for tmp_node_this_resMetaTuple_this in tmp_node_this_left_resMetaTuple]
                    elif not len(tmp_node_this_left_resMetaTuple) > 1 and len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(int(tmp_main_val_left[0] / tmp_node_this_resMetaTuple_this)) for tmp_node_this_resMetaTuple_this in tmp_node_this_right_resMetaTuple]
                    tmp_node_this_output_meta_tuple = tmp_node_this_resMetaTuple
                elif tmp_node_this.data == '^':
                    if tmp_main_val_left[0] == 0 and tmp_main_val_right[0] == 0:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left[0] > 10000:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_right[0] > 10000:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    tmp_node_this_output = int(tmp_main_val_left[0] ** tmp_main_val_right[0])
                    if boolByListAnd([
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        if tmp_main_val_left_obj.resIntMin < -1:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif tmp_main_val_left_obj.resIntMin == -1:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        elif tmp_main_val_left_obj.resIntMin == 0:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        else:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 1
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        if tmp_main_val_left_obj.resIntMax < -1:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == -1,
                            tmp_main_val_left_obj.resIntMin < -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == -1,
                            tmp_main_val_left_obj.resIntMin == -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 0,
                            tmp_main_val_left_obj.resIntMin < -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 0,
                            tmp_main_val_left_obj.resIntMin == -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 0,
                            tmp_main_val_left_obj.resIntMin == 0
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 0
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 1,
                            tmp_main_val_left_obj.resIntMin < -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 1,
                            tmp_main_val_left_obj.resIntMin == -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 1,
                            tmp_main_val_left_obj.resIntMin == 0
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 1,
                            tmp_main_val_left_obj.resIntMin == 1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 1
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax > 1,
                            tmp_main_val_left_obj.resIntMin < -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax > 1,
                            tmp_main_val_left_obj.resIntMin == -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        if tmp_main_val_right_obj.resIntMax <= 0:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        if tmp_main_val_right_obj.resIntMax < 0:
                            if tmp_main_val_left_obj.resIntMax < -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                        elif tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_left_obj.resIntMax < -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        if tmp_main_val_right_obj.resIntMax < 0:
                            if tmp_main_val_left_obj.resIntMin > 1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif tmp_main_val_left_obj.resIntMin >= 0:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                        elif tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_left_obj.resIntMin >= 0:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE
                    ]):
                        if tmp_main_val_right_obj.resIntMax < 0:
                            if tmp_main_val_left_obj.resIntMax < -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif tmp_main_val_left_obj.resIntMax == -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 0,
                                tmp_main_val_left_obj.resIntMin <= -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 0,
                                tmp_main_val_left_obj.resIntMin == 0
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 1,
                                tmp_main_val_left_obj.resIntMin <= -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 1,
                                tmp_main_val_left_obj.resIntMin > -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax > 1,
                                tmp_main_val_left_obj.resIntMin <= -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                        elif tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_left_obj.resIntMax < -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif tmp_main_val_left_obj.resIntMax == -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 0,
                                tmp_main_val_left_obj.resIntMin <= -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 0,
                                tmp_main_val_left_obj.resIntMin == 0
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 1,
                                tmp_main_val_left_obj.resIntMin <= -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax == 1,
                                tmp_main_val_left_obj.resIntMin > -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif boolByListAnd([
                                tmp_main_val_left_obj.resIntMax > 1,
                                tmp_main_val_left_obj.resIntMin <= -1
                            ]):
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        if tmp_main_val_left_obj.resIntMin > 0:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        elif tmp_main_val_left_obj.resIntMin == -1:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        else:
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        if tmp_main_val_left_obj.resIntMax < -1:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif tmp_main_val_left_obj.resIntMin < -1:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax <= 0,
                            tmp_main_val_left_obj.resIntMin == -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 0,
                            tmp_main_val_left_obj.resIntMin == 0
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 0
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 1,
                            tmp_main_val_left_obj.resIntMin <= -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax == 1,
                            tmp_main_val_left_obj.resIntMin > -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 1
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        elif boolByListAnd([
                            tmp_main_val_left_obj.resIntMax > 1,
                            tmp_main_val_left_obj.resIntMin <= -1
                        ]):
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        else:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            if tmp_main_val_left_obj.resIntMin == 0:
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_Min = int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMin)
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        if tmp_main_val_right_obj.resIntMax < 0:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 0
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = -1
                        elif tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_right_obj.resIntMin != tmp_main_val_right_obj.resIntMax:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 1
                        else:
                            if tmp_main_val_right_obj.resIntMin != tmp_main_val_right_obj.resIntMax:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                            else:
                                if tmp_main_val_right_obj.resIntMax % 2 == 0:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Min = 0
                                else:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        if tmp_main_val_right_obj.resIntMax < -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                        elif tmp_main_val_right_obj.resIntMax == -1:
                            if tmp_main_val_left_obj.resIntMax < -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                        elif tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_right_obj.resIntMin != tmp_main_val_right_obj.resIntMax:
                                if tmp_main_val_left_obj.resIntMax < -1:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Max = 1
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Min = 0
                                else:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Max = 1
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Min = -1
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 1
                        else:
                            if tmp_main_val_right_obj.resIntMin != tmp_main_val_right_obj.resIntMax:
                                if tmp_main_val_right_obj.resIntMax == 1:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Max = max(
                                        int(tmp_main_val_left_obj.resIntMax ** tmp_main_val_right_obj.resIntMax),
                                        0
                                    )
                                else:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                            else:
                                if tmp_main_val_right_obj.resIntMax % 2 == 0:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Min = 0
                                else:
                                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                    tmp_node_this_output_Max = max(
                                        int(tmp_main_val_left_obj.resIntMax ** tmp_main_val_right_obj.resIntMax),
                                        0
                                    )
                                    tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        if tmp_main_val_right_obj.resIntMax < -1:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Max = 0
                            tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                            tmp_node_this_output_Min = 0
                        if tmp_main_val_right_obj.resIntMax == -1:
                            if tmp_main_val_left_obj.resIntMin > 1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            elif tmp_main_val_left_obj.resIntMin > -1:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                        elif tmp_main_val_right_obj.resIntMax == 0:
                            if tmp_main_val_right_obj.resIntMin != tmp_main_val_right_obj.resIntMax:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = -1
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 1
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 1
                        else:
                            if tmp_main_val_right_obj.resIntMin != tmp_main_val_right_obj.resIntMax:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_min_val_list_1 = []
                                if tmp_main_val_left_obj.resIntMin <= 1:
                                    tmp_min_val_list_1.append(1)
                                if tmp_main_val_left_obj.resIntMin <= 0:
                                    tmp_min_val_list_1.append(0)
                                if tmp_main_val_left_obj.resIntMin <= -1:
                                    tmp_min_val_list_1.append(-1)
                                tmp_min_val_list_1.append(
                                    int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMax)
                                )
                                tmp_min_val_list_1.append(
                                    int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMin)
                                )
                                if tmp_main_val_right_obj.resIntMax > 1:
                                    tmp_min_val_list_1.append(
                                        int(tmp_main_val_left_obj.resIntMin ** (tmp_main_val_right_obj.resIntMax - 1))
                                    )
                                tmp_node_this_output_Min = min(tmp_min_val_list_1)
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_min_val_list_1 = []
                                if tmp_main_val_left_obj.resIntMin <= 1:
                                    tmp_min_val_list_1.append(1)
                                if tmp_main_val_left_obj.resIntMin <= 0:
                                    tmp_min_val_list_1.append(0)
                                if tmp_main_val_left_obj.resIntMin <= -1:
                                    tmp_min_val_list_1.append(-1)
                                tmp_min_val_list_1.append(
                                    int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMin)
                                )
                                tmp_node_this_output_Min = min(tmp_min_val_list_1)
                    elif boolByListAnd([
                        tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_left_obj.resIntMinType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_LIMITED,
                        tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_LIMITED
                    ]):
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                        tmp_node_this_output_Max = 0
                        tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                        tmp_node_this_output_Min = 0
                        tmp_max_val_list_1 = []
                        tmp_min_val_list_1 = []
                        tmp_max_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMax ** tmp_main_val_right_obj.resIntMax)
                        )
                        tmp_min_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMax ** tmp_main_val_right_obj.resIntMax)
                        )
                        tmp_max_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMax ** tmp_main_val_right_obj.resIntMin)
                        )
                        tmp_min_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMax ** tmp_main_val_right_obj.resIntMin)
                        )
                        tmp_max_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMax)
                        )
                        tmp_min_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMax)
                        )
                        tmp_max_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMin)
                        )
                        tmp_min_val_list_1.append(
                            int(tmp_main_val_left_obj.resIntMin ** tmp_main_val_right_obj.resIntMin)
                        )
                        if tmp_main_val_right_obj.resIntMin != tmp_main_val_right_obj.resIntMax:
                            tmp_max_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMax ** (tmp_main_val_right_obj.resIntMax - 1))
                            )
                            tmp_min_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMax ** (tmp_main_val_right_obj.resIntMax - 1))
                            )
                            tmp_max_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMax ** (tmp_main_val_right_obj.resIntMin + 1))
                            )
                            tmp_min_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMax ** (tmp_main_val_right_obj.resIntMin + 1))
                            )
                            tmp_max_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMin ** (tmp_main_val_right_obj.resIntMax - 1))
                            )
                            tmp_min_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMin ** (tmp_main_val_right_obj.resIntMax - 1))
                            )
                            tmp_max_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMin ** (tmp_main_val_right_obj.resIntMin + 1))
                            )
                            tmp_min_val_list_1.append(
                                int(tmp_main_val_left_obj.resIntMin ** (tmp_main_val_right_obj.resIntMin + 1))
                            )
                        if boolByListAnd([
                            tmp_main_val_right_obj.resIntMax >= 0,
                            tmp_main_val_right_obj.resIntMin <= 0,
                            boolByListOr([
                                tmp_main_val_left_obj.resIntMax != 0,
                                tmp_main_val_left_obj.resIntMin != 0
                            ])
                        ]):
                            tmp_max_val_list_1.append(1)
                            tmp_min_val_list_1.append(1)
                        if boolByListAnd([
                            tmp_main_val_left_obj.resIntMax >= -1,
                            tmp_main_val_left_obj.resIntMin <= -1,
                            boolByListOr([
                                tmp_main_val_right_obj.resIntMax != 0,
                                tmp_main_val_right_obj.resIntMin != 0
                            ])
                        ]):
                            tmp_max_val_list_1.append(-1)
                            tmp_min_val_list_1.append(-1)
                        if boolByListAnd([
                            tmp_main_val_left_obj.resIntMax >= 0,
                            tmp_main_val_left_obj.resIntMin <= 0,
                            boolByListOr([
                                tmp_main_val_right_obj.resIntMax != 0,
                                tmp_main_val_right_obj.resIntMin != 0
                            ])
                        ]):
                            tmp_max_val_list_1.append(0)
                            tmp_min_val_list_1.append(0)
                        if boolByListAnd([
                            tmp_main_val_left_obj.resIntMax >= 1,
                            tmp_main_val_left_obj.resIntMin <= 1,
                            boolByListOr([
                                tmp_main_val_right_obj.resIntMax != 0,
                                tmp_main_val_right_obj.resIntMin != 0
                            ])
                        ]):
                            tmp_max_val_list_1.append(1)
                            tmp_min_val_list_1.append(1)
                        tmp_node_this_output_Max = max(tmp_max_val_list_1)
                        tmp_node_this_output_Min = min(tmp_min_val_list_1)
                    tmp_node_this_output_str = tmp_main_val_left[1] + '^' + tmp_main_val_right[1]
                    tmp_node_this_output_data_final = tmp_main_val_left_data + [{'op': '^'}] + tmp_main_val_right_data
                    if tmp_priority_this < rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    elif forkSideRight and tmp_priority_this == rootPriority:
                        tmp_node_this_output_str = '(' + tmp_node_this_output_str + ')'
                        tmp_node_this_output_data_final = [{'op': '('}] + tmp_node_this_output_data_final + [{'op': ')'}]
                    # 多元组处理
                    tmp_node_this_left_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_node_this_right_resMetaTuple_raw = tmp_main_val_right_obj.resMetaTuple
                    tmp_node_this_left_resMetaTuple = self.get_from_metaTuple(tmp_node_this_left_resMetaTuple_raw)
                    tmp_node_this_right_resMetaTuple = self.get_from_metaTuple(tmp_node_this_right_resMetaTuple_raw)
                    tmp_node_this_resMetaTuple = [tmp_node_this_output]
                    if len(tmp_node_this_left_resMetaTuple) > 1 and not len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(int(tmp_node_this_resMetaTuple_this ** tmp_main_val_right[0])) for tmp_node_this_resMetaTuple_this in tmp_node_this_left_resMetaTuple]
                    elif not len(tmp_node_this_left_resMetaTuple) > 1 and len(tmp_node_this_right_resMetaTuple) > 1:
                        tmp_node_this_resMetaTuple = [(int(tmp_main_val_left[0] ** tmp_node_this_resMetaTuple_this)) for tmp_node_this_resMetaTuple_this in tmp_node_this_right_resMetaTuple]
                    tmp_node_this_output_meta_tuple = tmp_node_this_resMetaTuple
                elif tmp_node_this.data == 'd':
                    if tmp_main_val_right[0] <= 0 or tmp_main_val_right[0] > 10000:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left[0] <= 0 or tmp_main_val_left[0] > 10000:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    tmp_range_list = range(0, tmp_main_val_left[0])
                    tmp_node_this_output = 0
                    tmp_node_this_output_this = 0
                    tmp_node_this_output_list = []
                    tmp_node_this_output_list_2 = []
                    tmp_node_this_output_str = ''
                    tmp_node_this_output_str_1 = ''
                    tmp_node_this_output_str_2 = ''
                    tmp_node_this_output_str_3 = ''
                    tmp_node_this_output_data = {}
                    tmp_node_this_output_data_1 = []
                    tmp_node_this_output_data_2 = []
                    tmp_node_this_output_data_3 = []
                    tmp_node_this_output_data_final = []
                    if tmp_node_this.vals['a'] != None:
                        tmp_RD = RD('%sa(%s+1)k%sm%s' % (
                                str(tmp_main_val_left[0]),
                                str(tmp_main_val_right[0]),
                                str(tmp_node_this.vals['a']),
                                str(tmp_main_val_right[0])
                            ),
                            self.customDefault
                        )
                        tmp_RD.roll()
                        if tmp_RD.resError != None:
                            return tmp_RD.resError
                        else:
                            resRecursiveObj = self.resRecursive()
                            resRecursiveObj.resInt = tmp_RD.resInt
                            resRecursiveObj.resIntMax = tmp_RD.resIntMax
                            resRecursiveObj.resIntMin = tmp_RD.resIntMin
                            resRecursiveObj.resIntMaxType = tmp_RD.resIntMaxType
                            resRecursiveObj.resIntMinType = tmp_RD.resIntMinType
                            resRecursiveObj.resDetail = tmp_RD.resDetail
                            return resRecursiveObj
                    if tmp_node_this.vals['k'] != None and tmp_node_this.vals['q'] != None:
                        self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                        return resNoneTemplate
                    if tmp_node_this.vals['b'] != None and tmp_node_this.vals['p'] != None:
                        self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                        return resNoneTemplate
                    if tmp_node_this.vals['k'] != None or tmp_node_this.vals['q'] != None:
                        if tmp_node_this.vals['b'] != None or tmp_node_this.vals['p'] != None:
                            self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                            return resNoneTemplate
                    if tmp_node_this.vals['k'] != None or tmp_node_this.vals['q'] != None:
                        for tmp_it_this in tmp_range_list:
                            tmp_node_this_output_this = self.random(1, tmp_main_val_right[0])
                            tmp_node_this_output_list.append(tmp_node_this_output_this)
                            tmp_node_this_output_data_1.append(tmp_node_this_output_this)
                        if tmp_node_this.vals['k'] != None:
                            if tmp_node_this.vals['k'] > len(tmp_node_this_output_list):
                                self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                                return resNoneTemplate
                            tmp_node_this_output_list.sort(reverse = True)
                            tmp_node_this_output_data_1 = tmp_node_this_output_list
                            tmp_range_list = range(0, tmp_node_this.vals['k'])
                            for tmp_it_this in tmp_range_list:
                                tmp_it_this_2 = tmp_it_this
                                tmp_node_this_output += tmp_node_this_output_list[tmp_it_this_2]
                                tmp_node_this_output_list_2.append(tmp_node_this_output_list[tmp_it_this_2])
                                tmp_node_this_output_data_2.append(tmp_node_this_output_list[tmp_it_this_2])
                        elif tmp_node_this.vals['q'] != None:
                            if tmp_node_this.vals['q'] > len(tmp_node_this_output_list):
                                self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                                return resNoneTemplate
                            tmp_node_this_output_list.sort(reverse = False)
                            tmp_node_this_output_data_1 = tmp_node_this_output_list
                            tmp_range_list = range(0, tmp_node_this.vals['q'])
                            for tmp_it_this in tmp_range_list:
                                tmp_it_this_2 = tmp_it_this
                                tmp_node_this_output += tmp_node_this_output_list[tmp_it_this_2]
                                tmp_node_this_output_list_2.append(tmp_node_this_output_list[tmp_it_this_2])
                                tmp_node_this_output_data_2.append(tmp_node_this_output_list[tmp_it_this_2])
                    elif tmp_node_this.vals['b'] != None or tmp_node_this.vals['p'] != None:
                        if tmp_node_this.vals['b'] != None:
                            if tmp_node_this.vals['b'] <= 0 or tmp_node_this.vals['b'] * tmp_main_val_left[0] > 10000:
                                self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                                return resNoneTemplate
                            flag_begin = True
                            for tmp_it_this in tmp_range_list:
                                tmp_rd_this = RD('1b%d' % (tmp_node_this.vals['b'], ))
                                tmp_rd_this.roll()
                                if tmp_rd_this.resError != None:
                                    self.resError = tmp_rd_this.resError
                                    return
                                else:
                                    tmp_node_this_output_this = tmp_rd_this.resInt
                                    tmp_node_this_output += tmp_node_this_output_this
                                    tmp_node_this_output_list.append(tmp_node_this_output_this)
                                    if flag_begin:
                                        flag_begin = False
                                    else:
                                        tmp_node_this_output_str_1 += ','
                                        tmp_node_this_output_str_2 += '+'
                                    tmp_node_this_output_str_1 += str(tmp_rd_this.resDetail)
                                    tmp_node_this_output_str_2 += str(tmp_node_this_output_this)
                                    tmp_node_this_output_data_1.append(tmp_rd_this.resDetailData)
                                    tmp_node_this_output_data_2.append(tmp_node_this_output_this)
                        elif tmp_node_this.vals['p'] != None:
                            if tmp_node_this.vals['p'] <= 0 or tmp_node_this.vals['p'] * tmp_main_val_left[0] > 10000:
                                self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                                return resNoneTemplate
                            flag_begin = True
                            for tmp_it_this in tmp_range_list:
                                tmp_rd_this = RD('1p%d' % (tmp_node_this.vals['p'], ))
                                tmp_rd_this.roll()
                                if tmp_rd_this.resError != None:
                                    self.resError = tmp_rd_this.resError
                                    return
                                else:
                                    tmp_node_this_output_this = tmp_rd_this.resInt
                                    tmp_node_this_output += tmp_node_this_output_this
                                    tmp_node_this_output_list.append(tmp_node_this_output_this)
                                    if flag_begin:
                                        flag_begin = False
                                    else:
                                        tmp_node_this_output_str_1 += ','
                                        tmp_node_this_output_str_2 += '+'
                                    tmp_node_this_output_str_1 += str(tmp_rd_this.resDetail)
                                    tmp_node_this_output_str_2 += str(tmp_node_this_output_this)
                                    tmp_node_this_output_data_1.append(tmp_rd_this.resDetailData)
                                    tmp_node_this_output_data_2.append(tmp_node_this_output_this)
                    else:
                        for tmp_it_this in tmp_range_list:
                            tmp_node_this_output_this = self.random(1, tmp_main_val_right[0])
                            tmp_node_this_output_list.append(tmp_node_this_output_this)
                            tmp_node_this_output_data_1.append(tmp_node_this_output_this)
                        for tmp_node_this_output_this in tmp_node_this_output_list:
                            tmp_node_this_output += tmp_node_this_output_this
                            tmp_node_this_output_list_2.append(tmp_node_this_output_this)
                    tmp_node_this_output_data_3.append(tmp_node_this_output)
                    # data主要处理流程
                    tmp_node_this_output_data['result'] = [
                        tmp_node_this_output_data_1,
                        tmp_node_this_output_data_2,
                        tmp_node_this_output_data_3
                    ]
                    tmp_node_this_output_data['key'] = {
                        'op': 'd',
                        'l': tmp_main_val_left[0],
                        'r': tmp_main_val_right[0],
                        'v': tmp_node_this.vals
                    }
                    tmp_node_this_output_data_4 = tmp_node_this_output_data_1
                    if len(tmp_node_this_output_data_2) > 0:
                        tmp_node_this_output_data_4 = tmp_node_this_output_data_2
                    tmp_node_this_output_data_final = [tmp_node_this_output_data]
                    tmp_node_this_output_meta_tuple = tmp_node_this_output_data_4
                    # str主要处理流程
                    if tmp_node_this.vals['b'] == None and tmp_node_this.vals['p'] == None:
                        flag_begin = True
                        for tmp_node_this_output_list_this in tmp_node_this_output_list:
                            if flag_begin:
                                flag_begin = False
                            else:
                                tmp_node_this_output_str_1 += ','
                            tmp_node_this_output_str_1 += str(tmp_node_this_output_list_this)
                        flag_begin = True
                        for tmp_node_this_output_list_this in tmp_node_this_output_list_2:
                            if flag_begin:
                                flag_begin = False
                            else:
                                tmp_node_this_output_str_2 += '+'
                            tmp_node_this_output_str_2 += str(tmp_node_this_output_list_this)
                    if tmp_node_this.vals['k'] == None and tmp_node_this.vals['q'] == None and tmp_node_this.vals['b'] == None and tmp_node_this.vals['p'] == None:
                        if len(tmp_node_this_output_list_2) == 1:
                            if rootPriority != 0:
                                tmp_node_this_output_str = tmp_node_this_output_str = '{%s}(%d)' % (tmp_node_this_output_str_2, tmp_node_this_output)
                            else:
                                tmp_node_this_output_str = ''
                        else:
                            tmp_node_this_output_str = '{%s}(%d)' % (tmp_node_this_output_str_2, tmp_node_this_output)
                    else:
                        tmp_node_this_output_str = '{%s}[%s](%d)' % (tmp_node_this_output_str_1, tmp_node_this_output_str_2, tmp_node_this_output)
                    if tmp_node_this.vals['b'] != None or tmp_node_this.vals['p'] != None:
                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax * tmp_main_val_right_obj.resIntMax
                        tmp_node_this_output_Min = max(tmp_main_val_left_obj.resIntMin * 1, 1)
                    elif tmp_node_this.vals['k'] != None:
                        tmp_node_this_output_Max = tmp_node_this.vals['k'] * tmp_main_val_right_obj.resIntMax
                        tmp_node_this_output_Min = tmp_node_this.vals['k'] * 1
                    elif tmp_node_this.vals['q'] != None:
                        tmp_node_this_output_Max = tmp_node_this.vals['q'] * tmp_main_val_right_obj.resIntMax
                        tmp_node_this_output_Min = tmp_node_this.vals['q'] * 1
                    else:
                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax * tmp_main_val_right_obj.resIntMax
                        tmp_node_this_output_Min = max(tmp_main_val_left_obj.resIntMin * 1, 1)
                    if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_Max = 0
                    if tmp_main_val_right_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_Max = 0
                elif tmp_node_this.data == 'a':
                    if tmp_main_val_right[0] <= 1 or tmp_main_val_right[0] >= 1000:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left[0] <= 0 or tmp_main_val_left[0] >= 1000:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_node_this.vals['m'] != None and (tmp_node_this.vals['m'] <= 0 or tmp_node_this.vals['m'] >= 1000):
                        self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                        return resNoneTemplate
                    if tmp_node_this.vals['k'] != None and (tmp_node_this.vals['k'] <= 0 or tmp_node_this.vals['k'] >= 1000):
                        self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                        return resNoneTemplate
                    if tmp_node_this.vals['q'] != None and (tmp_node_this.vals['q'] <= 0 or tmp_node_this.vals['q'] >= 1000):
                        self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                        return resNoneTemplate
                    flag_if_k_work = tmp_node_this.vals['k'] != None and tmp_node_this.vals['m'] >= tmp_node_this.vals['k']
                    flag_if_q_work = tmp_node_this.vals['q'] != None and 1 <= tmp_node_this.vals['q']
                    if flag_if_k_work or flag_if_q_work:
                        if tmp_node_this.vals['m'] >= tmp_main_val_right_obj.resIntMin or tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE:
                            tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        else:
                            if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_LIMITED:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Max = 0
                                tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                                tmp_node_this_output_Min = 0
                                if flag_if_k_work and flag_if_q_work:
                                    if tmp_node_this.vals['k'] - tmp_node_this.vals['q'] == 1:
                                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax
                                        tmp_node_this_output_Min = tmp_main_val_left_obj.resIntMin
                                    elif tmp_node_this.vals['k'] - tmp_node_this.vals['q'] < 1:
                                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax * 2
                                        tmp_node_this_output_Min = tmp_main_val_left_obj.resIntMin
                                    else:
                                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax
                                        tmp_node_this_output_Min = 0
                                elif flag_if_k_work:
                                    tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax
                                elif flag_if_q_work:
                                    tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax
                            else:
                                tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                                tmp_node_this_output_Max = 0
                    else:
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                        tmp_node_this_output_Max = 0
                        tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                        tmp_node_this_output_Min = 0
                    flag_add_roll_not_empty = True
                    tmp_add_roll_first = tmp_main_val_left[0]
                    tmp_add_roll_threshold = tmp_main_val_right[0]
                    tmp_add_roll_count = tmp_add_roll_first
                    tmp_add_roll_m = tmp_node_this.vals['m']
                    tmp_add_roll_k = tmp_node_this.vals['k']
                    tmp_add_roll_q = tmp_node_this.vals['q']
                    tmp_node_this_output_this = 0
                    tmp_node_this_output_list = []
                    tmp_node_this_output_list_list = []
                    tmp_node_this_output = 0
                    tmp_node_this_output_data = {}
                    tmp_node_this_output_data_1 = []
                    tmp_node_this_output_data_2 = []
                    tmp_node_this_output_data_3 = []
                    tmp_node_this_output_data_final = []
                    tmp_node_this_output_1_this = 0
                    tmp_node_this_output_1_list = []
                    tmp_node_this_output_str = ''
                    while flag_add_roll_not_empty:
                        tmp_range_list = range(0, tmp_add_roll_count)
                        tmp_add_roll_count = 0
                        tmp_node_this_output_list = []
                        tmp_node_this_output_1_this = 0
                        for tmp_it_this in tmp_range_list:
                            tmp_node_this_output_this = self.random(1, tmp_add_roll_m)
                            tmp_node_this_output_list.append(tmp_node_this_output_this)
                            if tmp_add_roll_k != None and tmp_node_this_output_this >= tmp_add_roll_k:
                                tmp_node_this_output += 1
                                tmp_node_this_output_1_this += 1
                            if tmp_add_roll_q != None and tmp_node_this_output_this <= tmp_add_roll_q:
                                tmp_node_this_output += 1
                                tmp_node_this_output_1_this += 1
                            if tmp_node_this_output_this >= tmp_add_roll_threshold:
                                tmp_add_roll_count += 1
                        tmp_node_this_output_1_list.append(tmp_node_this_output_1_this)
                        tmp_node_this_output_list_list.append(tmp_node_this_output_list)
                        if tmp_add_roll_count == 0:
                            flag_add_roll_not_empty = False
                    flag_begin = True
                    for tmp_node_this_output_list_this in tmp_node_this_output_list_list:
                        tmp_node_this_output_data_1_1 = []
                        if flag_begin:
                            flag_begin = False
                        else:
                            tmp_node_this_output_str += ','
                        tmp_node_this_output_str += '{'
                        flag_begin_2 = True
                        for tmp_node_this_output_this in tmp_node_this_output_list_this:
                            tmp_node_this_output_data_1_1_1 = tmp_node_this_output_this
                            if flag_begin_2:
                                flag_begin_2 = False
                            else:
                                tmp_node_this_output_str += ','
                            tmp_node_this_output_str_this = str(tmp_node_this_output_this)
                            if tmp_add_roll_k != None and tmp_node_this_output_this >= tmp_add_roll_k:
                                tmp_node_this_output_str_this = '[' + tmp_node_this_output_str_this + ']'
                                tmp_node_this_output_data_1_1_1 = {
                                    'op': 'mark01',
                                    'v': tmp_node_this_output_data_1_1_1
                                }
                            if tmp_add_roll_q != None and tmp_node_this_output_this <= tmp_add_roll_q:
                                tmp_node_this_output_str_this = '[' + tmp_node_this_output_str_this + ']'
                                tmp_node_this_output_data_1_1_1 = {
                                    'op': 'mark01',
                                    'v': tmp_node_this_output_data_1_1_1
                                }
                            if tmp_node_this_output_this >= tmp_add_roll_threshold:
                                tmp_node_this_output_str_this = '<' + tmp_node_this_output_str_this + '>'
                                tmp_node_this_output_data_1_1_1 = {
                                    'op': 'mark02',
                                    'v': tmp_node_this_output_data_1_1_1
                                }
                            tmp_node_this_output_str += tmp_node_this_output_str_this
                            tmp_node_this_output_data_1_1.append(tmp_node_this_output_data_1_1_1)
                        tmp_node_this_output_str += '}'
                        tmp_node_this_output_data_1.append(tmp_node_this_output_data_1_1)
                    tmp_node_this_output_str_1 = tmp_node_this_output_str
                    tmp_node_this_output_str_2 = ''
                    flag_begin = True
                    for tmp_node_this_output_1_this in tmp_node_this_output_1_list:
                        if flag_begin:
                            flag_begin = False
                        else:
                            tmp_node_this_output_str_2 += '+'
                        tmp_node_this_output_str_2 += str(tmp_node_this_output_1_this)
                        tmp_node_this_output_data_2.append(tmp_node_this_output_1_this)
                    tmp_node_this_output_data_3 = [tmp_node_this_output]
                    if len(tmp_node_this_output_1_list) == 1:
                        tmp_node_this_output_str = '%s(%d)' % (tmp_node_this_output_str_1, tmp_node_this_output)
                    else:
                        tmp_node_this_output_str = '{%s}[%s](%d)' % (tmp_node_this_output_str_1, tmp_node_this_output_str_2, tmp_node_this_output)
                    # data主要处理流程
                    tmp_node_this_output_data['result'] = [
                        tmp_node_this_output_data_1,
                        tmp_node_this_output_data_2,
                        tmp_node_this_output_data_3
                    ]
                    tmp_node_this_output_data['key'] = {
                        'op': 'a',
                        'l': tmp_main_val_left[0],
                        'r': tmp_main_val_right[0],
                        'v': tmp_node_this.vals
                    }
                    tmp_node_this_output_data_final = [tmp_node_this_output_data]
                elif tmp_node_this.data == 'c':
                    if tmp_main_val_right[0] <= 1 or tmp_main_val_right[0] >= 1000:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left[0] <= 0 or tmp_main_val_left[0] >= 1000:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_node_this.vals['m'] <= 0 or tmp_node_this.vals['m'] >= 1000:
                        self.resError = self.resErrorType.NODE_SUB_VAL_INVALID
                        return resNoneTemplate
                    if tmp_node_this.vals['m'] > tmp_main_val_right_obj.resIntMin or tmp_main_val_right_obj.resIntMinType == self.resExtremeType.INT_NEGATIVE_INFINITE:
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                    else:
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                        tmp_node_this_output_Max = tmp_main_val_left_obj.resIntMax * tmp_node_this.vals['m']
                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_Min = 1
                    flag_add_roll_not_empty = True
                    tmp_add_roll_first = tmp_main_val_left[0]
                    tmp_add_roll_threshold = tmp_main_val_right[0]
                    tmp_add_roll_count = tmp_add_roll_first
                    tmp_add_roll_m = tmp_node_this.vals['m']
                    tmp_node_this_output_this = 0
                    tmp_node_this_output_list = []
                    tmp_node_this_output_list_list = []
                    tmp_node_this_output = 0
                    tmp_node_this_output_1 = 0
                    tmp_node_this_output_2 = 0
                    tmp_node_this_output_data = {}
                    tmp_node_this_output_data_1 = []
                    tmp_node_this_output_data_2 = []
                    tmp_node_this_output_data_3 = []
                    tmp_node_this_output_data_final = []
                    tmp_node_this_output_str = ''
                    tmp_node_this_output_this_max = 0
                    while flag_add_roll_not_empty:
                        tmp_range_list = range(0, tmp_add_roll_count)
                        tmp_add_roll_count = 0
                        tmp_node_this_output_list = []
                        tmp_node_this_output_this_max = 0
                        for tmp_it_this in tmp_range_list:
                            tmp_node_this_output_this = self.random(1, tmp_add_roll_m)
                            tmp_node_this_output_list.append(tmp_node_this_output_this)
                            if tmp_node_this_output_this >= tmp_add_roll_threshold:
                                tmp_add_roll_count += 1
                            if tmp_node_this_output_this_max < tmp_node_this_output_this:
                                tmp_node_this_output_this_max = tmp_node_this_output_this
                        if tmp_add_roll_count > 0:
                            tmp_node_this_output += tmp_add_roll_m
                            tmp_node_this_output_1 += 1
                        else:
                            tmp_node_this_output += tmp_node_this_output_this_max
                            tmp_node_this_output_2 += tmp_node_this_output_this_max
                        tmp_node_this_output_list_list.append(tmp_node_this_output_list)
                        if tmp_add_roll_count == 0:
                            flag_add_roll_not_empty = False
                    flag_begin = True
                    tmp_it_count = 0
                    tmp_it_count_max = len(tmp_node_this_output_list_list) - 1
                    for tmp_node_this_output_list_this in tmp_node_this_output_list_list:
                        tmp_node_this_output_data_1_1 = []
                        if flag_begin:
                            flag_begin = False
                        else:
                            tmp_node_this_output_str += ','
                        tmp_node_this_output_str += '{'
                        flag_begin_2 = True
                        for tmp_node_this_output_this in tmp_node_this_output_list_this:
                            tmp_node_this_output_data_1_1_1 = tmp_node_this_output_this
                            if flag_begin_2:
                                flag_begin_2 = False
                            else:
                                tmp_node_this_output_str += ','
                            tmp_node_this_output_str_this = str(tmp_node_this_output_this)
                            if tmp_node_this_output_this >= tmp_add_roll_threshold:
                                tmp_node_this_output_str_this = '<' + tmp_node_this_output_str_this + '>'
                                tmp_node_this_output_data_1_1_1 = {
                                    'op': 'mark02',
                                    'v': tmp_node_this_output_data_1_1_1
                                }
                            if tmp_it_count == tmp_it_count_max and tmp_node_this_output_this_max == tmp_node_this_output_this:
                                tmp_node_this_output_str_this = '[' + tmp_node_this_output_str_this + ']'
                                tmp_node_this_output_data_1_1_1 = {
                                    'op': 'mark01',
                                    'v': tmp_node_this_output_data_1_1_1
                                }
                            tmp_node_this_output_str += tmp_node_this_output_str_this
                            tmp_node_this_output_data_1_1.append(tmp_node_this_output_data_1_1_1)
                        tmp_node_this_output_str += '}'
                        tmp_node_this_output_data_1.append(tmp_node_this_output_data_1_1)
                        tmp_it_count += 1
                    tmp_node_this_output_str_1 = tmp_node_this_output_str
                    tmp_node_this_output_str_2 = '%d*%d+%d' % (tmp_add_roll_m, tmp_node_this_output_1, tmp_node_this_output_2)
                    tmp_node_this_output_data_2 = [tmp_add_roll_m, tmp_node_this_output_1, tmp_node_this_output_2]
                    tmp_node_this_output_data_3 = [tmp_node_this_output]
                    tmp_node_this_output_str = '{%s}[%s](%d)' % (tmp_node_this_output_str_1, tmp_node_this_output_str_2, tmp_node_this_output)
                    # data主要处理流程
                    tmp_node_this_output_data['result'] = [
                        tmp_node_this_output_data_1,
                        tmp_node_this_output_data_2,
                        tmp_node_this_output_data_3
                    ]
                    tmp_node_this_output_data['key'] = {
                        'op': 'c',
                        'l': tmp_main_val_left[0],
                        'r': tmp_main_val_right[0],
                        'v': tmp_node_this.vals
                    }
                    tmp_node_this_output_data_final = [tmp_node_this_output_data]
                elif tmp_node_this.data == 'b':
                    if tmp_main_val_right[0] > 10000:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left[0] > 10000:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_Max = 100
                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_Min = 1
                    tmp_node_this_output = 0
                    tmp_node_this_output_1 = 0
                    tmp_node_this_output_2 = 0
                    tmp_node_this_output_2_mark = 10
                    tmp_node_this_output_this = 0
                    tmp_node_this_output_list = []
                    tmp_node_this_output_list_2 = []
                    tmp_node_this_output_str = ''
                    tmp_node_this_output_str_1 = ''
                    tmp_node_this_output_str_2 = ''
                    tmp_node_this_output_data = {}
                    tmp_node_this_output_data_1 = []
                    tmp_node_this_output_data_2 = []
                    tmp_node_this_output_data_3 = []
                    tmp_node_this_output_data_final = []
                    tmp_node_this_output_this = self.random(1, 100)
                    tmp_node_this_output_1 = tmp_node_this_output_this
                    tmp_range_list = range(0, tmp_main_val_right[0])
                    tmp_node_this_output_1_1 = int(tmp_node_this_output_1 / 10)
                    tmp_node_this_output_1_2 = int(tmp_node_this_output_1 % 10)
                    for tmp_it_this in tmp_range_list:
                        tmp_node_this_output_this = self.random(1, 10) - 1
                        if tmp_node_this_output_1_2 == 0 and tmp_node_this_output_this == 0:
                            tmp_node_this_output_this = 10
                        tmp_node_this_output_list_2.append(tmp_node_this_output_this)
                        if tmp_node_this_output_2_mark > tmp_node_this_output_this:
                            tmp_node_this_output_2_mark = tmp_node_this_output_this
                    if tmp_node_this_output_1_2 == 0 and tmp_node_this_output_2_mark == 0:
                        tmp_node_this_output = 100
                    elif tmp_node_this_output_1_1 > tmp_node_this_output_2_mark:
                        tmp_node_this_output = tmp_node_this_output_1_2 + tmp_node_this_output_2_mark * 10
                    else:
                        tmp_node_this_output = tmp_node_this_output_1
                    # data主要处理流程
                    tmp_node_this_output_data_1 = [tmp_node_this_output_1]
                    for tmp_node_this_output_list_2_this in tmp_node_this_output_list_2:
                        tmp_node_this_output_list_2_this_res = tmp_node_this_output_list_2_this
                        if len(tmp_node_this_output_list_2) > 1 and tmp_node_this_output_2_mark == tmp_node_this_output_list_2_this:
                            tmp_node_this_output_list_2_this_res = {
                                'op': 'mark01',
                                'v': tmp_node_this_output_list_2_this_res
                            }
                        tmp_node_this_output_data_2.append(tmp_node_this_output_list_2_this_res)
                    tmp_node_this_output_data_3 = [tmp_node_this_output]
                    tmp_node_this_output_data['result'] = [
                        tmp_node_this_output_data_1,
                        tmp_node_this_output_data_2,
                        tmp_node_this_output_data_3
                    ]
                    tmp_node_this_output_data['key'] = {
                        'op': 'b',
                        'l': tmp_main_val_left[0],
                        'r': tmp_main_val_right[0],
                        'v': tmp_node_this.vals
                    }
                    tmp_node_this_output_data_final = [tmp_node_this_output_data]
                    # str主要处理流程
                    tmp_node_this_output_str_1 = '1D100=' + str(tmp_node_this_output_1)
                    tmp_node_this_output_str_2 = 'bonus:['
                    flag_begin = True
                    for tmp_node_this_output_list_2_this in tmp_node_this_output_list_2:
                        if flag_begin:
                            flag_begin = False
                        else:
                            tmp_node_this_output_str_2 += ','
                        tmp_node_this_output_list_2_this_str = str(tmp_node_this_output_list_2_this)
                        if len(tmp_node_this_output_list_2) > 1 and tmp_node_this_output_2_mark == tmp_node_this_output_list_2_this:
                            tmp_node_this_output_list_2_this_str = '[' + tmp_node_this_output_list_2_this_str + ']'
                        tmp_node_this_output_str_2 += tmp_node_this_output_list_2_this_str
                    tmp_node_this_output_str_2 += ']'
                    tmp_node_this_output_str = '{%s %s}(%s)' % (tmp_node_this_output_str_1, tmp_node_this_output_str_2, str(tmp_node_this_output))
                elif tmp_node_this.data == 'p':
                    if tmp_main_val_right[0] > 10000:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left[0] > 10000:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_Max = 100
                    tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                    tmp_node_this_output_Min = 1
                    tmp_node_this_output = 0
                    tmp_node_this_output_1 = 0
                    tmp_node_this_output_2 = 0
                    tmp_node_this_output_2_mark = 0
                    tmp_node_this_output_this = 0
                    tmp_node_this_output_list = []
                    tmp_node_this_output_list_2 = []
                    tmp_node_this_output_str = ''
                    tmp_node_this_output_str_1 = ''
                    tmp_node_this_output_str_2 = ''
                    tmp_node_this_output_data = {}
                    tmp_node_this_output_data_1 = []
                    tmp_node_this_output_data_2 = []
                    tmp_node_this_output_data_3 = []
                    tmp_node_this_output_data_final = []
                    tmp_node_this_output_this = self.random(1, 100)
                    tmp_node_this_output_1 = tmp_node_this_output_this
                    tmp_range_list = range(0, tmp_main_val_right[0])
                    tmp_node_this_output_1_1 = int(tmp_node_this_output_1 / 10)
                    tmp_node_this_output_1_2 = int(tmp_node_this_output_1 % 10)
                    for tmp_it_this in tmp_range_list:
                        tmp_node_this_output_this = self.random(1, 10) - 1
                        if tmp_node_this_output_1_2 == 0 and tmp_node_this_output_this == 0:
                            tmp_node_this_output_this = 10
                        tmp_node_this_output_list_2.append(tmp_node_this_output_this)
                        if tmp_node_this_output_2_mark < tmp_node_this_output_this:
                            tmp_node_this_output_2_mark = tmp_node_this_output_this
                    if tmp_node_this_output_1_2 == 0 and tmp_node_this_output_2_mark == 0:
                        tmp_node_this_output = 100
                    elif tmp_node_this_output_1_1 < tmp_node_this_output_2_mark:
                        tmp_node_this_output = tmp_node_this_output_1_2 + tmp_node_this_output_2_mark * 10
                    else:
                        tmp_node_this_output = tmp_node_this_output_1
                    # data主要处理流程
                    tmp_node_this_output_data_1 = [tmp_node_this_output_1]
                    for tmp_node_this_output_list_2_this in tmp_node_this_output_list_2:
                        tmp_node_this_output_list_2_this_res = tmp_node_this_output_list_2_this
                        if len(tmp_node_this_output_list_2) > 1 and tmp_node_this_output_2_mark == tmp_node_this_output_list_2_this:
                            tmp_node_this_output_list_2_this_res = {
                                'op': 'mark01',
                                'v': tmp_node_this_output_list_2_this_res
                            }
                        tmp_node_this_output_data_2.append(tmp_node_this_output_list_2_this_res)
                    tmp_node_this_output_data_3 = [tmp_node_this_output]
                    tmp_node_this_output_data['result'] = [
                        tmp_node_this_output_data_1,
                        tmp_node_this_output_data_2,
                        tmp_node_this_output_data_3
                    ]
                    tmp_node_this_output_data['key'] = {
                        'op': 'p',
                        'l': tmp_main_val_left[0],
                        'r': tmp_main_val_right[0],
                        'v': tmp_node_this.vals
                    }
                    tmp_node_this_output_data_final = [tmp_node_this_output_data]
                    # str主要处理流程
                    tmp_node_this_output_str_1 = '1D100=' + str(tmp_node_this_output_1)
                    tmp_node_this_output_str_2 = 'punish:['
                    flag_begin = True
                    for tmp_node_this_output_list_2_this in tmp_node_this_output_list_2:
                        if flag_begin:
                            flag_begin = False
                        else:
                            tmp_node_this_output_str_2 += ','
                        tmp_node_this_output_list_2_this_str = str(tmp_node_this_output_list_2_this)
                        if len(tmp_node_this_output_list_2) > 1 and tmp_node_this_output_2_mark == tmp_node_this_output_list_2_this:
                            tmp_node_this_output_list_2_this_str = '[' + tmp_node_this_output_list_2_this_str + ']'
                        tmp_node_this_output_str_2 += tmp_node_this_output_list_2_this_str
                    tmp_node_this_output_str_2 += ']'
                    tmp_node_this_output_str = '{%s %s}(%s)' % (tmp_node_this_output_str_1, tmp_node_this_output_str_2, str(tmp_node_this_output))
                elif tmp_node_this.data == 'f':
                    if tmp_main_val_right[0] <= 1 or tmp_main_val_right[0] > 10000:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left[0] <= 0 or tmp_main_val_left[0] > 10000:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_left_obj.resIntMaxType == self.resExtremeType.INT_POSITIVE_INFINITE:
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_POSITIVE_INFINITE
                        tmp_node_this_output_MinType = self.resExtremeType.INT_NEGATIVE_INFINITE
                    else:
                        tmp_node_this_output_MaxType = self.resExtremeType.INT_LIMITED
                        tmp_node_this_output_Max = tmp_main_val_left_obj.resInt * 1
                        tmp_node_this_output_MinType = self.resExtremeType.INT_LIMITED
                        tmp_node_this_output_Min = tmp_main_val_left_obj.resInt * (-1)
                    tmp_range_list = range(0, tmp_main_val_left[0])
                    tmp_node_this_output = 0
                    tmp_node_this_output_this = 0
                    tmp_node_this_output_list = []
                    tmp_node_this_output_list_2 = []
                    tmp_node_this_output_str = ''
                    tmp_node_this_output_str_1 = ''
                    tmp_node_this_output_str_2 = ''
                    tmp_node_this_output_str_3 = ''
                    tmp_node_this_output_data = {}
                    tmp_node_this_output_data_1 = []
                    tmp_node_this_output_data_2 = []
                    tmp_node_this_output_data_3 = []
                    tmp_node_this_output_data_final = []
                    for tmp_it_this in tmp_range_list:
                        tmp_node_this_output_this = self.random(-1, 1)
                        tmp_node_this_output += tmp_node_this_output_this
                        tmp_node_this_output_list.append(tmp_node_this_output_this)
                    flag_begin = True
                    for tmp_node_this_output_list_this in tmp_node_this_output_list:
                        if flag_begin:
                            flag_begin = False
                        else:
                            tmp_node_this_output_str_1 += ' '
                            if tmp_node_this_output_list_this >= 0:
                                tmp_node_this_output_str_2 += '+'
                        if tmp_node_this_output_list_this < 0:
                            tmp_node_this_output_str_1 += '-'
                        elif tmp_node_this_output_list_this == 0:
                            tmp_node_this_output_str_1 += '0'
                        elif tmp_node_this_output_list_this > 0:
                            tmp_node_this_output_str_1 += '+'
                        tmp_node_this_output_data_1.append(tmp_node_this_output_list_this)
                        tmp_node_this_output_str_2 += str(tmp_node_this_output_list_this)
                    tmp_node_this_output_data_2 = tmp_node_this_output_data_1
                    tmp_node_this_output_data_3 = [tmp_node_this_output]
                    tmp_node_this_output_str = '{%s}[%s](%d)' % (tmp_node_this_output_str_1, tmp_node_this_output_str_2, tmp_node_this_output)
                    # data主要处理流程
                    tmp_node_this_output_data['result'] = [
                        tmp_node_this_output_data_1,
                        tmp_node_this_output_data_2,
                        tmp_node_this_output_data_3
                    ]
                    tmp_node_this_output_data['key'] = {
                        'op': 'f',
                        'l': tmp_main_val_left[0],
                        'r': tmp_main_val_right[0],
                        'v': tmp_node_this.vals
                    }
                    tmp_node_this_output_data_final = [tmp_node_this_output_data]
                    tmp_node_this_output_meta_tuple = tmp_node_this_output_data_1
                elif tmp_node_this.data == '?':
                    if tmp_node_this.vals[':'] != None:
                        tmp_flag_True = True
                        if tmp_main_val_left[0] == 0:
                            tmp_flag_True = False
                        if tmp_flag_True:
                            tmp_node_this_output = tmp_main_val_right[0]
                        else:
                            tmp_node_this_output = tmp_node_this.vals[':']
                        tmp_node_this_output_Min = tmp_node_this_output
                        tmp_node_this_output_Max = tmp_node_this_output
                        tmp_node_this_output_str = '{%s?%s:%s}(%s)' % (
                            str(tmp_main_val_left[1]),
                            str(tmp_main_val_right[0]),
                            str(tmp_node_this.vals[':']),
                            tmp_node_this_output
                        )
                        tmp_node_this_output_data_final = [{
                            'key': {
                                'op': '?',
                                'l': tmp_main_val_left[0],
                                'r': tmp_main_val_right[0],
                                'v': tmp_node_this.vals
                            },
                            'result': [
                                [tmp_main_val_left_data, tmp_main_val_right[0], tmp_node_this.vals[':']],
                                [],
                                [tmp_node_this_output]
                            ]
                        }]
                    else:
                        if tmp_main_val_left[0] < 0:
                            self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                            return resNoneTemplate
                        tmp_last_num = tmp_main_val_left[0]
                        tmp_node_this_output = int(tmp_last_num * (1 + tmp_last_num) / 2)
                        tmp_node_this_output_Min = tmp_node_this_output
                        tmp_node_this_output_Max = tmp_node_this_output
                        tmp_node_this_output_str = '{%s?}[%s?](%s)' % (
                            tmp_main_val_left[1],
                            tmp_main_val_left[0],
                            str(tmp_node_this_output)
                        )
                        tmp_node_this_output_data_final = [{
                            'key': {
                                'op': '?',
                                'l': tmp_main_val_left[0],
                                'r': tmp_main_val_right[0],
                                'v': tmp_node_this.vals
                            },
                            'result': [
                                [tmp_main_val_left_data],
                                [tmp_main_val_left[0]],
                                [tmp_node_this_output]
                            ]
                        }]
                elif (
                    tmp_node_this.data == 'kh'
                ) or (
                    tmp_node_this.data == 'kl'
                ) or (
                    tmp_node_this.data == 'dh'
                ) or (
                    tmp_node_this.data == 'dl'
                ) or (
                    tmp_node_this.data == 'max'
                ) or (
                    tmp_node_this.data == 'min'
                ):
                    tmp_last_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_last_resMetaTuple_raw_new = tmp_last_resMetaTuple_raw
                    tmp_last_resMetaTuple = tmp_last_resMetaTuple_raw
                    if type(tmp_last_resMetaTuple) == list and len(tmp_last_resMetaTuple) > 0:
                        tmp_last_resMetaTuple = self.get_from_metaTuple(tmp_last_resMetaTuple_raw)
                    else:
                        tmp_last_resMetaTuple_raw = [tmp_main_val_left[0]]
                        tmp_last_resMetaTuple = tmp_last_resMetaTuple_raw
                    if len(tmp_last_resMetaTuple_raw) != len(tmp_last_resMetaTuple):
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    if tmp_main_val_right[0] <= 0:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    tmp_last_resMetaTuple_list = []
                    tmp_last_resMetaTuple_list_new = []
                    for tmp_last_resMetaTuple_i in range(len(tmp_last_resMetaTuple_raw)):
                        if tmp_last_resMetaTuple_i < len(tmp_last_resMetaTuple):
                            tmp_last_resMetaTuple_list.append([
                                tmp_last_resMetaTuple[tmp_last_resMetaTuple_i],
                                tmp_last_resMetaTuple_raw[tmp_last_resMetaTuple_i]
                            ])
                    tmp_node_this_output = 0
                    tmp_node_this_output_meta_tuple_res = []
                    if tmp_node_this.data == 'kh':
                        tmp_last_resMetaTuple_list.sort(reverse = True, key = lambda x:x[0])
                    elif tmp_node_this.data == 'kl':
                        tmp_last_resMetaTuple_list.sort(reverse = False, key = lambda x:x[0])
                    elif tmp_node_this.data == 'dh':
                        tmp_last_resMetaTuple_list.sort(reverse = True, key = lambda x:x[0])
                    elif tmp_node_this.data == 'dl':
                        tmp_last_resMetaTuple_list.sort(reverse = False, key = lambda x:x[0])
                    elif tmp_node_this.data == 'max':
                        for tmp_last_resMetaTuple_list_this in tmp_last_resMetaTuple_list:
                            if tmp_last_resMetaTuple_list_this[0] > tmp_main_val_right[0]:
                                tmp_last_resMetaTuple_list_this[0] = tmp_main_val_right[0]
                                tmp_last_resMetaTuple_list_this[1] = tmp_main_val_right[0]
                    elif tmp_node_this.data == 'min':
                        for tmp_last_resMetaTuple_list_this in tmp_last_resMetaTuple_list:
                            if tmp_last_resMetaTuple_list_this[0] < tmp_main_val_right[0]:
                                tmp_last_resMetaTuple_list_this[0] = tmp_main_val_right[0]
                                tmp_last_resMetaTuple_list_this[1] = tmp_main_val_right[0]
                    if tmp_node_this.data in ['kh', 'kl']:
                        if tmp_main_val_right[0] <= len(tmp_last_resMetaTuple_list):
                            tmp_last_resMetaTuple_list_new = tmp_last_resMetaTuple_list[:tmp_main_val_right[0]]
                        else:
                            tmp_last_resMetaTuple_list_new = tmp_last_resMetaTuple_list
                    elif tmp_node_this.data in ['dh', 'dl']:
                        if tmp_main_val_right[0] < len(tmp_last_resMetaTuple_list):
                            tmp_last_resMetaTuple_list_new = tmp_last_resMetaTuple_list[tmp_main_val_right[0]:]
                        else:
                            tmp_last_resMetaTuple_list_new = tmp_last_resMetaTuple_list
                    else:
                        tmp_last_resMetaTuple_list_new = tmp_last_resMetaTuple_list
                    tmp_last_resMetaTuple = [tmp_last_resMetaTuple_list_this[0] for tmp_last_resMetaTuple_list_this in tmp_last_resMetaTuple_list]
                    tmp_last_resMetaTuple_raw_new = [tmp_last_resMetaTuple_list_this[1] for tmp_last_resMetaTuple_list_this in tmp_last_resMetaTuple_list]
                    tmp_node_this_output_meta_tuple = [tmp_last_resMetaTuple_list_new_this[0] for tmp_last_resMetaTuple_list_new_this in tmp_last_resMetaTuple_list_new]
                    tmp_node_this_output = sum(tmp_node_this_output_meta_tuple)
                    tmp_node_this_output_Max = tmp_node_this_output
                    tmp_node_this_output_Min = tmp_node_this_output
                    tmp_node_this_output_str = '{%s}(%d)' % (
                        ','.join(self.get_str_from_metaTuple(tmp_last_resMetaTuple_raw, tmp_last_resMetaTuple)),
                        tmp_node_this_output
                    )
                    tmp_node_this_output_data_final = [{
                        'result': [
                            tmp_last_resMetaTuple,
                            tmp_last_resMetaTuple_raw_new,
                            tmp_node_this_output_meta_tuple
                        ],
                        'key': {
                            'op': tmp_node_this.data,
                            'l': tmp_main_val_left[0],
                            'r': tmp_main_val_right[0],
                            'v': tmp_node_this.vals
                        }
                    }]
                elif tmp_node_this.data in ['sp', 'tp']:
                    tmp_last_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_last_resMetaTuple_raw_new = tmp_last_resMetaTuple_raw
                    tmp_last_resMetaTuple = tmp_last_resMetaTuple_raw
                    if type(tmp_last_resMetaTuple) == list and len(tmp_last_resMetaTuple) > 0:
                        tmp_last_resMetaTuple = self.get_from_metaTuple(tmp_last_resMetaTuple_raw)
                    else:
                        tmp_last_resMetaTuple_raw = [tmp_main_val_left[0]]
                        tmp_last_resMetaTuple = tmp_last_resMetaTuple_raw
                    if len(tmp_last_resMetaTuple_raw) != len(tmp_last_resMetaTuple):
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    flag_cut = False
                    tmp_last_right_resMetaTuple_raw = [tmp_main_val_right[0]]
                    if tmp_main_val_right_obj.resMetaTupleEnable and len(tmp_main_val_right_obj.resMetaTuple) > 0:
                        tmp_last_right_resMetaTuple_raw = tmp_main_val_right_obj.resMetaTuple
                        if len(tmp_last_right_resMetaTuple_raw) > 1:
                            flag_cut = True
                    tmp_last_right_resMetaTuple = tmp_last_right_resMetaTuple_raw.copy()
                    tmp_last_right_resMetaTuple = self.get_from_metaTuple(tmp_last_right_resMetaTuple)
                    tmp_start = 1
                    tmp_step = 1
                    tmp_end = 1
                    if len(tmp_last_right_resMetaTuple) == 1:
                        tmp_end = tmp_last_right_resMetaTuple[0]
                    elif len(tmp_last_right_resMetaTuple) == 2:
                        tmp_start = tmp_last_right_resMetaTuple[0]
                        tmp_end = tmp_last_right_resMetaTuple[1]
                    elif len(tmp_last_right_resMetaTuple) >= 3:
                        tmp_start = tmp_last_right_resMetaTuple[0]
                        tmp_step = tmp_last_right_resMetaTuple[1]
                        tmp_end = tmp_last_right_resMetaTuple[2]
                    if tmp_node_this.data == 'tp':
                        tmp_start = 1
                        tmp_step = 1
                        tmp_end = len(tmp_last_resMetaTuple)
                        flag_cut = True
                    if tmp_start > tmp_end or tmp_step < 1:
                        self.resError = self.resErrorType.NODE_RIGHT_VAL_INVALID
                        return resNoneTemplate
                    tmp_last_resMetaTuple_list = []
                    tmp_last_resMetaTuple_list_new = []
                    for tmp_last_resMetaTuple_i in range(len(tmp_last_resMetaTuple_raw)):
                        if tmp_last_resMetaTuple_i < len(tmp_last_resMetaTuple):
                            tmp_last_resMetaTuple_list.append([
                                tmp_last_resMetaTuple[tmp_last_resMetaTuple_i],
                                tmp_last_resMetaTuple_raw[tmp_last_resMetaTuple_i]
                            ])
                    tmp_node_this_output = 0
                    tmp_node_this_output_meta_tuple_res = []
                    if flag_cut:
                        tmp_last_resMetaTuple_list_new_2 = []
                        tmp_last_resMetaTuple_list_new = tmp_last_resMetaTuple_list[tmp_start - 1:tmp_end]
                        for tmp_last_resMetaTuple_list_new_i in range(len(tmp_last_resMetaTuple_list_new)):
                            if tmp_last_resMetaTuple_list_new_i % tmp_step == 0:
                                tmp_last_resMetaTuple_list_new_2.append(tmp_last_resMetaTuple_list_new[tmp_last_resMetaTuple_list_new_i])
                        tmp_last_resMetaTuple_list_new = tmp_last_resMetaTuple_list_new_2
                        tmp_node_this_output_meta_tuple_enable = True
                    else:
                        tmp_last_resMetaTuple_list_new = [tmp_last_resMetaTuple_list[tmp_end - 1]]
                    tmp_last_resMetaTuple = [tmp_last_resMetaTuple_list_this[0] for tmp_last_resMetaTuple_list_this in tmp_last_resMetaTuple_list]
                    tmp_last_resMetaTuple_raw_new = [tmp_last_resMetaTuple_list_this[1] for tmp_last_resMetaTuple_list_this in tmp_last_resMetaTuple_list]
                    tmp_node_this_output_meta_tuple = [tmp_last_resMetaTuple_list_new_this[0] for tmp_last_resMetaTuple_list_new_this in tmp_last_resMetaTuple_list_new]
                    if len(tmp_last_resMetaTuple) > 0:
                        tmp_node_this_output = tmp_node_this_output_meta_tuple[-1]
                    tmp_node_this_output_Max = tmp_node_this_output
                    tmp_node_this_output_Min = tmp_node_this_output
                    tmp_node_this_output_str = '{%s}(%d)' % (
                        ','.join(self.get_str_from_metaTuple(tmp_last_resMetaTuple_raw, tmp_last_resMetaTuple)),
                        tmp_node_this_output
                    )
                    tmp_node_this_output_data_final = [{
                        'result': [
                            tmp_last_resMetaTuple,
                            tmp_last_resMetaTuple_raw_new,
                            tmp_node_this_output_meta_tuple
                        ],
                        'key': {
                            'op': tmp_node_this.data,
                            'l': tmp_main_val_left[0],
                            'r': tmp_main_val_right[0],
                            'v': tmp_node_this.vals
                        }
                    }]
                elif tmp_node_this.data == '$t':
                    tmp_key = 't%d' % tmp_main_val_right[0]
                    if tmp_node_this.vals['='] != None:
                        self.valueTable[tmp_key] = tmp_node_this.vals['=']
                        tmp_node_this_output = tmp_node_this.vals['=']
                    else:
                        if tmp_key in self.valueTable:
                            tmp_node_this_output = self.valueTable[tmp_key]
                    tmp_node_this_output_Max = tmp_node_this_output
                    tmp_node_this_output_Min = tmp_node_this_output
                    tmp_node_this_output_str = str(tmp_node_this_output)
                    tmp_node_this_output_data_final = [tmp_node_this_output]
                elif tmp_node_this.data == 'lp':
                    tmp_last_left_resMetaTuple_raw = [tmp_main_val_left[0]]
                    if tmp_main_val_left_obj.resMetaTupleEnable and len(tmp_main_val_left_obj.resMetaTuple) > 0:
                        tmp_last_left_resMetaTuple_raw = tmp_main_val_left_obj.resMetaTuple
                    tmp_last_left_resMetaTuple = tmp_last_left_resMetaTuple_raw.copy()
                    tmp_last_left_resMetaTuple = self.get_from_metaTuple(tmp_last_left_resMetaTuple)
                    tmp_last_right_resMetaTuple_raw = tmp_main_val_right_obj.resMetaTuple
                    tmp_last_right_resMetaTuple = tmp_last_right_resMetaTuple_raw.copy()
                    tmp_start = 1
                    tmp_step = 1
                    tmp_end = 1
                    if len(tmp_last_left_resMetaTuple) == 1:
                        tmp_end = tmp_last_left_resMetaTuple[0]
                    elif len(tmp_last_left_resMetaTuple) == 2:
                        tmp_start = tmp_last_left_resMetaTuple[0]
                        tmp_end = tmp_last_left_resMetaTuple[1]
                    elif len(tmp_last_left_resMetaTuple) >= 3:
                        tmp_start = tmp_last_left_resMetaTuple[0]
                        tmp_step = tmp_last_left_resMetaTuple[1]
                        tmp_end = tmp_last_left_resMetaTuple[2]
                    if tmp_start > tmp_end or tmp_step < 1:
                        self.resError = self.resErrorType.NODE_LEFT_VAL_INVALID
                        return resNoneTemplate
                    tmp_res_resMetaTuple = []
                    for tmp_count_i in range(tmp_start, tmp_end + 1, tmp_step):
                        tmp_res_resMetaTuple += [
                            tmp_last_right_resMetaTuple_this.replace('i', str(tmp_count_i))
                            for tmp_last_right_resMetaTuple_this in tmp_last_right_resMetaTuple
                        ]
                    if len(tmp_res_resMetaTuple) > 1000:
                        tmp_res_resMetaTuple = tmp_res_resMetaTuple[:1000]
                    tmp_node_this_output_str = '{%s:%s:%s}lp{%s}' % (
                        str(tmp_start), str(tmp_step), str(tmp_end),
                        ','.join([str(tmp_last_right_resMetaTuple_raw_this) for tmp_last_right_resMetaTuple_raw_this in tmp_last_right_resMetaTuple_raw])
                    )
                    tmp_node_this_output_data_final = [{
                        'key': {
                            'op': 'lp',
                            'l': tmp_main_val_left[0],
                            'r': tmp_main_val_right[0],
                            'v': tmp_node_this.vals
                        },
                        'result': [
                            [tmp_start, tmp_step, tmp_end],
                            tmp_last_right_resMetaTuple_raw,
                            []
                        ]
                    }]
                    tmp_node_this_output_meta_tuple = tmp_res_resMetaTuple
                    tmp_node_this_output_meta_tuple_enable = True
                else:
                    self.resError = self.resErrorType.NODE_OPERATION_INVALID
                    return resNoneTemplate
            else:
                self.resError = self.resErrorType.NODE_OPERATION_INVALID
                return resNoneTemplate
            resRecursiveObj = self.resRecursive()
            resRecursiveObj.resInt = tmp_node_this_output
            resRecursiveObj.resIntMax = tmp_node_this_output_Max
            resRecursiveObj.resIntMin = tmp_node_this_output_Min
            resRecursiveObj.resIntMaxType = tmp_node_this_output_MaxType
            resRecursiveObj.resIntMinType = tmp_node_this_output_MinType
            resRecursiveObj.resDetail = tmp_node_this_output_str
            resRecursiveObj.resDetailData = tmp_node_this_output_data_final
            resRecursiveObj.resMetaTuple = tmp_node_this_output_meta_tuple
            resRecursiveObj.resMetaTupleEnable = tmp_node_this_output_meta_tuple_enable
            return resRecursiveObj

    def get_from_metaTuple(self, data, flag_last = False, flag_update = True):
        res = []
        for data_this in data:
            if type(data_this) == int:
                res.append(data_this)
            elif type(data_this) == str:
                para_this = RD(
                    data_this,
                    customDefault = self.customDefault,
                    valueTable = self.valueTable
                )
                para_this.roll()
                if para_this.resError == None:
                    res.append(para_this.resInt)
                if flag_update:
                    self.valueTable.update(para_this.valueTable)
                if flag_last:
                    self.resInt = para_this.resInt
                    self.resIntMin = para_this.resIntMin
                    self.resIntMax = para_this.resIntMax
                    self.resIntMinType = para_this.resIntMinType
                    self.resIntMaxType = para_this.resIntMaxType
                    self.resDetail = para_this.resDetail
                    self.resDetailData = para_this.resDetailData
        return res

    def check_metaTuple(self, data):
        res = False
        for data_this in data:
            if type(data_this) == str:
                res = True
                break
        return res

    def get_str_from_metaTuple(self, data_raw, data):
        res = []
        for data_i in range(len(data)):
            if type(data_raw[data_i]) == int:
                res.append(str(data[data_i]))
            elif type(data_raw[data_i]) == str:
                try:
                    if int(data_raw[data_i]) == data[data_i]:
                        res.append(str(data[data_i]))
                    else:
                        raise Exception('not int')
                except:
                    res.append('%s=%s' % (str(data_raw[data_i]), str(data[data_i])))
        return res

def boolByListAnd(data):
    res = True
    for data_this in data:
        if not data_this:
            res = False
            return res
    return res

def boolByListOr(data):
    res = False
    for data_this in data:
        if data_this:
            res = True
            return res
    return res

if __name__ == '__main__':
    str_para_list = [
        '10d10-7a5k7*10+6',
        '10d10',
        '1d(7a5k7)a7',
        '(1d100)^(7a5k7)',
        '(1d100)^(1d20)',
        '1-1>2',
        '1+2>2',
        '((1-1>2)|(1-1<2))?(1+1):(1-2)',
        '(100-50+50)?',
        '1|2',
        '1&2',
        '{力量}+1*{魔法}',
        '{力量}+2',
        '1*{力量}+2{{STR}',
        '1*{力量}+2{{STR',
        '7a8k10q5m9',
        '7a10k10q5m9',
        '7a10k6q5m9',
        '7a10k5q5m9',
        '7df',
        '2d20kl',
        '2d20kh',
        '(2d20+2)kh',
        '(2d20-20)kh',
        '(2d20/10)kh',
        '((2d20)^2)kh',
        '[1,2]kh',
        '[1,2]kl',
        '[1d20,10]kl',
        '[1d20,[1,2]kh]kl',
        '[1,2]',
        '[1,2d6]',
        '2d6',
        '10d6max3',
        '10d6dl3',
        '10d6sp5',
        '10d6sp[2,2]',
        '10d6sp[1,3,6]',
        '10d6tp'
    ]
    val_table = {
        '力量': 60,
        'STR': 50
    }
    for str_para in str_para_list:
        rd_para = RD(str_para, valueTable=val_table)
        print(rd_para.originData)
        rd_para.roll()
        print('----------------')
        if rd_para.resError != None:
            print(rd_para.resError)
        else:
            print(rd_para.resInt)
            print(rd_para.resIntMax)
            print(rd_para.resIntMin)
            print(rd_para.resIntMaxType)
            print(rd_para.resIntMinType)
            print(rd_para.resDetail)
            print(rd_para.resDetailData)
            print(rd_para.resMetaTuple)
            print(rd_para.resMetaTupleEnable)
        print('================')
