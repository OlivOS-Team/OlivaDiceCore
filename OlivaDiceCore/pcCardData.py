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

dictPcCardTemplateDefault = {
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
                'HP',
                'MP'
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
                'HP',
                'MP',
                '克苏鲁神话',
                '信用'
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
            'HP': '({CON}+{SIZ})/10',
            'MP': '{POW}/5'
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
            'HP': ['生命值','HP','HitPoints'],
            'MP': ['魔法','MP','MagicPoints'],
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
            '侦查': ['侦查','Spot_Hidden'],
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
                'HP',
                'MP'
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
                'HP',
                'MP',
                '克苏鲁神话',
                '信用'
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
            'HP': '({CON}+{SIZ})/10',
            'MP': '{POW}/5'
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
            'HP': ['生命值','HP','HitPoints'],
            'MP': ['魔法','MP','MagicPoints'],
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
            '侦查': ['侦查','Spot_Hidden'],
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
                    '.and': {
                        '.<=': ['$roll', {'./': ['$skill', 10]}],
                        '.>=': ['$roll', 1],
                        '.<=': ['$roll', 5]
                    }
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
        'init': {
            'STR': '4d6k3',
            'DEX': '4d6k3',
            'CON': '4d6k3',
            'INT': '4d6k3',
            'POW': '4d6k3',
            'APP': '4d6k3'
        },
        'synonyms':{
            'STR': ['力量', 'STR'],
            'DEX': ['敏捷', 'DEX'],
            'CON': ['体质', 'CON'],
            'INT': ['智力', 'INT'],
            'POW': ['感知', 'POW'],
            'APP': ['魅力', 'APP'],
            'ABI-DALZIM’S_HORRID_WILTING':['亚比达奇凋死术','ABI-DALZIM’S_HORRID_WILTING'],
            'ABSORB_ELEMENTS':['吸收元素','ABSORB_ELEMENTS'],
            'ACID_ARROW':['强酸箭','ACID_ARROW'],
            'ACID_SPLASH':['酸液飞溅','ACID_SPLASH'],
            'AGANAZZAR’S_SCORCHER':['阿迦纳萨喷火术','AGANAZZAR’S_SCORCHER'],
            'AID':['援助术','AID'],
            'ALARM':['警报术','ALARM'],
            'ALTER_SELF':['变身术','ALTER_SELF'],
            'ANIMAL_FRIENDSHIP':['化兽为友','ANIMAL_FRIENDSHIP'],
            'ANIMAL_MESSENGER':['动物信使','ANIMAL_MESSENGER'],
            'ANIMAL_SHAPES':['动物形态','ANIMAL_SHAPES'],
            'ANIMATE_DEAD':['操纵死尸','ANIMATE_DEAD'],
            'ANIMATE_OBJECTS':['活化物体','ANIMATE_OBJECTS'],
            'ANTILIFE_SHELL':['防生物护罩','ANTILIFE_SHELL'],
            'ANTIMAGIC_FIELD':['反魔场','ANTIMAGIC_FIELD'],
            'ANTIPATHY':['关怀术','ANTIPATHY'],
            'SYMPATHY':['嫌恶','SYMPATHY'],
            'ARCANE_EYE':['秘法眼','ARCANE_EYE'],
            'ARCANE_GATE':['秘法门','ARCANE_GATE'],
            'ARCANE_HAND':['秘法魔掌','ARCANE_HAND'],
            'ARCANE_LOCK':['秘法锁','ARCANE_LOCK'],
            'ARCANE_WEAPON':['秘法武器','ARCANE_WEAPON'],
            "ARCANIST'S_MAGIC_AURA":['秘法师魔法灵光',"ARCANIST'S_MAGIC_AURA"],
            'ARMOR_OF_AGATHYS':['艾嘉西斯之铠','ARMOR_OF_AGATHYS'],
            'ARMS_OF_HADAR':['哈达之臂','ARMS_OF_HADAR'],
            'ASTRAL_PROJECTION':['星界投影','ASTRAL_PROJECTION'],
            'AUGURY':['卜筮术','AUGURY'],
            'AURA_OF_LIFE':['生命灵光','AURA_OF_LIFE'],
            'AURA_OF_PURITY':['净化灵光','AURA_OF_PURITY'],
            'AURA_OF_VITALITY':['活力灵光','AURA_OF_VITALITY'],
            'AWAKEN':['启蒙术','AWAKEN'],
        },
        'showName': {
            'STR': '力量',
            'DEX': '敏捷',
            'CON': '体质',
            'INT': '智力',
            'POW': '感知',
            'APP': '魅力',
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
