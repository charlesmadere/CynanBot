from typing import Any

from frozendict import frozendict

from .redemptionCounterBoosterPack import RedemptionCounterBoosterPack
from .redemptionCounterBoosterPackParserInterface import RedemptionCounterBoosterPackParserInterface
from ...misc import utils as utils


class RedemptionCounterBoosterPackParser(RedemptionCounterBoosterPackParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any],
    ) -> RedemptionCounterBoosterPack:
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        incrementAmount = utils.getIntFromDict(jsonContents, 'incrementAmount', fallback = 1)
        counterName = utils.getStrFromDict(jsonContents, 'counterName')

        emote: str | None = None
        if 'emote' in jsonContents and utils.isValidStr(jsonContents.get('emote', None)):
            emote = utils.getStrFromDict(jsonContents, 'emote')

        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        if not utils.isValidInt(incrementAmount):
            raise ValueError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif incrementAmount < 1 or incrementAmount >= utils.getShortMaxSafeSize():
            raise ValueError(f'incrementAmount argument is out of bounds: {incrementAmount}')
        elif not utils.isValidStr(counterName):
            raise ValueError(f'counterName argument is malformed: \"{counterName}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')

        return RedemptionCounterBoosterPack(
            incrementAmount = incrementAmount,
            counterName = counterName,
            emote = emote,
            rewardId = rewardId,
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None,
    ) -> frozendict[str, RedemptionCounterBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: dict[str, RedemptionCounterBoosterPack] = dict()
        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            boosterPacks[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacks)
