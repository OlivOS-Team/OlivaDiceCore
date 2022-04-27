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
            'SAN': ['理智', 'SAN']
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
            'SAN': ['理智', 'SAN']
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
            'APP': ['魅力', 'APP']
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
