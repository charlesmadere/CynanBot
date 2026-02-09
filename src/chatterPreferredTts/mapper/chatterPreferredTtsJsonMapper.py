from typing import Any, Final

from .chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
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
            raise TypeError(f'halfLifeVoiceParser argument is malformed: \"{halfLifeVoiceParser}\"')
        elif not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')
        elif not isinstance(microsoftTtsJsonParser, MicrosoftTtsJsonParserInterface):
            raise TypeError(f'microsoftTtsJsonParser argument is malformed: \"{microsoftTtsJsonParser}\"')
        elif not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')

        self.__decTalkVoiceMapper: Final[DecTalkVoiceMapperInterface] = decTalkVoiceMapper
        self.__halfLifeVoiceParser: Final[HalfLifeVoiceParserInterface] = halfLifeVoiceParser
        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__microsoftSamJsonParser: Final[MicrosoftSamJsonParserInterface] = microsoftSamJsonParser
        self.__microsoftTtsJsonParser: Final[MicrosoftTtsJsonParserInterface] = microsoftTtsJsonParser
        self.__streamElementsJsonParser: Final[StreamElementsJsonParserInterface] = streamElementsJsonParser
        self.__ttsMonsterPrivateApiJsonMapper: Final[TtsMonsterPrivateApiJsonMapperInterface] = ttsMonsterPrivateApiJsonMapper

    async def __parseCommodoreSamTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> CommodoreSamTtsProperties:
        return CommodoreSamTtsProperties()

    async def __parseDecTalkTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> DecTalkTtsProperties:
        voice: DecTalkVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('voice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__decTalkVoiceMapper.parseVoice(voiceString)

        return DecTalkTtsProperties(
            voice = voice,
        )

    async def __parseGoogleTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> GoogleTtsProperties:
        languageEntry: LanguageEntry | None = None

        if len(configurationJson) >= 1:
            languageEntryString: str | Any | None = configurationJson.get('iso6391', None)

            if utils.isValidStr(languageEntryString):
                languageEntry = await self.__languagesRepository.getLanguageForIso6391Code(
                    iso6391Code = languageEntryString,
                )

        return GoogleTtsProperties(
            languageEntry = languageEntry,
        )

    async def __parseHalfLifeTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> HalfLifeTtsProperties:
        voice: HalfLifeVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('halfLifeVoice', None)

            if utils.isValidStr(voiceString):
                voice = self.__halfLifeVoiceParser.parseVoice(
                    voiceString = voiceString,
                )

        return HalfLifeTtsProperties(
            voice = voice,
        )

    async def __parseMicrosoftSamTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> MicrosoftSamTtsProperties:
        voice: MicrosoftSamVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('microsoftSamVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__microsoftSamJsonParser.parseVoice(
                    string = voiceString,
                )

        return MicrosoftSamTtsProperties(
            voice = voice,
        )

    async def __parseMicrosoftTtsTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> MicrosoftTtsTtsProperties:
        voice: MicrosoftTtsVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('microsoftTtsVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__microsoftTtsJsonParser.parseVoice(
                    string = voiceString,
                )

        return MicrosoftTtsTtsProperties(
            voice = voice,
        )

    async def __parseRandoTtsTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> RandoTtsTtsProperties:
        return RandoTtsTtsProperties()

    async def __parseShotgunTtsTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> ShotgunTtsTtsProperties:
        return ShotgunTtsTtsProperties()

    async def __parseStreamElementsTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> StreamElementsTtsProperties:
        voice: StreamElementsVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('streamElementsVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__streamElementsJsonParser.parseVoice(
                    string = voiceString,
                )

        return StreamElementsTtsProperties(
            voice = voice,
        )

    async def __parseTtsMonsterTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> TtsMonsterTtsProperties:
        voice: TtsMonsterVoice | None = None

        if len(configurationJson) >= 1:
            voiceString: str | Any | None = configurationJson.get('ttsMonsterVoice', None)

            if utils.isValidStr(voiceString):
                voice = await self.__ttsMonsterPrivateApiJsonMapper.parseVoice(
                    string = voiceString,
                )

        return TtsMonsterTtsProperties(
            voice = voice,
        )

    async def __parseUnrestrictedDecTalkTtsProperties(
        self,
        configurationJson: dict[str, Any],
    ) -> UnrestrictedDecTalkTtsProperties:
        return UnrestrictedDecTalkTtsProperties()

    async def parseTtsProperties(
        self,
        configurationJson: dict[str, Any],
        provider: TtsProvider,
    ) -> AbsTtsProperties:
        if not isinstance(configurationJson, dict):
            raise TypeError(f'configurationJson argument is malformed: \"{configurationJson}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        match provider:
            case TtsProvider.COMMODORE_SAM:
                return await self.__parseCommodoreSamTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.DEC_TALK:
                return await self.__parseDecTalkTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.GOOGLE:
                return await self.__parseGoogleTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.HALF_LIFE:
                return await self.__parseHalfLifeTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.MICROSOFT:
                return await self.__parseMicrosoftTtsTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.MICROSOFT_SAM:
                return await self.__parseMicrosoftSamTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.RANDO_TTS:
                return await self.__parseRandoTtsTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.SHOTGUN_TTS:
                return await self.__parseShotgunTtsTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.STREAM_ELEMENTS:
                return await self.__parseStreamElementsTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.TTS_MONSTER:
                return await self.__parseTtsMonsterTtsProperties(
                    configurationJson = configurationJson,
                )

            case TtsProvider.UNRESTRICTED_DEC_TALK:
                return await self.__parseUnrestrictedDecTalkTtsProperties(
                    configurationJson = configurationJson,
                )

            case _:
                raise ValueError(f'Encountered unknown PreferredTtsProvider: \"{provider}\"')

    async def __serializeCommodoreSamTtsProperties(
        self,
        ttsProperties: CommodoreSamTtsProperties,
    ) -> dict[str, Any]:
        return dict()

    async def __serializeDecTalkTtsProperties(
        self,
        ttsProperties: DecTalkTtsProperties,
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if ttsProperties.voice is not None:
            configurationJson['voice'] = await self.__decTalkVoiceMapper.serializeVoice(
                voice = ttsProperties.voice,
            )

        return configurationJson

    async def __serializeGoogleTtsProperties(
        self,
        ttsProperties: GoogleTtsProperties,
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if ttsProperties.languageEntry is not None:
            configurationJson['iso6391'] = ttsProperties.languageEntry.iso6391Code

        return configurationJson

    async def __serializeHalfLifeTtsProperties(
        self,
        ttsProperties: HalfLifeTtsProperties,
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if ttsProperties.voice is not None:
            configurationJson['halfLifeVoice'] = self.__halfLifeVoiceParser.serializeVoice(
                voice = ttsProperties.voice,
            )

        return configurationJson

    async def __serializeMicrosoftSamTtsProperties(
        self,
        ttsProperties: MicrosoftSamTtsProperties,
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if ttsProperties.voice is not None:
            configurationJson['microsoftSamVoice'] = await self.__microsoftSamJsonParser.serializeVoice(
                voice = ttsProperties.voice,
            )

        return configurationJson

    async def __serializeMicrosoftTtsTtsProperties(
        self,
        ttsProperties: MicrosoftTtsTtsProperties,
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if ttsProperties.voice is not None:
            configurationJson['microsoftTtsVoice'] = await self.__microsoftTtsJsonParser.serializeVoice(
                voice = ttsProperties.voice,
            )

        return configurationJson

    async def __serializeRandoTtsTtsProperties(
        self,
        ttsProperties: RandoTtsTtsProperties,
    ) -> dict[str, Any]:
        return dict()

    async def __serializeShotgunTtsTtsProperties(
        self,
        ttsProperties: ShotgunTtsTtsProperties,
    ) -> dict[str, Any]:
        return dict()

    async def __serializeStreamElementsTtsProperties(
        self,
        ttsProperties: StreamElementsTtsProperties,
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if ttsProperties.voice is not None:
            configurationJson['streamElementsVoice'] = await self.__streamElementsJsonParser.serializeVoice(
                voice = ttsProperties.voice,
            )

        return configurationJson

    async def __serializeTtsMonsterTtsProperties(
        self,
        ttsProperties: TtsMonsterTtsProperties,
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if ttsProperties.voice is not None:
            configurationJson['ttsMonsterVoice'] = await self.__ttsMonsterPrivateApiJsonMapper.serializeVoice(
                voice = ttsProperties.voice,
            )

        return configurationJson

    async def __serializeUnrestrictedDecTalkTtsProperties(
        self,
        ttsProperties: UnrestrictedDecTalkTtsProperties,
    ) -> dict[str, Any]:
        return dict()

    async def serializeTtsProperties(
        self,
        ttsProperties: AbsTtsProperties,
    ) -> dict[str, Any]:
        if not isinstance(ttsProperties, AbsTtsProperties):
            raise TypeError(f'preferredTts argument is malformed: \"{ttsProperties}\"')

        if isinstance(ttsProperties, CommodoreSamTtsProperties):
            return await self.__serializeCommodoreSamTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, DecTalkTtsProperties):
            return await self.__serializeDecTalkTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, GoogleTtsProperties):
            return await self.__serializeGoogleTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, HalfLifeTtsProperties):
            return await self.__serializeHalfLifeTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, MicrosoftSamTtsProperties):
            return await self.__serializeMicrosoftSamTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, MicrosoftTtsTtsProperties):
            return await self.__serializeMicrosoftTtsTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, RandoTtsTtsProperties):
            return await self.__serializeRandoTtsTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, ShotgunTtsTtsProperties):
            return await self.__serializeShotgunTtsTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, StreamElementsTtsProperties):
            return await self.__serializeStreamElementsTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, TtsMonsterTtsProperties):
            return await self.__serializeTtsMonsterTtsProperties(
                ttsProperties = ttsProperties,
            )

        elif isinstance(ttsProperties, UnrestrictedDecTalkTtsProperties):
            return await self.__serializeUnrestrictedDecTalkTtsProperties(
                ttsProperties = ttsProperties,
            )

        else:
            raise ValueError(f'preferredTts is an unknown type: \"{ttsProperties}\"')
