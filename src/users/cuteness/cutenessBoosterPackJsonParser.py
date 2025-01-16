from typing import Any

from frozendict import frozendict

from .cutenessBoosterPack import CutenessBoosterPack
from .cutenessBoosterPackJsonParserInterface import CutenessBoosterPackJsonParserInterface
from ...misc import utils as utils


class CutenessBoosterPackJsonParser(CutenessBoosterPackJsonParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> CutenessBoosterPack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        amount = utils.getIntFromDict(jsonContents, 'amount')
        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        return CutenessBoosterPack(
            amount = amount,
            rewardId = rewardId
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, CutenessBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: dict[str, CutenessBoosterPack] = dict()

        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            boosterPacks[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacks)
