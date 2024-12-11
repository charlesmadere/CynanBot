from typing import Any

from frozendict import frozendict

from .pkmnCatchBoosterPack import PkmnCatchBoosterPack
from .pkmnCatchType import PkmnCatchType
from .pkmnJsonParserInterface import PkmnJsonParserInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class PkmnJsonParser(PkmnJsonParserInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> PkmnCatchBoosterPack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        catchType = self.parseCatchType(jsonContents.get('catchType', None))
        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        return PkmnCatchBoosterPack(
            catchType = catchType,
            rewardId =  rewardId
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, PkmnCatchBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: dict[str, PkmnCatchBoosterPack] = dict()

        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            boosterPacks[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacks)

    def parseCatchType(
        self,
        catchType: str | Any | None
    ) -> PkmnCatchType | None:
        if not utils.isValidStr(catchType):
            return None

        catchType = catchType.lower()

        match catchType:
            case 'great': return PkmnCatchType.GREAT
            case 'normal': return PkmnCatchType.NORMAL
            case 'ultra': return PkmnCatchType.ULTRA
            case _:
                self.__timber.log('PkmnJsonParser', f'Encountered unknown PkmnCatchType: \"{catchType}\"')
                return None
