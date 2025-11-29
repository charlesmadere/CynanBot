from typing import Any, Final

from frozenlist import FrozenList

from .ttsBoosterPack import TtsBoosterPack
from .ttsBoosterPackParserInterface import TtsBoosterPackParserInterface
from ...misc import utils as utils
from ...tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface


class TtsBoosterPackParser(TtsBoosterPackParserInterface):

    def __init__(
        self,
        ttsJsonMapper: TtsJsonMapperInterface,
    ):
        if not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')

        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any],
    ) -> TtsBoosterPack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        isEnabled = utils.getBoolFromDict(jsonContents, 'enabled', fallback = True)
        cheerAmount = utils.getIntFromDict(jsonContents, 'cheerAmount')
        ttsProvider = self.__ttsJsonMapper.requireProvider(utils.getStrFromDict(jsonContents, 'ttsProvider'))

        return TtsBoosterPack(
            isEnabled = isEnabled,
            cheerAmount = cheerAmount,
            ttsProvider = ttsProvider,
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None,
    ) -> FrozenList[TtsBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: list[TtsBoosterPack] = list()

        for boosterPackJson in jsonContents:
            boosterPacks.append(self.parseBoosterPack(boosterPackJson))

        boosterPacks.sort(key = lambda boosterPack: boosterPack.cheerAmount, reverse = True)
        frozenBoosterPacks: FrozenList[TtsBoosterPack] = FrozenList(boosterPacks)
        frozenBoosterPacks.freeze()

        return frozenBoosterPacks
