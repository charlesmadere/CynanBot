from typing import Any

from frozendict import frozendict

from src.users.crowdControl.crowdControlBoosterPack import CrowdControlBoosterPack
from src.users.crowdControl.crowdControlInputType import CrowdControlInputType
from src.users.crowdControl.crowdControlJsonParser import CrowdControlJsonParser
from src.users.crowdControl.crowdControlJsonParserInterface import CrowdControlJsonParserInterface


class TestCrowdControlJsonParser:

    jsonParser: CrowdControlJsonParserInterface = CrowdControlJsonParser()

    def test_parseBoosterPack(self):
        jsonContents: dict[str, Any] = {
            'inputType': 'button_a',
            'rewardId': 'abc123'
        }

        result = self.jsonParser.parseBoosterPack(jsonContents)
        assert isinstance(result, CrowdControlBoosterPack)
        assert result.inputType is CrowdControlInputType.BUTTON_A
        assert result.rewardId == 'abc123'

    def test_parseBoosterPacks(self):
        jsonContents: list[dict[str, Any]] = [
            {
                'inputType': 'button_x',
                'rewardId': 'abc123'
            },
            {
                'inputType': 'game_shuffle',
                'rewardId': 'def456'
            }
        ]

        result = self.jsonParser.parseBoosterPacks(jsonContents)
        assert isinstance(result, frozendict)
        assert len(result) == 2

        boosterPack = result.get('abc123')
        assert isinstance(boosterPack, CrowdControlBoosterPack)
        assert boosterPack.inputType is CrowdControlInputType.BUTTON_X
        assert boosterPack.rewardId == 'abc123'

        boosterPack = result.get('def456')
        assert isinstance(boosterPack, CrowdControlBoosterPack)
        assert boosterPack.inputType is CrowdControlInputType.GAME_SHUFFLE
        assert boosterPack.rewardId == 'def456'

    def test_parseBoosterPacks_withEmptyList(self):
        result = self.jsonParser.parseBoosterPacks(list())
        assert result is None

    def test_parseBoosterPacks_withNone(self):
        result = self.jsonParser.parseBoosterPacks(None)
        assert result is None

    def test_parseInputType_withButtonA(self):
        result = self.jsonParser.parseInputType('button_a')
        assert result is CrowdControlInputType.BUTTON_A

    def test_parseInputType_withButtonB(self):
        result = self.jsonParser.parseInputType('button_b')
        assert result is CrowdControlInputType.BUTTON_B

    def test_parseInputType_withButtonC(self):
        result = self.jsonParser.parseInputType('button_c')
        assert result is CrowdControlInputType.BUTTON_C

    def test_parseInputType_withButtonX(self):
        result = self.jsonParser.parseInputType('button_x')
        assert result is CrowdControlInputType.BUTTON_X

    def test_parseInputType_withButtonY(self):
        result = self.jsonParser.parseInputType('button_y')
        assert result is CrowdControlInputType.BUTTON_Y

    def test_parseInputType_withButtonZ(self):
        result = self.jsonParser.parseInputType('button_z')
        assert result is CrowdControlInputType.BUTTON_Z

    def test_parseInputType_withDpadDown(self):
        result = self.jsonParser.parseInputType('dpad_down')
        assert result is CrowdControlInputType.DPAD_DOWN

    def test_parseInputType_withDpadLeft(self):
        result = self.jsonParser.parseInputType('dpad_left')
        assert result is CrowdControlInputType.DPAD_LEFT

    def test_parseInputType_withDpadRight(self):
        result = self.jsonParser.parseInputType('dpad_right')
        assert result is CrowdControlInputType.DPAD_RIGHT

    def test_parseInputType_withDpadUp(self):
        result = self.jsonParser.parseInputType('dpad_up')
        assert result is CrowdControlInputType.DPAD_UP

    def test_parseInputType_withGameShuffle(self):
        result = self.jsonParser.parseInputType('game_shuffle')
        assert result is CrowdControlInputType.GAME_SHUFFLE

    def test_parseInputType_withSelect(self):
        result = self.jsonParser.parseInputType('select')
        assert result is CrowdControlInputType.SELECT

    def test_parseInputType_withStart(self):
        result = self.jsonParser.parseInputType('start')
        assert result is CrowdControlInputType.START

    def test_parseInputType_withTriggerLeft(self):
        result = self.jsonParser.parseInputType('trigger_left')
        assert result is CrowdControlInputType.TRIGGER_LEFT

    def test_parseInputType_withTriggerRight(self):
        result = self.jsonParser.parseInputType('trigger_right')
        assert result is CrowdControlInputType.TRIGGER_RIGHT

    def test_parseInputType_withUserInputButton(self):
        result = self.jsonParser.parseInputType('user_input_button')
        assert result is CrowdControlInputType.USER_INPUT_BUTTON
