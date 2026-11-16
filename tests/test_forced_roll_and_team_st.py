import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import OlivaDiceCore as core


class ForcedRollPrefixTests(unittest.TestCase):
    def test_prefix_table(self):
        cases = [
            ('(5) 魅惑', 5, '魅惑'),
            ('(5)魅惑', 5, '魅惑'),
            ('( 5 ) 魅惑', 5, '魅惑'),
            ('(5)+魅惑', None, '(5)+魅惑'),
            ('(5) +7', None, '(5) +7'),
            ('(-5)+7+魅惑', None, '(-5)+7+魅惑'),
            ('(1)(-5)+7+魅惑', 1, '(-5)+7+魅惑'),
            ('(-4)(23)+(魅惑)+7+魅惑', 1, '(23)+(魅惑)+7+魅惑'),
            ('(0) 魅惑', 1, '魅惑'),
            ('(5.5) 魅惑', None, '(5.5) 魅惑'),
            ('(+5) 魅惑', None, '(+5) 魅惑'),
            ('(5)(3) 魅惑', 5, '(3) 魅惑'),
            ('  (123456)  ', 123456, ''),
        ]
        for text, forced, rest in cases:
            with self.subTest(text=text):
                self.assertEqual(core.msgReplyModel.parse_forced_roll_prefix(text), (forced, rest))

    def test_real_dice_short_format(self):
        dice = core.onedice.RD('33+5')
        dice.roll()
        detail = core.onediceOverride.RDDataFormat(data=dice.resDetailData, mode='short')
        expected = f'33+5={detail}=38' if detail else '33+5=38'
        self.assertEqual(core.msgReplyModel.format_skill_update_roll('33+5', dice), expected)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.patches = [
            patch.object(core.data, 'dataDirRoot', self.temp.name.replace('\\', '/')),
            patch.object(core.pcCard, 'dictPcCardData', {'unity': {}}),
            patch.object(core.pcCardData, 'dictPcCardTemplateDefault',
                         copy.deepcopy(core.pcCardData.dictPcCardTemplateDefaultTemp)),
            patch.object(core.pcCard, 'dictPcCardTemplateDefault', {'unity': {}}),
            patch.object(core.pcCard, 'dictPcCardSelection', {'unity': {}}),
            patch.object(core.pcCard, 'dictPcCardTemplate', {'unity': {}}),
            patch.object(core.pcCard, 'dictPcCardHiy', {'unity': {}}),
            patch.object(core.pcCard, 'dictPcCardMH', {'unity': {}}),
            patch.object(core.console, 'dictConsoleSwitch', {}),
            patch.object(core.msgCustom, 'dictStrCustomDict', {'bot': core.msgCustom.dictStrCustom.copy()}),
            patch.object(core.userConfig, 'setMsgCount'),
            patch.object(core.userConfig, 'setUserConfigByKey'),
            patch.object(core.userConfig, 'releaseUnityMsgCount'),
            patch.object(core.ordinaryInviteManager, 'isInMasterList', return_value=False),
            patch.object(core.msgReply, 'trigger_auto_sn_update'),
        ]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)
        self.replies = []
        self.private_replies = []
        self.reply_patch = patch.object(core.msgReply, 'replyMsg', side_effect=self.capture_reply)
        self.reply_patch.start()
        self.addCleanup(self.reply_patch.stop)
        private_patch = patch.object(core.msgReply, 'replyMsgPrivateByEvent', side_effect=self.capture_private_reply)
        private_patch.start()
        self.addCleanup(private_patch.stop)
        self.event = SimpleNamespace(
            data=SimpleNamespace(
                sender={'name': 'tester', 'role': 'admin'}, user_id='user', group_id='group',
                host_id=None, extend={}, message='',
            ),
            platform={'platform': 'test', 'sdk': 'test'},
            plugin_info={'func_type': 'group_message'},
            bot_info=SimpleNamespace(hash='bot'),
            base_info={'self_id': 'bot'},
            set_block=lambda: None,
        )
        core.console.initConsoleSwitch('bot')
        core.pcCard.dataPcCardTemplateInit()
        self.pc_hash = core.pcCard.getPcHash('user', 'test')
        core.pcCard.pcCardDataSetBySkillName(self.pc_hash, 'SHM', 33, 'card', hagId='group')
        core.pcCard.pcCardDataSetBySkillName(self.pc_hash, '魅惑', 50, 'card', hagId='group')
        config_patch = patch.object(core.userConfig, 'getUserConfigByKey', side_effect=self.config_value)
        config_patch.start()
        self.addCleanup(config_patch.stop)

    def capture_reply(self, event, message, *args, **kwargs):
        self.replies.append(str(message))

    def capture_private_reply(self, event, message, *args, **kwargs):
        self.private_replies.append(str(message))

    def config_value(self, *args, **kwargs):
        key = kwargs.get('userConfigKey')
        if key == 'groupEnable':
            return True
        if key == 'teamConfig':
            return {'team': {'members': ['user']}}
        if key == 'activeTeam':
            return 'team'
        if key == 'userName':
            return 'tester'
        return kwargs.get('default')

    def command(self, text):
        self.event.data.message = text
        core.msgReply.unity_reply(self.event, None)
        return self.replies[-1]

    def test_st_operator_assignment_and_count(self):
        output = self.command('.st SHM+5')
        dice = core.onedice.RD('33+5')
        dice.roll()
        detail = core.onediceOverride.RDDataFormat(data=dice.resDetailData, mode='short')
        expected = f'33+5={detail}=38' if detail else '33+5=38'
        self.assertIn('[SHM]: ' + expected, output)
        self.assertIn('本次录入了1条', output)
        output = self.command('.st SHM=1+2')
        self.assertIn('[SHM]: 38 -> 3', output)
        self.assertNotIn('1+2', output)
        output = self.command('.st 和=50')
        self.assertIn('[和]: 0 -> 50', output)
        self.assertIn('本次录入了1条', output)
        output = self.command('.st SHM+5&映射=2')
        self.assertIn('本次录入了2条', output)
        self.assertEqual(
            core.pcCard.pcCardDataGetTemplateDataByKey(self.pc_hash, 'card', 'mappingRecord', {}), {'映射': '2'}
        )
        output = self.command('.st SHM+1d1')
        self.assertIn('[SHM]: 8+1d1=', output)
        self.assertTrue(output.rstrip().endswith('=9'))
        output = self.command('.st SHM=1d1')
        self.assertIn('[SHM]: 9 -> 1', output)
        self.assertNotIn('1d1', output)
        output = self.command('.st SHM+1/0&另一个=2')
        self.assertIn('表达式错误', output)
        self.assertIn('本次录入了1条', output)
        output = self.command('.st &单独=3')
        self.assertIn('本次录入了1条', output)
        output = self.command('.st 力量33敏捷44')
        self.assertIn('本次录入了2条', output)

    def test_team_st_operator_and_assignment(self):
        output = self.command('.team st SHM+5')
        self.assertIn('33+5=', output)
        self.assertIn('=38', output)
        self.assertIn('本次录入了1条', output)
        output = self.command('.team st SHM=1+2')
        self.assertIn('38 -> 3', output)
        self.assertNotIn('1+2', output)
        output = self.command('.team st SHM=1d1')
        self.assertIn('3 -> 1', output)
        self.assertNotIn('1d1', output)

    def test_forced_checks_do_not_roll_main_die(self):
        real_roll = core.onedice.RD.roll

        def no_check_die(dice):
            self.assertNotIn(dice.originDataRaw.upper(), ('1D100', 'B', 'B1', 'P', 'P1'))
            return real_roll(dice)

        with patch.object(core.onedice.RD, 'roll', no_check_die):
            for command in ('.ra(5) 魅惑', '.rc(5) 魅惑', '.rab(5) 魅惑'):
                with self.subTest(command=command):
                    output = self.command(command)
                    self.assertIn('1D100=5/50', output)
            output = self.command('.ra2#b(5) 魅惑')
            self.assertEqual(output.count('1D100=5/50'), 2)
            self.command('.rah(5) 魅惑')
            self.assertIn('1D100=5/50', self.private_replies[-1])
            output = self.command('.team ra (5) 魅惑')
            self.assertIn('1D100=5/50', output)
            output = self.command('.ra(1)(-5)+7+魅惑')
            self.assertIn('1D100=1/52', output)
            output = self.command('.ra(-4)(23)+(魅惑)+7+魅惑')
            self.assertIn('1D100=1/130', output)
            output = self.command('.ra(101) 魅惑')
            self.assertIn('1D100=101/50', output)
            self.assertIn('失败', output)

    def test_parentheses_followed_by_operator_remain_expression(self):
        real_roll = core.onedice.RD.roll
        expressions = []

        def capture_roll(dice):
            expressions.append(dice.originDataRaw.upper())
            return real_roll(dice)

        with patch.object(core.onedice.RD, 'roll', capture_roll):
            output = self.command('.ra(5)+魅惑')
        self.assertIn('/55', output)
        self.assertIn('1D100', expressions)


