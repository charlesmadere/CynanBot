from typing import Any

from frozendict import frozendict

from .timeoutBoosterPack import TimeoutBoosterPack
from .timeoutBoosterPackJsonParserInterface import TimeoutBoosterPackJsonParserInterface
from ...misc import utils as utils


class TimeoutBoosterPackJsonParser(TimeoutBoosterPackJsonParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> TimeoutBoosterPack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        durationSeconds = utils.getIntFromDict(jsonContents, 'durationSeconds')
        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        return TimeoutBoosterPack(
            durationSeconds = durationSeconds,
            rewardId = rewardId
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TimeoutBoosterPack] | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        boosterPacks: dict[str, TimeoutBoosterPack] = dict()

        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            boosterPacks[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacks)
