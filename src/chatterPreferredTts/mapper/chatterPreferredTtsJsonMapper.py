from typing import Any

from .chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from ..models.absPreferredTts import AbsPreferredTts
from ..models.commodoreSam.commodoreSamPreferredTts import CommodoreSamPreferredTts
from ..models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from ..models.google.googlePreferredTts import GooglePreferredTts
from ..models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
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
from ...microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ...microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ...misc import utils as utils
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ...tts.models.ttsProvider import TtsProvider
from ...ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice
from ...ttsMonster.parser.ttsMonsterVoiceParserInterface import TtsMonsterVoiceParserInterface


class ChatterPreferredTtsJsonMapper(ChatterPreferredTtsJsonMapperInterface):

    def __init__(
        self,
        decTalkVoiceMapper: DecTalkVoiceMapperInterface,
        halfLifeVoiceParser: HalfLifeVoiceParserInterface,
        languagesRepository: LanguagesRepositoryInterface,
        microsoftSamJsonParser: MicrosoftSamJsonParserInterface,
        streamElementsJsonParser: StreamElementsJsonParserInterface,
        ttsMonsterVoiceParser: TtsMonsterVoiceParserInterface
    ):
        if not isinstance(decTalkVoiceMapper, DecTalkVoiceMapperInterface):
            raise TypeError(f'decTalkVoiceMapper argument is malformed: \"{decTalkVoiceMapper}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(halfLifeVoiceParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeVoiceParser}\"')
        elif not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')
        elif not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')
        elif not isinstance(ttsMonsterVoiceParser, TtsMonsterVoiceParserInterface):
            raise TypeError(f'ttsMonsterVoiceParser argument is malformed: \"{ttsMonsterVoiceParser}\"')

        self.__decTalkVoiceMapper: DecTalkVoiceMapperInterface = decTalkVoiceMapper
        self.__halfLifeJsonParser: HalfLifeVoiceParserInterface = halfLifeVoiceParser
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__microsoftSamJsonParser: MicrosoftSamJsonParserInterface = microsoftSamJsonParser
        self.__streamElementsJsonParser: StreamElementsJsonParserInterface = streamElementsJsonParser
        self.__ttsMonsterVoiceParser: TtsMonsterVoiceParserInterface = ttsMonsterVoiceParser

    async def __parseCommodoreSamPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> CommodoreSamPreferredTts:
        return CommodoreSamPreferredTts()

    async def __parseDecTalkPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> DecTalkPreferredTts:
        voice: DecTalkVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('voice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__decTalkVoiceMapper.parseVoice(voiceString)

        return DecTalkPreferredTts(
            voice = voice
        )

    async def __parseGooglePreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> GooglePreferredTts:
        languageEntry: LanguageEntry | None = None

        if len(configurationJson) >= 1:
            languageEntryString: str | Any | None = configurationJson.get('iso6391', None)

            if utils.isValidStr(languageEntryString):
                languageEntry = await self.__languagesRepository.getLanguageForIso6391Code(
                    iso6391Code = languageEntryString
                )

        return GooglePreferredTts(
            languageEntry = languageEntry
        )

    async def __parseHalfLifePreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> HalfLifePreferredTts:
        halfLifeVoice: HalfLifeVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('halfLifeVoice', None)

            if utils.isValidStr(voiceString):
                halfLifeVoice = self.__halfLifeJsonParser.parseVoice(voiceString)

        return HalfLifePreferredTts(
            halfLifeVoice = halfLifeVoice
        )

    async def __parseMicrosoftSamPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> MicrosoftSamPreferredTts:
        voice: MicrosoftSamVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('microsoftSamVoice', None)

            if utils.isValidStr(voiceString):
                voice = self.__microsoftSamJsonParser.parseVoice(voiceString)

        return MicrosoftSamPreferredTts(
            voice = voice
        )

    async def __parseSingingDecTalkPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> SingingDecTalkPreferredTts:
        return SingingDecTalkPreferredTts()

    async def __parseStreamElementsPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> StreamElementsPreferredTts:
        voice: StreamElementsVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('streamElementsVoice', None)

            if utils.isValidStr(voiceString):
                voice = self.__streamElementsJsonParser.parseVoice(voiceString)

        return StreamElementsPreferredTts(
            voice = voice
        )

    async def __parseTtsMonsterPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> TtsMonsterPreferredTts:
        ttsMonsterVoice: TtsMonsterVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('ttsMonsterVoice', None)

            if utils.isValidStr(voiceString):
                ttsMonsterVoice = self.__ttsMonsterVoiceParser.parseVoice(voiceString)

        return TtsMonsterPreferredTts(
            ttsMonsterVoice = ttsMonsterVoice
        )

    async def parsePreferredTts(
        self,
        configurationJson: dict[str, Any],
        provider: TtsProvider
    ) -> AbsPreferredTts:
        if not isinstance(configurationJson, dict):
            raise TypeError(f'configurationJson argument is malformed: \"{configurationJson}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        match provider:
            case TtsProvider.COMMODORE_SAM:
                return await self.__parseCommodoreSamPreferredTts(
                    configurationJson = configurationJson
                )

            case TtsProvider.DEC_TALK:
                return await self.__parseDecTalkPreferredTts(
                    configurationJson = configurationJson
                )

            case TtsProvider.GOOGLE:
                return await self.__parseGooglePreferredTts(
                    configurationJson = configurationJson
                )

            case TtsProvider.HALF_LIFE:
                return await self.__parseHalfLifePreferredTts(
                    configurationJson = configurationJson
                )

            case TtsProvider.MICROSOFT_SAM:
                return await self.__parseMicrosoftSamPreferredTts(
                    configurationJson = configurationJson
                )

            case TtsProvider.SINGING_DEC_TALK:
                return await self.__parseSingingDecTalkPreferredTts(
                    configurationJson = configurationJson
                )

            case TtsProvider.STREAM_ELEMENTS:
                return await self.__parseStreamElementsPreferredTts(
                    configurationJson = configurationJson
                )

            case TtsProvider.TTS_MONSTER:
                return await self.__parseTtsMonsterPreferredTts(
                    configurationJson = configurationJson
                )

            case _:
                raise ValueError(f'Encountered unknown PreferredTtsProvider: \"{provider}\"')

    async def __serializeCommodoreSamPreferredTts(
        self,
        preferredTts: CommodoreSamPreferredTts
    ) -> dict[str, Any]:
        return dict()

    async def __serializeDecTalkPreferredTts(
        self,
        preferredTts: DecTalkPreferredTts
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['decTalkVoice'] = await self.__decTalkVoiceMapper.serializeVoice(preferredTts.voice)

        return configurationJson

    async def __serializeGooglePreferredTts(
        self,
        preferredTts: GooglePreferredTts
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.languageEntry is not None:
            configurationJson['iso6391'] = preferredTts.languageEntry.iso6391Code

        return configurationJson

    async def __serializeHalfLifePreferredTts(
        self,
        preferredTts: HalfLifePreferredTts
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.halfLifeVoiceEntry is not None:
            configurationJson['halfLifeVoice'] = preferredTts.halfLifeVoiceEntry.keyName

        return configurationJson

    async def __serializeMicrosoftSamPreferredTts(
        self,
        preferredTts: MicrosoftSamPreferredTts
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['microsoftSamVoice'] = preferredTts.voice.jsonValue

        return configurationJson

    async def __serializeSingingDecTalkPreferredTts(
        self,
        preferredTts: SingingDecTalkPreferredTts
    ) -> dict[str, Any]:
        return dict()

    async def __serializeStreamElementsPreferredTts(
        self,
        preferredTts: StreamElementsPreferredTts
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['streamElementsVoice'] = self.__streamElementsJsonParser.serializeVoice(
                voice = preferredTts.voice
            )

        return configurationJson

    async def __serializeTtsMonsterPreferredTts(
        self,
        preferredTts: TtsMonsterPreferredTts
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.ttsMonsterVoiceEntry is not None:
            configurationJson['ttsMonsterVoice'] = preferredTts.ttsMonsterVoiceEntry.inMessageName

        return configurationJson

    async def serializePreferredTts(
        self,
        preferredTts: AbsPreferredTts
    ) -> dict[str, Any]:
        if not isinstance(preferredTts, AbsPreferredTts):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        if isinstance(preferredTts, CommodoreSamPreferredTts):
            return await self.__serializeCommodoreSamPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, DecTalkPreferredTts):
            return await self.__serializeDecTalkPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, GooglePreferredTts):
            return await self.__serializeGooglePreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, HalfLifePreferredTts):
            return await self.__serializeHalfLifePreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, MicrosoftSamPreferredTts):
            return await self.__serializeMicrosoftSamPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, SingingDecTalkPreferredTts):
            return await self.__serializeSingingDecTalkPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, StreamElementsPreferredTts):
            return await self.__serializeStreamElementsPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, TtsMonsterPreferredTts):
            return await self.__serializeTtsMonsterPreferredTts(
                preferredTts = preferredTts
            )

        else:
            raise ValueError(f'preferredTts is an unknown type: \"{preferredTts}\"')
