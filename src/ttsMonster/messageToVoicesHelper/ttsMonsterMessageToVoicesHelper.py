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
    class VoiceMessageHeader:
        start: int
        end: int
        voice: TtsMonsterVoice

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

        voiceMessageHeaders = await self.__buildVoiceMessageHeaders(
            voiceNamesToVoice = voiceNamesToVoice,
            message = message
        )

        if len(voiceMessageHeaders) == 0:
            voicePairs.freeze()
            return voicePairs

        sectionStart: int | None = None
        sectionVoice: TtsMonsterVoice | None = None

        for voiceMessageHeader in voiceMessageHeaders:
            if sectionStart is None or sectionVoice is None:
                sectionStart = voiceMessageHeader.end
                sectionVoice = voiceMessageHeader.voice
                continue

            sectionEnd = voiceMessageHeader.start

            voicePairs.append(TtsMonsterMessageToVoicePair(
                message = message[sectionStart:sectionEnd].strip(),
                voice = sectionVoice
            ))

            sectionStart = voiceMessageHeader.end
            sectionVoice = voiceMessageHeader.voice

        if sectionStart is None or sectionVoice is None:
            voicePairs.freeze()
            return voicePairs

        voicePairs.append(TtsMonsterMessageToVoicePair(
            message = message[sectionStart:len(message)].strip(),
            voice = sectionVoice
        ))

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

    async def __buildVoiceMessageHeaders(
        self,
        voiceNamesToVoice: frozendict[str, TtsMonsterVoice],
        message: str
    ) -> FrozenList[VoiceMessageHeader]:
        locations: FrozenList[TtsMonsterMessageToVoicesHelper.VoiceMessageHeader] = FrozenList()
        occurrences = self.__voicePatternRegEx.finditer(message)

        if occurrences is None:
            locations.freeze()
            return locations

        for occurrence in occurrences:
            voiceName = occurrence.group(2).casefold()
            voice = voiceNamesToVoice.get(voiceName, None)

            start = occurrence.start()
            end = occurrence.end()

            while message[start].isspace():
                start = start + 1

            locations.append(TtsMonsterMessageToVoicesHelper.VoiceMessageHeader(
                start = start,
                end = end,
                voice = voice
            ))

        locations.freeze()
        return locations
