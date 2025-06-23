from typing import Any

from frozenlist import FrozenList

from .supStreamerBoosterPack import SupStreamerBoosterPack
from .supStreamerBoosterPackJsonParserInterface import SupStreamerBoosterPackJsonParserInterface
from ...misc import utils as utils


class SupStreamerBoosterPackJsonParser(SupStreamerBoosterPackJsonParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> SupStreamerBoosterPack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        message = utils.getStrFromDict(jsonContents, 'message', '')
        reply = utils.getStrFromDict(jsonContents, 'reply', '')

        return SupStreamerBoosterPack(
            message = message,
            reply = reply
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> FrozenList[SupStreamerBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        supStreamerMessages: FrozenList[SupStreamerBoosterPack] = FrozenList()

        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(boosterPackJson)
            supStreamerMessages.append(boosterPack)

        supStreamerMessages.freeze()
        return supStreamerMessages
