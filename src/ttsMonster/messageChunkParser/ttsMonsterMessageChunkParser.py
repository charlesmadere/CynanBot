import re
from dataclasses import dataclass
from typing import Match, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .ttsMonsterMessageChunkParserInterface import TtsMonsterMessageChunkParserInterface
from ..models.ttsMonsterMessageChunk import TtsMonsterMessageChunk
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils


class TtsMonsterMessageChunkParser(TtsMonsterMessageChunkParserInterface):

    @dataclass(frozen = True)
    class MessageChunkData:
        start: int
        end: int
        voice: TtsMonsterVoice

    def __init__(self):
        self.__voicePatternRegEx: Pattern = re.compile(r'(?:^|\s+)(\w+):', re.IGNORECASE)

    async def __buildMessagePairs(
        self,
        voiceMessageHeaders: FrozenList[MessageChunkData],
        message: str
    ) -> FrozenList[TtsMonsterMessageChunk] | None:
        voicePairs: FrozenList[TtsMonsterMessageChunk] = FrozenList()

        sectionStart: int | None = None
        sectionVoice: TtsMonsterVoice | None = None

        for voiceMessageHeader in voiceMessageHeaders:
            if sectionStart is None or sectionVoice is None:
                sectionStart = voiceMessageHeader.end
                sectionVoice = voiceMessageHeader.voice
                continue

            sectionEnd = voiceMessageHeader.start
            sectionMessage = message[sectionStart:sectionEnd].strip()

            if len(sectionMessage) >= 1:
                voicePairs.append(TtsMonsterMessageChunk(
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
            voicePairs.append(TtsMonsterMessageChunk(
                message = sectionMessage,
                voice = sectionVoice
            ))

        if len(voicePairs) == 0:
            return None

        voicePairs.freeze()
        return voicePairs

    async def __buildVoiceMessageHeaders(
        self,
        voiceNamesToVoice: frozendict[str, TtsMonsterVoice],
        message: str,
        defaultVoice: TtsMonsterVoice
    ) -> FrozenList[MessageChunkData]:
        locations: FrozenList[TtsMonsterMessageChunkParser.MessageChunkData] = FrozenList()
        occurrencesIterator = self.__voicePatternRegEx.finditer(message)

        if occurrencesIterator is None:
            if defaultVoice is not None:
                locations.append(TtsMonsterMessageChunkParser.MessageChunkData(
                    start = 0,
                    end = 0,
                    voice = defaultVoice
                ))

            locations.freeze()
            return locations

        occurrences: list[Match[str]] = list(occurrencesIterator)

        if len(occurrences) == 0:
            if defaultVoice is not None:
                locations.append(TtsMonsterMessageChunkParser.MessageChunkData(
                    start = 0,
                    end = 0,
                    voice = defaultVoice
                ))

            locations.freeze()
            return locations

        # check for a prefix chunk of text that has no written voice
        prefixMessageChunk: str | None = message[0:occurrences[0].start()].strip()

        if utils.isValidStr(prefixMessageChunk) and defaultVoice is not None:
            locations.append(TtsMonsterMessageChunkParser.MessageChunkData(
                start = 0,
                end = 0,
                voice = defaultVoice
            ))

        for occurrence in occurrences:
            voiceName = occurrence.group(1).casefold()
            voice = voiceNamesToVoice.get(voiceName, None)

            if voice is None:
                continue

            start = occurrence.start()
            end = occurrence.end()

            while message[start].isspace():
                start = start + 1

            locations.append(TtsMonsterMessageChunkParser.MessageChunkData(
                start = start,
                end = end,
                voice = voice
            ))

        locations.freeze()
        return locations

    async def __buildVoiceNamesToVoiceDictionary(self) -> frozendict[str, TtsMonsterVoice]:
        voiceNamesToVoiceDictionary: dict[str, TtsMonsterVoice] = dict()

        for voice in TtsMonsterVoice:
            voiceNamesToVoiceDictionary[voice.inMessageName] = voice

        return frozendict(voiceNamesToVoiceDictionary)

    async def parse(
        self,
        message: str | None,
        defaultVoice: TtsMonsterVoice
    ) -> FrozenList[TtsMonsterMessageChunk] | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(defaultVoice, TtsMonsterVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        if not utils.isValidStr(message):
            return None

        voiceNamesToVoice = await self.__buildVoiceNamesToVoiceDictionary()

        messageChunks = await self.__buildVoiceMessageHeaders(
            voiceNamesToVoice = voiceNamesToVoice,
            message = message,
            defaultVoice = defaultVoice
        )

        if len(messageChunks) == 0:
            return None

        return await self.__buildMessagePairs(
            voiceMessageHeaders = messageChunks,
            message = message
        )
