# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   pcCardData.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivaDiceCore

dictPcCardTemplateDefault = {}

dictPcCardTemplateModel = {
    'mainDice': '1D100',
    'customDefault': {},
    'skill': {},
    'skillConfig': {
        'skipEnhance': [],
        'forceMapping': []
    },
    'init': {},
    'mapping': {},
    'synonyms':{},
    'redirect': {},
    'showName': {},
    'checkRules': {
        'default': {
            'checkList': []
        }
    }
}

dictPcCardTemplateDefaultTemp = {
    'default': {
        'mainDice': '1D100',
        'customDefault': {
            'd': {
                'leftD': 1,
                'rightD': 100,
                'sub': {
                    'k': None,
                    'q': None,
                    'p': None,
                    'b': None
                },
                'subD': {
                    'p': 1,
                    'b': 1
                }
            }
        },
        'skill': {
            '属性': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX'
            ],
            '技能': [
                '会计',
                '人类学',
                '估价',
                '考古学',
                '取悦',
                '攀爬',
                '计算机使用',
                '信用',
                '克苏鲁神话',
                '乔装',
                '闪避',
                '汽车驾驶',
                '电气维修',
                '电子学',
                '话术',
                '急救',
                '历史',
                '恐吓',
                '跳跃',
                '法律',
                '图书馆',
                '聆听',
                '锁匠',
                '机械维修',
                '医学',
                '博物',
                '导航',
                '神秘学',
                '操作重型机械',
                '说服',
                '精神分析',
                '心理学',
                '骑乘',
                '妙手',
                '侦查',
                '潜行',
                '游泳',
                '投掷',
                '追踪',
                '驯兽',
                '潜水',
                '爆破',
                '读唇',
                '催眠',
                '炮术',
                '母语'
            ]
        },
        'skillConfig': {
            'skipEnhance': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX',
                '克苏鲁神话',
                '信用'
            ],
            'forceMapping': [
                'SANMAX',
                'HPMAX',
                'MPMAX'
            ]
        },
        'init': {
            'STR': '3d6x5',
            'CON': '3d6x5',
            'SIZ': '(2d6+6)x5',
            'DEX': '3d6x5',
            'APP': '3d6x5',
            'INT': '(2d6+6)x5',
            'POW': '3d6x5',
            'EDU': '(2d6+6)x5',
            'LUC': '3d6x5'
        },
        'mapping': {
            '闪避': '{DEX}/2',
            '母语': '{EDU}',
            'SAN': '{POW}',
            'SANMAX': '{POW}',
            'HP': '({CON}+{SIZ})/10',
            'HPMAX': '({CON}+{SIZ})/10',
            'MP': '{POW}/5',
            'MPMAX': '{POW}/5'
        },
        'synonyms':{
            'STR': ['力量', 'STR'],
            'CON': ['体质', 'CON'],
            'SIZ': ['体型', 'SIZ'],
            'DEX': ['敏捷', 'DEX'],
            'APP': ['外貌', 'APP'],
            'INT': ['智力', 'INT'],
            'POW': ['意志', 'POW'],
            'EDU': ['教育', 'EDU'],
            'LUC': ['幸运', 'LUC'],
            'SAN': ['理智', 'SAN','Sanity'],
            'SANMAX': ['理智上限', 'SANMAX','SanityMAX'],
            'HP': ['生命值','HP','HitPoints'],
            'HPMAX': ['生命值上限','HPMAX','HitPointsMAX'],
            'MP': ['魔法','MP','MagicPoints'],
            'MPMAX': ['魔法上限','MPMAX','MagicPointsMAX'],
            'MOV': ['移动力','MOV'],
            '会计': ['会计','Accounting'],
            '人类学': ['人类学','Anthropology'],
            '估价': ['估价','Aooraise'],
            '考古学': ['考古学','Archaeology'],
            '取悦': ['取悦','魅惑','Charm'],
            '攀爬': ['攀爬','Climb'],
            '计算机使用': ['计算机使用','计算机','电脑','电脑使用','Computer_Use'],
            '信用': ['信用评级','CR','信誉','信用度','信用','信誉度','Credit_Rating'],
            '克苏鲁神话': ['克苏鲁神话','CM','克苏鲁','Cthulhu_Mythos'],
            '乔装': ['乔装','Disguise'],
            '闪避': ['闪避','Dodge'],
            '汽车驾驶': ['汽车驾驶','Drive_Auto'],
            '电气维修': ['电气维修','电器维修','Electical_Repair'],
            '电子学': ['电子学','Electronics'],
            '话术': ['话术','快速交谈','Fast_Talk'],
            '急救': ['急救','First_Aid'],
            '历史': ['历史','History'],
            '恐吓': ['恐吓','Intimidate'],
            '跳跃': ['跳跃','Jump'],
            '法律': ['法律','Law'],
            '图书馆': ['图书馆使用','图书馆','Library_Use'],
            '聆听': ['聆听','Listen'],
            '锁匠': ['锁匠','Locksmith'],
            '机械维修': ['机械维修','Mechanical_Repair'],
            '医学': ['医学','Medicine'],
            '博物': ['博物', '博物学','自然学','自然史','Natural_World'],
            '导航': ['导航','领航','Navigate'],
            '神秘学': ['神秘学','Occult'],
            '操作重型机械': ['操作重型机械','Operate_Heavy_Machinery'],
            '说服': ['说服','Persuade'],
            '精神分析': ['精神分析','Psychoanalysis'],
            '心理学': ['心理学','Psychology'],
            '骑乘': ['骑术','骑乘','Ride'],
            '妙手': ['妙手','Sleight_of_Hand'],
            '侦查': ['侦查','侦察','Spot_Hidden'],
            '潜行': ['潜行','Stealth'],
            '游泳': ['游泳','Swim'],
            '投掷': ['投掷','Throw'],
            '追踪': ['追踪','Track'],
            '驯兽': ['驯兽','Beast_Training'],
            '潜水': ['潜水','Diving'],
            '爆破': ['爆破','Demolitions'],
            '读唇': ['读唇','Read_Lips'],
            '催眠': ['催眠','Hypnosis'],
            '炮术': ['炮术','Artillery']
        },
        'redirect': {
            '力量': 'STR',
            '体质': 'CON',
            '体型': 'SIZ',
            '敏捷': 'DEX',
            '外貌': 'APP',
            '智力': 'INT',
            '意志': 'POW',
            '教育': 'EDU',
            '幸运': 'LUC',
            '理智': 'SAN',
        },
        'showName': {
            'STR': '力量',
            'CON': '体质',
            'SIZ': '体型',
            'DEX': '敏捷',
            'APP': '外貌',
            'INT': '智力',
            'POW': '意志',
            'EDU': '教育',
            'LUC': '幸运'
        },
        'defaultSkillValue': {
            '会计': 5,
            '人类学': 1,
            '估价': 5,
            '考古学': 1,
            '取悦': 15,
            '攀爬': 20,
            '计算机使用': 5,
            '信用': 0,
            '克苏鲁神话': 0,
            '乔装': 5,
            '汽车驾驶': 20,
            '电气维修': 10,
            '电子学': 1,
            '话术': 5,
            '急救': 30,
            '历史': 5,
            '恐吓': 15,
            '跳跃': 20,
            '法律': 5,
            '图书馆': 20,
            '聆听': 20,
            '锁匠': 1,
            '机械维修': 10,
            '医学': 1,
            '博物': 10,
            '导航': 10,
            '神秘学': 5,
            '操作重型机械': 1,
            '说服': 10,
            '精神分析': 1,
            '心理学': 10,
            '骑乘': 5,
            '妙手': 10,
            '侦查': 25,
            '潜行': 20,
            '游泳': 20,
            '投掷': 20,
            '追踪': 10,
            '驯兽': 5,
            '潜水': 1,
            '爆破': 1,
            '读唇': 1,
            '催眠': 1,
            '炮术': 1
        },
        'checkRules': {
            'default': {
                'checkList': [
                    'success',
                    'hardSuccess',
                    'extremeHardSuccess',
                    'greatSuccess',
                    'fail',
                    'greatFail'
                ],
                'success': {
                    '.<=': ['$roll', '$skill']
                },
                'fail': {
                    '.>': ['$roll', '$skill']
                },
                'hardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 2]
                        }
                    ]
                },
                'extremeHardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 5]
                        }
                    ]
                },
                'greatSuccess': {
                    '.==': ['$roll', 1]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    },
    'COC7': {
        'mainDice': '1D100',
        'customDefault': {
            'd': {
                'leftD': 1,
                'rightD': 100,
                'sub': {
                    'k': None,
                    'q': None,
                    'p': None,
                    'b': None
                },
                'subD': {
                    'p': 1,
                    'b': 1
                }
            }
        },
        'skill': {
            '属性': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX'
            ],
            '技能': [
                '会计',
                '人类学',
                '估价',
                '考古学',
                '取悦',
                '攀爬',
                '计算机使用',
                '信用',
                '克苏鲁神话',
                '乔装',
                '闪避',
                '汽车驾驶',
                '电气维修',
                '电子学',
                '话术',
                '急救',
                '历史',
                '恐吓',
                '跳跃',
                '法律',
                '图书馆',
                '聆听',
                '锁匠',
                '机械维修',
                '医学',
                '博物',
                '导航',
                '神秘学',
                '操作重型机械',
                '说服',
                '精神分析',
                '心理学',
                '骑乘',
                '妙手',
                '侦查',
                '潜行',
                '游泳',
                '投掷',
                '追踪',
                '驯兽',
                '潜水',
                '爆破',
                '读唇',
                '催眠',
                '炮术',
                '母语'
            ]
        },
        'skillConfig': {
            'skipEnhance': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX',
                '克苏鲁神话',
                '信用'
            ],
            'forceMapping': [
                'SANMAX',
                'HPMAX',
                'MPMAX'
            ]
        },
        'init': {
            'STR': '3d6x5',
            'CON': '3d6x5',
            'SIZ': '(2d6+6)x5',
            'DEX': '3d6x5',
            'APP': '3d6x5',
            'INT': '(2d6+6)x5',
            'POW': '3d6x5',
            'EDU': '(2d6+6)x5',
            'LUC': '3d6x5'
        },
        'mapping': {
            '闪避': '{DEX}/2',
            '母语': '{EDU}',
            'SAN': '{POW}',
            'SANMAX': '{POW}',
            'HP': '({CON}+{SIZ})/10',
            'HPMAX': '({CON}+{SIZ})/10',
            'MP': '{POW}/5',
            'MPMAX': '{POW}/5'
        },
        'synonyms':{
            'STR': ['力量', 'STR'],
            'CON': ['体质', 'CON'],
            'SIZ': ['体型', 'SIZ'],
            'DEX': ['敏捷', 'DEX'],
            'APP': ['外貌', 'APP'],
            'INT': ['智力', 'INT'],
            'POW': ['意志', 'POW'],
            'EDU': ['教育', 'EDU'],
            'LUC': ['幸运', 'LUC'],
            'SAN': ['理智', 'SAN','Sanity'],
            'SANMAX': ['理智上限', 'SANMAX','SanityMAX'],
            'HP': ['生命值','HP','HitPoints'],
            'HPMAX': ['生命值上限','HPMAX','HitPointsMAX'],
            'MP': ['魔法','MP','MagicPoints'],
            'MPMAX': ['魔法上限','MPMAX','MagicPointsMAX'],
            'MOV': ['移动力','MOV'],
            '会计': ['会计','Accounting'],
            '人类学': ['人类学','Anthropology'],
            '估价': ['估价','Aooraise'],
            '考古学': ['考古学','Archaeology'],
            '取悦': ['取悦','魅惑','Charm'],
            '攀爬': ['攀爬','Climb'],
            '计算机使用': ['计算机使用','计算机','电脑','电脑使用','Computer_Use'],
            '信用': ['信用评级','CR','信誉','信用度','信用','信誉度','Credit_Rating'],
            '克苏鲁神话': ['克苏鲁神话','CM','克苏鲁','Cthulhu_Mythos'],
            '乔装': ['乔装','Disguise'],
            '闪避': ['闪避','Dodge'],
            '汽车驾驶': ['汽车驾驶','Drive_Auto'],
            '电气维修': ['电气维修','电器维修','Electical_Repair'],
            '电子学': ['电子学','Electronics'],
            '话术': ['话术','快速交谈','Fast_Talk'],
            '急救': ['急救','First_Aid'],
            '历史': ['历史','History'],
            '恐吓': ['恐吓','Intimidate'],
            '跳跃': ['跳跃','Jump'],
            '法律': ['法律','Law'],
            '图书馆': ['图书馆使用','图书馆','Library_Use'],
            '聆听': ['聆听','Listen'],
            '锁匠': ['锁匠','Locksmith'],
            '机械维修': ['机械维修','Mechanical_Repair'],
            '医学': ['医学','Medicine'],
            '博物': ['博物', '博物学','自然学','自然史','Natural_World'],
            '导航': ['导航','领航','Navigate'],
            '神秘学': ['神秘学','Occult'],
            '操作重型机械': ['操作重型机械','Operate_Heavy_Machinery'],
            '说服': ['说服','Persuade'],
            '精神分析': ['精神分析','Psychoanalysis'],
            '心理学': ['心理学','Psychology'],
            '骑乘': ['骑术','骑乘','Ride'],
            '妙手': ['妙手','Sleight_of_Hand'],
            '侦查': ['侦查','侦察','Spot_Hidden'],
            '潜行': ['潜行','Stealth'],
            '游泳': ['游泳','Swim'],
            '投掷': ['投掷','Throw'],
            '追踪': ['追踪','Track'],
            '驯兽': ['驯兽','Beast_Training'],
            '潜水': ['潜水','Diving'],
            '爆破': ['爆破','Demolitions'],
            '读唇': ['读唇','Read_Lips'],
            '催眠': ['催眠','Hypnosis'],
            '炮术': ['炮术','Artillery']
        },
        'redirect': {
            '力量': 'STR',
            '体质': 'CON',
            '体型': 'SIZ',
            '敏捷': 'DEX',
            '外貌': 'APP',
            '智力': 'INT',
            '意志': 'POW',
            '教育': 'EDU',
            '幸运': 'LUC',
            '理智': 'SAN',
        },
        'showName': {
            'STR': '力量',
            'CON': '体质',
            'SIZ': '体型',
            'DEX': '敏捷',
            'APP': '外貌',
            'INT': '智力',
            'POW': '意志',
            'EDU': '教育',
            'LUC': '幸运'
        },
        'defaultSkillValue': {
            '会计': 5,
            '人类学': 1,
            '估价': 5,
            '考古学': 1,
            '取悦': 15,
            '攀爬': 20,
            '计算机使用': 5,
            '信用': 0,
            '克苏鲁神话': 0,
            '乔装': 5,
            '汽车驾驶': 20,
            '电气维修': 10,
            '电子学': 1,
            '话术': 5,
            '急救': 30,
            '历史': 5,
            '恐吓': 15,
            '跳跃': 20,
            '法律': 5,
            '图书馆': 20,
            '聆听': 20,
            '锁匠': 1,
            '机械维修': 10,
            '医学': 1,
            '博物': 10,
            '导航': 10,
            '神秘学': 5,
            '操作重型机械': 1,
            '说服': 10,
            '精神分析': 1,
            '心理学': 10,
            '骑乘': 5,
            '妙手': 10,
            '侦查': 25,
            '潜行': 20,
            '游泳': 20,
            '投掷': 20,
            '追踪': 10,
            '驯兽': 5,
            '潜水': 1,
            '爆破': 1,
            '读唇': 1,
            '催眠': 1,
            '炮术': 1
        },
        'checkRules': {
            'default': {
                'checkList': [
                    'success',
                    'hardSuccess',
                    'extremeHardSuccess',
                    'greatSuccess',
                    'fail',
                    'greatFail'
                ],
                'success': {
                    '.<=': ['$roll', '$skill']
                },
                'fail': {
                    '.>': ['$roll', '$skill']
                },
                'hardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 2]
                        }
                    ]
                },
                'extremeHardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 5]
                        }
                    ]
                },
                'greatSuccess': {
                    '.==': ['$roll', 1]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C0': {
                'greatSuccess': {
                    '.==': ['$roll', 1]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C1': {
                'greatSuccess': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 1]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 1]
                                },
                                {
                                    '.<=': ['$roll', 5]
                                }
                            ]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C2': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': ['$roll', '$skill']
                        },
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 5]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.>': ['$roll', '$skill']
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.==': ['$roll', 100]
                        }
                    ]
                }
            },
            'C3': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 5]
                        }
                    ]
                },
                'greatFail': {
                    '.and': [
                        {
                            '.>=': ['$roll', 96],
                        },
                        {
                            '.<=': ['$roll', 100]
                        }
                    ]
                }
            },
            'C4': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': ['$roll', {'./': ['$skill', 10]}]
                        },
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 5]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': [
                                        '$roll',
                                        {
                                            '.+': [
                                                96,
                                                {
                                                    './': ['$skill', 10]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C5': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': [
                                '$roll',
                                {
                                    './': ['$skill', 5]
                                }
                            ]
                        },
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 2]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 99]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C6': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 3]
                        }
                    ]
                },
                'greatFail': {
                    '.and': [
                        {
                            '.>=': ['$roll', 98],
                        },
                        {
                            '.<=': ['$roll', 100]
                        }
                    ]
                }
            },
            'DeltaGreen': {
                'success': {
                    '.<=': ['$roll', '$skill']
                },
                'fail': {
                    '.>': ['$roll', '$skill']
                },
                'hardSuccess': None,
                'extremeHardSuccess': None,
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': ['$roll', '$skill']
                        },
                        {
                            '.or': [
                                {
                                    '.==': ['$roll', 1],
                                },
                                {
                                    '.==': [{'.%': ['$roll', 11]}, 0]
                                }
                            ]
                        }
                    ]
                },
                'greatFail': {
                    '.and': [
                        {
                            '.>': ['$roll', '$skill']
                        },
                        {
                            '.or': [
                                {
                                    '.==': ['$roll', 100],
                                },
                                {
                                    '.==': [
                                        {
                                            '.%': ['$roll', 11]
                                        },
                                        0
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    },
    '纯净COC7': {
        'mainDice': '1D100',
        'customDefault': {
            'd': {
                'leftD': 1,
                'rightD': 100,
                'sub': {
                    'k': None,
                    'q': None,
                    'p': None,
                    'b': None
                },
                'subD': {
                    'p': 1,
                    'b': 1
                }
            }
        },
        'skill': {
            '属性': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX'
            ],
            '技能': [
                '会计',
                '人类学',
                '估价',
                '考古学',
                '取悦',
                '攀爬',
                '计算机使用',
                '信用',
                '克苏鲁神话',
                '乔装',
                '闪避',
                '汽车驾驶',
                '电气维修',
                '电子学',
                '话术',
                '急救',
                '历史',
                '恐吓',
                '跳跃',
                '法律',
                '图书馆',
                '聆听',
                '锁匠',
                '机械维修',
                '医学',
                '博物',
                '导航',
                '神秘学',
                '操作重型机械',
                '说服',
                '精神分析',
                '心理学',
                '骑乘',
                '妙手',
                '侦查',
                '潜行',
                '游泳',
                '投掷',
                '追踪',
                '驯兽',
                '潜水',
                '爆破',
                '读唇',
                '催眠',
                '炮术',
                '母语'
            ]
        },
        'skillConfig': {
            'skipEnhance': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX',
                '克苏鲁神话',
                '信用'
            ],
            'forceMapping': [
                'SANMAX',
                'HPMAX',
                'MPMAX'
            ]
        },
        'init': {
            'STR': '3d6x5',
            'CON': '3d6x5',
            'SIZ': '(2d6+6)x5',
            'DEX': '3d6x5',
            'APP': '3d6x5',
            'INT': '(2d6+6)x5',
            'POW': '3d6x5',
            'EDU': '(2d6+6)x5',
            'LUC': '3d6x5'
        },
        'mapping': {
            'SAN': '{POW}',
            'SANMAX': '{POW}',
            'HP': '({CON}+{SIZ})/10',
            'HPMAX': '({CON}+{SIZ})/10',
            'MP': '{POW}/5',
            'MPMAX': '{POW}/5'
        },
        'synonyms':{
            'STR': ['力量', 'STR'],
            'CON': ['体质', 'CON'],
            'SIZ': ['体型', 'SIZ'],
            'DEX': ['敏捷', 'DEX'],
            'APP': ['外貌', 'APP'],
            'INT': ['智力', 'INT'],
            'POW': ['意志', 'POW'],
            'EDU': ['教育', 'EDU'],
            'LUC': ['幸运', 'LUC'],
            'SAN': ['理智', 'SAN','Sanity'],
            'SANMAX': ['理智上限', 'SANMAX','SanityMAX'],
            'HP': ['生命值','HP','HitPoints'],
            'HPMAX': ['生命值上限','HPMAX','HitPointsMAX'],
            'MP': ['魔法','MP','MagicPoints'],
            'MPMAX': ['魔法上限','MPMAX','MagicPointsMAX'],
            'MOV': ['移动力','MOV'],
            '会计': ['会计','Accounting'],
            '人类学': ['人类学','Anthropology'],
            '估价': ['估价','Aooraise'],
            '考古学': ['考古学','Archaeology'],
            '取悦': ['取悦','魅惑','Charm'],
            '攀爬': ['攀爬','Climb'],
            '计算机使用': ['计算机使用','计算机','电脑','电脑使用','Computer_Use'],
            '信用': ['信用评级','CR','信誉','信用度','信用','信誉度','Credit_Rating'],
            '克苏鲁神话': ['克苏鲁神话','CM','克苏鲁','Cthulhu_Mythos'],
            '乔装': ['乔装','Disguise'],
            '闪避': ['闪避','Dodge'],
            '汽车驾驶': ['汽车驾驶','Drive_Auto'],
            '电气维修': ['电气维修','电器维修','Electical_Repair'],
            '电子学': ['电子学','Electronics'],
            '话术': ['话术','快速交谈','Fast_Talk'],
            '急救': ['急救','First_Aid'],
            '历史': ['历史','History'],
            '恐吓': ['恐吓','Intimidate'],
            '跳跃': ['跳跃','Jump'],
            '法律': ['法律','Law'],
            '图书馆': ['图书馆使用','图书馆','Library_Use'],
            '聆听': ['聆听','Listen'],
            '锁匠': ['锁匠','Locksmith'],
            '机械维修': ['机械维修','Mechanical_Repair'],
            '医学': ['医学','Medicine'],
            '博物': ['博物', '博物学','自然学','自然史','Natural_World'],
            '导航': ['导航','领航','Navigate'],
            '神秘学': ['神秘学','Occult'],
            '操作重型机械': ['操作重型机械','Operate_Heavy_Machinery'],
            '说服': ['说服','Persuade'],
            '精神分析': ['精神分析','Psychoanalysis'],
            '心理学': ['心理学','Psychology'],
            '骑乘': ['骑术','骑乘','Ride'],
            '妙手': ['妙手','Sleight_of_Hand'],
            '侦查': ['侦查','侦察','Spot_Hidden'],
            '潜行': ['潜行','Stealth'],
            '游泳': ['游泳','Swim'],
            '投掷': ['投掷','Throw'],
            '追踪': ['追踪','Track'],
            '驯兽': ['驯兽','Beast_Training'],
            '潜水': ['潜水','Diving'],
            '爆破': ['爆破','Demolitions'],
            '读唇': ['读唇','Read_Lips'],
            '催眠': ['催眠','Hypnosis'],
            '炮术': ['炮术','Artillery']
        },
        'redirect': {
            '力量': 'STR',
            '体质': 'CON',
            '体型': 'SIZ',
            '敏捷': 'DEX',
            '外貌': 'APP',
            '智力': 'INT',
            '意志': 'POW',
            '教育': 'EDU',
            '幸运': 'LUC',
            '理智': 'SAN',
        },
        'showName': {
            'STR': '力量',
            'CON': '体质',
            'SIZ': '体型',
            'DEX': '敏捷',
            'APP': '外貌',
            'INT': '智力',
            'POW': '意志',
            'EDU': '教育',
            'LUC': '幸运'
        },
        'defaultSkillValue': {},
        'checkRules': {
            'default': {
                'checkList': [
                    'success',
                    'hardSuccess',
                    'extremeHardSuccess',
                    'greatSuccess',
                    'fail',
                    'greatFail'
                ],
                'success': {
                    '.<=': ['$roll', '$skill']
                },
                'fail': {
                    '.>': ['$roll', '$skill']
                },
                'hardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 2]
                        }
                    ]
                },
                'extremeHardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 5]
                        }
                    ]
                },
                'greatSuccess': {
                    '.==': ['$roll', 1]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C0': {
                'greatSuccess': {
                    '.==': ['$roll', 1]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C1': {
                'greatSuccess': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 1]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 1]
                                },
                                {
                                    '.<=': ['$roll', 5]
                                }
                            ]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C2': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': ['$roll', '$skill']
                        },
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 5]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.>': ['$roll', '$skill']
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.==': ['$roll', 100]
                        }
                    ]
                }
            },
            'C3': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 5]
                        }
                    ]
                },
                'greatFail': {
                    '.and': [
                        {
                            '.>=': ['$roll', 96],
                        },
                        {
                            '.<=': ['$roll', 100]
                        }
                    ]
                }
            },
            'C4': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': ['$roll', {'./': ['$skill', 10]}]
                        },
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 5]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': [
                                        '$roll',
                                        {
                                            '.+': [
                                                96,
                                                {
                                                    './': ['$skill', 10]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.==': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C5': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': [
                                '$roll',
                                {
                                    './': ['$skill', 5]
                                }
                            ]
                        },
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 2]
                        }
                    ]
                },
                'greatFail': {
                    '.or': [
                        {
                            '.and': [
                                {
                                    '.<': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 96]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        },
                        {
                            '.and': [
                                {
                                    '.>=': ['$skill', 50]
                                },
                                {
                                    '.>=': ['$roll', 99]
                                },
                                {
                                    '.<=': ['$roll', 100]
                                }
                            ]
                        }
                    ]
                }
            },
            'C6': {
                'greatSuccess': {
                    '.and': [
                        {
                            '.>=': ['$roll', 1]
                        },
                        {
                            '.<=': ['$roll', 3]
                        }
                    ]
                },
                'greatFail': {
                    '.and': [
                        {
                            '.>=': ['$roll', 98],
                        },
                        {
                            '.<=': ['$roll', 100]
                        }
                    ]
                }
            },
            'DeltaGreen': {
                'success': {
                    '.<=': ['$roll', '$skill']
                },
                'fail': {
                    '.>': ['$roll', '$skill']
                },
                'hardSuccess': None,
                'extremeHardSuccess': None,
                'greatSuccess': {
                    '.and': [
                        {
                            '.<=': ['$roll', '$skill']
                        },
                        {
                            '.or': [
                                {
                                    '.==': ['$roll', 1],
                                },
                                {
                                    '.==': [{'.%': ['$roll', 11]}, 0]
                                }
                            ]
                        }
                    ]
                },
                'greatFail': {
                    '.and': [
                        {
                            '.>': ['$roll', '$skill']
                        },
                        {
                            '.or': [
                                {
                                    '.==': ['$roll', 100],
                                },
                                {
                                    '.==': [
                                        {
                                            '.%': ['$roll', 11]
                                        },
                                        0
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    },
    'COC6': {
        'mainDice': '1D100',
        'customDefault': {
            'd': {
                'leftD': 1,
                'rightD': 100,
                'sub': {
                    'k': None,
                    'q': None,
                    'p': None,
                    'b': None
                },
                'subD': {
                    'p': 1,
                    'b': 1
                }
            }
        },
        'skill': {
            '属性': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX',
                'IDEA',
                'KNOW'
            ],
            '技能': [
                '会计',
                '人类学',
                '估价',
                '考古学',
                '取悦',
                '攀爬',
                '计算机使用',
                '信用',
                '克苏鲁神话',
                '乔装',
                '闪避',
                '汽车驾驶',
                '电气维修',
                '电子学',
                '话术',
                '急救',
                '历史',
                '恐吓',
                '跳跃',
                '法律',
                '图书馆',
                '聆听',
                '锁匠',
                '机械维修',
                '医学',
                '博物',
                '导航',
                '神秘学',
                '操作重型机械',
                '说服',
                '精神分析',
                '心理学',
                '骑乘',
                '妙手',
                '侦查',
                '潜行',
                '游泳',
                '投掷',
                '追踪',
                '驯兽',
                '潜水',
                '爆破',
                '读唇',
                '催眠',
                '炮术'
            ]
        },
        'skillConfig': {
            'skipEnhance': [
                'STR',
                'CON',
                'SIZ',
                'DEX',
                'APP',
                'INT',
                'POW',
                'EDU',
                'LUC',
                'SAN',
                'SANMAX',
                'HP',
                'HPMAX',
                'MP',
                'MPMAX',
                '克苏鲁神话',
                '信用'
            ],
            'forceMapping': [
                'SANMAX',
                'HPMAX',
                'MPMAX'
            ]
        },
        'init': {
            'STR': '3d6',
            'CON': '3d6',
            'SIZ': '2d6+6',
            'DEX': '3d6',
            'APP': '3d6',
            'INT': '2d6+6',
            'POW': '3d6',
            'EDU': '2d6+6'
        },
        'mapping': {
            'SAN': '{POW}*5',
            'HP': '({CON}+{SIZ})/2',
            'HPMAX': '({CON}+{SIZ})/2',
            'MP': '{POW}',
            'MPMAX': '{POW}',
            'LUC': '{POW}*5',
            'IDEA': '{INT}*5',
            'KNOW': '{EDU}*5'
        },
        'synonyms':{
            'STR': ['力量', 'STR'],
            'CON': ['体质', 'CON'],
            'SIZ': ['体型', 'SIZ'],
            'DEX': ['敏捷', 'DEX'],
            'APP': ['外貌', 'APP'],
            'INT': ['智力', 'INT'],
            'POW': ['意志', 'POW'],
            'EDU': ['教育', 'EDU'],
            'LUC': ['幸运', 'LUC'],
            'SAN': ['理智', 'SAN', 'Sanity'],
            'SANMAX': ['理智上限', 'SANMAX', 'SanityMAX'],
            'HP': ['生命值','HP', 'HitPoints'],
            'HPMAX': ['生命值上限','HPMAX', 'HitPointsMAX'],
            'MP': ['魔法','MP', 'MagicPoints'],
            'MPMAX': ['魔法上限','MPMAX', 'MagicPointsMAX'],
            'IDEA': ['灵感', 'IDEA'],
            'KNOW': ['知识', 'KNOW'],
            'MOV': ['移动力','MOV'],
            '会计': ['会计','Accounting'],
            '人类学': ['人类学','Anthropology'],
            '估价': ['估价','Aooraise'],
            '考古学': ['考古学','Archaeology'],
            '取悦': ['取悦','魅惑','Charm'],
            '攀爬': ['攀爬','Climb'],
            '计算机使用': ['计算机使用','计算机','电脑','电脑使用','Computer_Use'],
            '信用': ['信用评级','CR','信誉','信用度','信用','信誉度','Credit_Rating'],
            '克苏鲁神话': ['克苏鲁神话','CM','克苏鲁','Cthulhu_Mythos'],
            '乔装': ['乔装','Disguise'],
            '闪避': ['闪避','Dodge'],
            '汽车驾驶': ['汽车驾驶','Drive_Auto'],
            '电气维修': ['电气维修','电器维修','Electical_Repair'],
            '电子学': ['电子学','Electronics'],
            '话术': ['话术','快速交谈','Fast_Talk'],
            '急救': ['急救','First_Aid'],
            '历史': ['历史','History'],
            '恐吓': ['恐吓','Intimidate'],
            '跳跃': ['跳跃','Jump'],
            '法律': ['法律','Law'],
            '图书馆': ['图书馆使用','图书馆','Library_Use'],
            '聆听': ['聆听','Listen'],
            '锁匠': ['锁匠','Locksmith'],
            '机械维修': ['机械维修','Mechanical_Repair'],
            '医学': ['医学','Medicine'],
            '博物': ['博物', '博物学','自然学','自然史','Natural_World'],
            '导航': ['导航','领航','Navigate'],
            '神秘学': ['神秘学','Occult'],
            '操作重型机械': ['操作重型机械','Operate_Heavy_Machinery'],
            '说服': ['说服','Persuade'],
            '精神分析': ['精神分析','Psychoanalysis'],
            '心理学': ['心理学','Psychology'],
            '骑乘': ['骑术','骑乘','Ride'],
            '妙手': ['妙手','Sleight_of_Hand'],
            '侦查': ['侦查','侦察','Spot_Hidden'],
            '潜行': ['潜行','Stealth'],
            '游泳': ['游泳','Swim'],
            '投掷': ['投掷','Throw'],
            '追踪': ['追踪','Track'],
            '驯兽': ['驯兽','Beast_Training'],
            '潜水': ['潜水','Diving'],
            '爆破': ['爆破','Demolitions'],
            '读唇': ['读唇','Read_Lips'],
            '催眠': ['催眠','Hypnosis'],
            '炮术': ['炮术','Artillery']
        },
        'redirect': {
            '力量': 'STR',
            '体质': 'CON',
            '体型': 'SIZ',
            '敏捷': 'DEX',
            '外貌': 'APP',
            '智力': 'INT',
            '意志': 'POW',
            '教育': 'EDU',
            '幸运': 'LUC',
            '理智': 'SAN',
            '灵感': 'IDEA',
            '知识': 'KNOW'
        },
        'showName': {
            'STR': '力量',
            'CON': '体质',
            'SIZ': '体型',
            'DEX': '敏捷',
            'APP': '外貌',
            'INT': '智力',
            'POW': '意志',
            'EDU': '教育',
            'LUC': '幸运',
            'IDEA': '灵感',
            'KNOW': '知识'
        },
        'checkRules': {
            'default': {
                'checkList': [
                    'success',
                    'hardSuccess',
                    'extremeHardSuccess',
                    'greatSuccess',
                    'fail',
                    'greatFail'
                ],
                'success': {
                    '.<=': ['$roll', '$skill']
                },
                'fail': {
                    '.>': ['$roll', '$skill']
                },
                'hardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 2]
                        }
                    ]
                },
                'extremeHardSuccess': {
                    '.<=': [
                        '$roll',
                        {
                            './': ['$skill', 5]
                        }
                    ]
                },
                'greatSuccess': {
                    '.<=': ['$roll', 5]
                },
                'greatFail': {
                    '.>=': ['$roll', 96]
                },
            }
        }
    },
    'DND5E': {
        'mainDice': '1D20',
        'customDefault': {
            'd': {
                'leftD': 1,
                'rightD': 20,
                'sub': {
                    'k': None,
                    'q': None,
                    'p': None,
                    'b': None
                },
                'subD': {
                    'p': 1,
                    'b': 1
                }
            }
        },
        'skill': {
            '属性': [
                'STR',
                'DEX',
                'CON',
                'INT',
                'WIS',
                'CHA',
                '速度',
                '先攻'
            ],
            '状态': [
                '载重',
                '负重',
                '护甲等级'
            ],
            '技能': [
                '运动',
                '体操',
                '巧手',
                '隐匿',
                '调查',
                '奥秘',
                '历史',
                '自然',
                '宗教',
                '察觉',
                '洞悉',
                '驯兽',
                '医药',
                '生存',
                '游说',
                '欺瞒',
                '威吓',
                '表演'
            ],
            '物品': [
                '金币',
                '银币',
                '铜币',
                '铂金币',
                '白金币'
            ],
            '法术': [
                '亚比达奇凋死术',
                '吸收元素',
                '强酸箭',
                '酸液飞溅',
                '阿迦纳萨喷火术',
                '援助术',
                '警报术',
                '变身术',
                '化兽为友',
                '动物信使',
                '动物形态',
                '操纵死尸',
                '活化物体',
                '防生物护罩',
                '反魔场',
                '关怀术',
                '嫌恶',
                '秘法眼',
                '秘法门',
                '秘法魔掌',
                '秘法锁',
                '秘法武器',
                '秘法师魔法灵光',
                '艾嘉西斯之铠',
                '哈达之臂',
                '星界投影',
                '卜筮术',
                '生命灵光',
                '净化灵光',
                '活力灵光',
                '启蒙术'
            ]
        },
        'skillConfig': {
            'skipEnhance': [
                'STR',
                'DEX',
                'CON',
                'INT',
                'WIS',
                'CHA'
            ]
        },
        'init': {
            'STR': '4d6k3',
            'DEX': '4d6k3',
            'CON': '4d6k3',
            'INT': '4d6k3',
            'WIS': '4d6k3',
            'CHA': '4d6k3'
        },
        'synonyms':{
            'STR': ['力量', 'STR', 'Strength'],
            'DEX': ['敏捷', 'DEX', 'Dexterity'],
            'CON': ['体质', 'CON', 'Constitution'],
            'INT': ['智力', 'INT', 'Intelligence'],
            'WIS': ['感知', 'WIS', 'Wisdom'],
            'CHA': ['魅力', 'CHA', 'Charisma'],
            '运动': ['运动', 'Athletics'],
            '先攻': ['先攻', 'Initiative'],
            '速度': ['速度', 'Speed'],

            '体操': ['体操', 'Acrobatics'],
            '巧手': ['Sleight_of_Hand', '巧手', '手上功夫'],
            '隐匿': ['Stealth', '隐匿'],
            '奥秘': ['Arcana', '奥秘'],
            '历史': ['History', '历史'],
            '调查': ['Investigate', '调查'],
            '自然': ['Nature', '自然'],
            '宗教': ['Religion', '宗教'],
            '驯兽': ['Animal_Handling', '动物驯养', '驯兽'],
            '洞悉': ['Insight', '洞悉'],
            '医药': ['Medicine', '医药'],
            '观察': ['Perception', '察觉', '观察'],
            '生存': ['Survival', '生存', '求生'],
            '欺瞒': ['Deception', '欺瞒'],
            '威吓': ['Intimidation', '威吓'],
            '表演': ['Performance', '表演'],
            '游说': ['Persuasion', '游说'],

            '载重': ['载重', 'Carring_Capacity'],
            '负重': ['负重', 'Encumbrance'],
            '护甲等级': ['AC', 'Armor_Class', '护甲等级'],

            '金币': ['Gold_Piece', '金币', 'GP'],
            '银币': ['Silver_Piece', '银币', 'SP'],
            '铜币': ['Copper_Piece', 'CP', '铜币'],
            '铂金币': ['Electrum_Piece', '铂金币', 'EP'],
            '白金币': ['Platium_Piece', '白金币', 'PP'],

            '亚比达奇凋死术': ['亚比达奇凋死术', 'ABI_DALZIM_S_HORRID_WILTING'],
            '吸收元素': ['吸收元素', 'ABSORB_ELEMENTS'],
            '强酸箭': ['强酸箭', 'ACID_ARROW'],
            '酸液飞溅': ['酸液飞溅', 'ACID_SPLASH'],
            '阿迦纳萨喷火术': ['阿迦纳萨喷火术', 'AGANAZZAR_S_SCORCHER'],
            '援助术': ['援助术', 'AID'],
            '警报术': ['警报术', 'ALARM'],
            '变身术': ['变身术', 'ALTER_SELF'],
            '化兽为友': ['化兽为友', 'ANIMAL_FRIENDSHIP'],
            '动物信使': ['动物信使', 'ANIMAL_MESSENGER'],
            '动物形态': ['动物形态', 'ANIMAL_SHAPES'],
            '操纵死尸': ['操纵死尸', 'ANIMATE_DEAD'],
            '活化物体': ['活化物体', 'ANIMATE_OBJECTS'],
            '防生物护罩': ['防生物护罩', 'ANTILIFE_SHELL'],
            '反魔场': ['反魔场', 'ANTIMAGIC_FIELD'],
            '关怀术': ['关怀术', 'ANTIPATHY'],
            '嫌恶': ['嫌恶', 'SYMPATHY'],
            '秘法眼': ['秘法眼', 'ARCANE_EYE'],
            '秘法门': ['秘法门', 'ARCANE_GATE'],
            '秘法魔掌': ['秘法魔掌', 'ARCANE_HAND'],
            '秘法锁': ['秘法锁', 'ARCANE_LOCK'],
            '秘法武器': ['秘法武器', 'ARCANE_WEAPON'],
            '秘法师魔法灵光': ['秘法师魔法灵光', 'ARCANIST_S_MAGIC_AURA'],
            '艾嘉西斯之铠': ['艾嘉西斯之铠', 'ARMOR_OF_AGATHYS'],
            '哈达之臂': ['哈达之臂', 'ARMS_OF_HADAR'],
            '星界投影': ['星界投影', 'ASTRAL_PROJECTION'],
            '卜筮术': ['卜筮术', 'AUGURY'],
            '生命灵光': ['生命灵光', 'AURA_OF_LIFE'],
            '净化灵光': ['净化灵光', 'AURA_OF_PURITY'],
            '活力灵光': ['活力灵光', 'AURA_OF_VITALITY'],
            '启蒙术': ['启蒙术', 'AWAKEN']
        },
        'showName': {
            'STR': '力量',
            'DEX': '敏捷',
            'CON': '体质',
            'INT': '智力',
            'WIS': '感知',
            'CHA': '魅力',
        },
        'checkRules': {
            'default': {
                'checkList': [
                    'greatSuccess',
                    'greatFail'
                ],
                'greatSuccess': {
                    '.>=': ['$roll', 20]
                },
                'greatFail': {
                    '.<=': ['$roll', 1]
                }
            }
        }
    },
    'DX3': {
        'mainDice': '10C8',
        'mainDiceAdvance': '{skill}C8',
        'customDefault': {
        },
        'checkRules': {
            'default': {
                'checkList': []
            }
        }
    },
    'FATE': {
        'mainDice': 'F',
        'customDefault': {
            'f': {
                'leftD': 4,
                'rightD': 3
            }
        },
        'checkRules': {
            'default': {
                'checkList': [
                    'fate01',
                    'fate02',
                    'fate03',
                    'fate04',
                    'fate05',
                    'fate06',
                    'fate07',
                    'fate08',
                    'fate09',
                    'fate10',
                    'fate11'
                ],
                'fate01': {
                    '.<=': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        -2
                    ]
                },
                'fate02': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        -1
                    ]
                },
                'fate03': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        0
                    ]
                },
                'fate04': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        1
                    ]
                },
                'fate05': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        2
                    ]
                },
                'fate06': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        3
                    ]
                },
                'fate07': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        4
                    ]
                },
                'fate08': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        5
                    ]
                },
                'fate09': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        6
                    ]
                },
                'fate10': {
                    '.==': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        7
                    ]
                },
                'fate11': {
                    '.>=': [
                        {
                            '.+': ['$roll', '$skill']
                        },
                        8
                    ]
                }
            }
        }
    }
}

# 特殊处理方法表
dictPcCardMappingSpecial = {
    'default': ['体格', 'DB'],
    'COC7': ['体格', 'DB']
}
