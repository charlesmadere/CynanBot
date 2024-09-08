import re
from dataclasses import dataclass
from typing import Collection, Match, Pattern

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
        self.__voicePatternRegEx: Pattern = re.compile(r'(^|\s+)(\w+):', re.IGNORECASE)

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

        await self.__buildMessagePairs(
            voicePairs = voicePairs,
            voiceMessageHeaders = voiceMessageHeaders,
            message = message
        )

        voicePairs.freeze()
        return voicePairs

    async def __buildMessagePairs(
        self,
        voicePairs: FrozenList[TtsMonsterMessageToVoicePair],
        voiceMessageHeaders: FrozenList[VoiceMessageHeader],
        message: str
    ) -> FrozenList[TtsMonsterMessageToVoicePair]:
        sectionStart: int | None = None
        sectionVoice: TtsMonsterVoice | None = None

        for index, voiceMessageHeader in enumerate(voiceMessageHeaders):
            if sectionStart is None or sectionVoice is None:
                sectionStart = voiceMessageHeader.end
                sectionVoice = voiceMessageHeader.voice
                continue

            sectionEnd = voiceMessageHeader.start
            sectionMessage = message[sectionStart:sectionEnd].strip()

            if len(sectionMessage) >= 1:
                voicePairs.append(TtsMonsterMessageToVoicePair(
                    message = sectionMessage,
                    voice = sectionVoice
                ))

            sectionStart = voiceMessageHeader.end
            sectionVoice = voiceMessageHeader.voice

        if sectionStart is None or sectionVoice is None:
            voicePairs.freeze()
            return voicePairs

        sectionMessage = message[sectionStart:len(message)].strip()

        if len(sectionMessage) >= 1:
            voicePairs.append(TtsMonsterMessageToVoicePair(
                message = sectionMessage,
                voice = sectionVoice
            ))

        voicePairs.freeze()

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
        occurrencesIterator = self.__voicePatternRegEx.finditer(message)

        if occurrencesIterator is None:
            locations.freeze()
            return locations

        occurrences: list[Match] = list(occurrencesIterator)

        for index, occurrence in enumerate(occurrences):
            voiceName = occurrence.group(2).casefold()
            voice = voiceNamesToVoice.get(voiceName, None)

            if voice is None:
                continue

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
