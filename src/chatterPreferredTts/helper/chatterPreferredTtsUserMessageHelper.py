import re
from typing import Any, Match, Pattern

from .chatterPreferredTtsUserMessageHelperInterface import ChatterPreferredTtsUserMessageHelperInterface
from ..models.absPreferredTts import AbsPreferredTts
from ..models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from ..models.google.googlePreferredTts import GooglePreferredTts
from ..models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from ..models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from ..models.singingDecTalk.singingDecTalkPreferredTts import SingingDecTalkPreferredTts
from ..models.streamElements.streamElementsPreferredTts import StreamElementsPreferredTts
from ..models.ttsMonster.ttsMonsterPreferredTts import TtsMonsterPreferredTts
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...halfLife.parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from ...language.languageEntry import LanguageEntry
from ...language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ...misc import utils as utils


class ChatterPreferredTtsUserMessageHelper(ChatterPreferredTtsUserMessageHelperInterface):

    def __init__(
        self,
        halfLifeVoiceParser: HalfLifeVoiceParserInterface,
        languagesRepository: LanguagesRepositoryInterface
    ):
        if not isinstance(halfLifeVoiceParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeVoiceParser}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')

        self.__halfLifeJsonParser: HalfLifeVoiceParserInterface = halfLifeVoiceParser
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository

        self.__decTalkRegEx: Pattern = re.compile(r'^\s*dec(?:\s+|_|-)?talk\s*$', re.IGNORECASE)
        self.__googleRegEx: Pattern = re.compile(r'^\s*goog(?:le?)?\s*(\w+)?\s*$', re.IGNORECASE)
        self.__halfLifeRegEx: Pattern = re.compile(r'^\s*half(?:\s+|_|-)?life\s*(\w+)?\s*$', re.IGNORECASE)
        self.__microsoftSamRegEx: Pattern = re.compile(r'^\s*(?:microsoft|ms)(?:\s|_|-)*sam\s*$', re.IGNORECASE)
        self.__singingDecTalkRegEx: Pattern = re.compile(r'^\s*singing(?:\s+|_|-)?dec(?:\s+|_|-)?talk\s*$', re.IGNORECASE)
        self.__streamElementsRegEx: Pattern = re.compile(r'^\s*stream(?:\s+|_|-)?elements\s*(\w+)?\s*$', re.IGNORECASE)
        self.__ttsMonsterRegEx: Pattern = re.compile(r'^\s*tts(?:\s+|_|-)?monster\s*(\w+)?\s*$', re.IGNORECASE)

    async def __createDecTalkTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return DecTalkPreferredTts()

    async def __createGoogleTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        languageEntry: LanguageEntry | None = None
        languageEntryCommand = match.group(1)

        if utils.isValidStr(languageEntryCommand):
            languageEntry = await self.__languagesRepository.getLanguageForCommand(
                command = languageEntryCommand
            )

        return GooglePreferredTts(
            languageEntry = languageEntry
        )

    async def __createHalfLifeTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        halfLifeVoiceEntry: HalfLifeVoice = HalfLifeVoice.ALL
        halfLifeEntryCommand = match.group(1)

        if utils.isValidStr(halfLifeEntryCommand):
            maybeHalfLifeVoice: HalfLifeVoice | None = self.__halfLifeJsonParser.parseVoice(
                voiceString = halfLifeEntryCommand
            )
            if maybeHalfLifeVoice is not None:
                halfLifeVoiceEntry = maybeHalfLifeVoice

        return HalfLifePreferredTts(
            halfLifeVoice = halfLifeVoiceEntry
        )

    async def __createMicrosoftSamTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return MicrosoftSamPreferredTts()

    async def __createSingingDecTalkTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return SingingDecTalkPreferredTts()

    async def __createStreamElementsTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return StreamElementsPreferredTts()

    async def __createTtsMonsterTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return TtsMonsterPreferredTts()

    async def parseUserMessage(
        self,
        userMessage: str | Any | None
    ) -> AbsPreferredTts | None:
        if not utils.isValidStr(userMessage):
            return None

        userMessage = utils.cleanStr(userMessage)

        decTalkMatch = self.__decTalkRegEx.fullmatch(userMessage)
        googleMatch = self.__googleRegEx.fullmatch(userMessage)
        halfLifeMatch = self.__halfLifeRegEx.fullmatch(userMessage)
        microsoftSamMatch = self.__microsoftSamRegEx.fullmatch(userMessage)
        singingDecTalkMatch = self.__singingDecTalkRegEx.fullmatch(userMessage)
        streamElementsMatch = self.__streamElementsRegEx.fullmatch(userMessage)
        ttsMonsterMatch = self.__ttsMonsterRegEx.fullmatch(userMessage)

        if decTalkMatch is not None:
            return await self.__createDecTalkTtsProperties(decTalkMatch)

        elif googleMatch is not None:
            return await self.__createGoogleTtsProperties(googleMatch)

        elif halfLifeMatch is not None:
            return await self.__createHalfLifeTtsProperties(halfLifeMatch)

        elif microsoftSamMatch is not None:
            return await self.__createMicrosoftSamTtsProperties(microsoftSamMatch)

        elif singingDecTalkMatch is not None:
            return await self.__createSingingDecTalkTtsProperties(singingDecTalkMatch)

        elif streamElementsMatch is not None:
            return await self.__createStreamElementsTtsProperties(streamElementsMatch)

        elif ttsMonsterMatch is not None:
            return await self.__createTtsMonsterTtsProperties(ttsMonsterMatch)

        else:
            return None
