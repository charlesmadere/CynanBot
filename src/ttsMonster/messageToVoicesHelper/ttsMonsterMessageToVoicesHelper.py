import re
from dataclasses import dataclass
from typing import Collection, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from .ttsMonsterMessageToVoicesHelperInterface import TtsMonsterMessageToVoicesHelperInterface
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils


class TtsMonsterMessageToVoicesHelper(TtsMonsterMessageToVoicesHelperInterface):

    @dataclass(frozen = True)
    class VoiceLocation:
        start: int
        end: int

    def __init__(self):
        self.__voicePatternRegEx: Pattern = re.compile(r'(^|\s+)(\w+):\s+', re.IGNORECASE)
        self.__whiteSpaceRegEx: Pattern = re.compile('\s+', re.IGNORECASE)

    async def build(
        self,
        voices: Collection[TtsMonsterVoice],
        message: str
    ) -> FrozenList[TtsMonsterMessageToVoicePair]:
        if not isinstance(voices, Collection):
            raise TypeError(f'voices argument is malformed: \"{voices}\"')
        elif not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        voicePairs: FrozenList[TtsMonsterMessageToVoicePair] = FrozenList()

        if len(voices) == 0 or not utils.isValidStr(message):
            voicePairs.freeze()
            return voicePairs

        voiceNamesToVoice = await self.__buildVoiceNamesToVoiceDictionary(
            voices = voices
        )

        voicePatternLocations = await self.__buildVoicePatternLocations(
            voiceNames = frozenset(voiceNamesToVoice.keys()),
            message = message
        )

        # TODO
        pass

        voicePairs.freeze()
        return voicePairs

    async def __buildVoiceNamesToVoiceDictionary(
        self,
        voices: Collection[TtsMonsterVoice]
    ) -> frozendict[str, TtsMonsterVoice]:
        if not isinstance(voices, Collection):
            raise TypeError(f'voices argument is malformed: \"{voices}\"')

        voiceNamesToVoiceDictionary: dict[str, TtsMonsterVoice] = dict()

        for voice in voices:
            voiceNamesToVoiceDictionary[voice.name.casefold()] = voice

        return frozendict(voiceNamesToVoiceDictionary)

    async def __buildVoicePatternLocations(
        self,
        voiceNames: frozenset[str],
        message: str
    ) -> FrozenList[VoiceLocation]:
        locations: FrozenList[TtsMonsterMessageToVoicesHelper.VoiceLocation] = FrozenList()
        occurrences = self.__voicePatternRegEx.finditer(message)

        if occurrences is None:
            locations.freeze()
            return locations

        for occurrence in occurrences:
            if occurrence.group(2) not in voiceNames:
                continue

            start = occurrence.start()
            end = occurrence.end()

            while message[start].isspace():
                start = start + 1

            locations.append(TtsMonsterMessageToVoicesHelper.VoiceLocation(
                start = start,
                end = end
            ))

        locations.freeze()
        return locations
