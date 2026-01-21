import re
from dataclasses import dataclass
from typing import Final, Match, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .ttsMonsterMessageChunkParserInterface import TtsMonsterMessageChunkParserInterface
from ..models.ttsMonsterMessageChunk import TtsMonsterMessageChunk
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils


class TtsMonsterMessageChunkParser(TtsMonsterMessageChunkParserInterface):

    @dataclass(frozen = True, slots = True)
    class WorkingMessageChunk:
        start: int
        end: int
        voice: TtsMonsterVoice

    def __init__(self):
        self.__voiceNamesToVoiceDictionary: Final[frozendict[str, TtsMonsterVoice]] = self.__createVoiceNamesToVoiceDictionary()
        self.__voicePatternRegEx: Final[Pattern] = re.compile(r'(?:^|\s+)(\w+):', re.IGNORECASE)

    async def __buildMessageChunks(
        self,
        workingMessageChunks: FrozenList[WorkingMessageChunk],
        message: str
    ) -> FrozenList[TtsMonsterMessageChunk] | None:
        voicePairs: FrozenList[TtsMonsterMessageChunk] = FrozenList()

        sectionStart: int | None = None
        sectionVoice: TtsMonsterVoice | None = None

        for workingMessageChunk in workingMessageChunks:
            if sectionStart is None or sectionVoice is None:
                sectionStart = workingMessageChunk.end
                sectionVoice = workingMessageChunk.voice
                continue

            sectionEnd = workingMessageChunk.start
            sectionMessage = message[sectionStart:sectionEnd].strip()

            if len(sectionMessage) >= 1:
                voicePairs.append(TtsMonsterMessageChunk(
                    message = sectionMessage,
                    voice = sectionVoice
                ))

            sectionStart = workingMessageChunk.end
            sectionVoice = workingMessageChunk.voice

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

    async def __buildWorkingMessageChunks(
        self,
        message: str,
        defaultVoice: TtsMonsterVoice
    ) -> FrozenList[WorkingMessageChunk]:
        chunks: FrozenList[TtsMonsterMessageChunkParser.WorkingMessageChunk] = FrozenList()
        occurrencesIterator = self.__voicePatternRegEx.finditer(message)

        if occurrencesIterator is None:
            if defaultVoice is not None:
                chunks.append(TtsMonsterMessageChunkParser.WorkingMessageChunk(
                    start = 0,
                    end = 0,
                    voice = defaultVoice
                ))

            chunks.freeze()
            return chunks

        occurrences: list[Match[str]] = list(occurrencesIterator)

        if len(occurrences) == 0:
            if defaultVoice is not None:
                chunks.append(TtsMonsterMessageChunkParser.WorkingMessageChunk(
                    start = 0,
                    end = 0,
                    voice = defaultVoice
                ))

            chunks.freeze()
            return chunks

        # check for a prefix chunk of text that has no written voice
        prefixMessageChunk: str | None = message[0:occurrences[0].start()].strip()

        if utils.isValidStr(prefixMessageChunk) and defaultVoice is not None:
            chunks.append(TtsMonsterMessageChunkParser.WorkingMessageChunk(
                start = 0,
                end = 0,
                voice = defaultVoice
            ))

        for occurrence in occurrences:
            voiceName = occurrence.group(1).casefold()
            voice = self.__voiceNamesToVoiceDictionary.get(voiceName, None)

            if voice is None:
                continue

            start = occurrence.start()
            end = occurrence.end()

            while message[start].isspace():
                start = start + 1

            chunks.append(TtsMonsterMessageChunkParser.WorkingMessageChunk(
                start = start,
                end = end,
                voice = voice
            ))

        chunks.freeze()
        return chunks

    def __createVoiceNamesToVoiceDictionary(self) -> frozendict[str, TtsMonsterVoice]:
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

        workingMessageChunks = await self.__buildWorkingMessageChunks(
            message = message,
            defaultVoice = defaultVoice
        )

        if len(workingMessageChunks) == 0:
            return None

        return await self.__buildMessageChunks(
            workingMessageChunks = workingMessageChunks,
            message = message
        )
