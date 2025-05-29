import re
from typing import Any, Match, Pattern

from .chatterPreferredTtsUserMessageHelperInterface import ChatterPreferredTtsUserMessageHelperInterface
from ..models.absPreferredTts import AbsPreferredTts
from ..models.commodoreSam.commodoreSamPreferredTts import CommodoreSamPreferredTts
from ..models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from ..models.google.googlePreferredTts import GooglePreferredTts
from ..models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from ..models.microsoft.microsoftTtsPreferredTts import MicrosoftTtsPreferredTts
from ..models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from ..models.singingDecTalk.singingDecTalkPreferredTts import SingingDecTalkPreferredTts
from ..models.streamElements.streamElementsPreferredTts import StreamElementsPreferredTts
from ..models.ttsMonster.ttsMonsterPreferredTts import TtsMonsterPreferredTts
from ...decTalk.mapper.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from ...decTalk.models.decTalkVoice import DecTalkVoice
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...halfLife.parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from ...language.languageEntry import LanguageEntry
from ...language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ...microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from ...microsoft.parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
from ...microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ...microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ...misc import utils as utils
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ...ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ...ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class ChatterPreferredTtsUserMessageHelper(ChatterPreferredTtsUserMessageHelperInterface):

    def __init__(
        self,
        decTalkVoiceMapper: DecTalkVoiceMapperInterface,
        halfLifeVoiceParser: HalfLifeVoiceParserInterface,
        languagesRepository: LanguagesRepositoryInterface,
        microsoftSamJsonParser: MicrosoftSamJsonParserInterface,
        microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface,
        streamElementsJsonParser: StreamElementsJsonParserInterface,
        ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface
    ):
        if not isinstance(decTalkVoiceMapper, DecTalkVoiceMapperInterface):
            raise TypeError(f'decTalkVoiceMapper argument is malformed: \"{decTalkVoiceMapper}\"')
        elif not isinstance(halfLifeVoiceParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeVoiceParser}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')
        elif not isinstance(microsoftTtsJsonParser, MicrosoftTtsJsonParserInterface):
            raise TypeError(f'microsoftTtsJsonParser argument is malformed: \"{microsoftTtsJsonParser}\"')
        elif not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')

        self.__decTalkVoiceMapper: DecTalkVoiceMapperInterface = decTalkVoiceMapper
        self.__halfLifeJsonParser: HalfLifeVoiceParserInterface = halfLifeVoiceParser
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__microsoftSamJsonParser: MicrosoftSamJsonParserInterface = microsoftSamJsonParser
        self.__microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface = microsoftTtsJsonParser
        self.__streamElementsJsonParser: StreamElementsJsonParserInterface = streamElementsJsonParser
        self.__ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = ttsMonsterPrivateApiJsonMapper

        self.__commodoreSamRegEx: Pattern = re.compile(r'^\s*commodore(?:\s+|_|-)?sam\s*$', re.IGNORECASE)
        self.__decTalkRegEx: Pattern = re.compile(r'^\s*dec(?:\s+|_|-)?talk:?\s*(\w+\s*\w*)?\s*$', re.IGNORECASE)
        self.__googleRegEx: Pattern = re.compile(r'^\s*goog(?:le?)?\s*(\w+)?\s*$', re.IGNORECASE)
        self.__halfLifeRegEx: Pattern = re.compile(r'^\s*half(?:\s+|_|-)?life\s*(\w+)?\s*$', re.IGNORECASE)
        self.__microsoftSamRegEx: Pattern = re.compile(r'^\s*(?:microsoft|ms)(?:\s|_|-)*sam\s*(\w+)?\s*$', re.IGNORECASE)
        self.__microsoftTtsRegEx: Pattern = re.compile(r'^\s*(?:microsoft|ms)\s*(\w+)?\s*$', re.IGNORECASE)
        self.__singingDecTalkRegEx: Pattern = re.compile(r'^\s*singing(?:\s+|_|-)?dec(?:\s+|_|-)?talk\s*$', re.IGNORECASE)
        self.__streamElementsRegEx: Pattern = re.compile(r'^\s*stream(?:\s+|_|-)?elements\s*(\w+)?\s*$', re.IGNORECASE)
        self.__ttsMonsterRegEx: Pattern = re.compile(r'^\s*tts(?:\s+|_|-)?monster:?\s*(\w+)?\s*$', re.IGNORECASE)

    async def __createCommodoreSamTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return CommodoreSamPreferredTts()

    async def __createDecTalkTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        decTalkVoice: DecTalkVoice | None = None
        decTalkVoiceCommand = match.group(1)

        if utils.isValidStr(decTalkVoiceCommand):
            decTalkVoice = await self.__decTalkVoiceMapper.parseVoice(decTalkVoiceCommand)

        return DecTalkPreferredTts(
            voice = decTalkVoice
        )

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

        microsoftSamVoice: MicrosoftSamVoice | None = None
        microsoftSamVoiceCommand = match.group(1)

        if utils.isValidStr(microsoftSamVoiceCommand):
            microsoftSamVoice = await self.__microsoftSamJsonParser.parseVoice(microsoftSamVoiceCommand)

        return MicrosoftSamPreferredTts(
            voice = microsoftSamVoice
        )

    async def __createMicrosoftTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        microsoftTtsVoice: MicrosoftTtsVoice | None = None
        microsoftTtsVoiceCommand = match.group(1)

        if utils.isValidStr(microsoftTtsVoiceCommand):
            microsoftTtsVoice = await self.__microsoftTtsJsonParser.parseVoice(microsoftTtsVoiceCommand)

        return MicrosoftTtsPreferredTts(
            voice = microsoftTtsVoice
        )

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

        streamElementsVoice: StreamElementsVoice | None = None
        streamElementsVoiceCommand = match.group(1)

        if utils.isValidStr(streamElementsVoiceCommand):
            streamElementsVoice = await self.__streamElementsJsonParser.parseVoice(
                string = streamElementsVoiceCommand
            )

        return StreamElementsPreferredTts(
            voice = streamElementsVoice
        )

    async def __createTtsMonsterTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        ttsMonsterVoice: TtsMonsterVoice | None = None
        ttsMonsterVoiceCommand = match.group(1)

        if utils.isValidStr(ttsMonsterVoiceCommand):
            ttsMonsterVoice = await self.__ttsMonsterPrivateApiJsonMapper.parseVoice(
                string = ttsMonsterVoiceCommand
            )

        return TtsMonsterPreferredTts(
            voice = ttsMonsterVoice
        )

    async def parseUserMessage(
        self,
        userMessage: str | Any | None
    ) -> AbsPreferredTts | None:
        if not utils.isValidStr(userMessage):
            return None

        userMessage = utils.cleanStr(userMessage)

        commodoreSamMatch = self.__commodoreSamRegEx.fullmatch(userMessage)
        decTalkMatch = self.__decTalkRegEx.fullmatch(userMessage)
        googleMatch = self.__googleRegEx.fullmatch(userMessage)
        halfLifeMatch = self.__halfLifeRegEx.fullmatch(userMessage)
        microsoftSamMatch = self.__microsoftSamRegEx.fullmatch(userMessage)
        microsoftTtsMatch = self.__microsoftTtsRegEx.fullmatch(userMessage)
        singingDecTalkMatch = self.__singingDecTalkRegEx.fullmatch(userMessage)
        streamElementsMatch = self.__streamElementsRegEx.fullmatch(userMessage)
        ttsMonsterMatch = self.__ttsMonsterRegEx.fullmatch(userMessage)

        if commodoreSamMatch is not None:
            return await self.__createCommodoreSamTtsProperties(commodoreSamMatch)

        elif decTalkMatch is not None:
            return await self.__createDecTalkTtsProperties(decTalkMatch)

        elif googleMatch is not None:
            return await self.__createGoogleTtsProperties(googleMatch)

        elif halfLifeMatch is not None:
            return await self.__createHalfLifeTtsProperties(halfLifeMatch)

        elif microsoftSamMatch is not None:
            return await self.__createMicrosoftSamTtsProperties(microsoftSamMatch)

        elif microsoftTtsMatch is not None:
            return await self.__createMicrosoftTtsProperties(microsoftTtsMatch)

        elif singingDecTalkMatch is not None:
            return await self.__createSingingDecTalkTtsProperties(singingDecTalkMatch)

        elif streamElementsMatch is not None:
            return await self.__createStreamElementsTtsProperties(streamElementsMatch)

        elif ttsMonsterMatch is not None:
            return await self.__createTtsMonsterTtsProperties(ttsMonsterMatch)

        else:
            return None
