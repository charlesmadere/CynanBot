from collections import OrderedDict
from typing import Any

from frozendict import frozendict

from .ttsBoosterPack import TtsBoosterPack
from .ttsJsonParserInterface import TtsJsonParserInterface
from ...misc import utils as utils
from ...tts.ttsProvider import TtsProvider


class TtsJsonParser(TtsJsonParserInterface):

    def parseBoosterPack(
        self,
        jsonContents: dict[str, Any]
    ) -> TtsBoosterPack:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        cheerAmount = utils.getIntFromDict(jsonContents, 'cheerAmount')
        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')
        ttsProvider = self.parseTtsProvider(utils.getStrFromDict(jsonContents, 'ttsProvider'))

        return TtsBoosterPack(
            cheerAmount = cheerAmount,
            rewardId = rewardId,
            ttsProvider = ttsProvider
        )

    def parseBoosterPacks(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TtsBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        boosterPacks: list[TtsBoosterPack] = list()

        for boosterPackJson in jsonContents:
            boosterPacks.append(self.parseBoosterPack(boosterPackJson))

        boosterPacks.sort(key = lambda boosterPack: boosterPack.cheerAmount)
        boosterPacksDictionary: dict[str, TtsBoosterPack] = OrderedDict()

        for boosterPack in boosterPacks:
            boosterPacksDictionary[boosterPack.rewardId] = boosterPack

        return frozendict(boosterPacksDictionary)

    def parseTtsProvider(
        self,
        ttsProvider: str
    ) -> TtsProvider:
        if not utils.isValidStr(ttsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        ttsProvider = ttsProvider.lower()

        match ttsProvider:
            case 'dectalk': return TtsProvider.DEC_TALK
            case 'google': return TtsProvider.GOOGLE
            case 'streamelements': return TtsProvider.STREAM_ELEMENTS
            case 'ttsmonster': return TtsProvider.TTS_MONSTER
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{ttsProvider}\"')
