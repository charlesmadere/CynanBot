from typing import Any

from frozendict import frozendict

from .crowdControlBoosterPack import CrowdControlBoosterPack
from .crowdControlInputType import CrowdControlInputType
from .crowdControlJsonParserInterface import CrowdControlJsonParserInterface
from ...misc import utils as utils


class CrowdControlJsonParser(CrowdControlJsonParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> CrowdControlBoosterPack:
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        inputType = self.parseInputType(utils.getStrFromDict(jsonContents, 'inputType'))
        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        return CrowdControlBoosterPack(
            inputType = inputType,
            rewardId = rewardId
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, CrowdControlBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: dict[str, CrowdControlBoosterPack] = dict()

        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            boosterPacks[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacks)

    def parseInputType(
        self,
        inputType: str
    ) -> CrowdControlInputType:
        if not utils.isValidStr(inputType):
            raise TypeError(f'inputType argument is malformed: \"{inputType}\"')

        inputType = inputType.lower()

        match inputType:
            case 'button_a': return CrowdControlInputType.BUTTON_A
            case 'button_b': return CrowdControlInputType.BUTTON_B
            case 'button_x': return CrowdControlInputType.BUTTON_X
            case 'button_y': return CrowdControlInputType.BUTTON_Y
            case 'dpad_down': return CrowdControlInputType.DPAD_DOWN
            case 'dpad_left': return CrowdControlInputType.DPAD_LEFT
            case 'dpad_right': return CrowdControlInputType.DPAD_RIGHT
            case 'dpad_up': return CrowdControlInputType.DPAD_UP
            case 'game_shuffle': return CrowdControlInputType.GAME_SHUFFLE
            case 'select': return CrowdControlInputType.SELECT
            case 'start': return CrowdControlInputType.START
            case 'trigger_left': return CrowdControlInputType.TRIGGER_LEFT
            case 'trigger_right': return CrowdControlInputType.TRIGGER_RIGHT
            case 'user_input_button': return CrowdControlInputType.USER_INPUT_BUTTON
            case _: raise ValueError(f'Encountered unknown CrowdControlInputType: \"{inputType}\"')
