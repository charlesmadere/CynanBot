import re
from typing import Any, Final, Match, Pattern

from .chatterPreferredTtsUserMessageHelperInterface import ChatterPreferredTtsUserMessageHelperInterface
from ..models.absTtsProperties import AbsTtsProperties
from ..models.commodoreSam.commodoreSamTtsProperties import CommodoreSamTtsProperties
from ..models.decTalk.decTalkTtsProperties import DecTalkTtsProperties
from ..models.google.googleTtsProperties import GoogleTtsProperties
from ..models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from ..models.microsoft.microsoftTtsTtsProperties import MicrosoftTtsTtsProperties
from ..models.microsoftSam.microsoftSamTtsProperties import MicrosoftSamTtsProperties
from ..models.randoTts.randoTtsTtsProperties import RandoTtsTtsProperties
from ..models.shotgunTts.shotgunTtsTtsProperties import ShotgunTtsTtsProperties
from ..models.streamElements.streamElementsTtsProperties import StreamElementsTtsProperties
from ..models.ttsMonster.ttsMonsterTtsProperties import TtsMonsterTtsProperties
from ..models.unrestrictedDecTalk.unrestrictedDecTalkTtsProperties import UnrestrictedDecTalkTtsProperties
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
from ...timber.timberInterface import TimberInterface
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
        timber: TimberInterface,
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
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')

        self.__decTalkVoiceMapper: Final[DecTalkVoiceMapperInterface] = decTalkVoiceMapper
        self.__halfLifeJsonParser: Final[HalfLifeVoiceParserInterface] = halfLifeVoiceParser
        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__microsoftSamJsonParser: Final[MicrosoftSamJsonParserInterface] = microsoftSamJsonParser
        self.__microsoftTtsJsonParser: Final[MicrosoftTtsJsonParserInterface] = microsoftTtsJsonParser
        self.__streamElementsJsonParser: Final[StreamElementsJsonParserInterface] = streamElementsJsonParser
        self.__timber: Final[TimberInterface] = timber
        self.__ttsMonsterPrivateApiJsonMapper: Final[TtsMonsterPrivateApiJsonMapperInterface] = ttsMonsterPrivateApiJsonMapper

        self.__commodoreSamRegEx: Final[Pattern] = re.compile(r'^\s*commodore(?:\s+|_|-)?sam\s*$', re.IGNORECASE)
        self.__decTalkRegEx: Final[Pattern] = re.compile(r'^\s*dec(?:\s+|_|-)?talk:?\s*([\w|\s\-]+)?\s*$', re.IGNORECASE)
        self.__googleRegEx: Final[Pattern] = re.compile(r'^\s*goog(?:le?)?:?\s*([\w|\s\-]+)?\s*$', re.IGNORECASE)
        self.__halfLifeRegEx: Final[Pattern] = re.compile(r'^\s*half(?:\s+|_|-)?life:?\s*([\w|\s\-]+)?\s*$', re.IGNORECASE)
        self.__microsoftSamRegEx: Final[Pattern] = re.compile(r'^\s*(?:microsoft|ms)(?:\s|_|-)*sam:?\s*([\w|\s\-]+)?\s*$', re.IGNORECASE)
        self.__microsoftTtsRegEx: Final[Pattern] = re.compile(r'^\s*(?:microsoft|ms):?\s*([\w|\s\-]+)?\s*$', re.IGNORECASE)
        self.__randoTtsRegEx: Final[Pattern] = re.compile(r'^\s*random?(?:\s+|_|-)?(?:tts)?\s*$', re.IGNORECASE)
        self.__shotgunTtsRegEx: Final[Pattern] = re.compile(r'^\s*shotgun?(?:\s+|_|-)?(?:tts)?\s*$', re.IGNORECASE)
        self.__streamElementsRegEx: Final[Pattern] = re.compile(r'^\s*stream(?:\s+|_|-)?elements:?\s*([\w|\s\-]+)?\s*$', re.IGNORECASE)
        self.__ttsMonsterRegEx: Final[Pattern] = re.compile(r'^\s*tts(?:\s+|_|-)?monster:?\s*([\w|\s\-]+)?\s*$', re.IGNORECASE)
        self.__unrestrictedDecTalkRegEx: Final[Pattern] = re.compile(r'^\s*unrestricted(?:\s+|_|-)?dec(?:\s+|_|-)?talk\s*$', re.IGNORECASE)

    async def __createCommodoreSamTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return CommodoreSamTtsProperties()

    async def __createDecTalkTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        decTalkVoice: DecTalkVoice | None = None
        decTalkVoiceCommand = match.group(1)

        if utils.isValidStr(decTalkVoiceCommand):
            decTalkVoice = await self.__decTalkVoiceMapper.parseVoice(
                string = decTalkVoiceCommand
            )

        return DecTalkTtsProperties(
            voice = decTalkVoice
        )

    async def __createGoogleTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        languageEntry: LanguageEntry | None = None
        languageEntryCommand = match.group(1)

        if utils.isValidStr(languageEntryCommand):
            languageEntry = await self.__languagesRepository.getLanguageForCommand(
                command = languageEntryCommand
            )

        return GoogleTtsProperties(
            languageEntry = languageEntry
        )

    async def __createHalfLifeTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        halfLifeVoice: HalfLifeVoice | None = None
        halfLifeVoiceCommand = match.group(1)

        if utils.isValidStr(halfLifeVoiceCommand):
            halfLifeVoice = self.__halfLifeJsonParser.parseVoice(
                voiceString = halfLifeVoiceCommand
            )

        return HalfLifeTtsProperties(
            voice = halfLifeVoice
        )

    async def __createMicrosoftSamTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        microsoftSamVoice: MicrosoftSamVoice | None = None
        microsoftSamVoiceCommand = match.group(1)

        if utils.isValidStr(microsoftSamVoiceCommand):
            microsoftSamVoice = await self.__microsoftSamJsonParser.parseVoice(
                string = microsoftSamVoiceCommand
            )

        return MicrosoftSamTtsProperties(
            voice = microsoftSamVoice
        )

    async def __createMicrosoftTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        microsoftTtsVoice: MicrosoftTtsVoice | None = None
        microsoftTtsVoiceCommand = match.group(1)

        if utils.isValidStr(microsoftTtsVoiceCommand):
            microsoftTtsVoice = await self.__microsoftTtsJsonParser.parseVoice(
                string = microsoftTtsVoiceCommand
            )

        return MicrosoftTtsTtsProperties(
            voice = microsoftTtsVoice
        )

    async def __createRandoTtsTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return RandoTtsTtsProperties()

    async def __createShotgunTtsTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return ShotgunTtsTtsProperties()

    async def __createStreamElementsTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        streamElementsVoice: StreamElementsVoice | None = None
        streamElementsVoiceCommand = match.group(1)

        if utils.isValidStr(streamElementsVoiceCommand):
            streamElementsVoice = await self.__streamElementsJsonParser.parseVoice(
                string = streamElementsVoiceCommand
            )

        return StreamElementsTtsProperties(
            voice = streamElementsVoice
        )

    async def __createTtsMonsterTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        ttsMonsterVoice: TtsMonsterVoice | None = None
        ttsMonsterVoiceCommand = match.group(1)

        if utils.isValidStr(ttsMonsterVoiceCommand):
            ttsMonsterVoice = await self.__ttsMonsterPrivateApiJsonMapper.parseVoice(
                string = ttsMonsterVoiceCommand
            )

        return TtsMonsterTtsProperties(
            voice = ttsMonsterVoice
        )

    async def __createUnrestrictedDecTalkTtsProperties(
        self,
        match: Match[str]
    ) -> AbsTtsProperties | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return UnrestrictedDecTalkTtsProperties()

    async def parseUserMessage(
        self,
        userMessage: str | Any | None
    ) -> AbsTtsProperties | None:
        if not utils.isValidStr(userMessage):
            return None

        userMessage = utils.cleanStr(userMessage)

        commodoreSamMatch = self.__commodoreSamRegEx.fullmatch(userMessage)
        decTalkMatch = self.__decTalkRegEx.fullmatch(userMessage)
        googleMatch = self.__googleRegEx.fullmatch(userMessage)
        halfLifeMatch = self.__halfLifeRegEx.fullmatch(userMessage)
        microsoftSamMatch = self.__microsoftSamRegEx.fullmatch(userMessage)
        microsoftTtsMatch = self.__microsoftTtsRegEx.fullmatch(userMessage)
        randoTtsMatch = self.__randoTtsRegEx.fullmatch(userMessage)
        shotgunTtsMatch = self.__shotgunTtsRegEx.fullmatch(userMessage)
        streamElementsMatch = self.__streamElementsRegEx.fullmatch(userMessage)
        ttsMonsterMatch = self.__ttsMonsterRegEx.fullmatch(userMessage)
        unrestrictedDecTalkMatch = self.__unrestrictedDecTalkRegEx.fullmatch(userMessage)

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

        elif randoTtsMatch is not None:
            return await self.__createRandoTtsTtsProperties(randoTtsMatch)

        elif shotgunTtsMatch is not None:
            return await self.__createShotgunTtsTtsProperties(shotgunTtsMatch)

        elif streamElementsMatch is not None:
            return await self.__createStreamElementsTtsProperties(streamElementsMatch)

        elif ttsMonsterMatch is not None:
            return await self.__createTtsMonsterTtsProperties(ttsMonsterMatch)

        elif unrestrictedDecTalkMatch is not None:
            return await self.__createUnrestrictedDecTalkTtsProperties(unrestrictedDecTalkMatch)

        elif utils.isValidStr(userMessage):
            # User input edge case: let's assume the user might've been confused by the
            # directions for this command, and just typed in a language instead. If so,
            # we might be able to match up their string with a language name.
            languageEntry = await self.__languagesRepository.getLanguageForCommand(
                command = userMessage
            )

            if languageEntry is not None:
                googleProperties = GoogleTtsProperties(
                    languageEntry = languageEntry
                )

                self.__timber.log('ChatterPreferredTtsUserMessageHelper', f'Hit fall-back language-based case for user message ({googleProperties=}) ({languageEntry=}) ({userMessage=})')
                return googleProperties

            # User input edge case: let's assume the user might've been confused by the
            # directions for this command, and just typed in the name of a TTS Monster
            # voice instead.
            ttsMonsterVoice = await self.__ttsMonsterPrivateApiJsonMapper.parseVoice(
                string = userMessage
            )

            if ttsMonsterVoice is not None:
                ttsMonsterTtsProperties = TtsMonsterTtsProperties(
                    voice = ttsMonsterVoice
                )

                self.__timber.log('ChatterPreferredTtsUserMessageHelper', f'Hit fall-back TTS Monster voice case for user message ({ttsMonsterTtsProperties=}) ({ttsMonsterVoice=}) ({userMessage=})')
                return ttsMonsterTtsProperties

        return None
