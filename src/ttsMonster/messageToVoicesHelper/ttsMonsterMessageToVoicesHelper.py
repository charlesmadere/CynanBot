import re
from dataclasses import dataclass
from typing import Collection, Match, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from .ttsMonsterMessageToVoicesHelperInterface import TtsMonsterMessageToVoicesHelperInterface
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ..settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...misc import utils as utils


class TtsMonsterMessageToVoicesHelper(TtsMonsterMessageToVoicesHelperInterface):

    @dataclass(frozen = True)
    class VoiceMessageHeader:
        start: int
        end: int
        voice: TtsMonsterVoice

    def __init__(
        self,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface
    ):
        if not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')

        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository

        self.__voicePatternRegEx: Pattern = re.compile(r'(^|\s+)(\w+):', re.IGNORECASE)

    async def build(
        self,
        voices: frozenset[TtsMonsterVoice],
        message: str | None
    ) -> FrozenList[TtsMonsterMessageToVoicePair] | None:
        if not isinstance(voices, frozenset):
            raise TypeError(f'voices argument is malformed: \"{voices}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if len(voices) == 0 or not utils.isValidStr(message):
            return None

        voiceNamesToVoice = await self.__buildVoiceNamesToVoiceDictionary(
            voices = voices
        )

        voiceMessageHeaders = await self.__buildVoiceMessageHeaders(
            voiceNamesToVoice = voiceNamesToVoice,
            message = message
        )

        if len(voiceMessageHeaders) == 0:
            return None

        return await self.__buildMessagePairs(
            voiceMessageHeaders = voiceMessageHeaders,
            message = message
        )

    async def __buildMessagePairs(
        self,
        voiceMessageHeaders: FrozenList[VoiceMessageHeader],
        message: str
    ) -> FrozenList[TtsMonsterMessageToVoicePair] | None:
        voicePairs: FrozenList[TtsMonsterMessageToVoicePair] = FrozenList()

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

        if len(voicePairs) == 0:
            return None

        voicePairs.freeze()
        return voicePairs

    async def __buildVoiceNamesToVoiceDictionary(
        self,
        voices: frozenset[TtsMonsterVoice]
    ) -> frozendict[str, TtsMonsterVoice]:
        if not isinstance(voices, frozenset):
            raise TypeError(f'voices argument is malformed: \"{voices}\"')

        voiceNamesToVoiceDictionary: dict[str, TtsMonsterVoice] = dict()

        for voice in voices:
            if voice.websiteVoice is None:
                continue
            elif await self.__ttsMonsterSettingsRepository.isWebsiteVoiceEnabled(voice.websiteVoice):
                voiceNamesToVoiceDictionary[voice.websiteVoice.websiteName.casefold()] = voice

        return frozendict(voiceNamesToVoiceDictionary)

    async def __buildVoiceMessageHeaders(
        self,
        voiceNamesToVoice: frozendict[str, TtsMonsterVoice],
        message: str
    ) -> FrozenList[VoiceMessageHeader]:
        locations: FrozenList[TtsMonsterMessageToVoicesHelper.VoiceMessageHeader] = FrozenList()
        occurrencesIterator = self.__voicePatternRegEx.finditer(message)
        defaultVoice = await self.__getDefaultVoice(voiceNamesToVoice.values())

        if occurrencesIterator is None:
            if defaultVoice is not None:
                locations.append(TtsMonsterMessageToVoicesHelper.VoiceMessageHeader(
                    start = 0,
                    end = 0,
                    voice = defaultVoice
                ))

            locations.freeze()
            return locations

        occurrences: list[Match] = list(occurrencesIterator)

        if len(occurrences) == 0:
            if defaultVoice is not None:
                locations.append(TtsMonsterMessageToVoicesHelper.VoiceMessageHeader(
                    start = 0,
                    end = 0,
                    voice = defaultVoice
                ))

            locations.freeze()
            return locations

        # check for a prefix chunk of text that has no written voice
        prefixMessageChunk: str | None = message[0:occurrences[0].start()].strip()

        if utils.isValidStr(prefixMessageChunk) and defaultVoice is not None:
            locations.append(TtsMonsterMessageToVoicesHelper.VoiceMessageHeader(
                start = 0,
                end = 0,
                voice = defaultVoice
            ))

        for occurrence in occurrences:
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

    async def __getDefaultVoice(self, voices: Collection[TtsMonsterVoice]) -> TtsMonsterVoice | None:
        if not isinstance(voices, Collection):
            raise TypeError(f'voices argument is malformed: \"{voices}\"')

        defaultWebsiteVoice = await self.__ttsMonsterSettingsRepository.getDefaultVoice()

        for voice in voices:
            if voice.websiteVoice == defaultWebsiteVoice:
                return voice

        return None
