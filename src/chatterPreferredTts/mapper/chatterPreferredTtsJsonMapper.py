from typing import Any

from .chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from ..models.absTtsProperties import AbsTtsProperties
from ..models.commodoreSam.commodoreSamTtsProperties import CommodoreSamTtsProperties
from ..models.decTalk.decTalkTtsProperties import DecTalkTtsProperties
from ..models.google.googleTtsProperties import GoogleTtsProperties
from ..models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from ..models.microsoft.microsoftTtsTtsProperties import MicrosoftTtsTtsProperties
from ..models.microsoftSam.microsoftSamTtsProperties import MicrosoftSamTtsProperties
from ..models.singingDecTalk.singingDecTalkTtsProperties import SingingDecTalkTtsProperties
from ..models.streamElements.streamElementsTtsProperties import StreamElementsTtsProperties
from ..models.ttsMonster.ttsMonsterTtsProperties import TtsMonsterTtsProperties
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
from ...tts.models.ttsProvider import TtsProvider
from ...ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ...ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class ChatterPreferredTtsJsonMapper(ChatterPreferredTtsJsonMapperInterface):

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
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(halfLifeVoiceParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeVoiceParser}\"')
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

    async def __parseCommodoreSamTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> CommodoreSamTtsProperties:
        return CommodoreSamTtsProperties()

    async def __parseDecTalkTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> DecTalkTtsProperties:
        voice: DecTalkVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('voice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__decTalkVoiceMapper.parseVoice(voiceString)

        return DecTalkTtsProperties(
            voice = voice
        )

    async def __parseGoogleTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> GoogleTtsProperties:
        languageEntry: LanguageEntry | None = None

        if len(configurationJson) >= 1:
            languageEntryString: str | Any | None = configurationJson.get('iso6391', None)

            if utils.isValidStr(languageEntryString):
                languageEntry = await self.__languagesRepository.getLanguageForIso6391Code(
                    iso6391Code = languageEntryString
                )

        return GoogleTtsProperties(
            languageEntry = languageEntry
        )

    async def __parseHalfLifeTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> HalfLifeTtsProperties:
        voice: HalfLifeVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('halfLifeVoice', None)

            if utils.isValidStr(voiceString):
                voice = self.__halfLifeJsonParser.parseVoice(voiceString)

        return HalfLifeTtsProperties(
            voice = voice
        )

    async def __parseMicrosoftSamTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> MicrosoftSamTtsProperties:
        voice: MicrosoftSamVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('microsoftSamVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__microsoftSamJsonParser.parseVoice(voiceString)

        return MicrosoftSamTtsProperties(
            voice = voice
        )

    async def __parseMicrosoftTtsTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> MicrosoftTtsTtsProperties:
        voice: MicrosoftTtsVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('microsoftTtsVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__microsoftTtsJsonParser.parseVoice(voiceString)

        return MicrosoftTtsTtsProperties(
            voice = voice
        )

    async def __parseSingingDecTalkTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> SingingDecTalkTtsProperties:
        return SingingDecTalkTtsProperties()

    async def __parseStreamElementsTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> StreamElementsTtsProperties:
        voice: StreamElementsVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('streamElementsVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__streamElementsJsonParser.parseVoice(
                    string = voiceString
                )

        return StreamElementsTtsProperties(
            voice = voice
        )

    async def __parseTtsMonsterTtsProperties(
        self,
        configurationJson: dict[str, Any]
    ) -> TtsMonsterTtsProperties:
        voice: TtsMonsterVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('ttsMonsterVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__ttsMonsterPrivateApiJsonMapper.parseVoice(
                    string = voiceString
                )

        return TtsMonsterTtsProperties(
            voice = voice
        )

    async def parsePreferredTts(
        self,
        configurationJson: dict[str, Any],
        provider: TtsProvider
    ) -> AbsTtsProperties:
        if not isinstance(configurationJson, dict):
            raise TypeError(f'configurationJson argument is malformed: \"{configurationJson}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        match provider:
            case TtsProvider.COMMODORE_SAM:
                return await self.__parseCommodoreSamTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.DEC_TALK:
                return await self.__parseDecTalkTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.GOOGLE:
                return await self.__parseGoogleTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.HALF_LIFE:
                return await self.__parseHalfLifeTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.MICROSOFT:
                return await self.__parseMicrosoftTtsTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.MICROSOFT_SAM:
                return await self.__parseMicrosoftSamTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.SINGING_DEC_TALK:
                return await self.__parseSingingDecTalkTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.STREAM_ELEMENTS:
                return await self.__parseStreamElementsTtsProperties(
                    configurationJson = configurationJson
                )

            case TtsProvider.TTS_MONSTER:
                return await self.__parseTtsMonsterTtsProperties(
                    configurationJson = configurationJson
                )

            case _:
                raise ValueError(f'Encountered unknown PreferredTtsProvider: \"{provider}\"')

    async def __serializeCommodoreSamPreferredTts(
        self,
        preferredTts: CommodoreSamTtsProperties
    ) -> dict[str, Any]:
        return dict()

    async def __serializeDecTalkPreferredTts(
        self,
        preferredTts: DecTalkTtsProperties
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['voice'] = await self.__decTalkVoiceMapper.serializeVoice(preferredTts.voice)

        return configurationJson

    async def __serializeGooglePreferredTts(
        self,
        preferredTts: GoogleTtsProperties
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.languageEntry is not None:
            configurationJson['iso6391'] = preferredTts.languageEntry.iso6391Code

        return configurationJson

    async def __serializeHalfLifePreferredTts(
        self,
        preferredTts: HalfLifeTtsProperties
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['halfLifeVoice'] = preferredTts.voice.keyName

        return configurationJson

    async def __serializeMicrosoftSamPreferredTts(
        self,
        preferredTts: MicrosoftSamTtsProperties
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['microsoftSamVoice'] = await self.__microsoftSamJsonParser.serializeVoice(
                voice = preferredTts.voice
            )

        return configurationJson

    async def __serializeMicrosoftTtsPreferredTts(
        self,
        preferredTts: MicrosoftTtsTtsProperties
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['microsoftTtsVoice'] = await self.__microsoftTtsJsonParser.serializeVoice(
                voice = preferredTts.voice
            )

        return configurationJson

    async def __serializeSingingDecTalkPreferredTts(
        self,
        preferredTts: SingingDecTalkTtsProperties
    ) -> dict[str, Any]:
        return dict()

    async def __serializeStreamElementsPreferredTts(
        self,
        preferredTts: StreamElementsTtsProperties
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['streamElementsVoice'] = await self.__streamElementsJsonParser.serializeVoice(
                voice = preferredTts.voice
            )

        return configurationJson

    async def __serializeTtsMonsterPreferredTts(
        self,
        preferredTts: TtsMonsterTtsProperties
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.voice is not None:
            configurationJson['ttsMonsterVoice'] = await self.__ttsMonsterPrivateApiJsonMapper.serializeVoice(
                voice = preferredTts.voice
            )

        return configurationJson

    async def serializePreferredTts(
        self,
        preferredTts: AbsTtsProperties
    ) -> dict[str, Any]:
        if not isinstance(preferredTts, AbsTtsProperties):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        if isinstance(preferredTts, CommodoreSamTtsProperties):
            return await self.__serializeCommodoreSamPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, DecTalkTtsProperties):
            return await self.__serializeDecTalkPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, GoogleTtsProperties):
            return await self.__serializeGooglePreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, HalfLifeTtsProperties):
            return await self.__serializeHalfLifePreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, MicrosoftSamTtsProperties):
            return await self.__serializeMicrosoftSamPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, MicrosoftTtsTtsProperties):
            return await self.__serializeMicrosoftTtsPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, SingingDecTalkTtsProperties):
            return await self.__serializeSingingDecTalkPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, StreamElementsTtsProperties):
            return await self.__serializeStreamElementsPreferredTts(
                preferredTts = preferredTts
            )

        elif isinstance(preferredTts, TtsMonsterTtsProperties):
            return await self.__serializeTtsMonsterPreferredTts(
                preferredTts = preferredTts
            )

        else:
            raise ValueError(f'preferredTts is an unknown type: \"{preferredTts}\"')