class ConsoleSwitchTests(unittest.TestCase):
    def test_old_settings_are_preserved_and_new_switch_saved(self):
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(core.data, 'dataDirRoot', tmp.replace('\\', '/')), \
                patch.object(core.console, 'dictConsoleSwitch', {}):
            switch_path = Path(tmp) / 'bot' / 'console' / 'switch.json'
            switch_path.parent.mkdir(parents=True)
            switch_path.write_text(json.dumps({'censorMode': 0, 'masterList': ['owner']}), encoding='utf-8')
            core.console.initConsoleSwitch('bot')
            core.console.readConsoleSwitch()
            core.console.initConsoleSwitch('bot')
            core.console.saveConsoleSwitch()
            saved = json.loads(switch_path.read_text(encoding='utf-8'))
            self.assertEqual(saved['censorMode'], 0)
            self.assertEqual(saved['masterList'], ['owner'])
            self.assertEqual(saved['forceMarkdownReply'], 0)

    def test_markdown_platform_and_switch(self):
        event = SimpleNamespace(
            platform={'sdk': 'qqGuildv2_link'},
            indeAPI=SimpleNamespace(hasAPI=lambda name: True),
            bot_info=SimpleNamespace(hash='bot'),
            data=SimpleNamespace(extend={}),
        )
        with patch.object(core.console, 'dictConsoleSwitch', {'bot': {'forceMarkdownReply': 1}}):
            self.assertTrue(core.msgReply._isQQGuildv2MarkdownAble(event, 'plain text'))
            event.platform['sdk'] = 'other'
            self.assertFalse(core.msgReply._isQQGuildv2MarkdownAble(event, '[CQ:at,qq=123]'))
            event.platform['sdk'] = 'qqGuildv2_link'
            event.indeAPI = SimpleNamespace(hasAPI=lambda name: False)
            self.assertFalse(core.msgReply._isQQGuildv2MarkdownAble(event, 'plain text'))
            event.indeAPI = SimpleNamespace(hasAPI=lambda name: True)
            core.console.dictConsoleSwitch['bot']['forceMarkdownReply'] = 0
            self.assertFalse(core.msgReply._isQQGuildv2MarkdownAble(event, 'plain text'))
            self.assertTrue(core.msgReply._isQQGuildv2MarkdownAble(event, '[CQ:at,qq=123]'))
            self.assertFalse(core.msgReply._isQQGuildv2MarkdownAble(event, '[CQ:image,file=a.png]'))
            event.data.extend['flag_from_qq'] = True
            self.assertTrue(core.msgReply._isQQGuildv2MarkdownAble(event, '[CQ:image,file=a.png]'))

    def test_forced_markdown_uses_censor_and_roll_protection(self):
        sent = []
        event = SimpleNamespace(
            platform={'sdk': 'qqGuildv2_link'},
            indeAPI=SimpleNamespace(
                hasAPI=lambda name: True,
                create_markdown_message=lambda **kwargs: sent.append(kwargs) or {'active': True},
            ),
            bot_info=SimpleNamespace(hash='bot', id='bot'),
            data=SimpleNamespace(extend={}, group_id='group', user_id='user'),
        )
        with patch.object(core.console, 'dictConsoleSwitch', {'bot': {'forceMarkdownReply': 1}}), \
                patch.object(core.msgCustom, 'dictStrCustomDict', {'bot': core.msgCustom.dictStrCustom.copy()}), \
                patch.object(core.censorAPI, 'doCensorReplaceOlivOSSafe',
                             side_effect=lambda botHash, msg: msg.replace('敏感', '***')):
            core.msgReply.replyMsg(event, '敏感 1D100=5/50', markdown_code='1D100=5/50')
        self.assertEqual(sent[0]['chat_id'], 'group')
        self.assertEqual(sent[0]['markdown']['content'], '*** `1D100=5/50`')


if __name__ == '__main__':
    unittest.main()
