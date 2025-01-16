from typing import Any

from frozendict import frozendict

from .timeoutBoosterPack import TimeoutBoosterPack
from .timeoutBoosterPackJsonParserInterface import TimeoutBoosterPackJsonParserInterface
from .timeoutBoosterPackType import TimeoutBoosterPackType
from ...misc import utils as utils


class TimeoutBoosterPackJsonParser(TimeoutBoosterPackJsonParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> TimeoutBoosterPack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        randomChanceEnabled = utils.getBoolFromDict(jsonContents, 'randomChanceEnabled', True)
        durationSeconds = utils.getIntFromDict(jsonContents, 'durationSeconds')
        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        timeoutType = TimeoutBoosterPackType.USER_TARGET
        if 'timeoutType' in jsonContents and utils.isValidStr(jsonContents.get('timeoutType')):
            timeoutType = self.parseBoosterPackType(utils.getStrFromDict(jsonContents, 'timeoutType'))

        return TimeoutBoosterPack(
            randomChanceEnabled = randomChanceEnabled,
            durationSeconds = durationSeconds,
            rewardId = rewardId,
            timeoutType = timeoutType
        )

    def parseBoosterPackType(
        self,
        boosterPackType: str
    ) -> TimeoutBoosterPackType:
        if not utils.isValidStr(boosterPackType):
            raise TypeError(f'boosterPackType argument is malformed: \"{boosterPackType}\"')

        boosterPackType = boosterPackType.lower()

        match boosterPackType:
            case 'random': return TimeoutBoosterPackType.RANDOM_TARGET
            case 'user': return TimeoutBoosterPackType.USER_TARGET
            case _: raise ValueError(f'Unknown TimeoutBoosterPackType value: \"{boosterPackType}\"')

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TimeoutBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: dict[str, TimeoutBoosterPack] = dict()

        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            boosterPacks[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacks)
