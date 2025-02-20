from typing import Any

from .chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
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
from ...tts.ttsProvider import TtsProvider


class ChatterPreferredTtsJsonMapper(ChatterPreferredTtsJsonMapperInterface):

    def __init__(
        self,
        halfLifeVoiceParser: HalfLifeVoiceParserInterface,
        languagesRepository: LanguagesRepositoryInterface
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(halfLifeVoiceParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeVoiceParser}\"')

        self.__halfLifeJsonParser: HalfLifeVoiceParserInterface = halfLifeVoiceParser
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository

    async def __parseDecTalkPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> DecTalkPreferredTts:
        return DecTalkPreferredTts()

    async def __parseGooglePreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> GooglePreferredTts:
        languageEntry: LanguageEntry | None = None

        if isinstance(configurationJson, dict):
            languageEntryString = configurationJson.get('iso6391', None)

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
        halfLifeVoice: HalfLifeVoice = HalfLifeVoice.ALL

        if isinstance(configurationJson, dict):
            halfLifeVoiceString = configurationJson.get('halfLifeVoice', None)

            if utils.isValidStr(halfLifeVoiceString):
                halfLifeVoice = self.__halfLifeJsonParser.requireVoice(halfLifeVoiceString)

        return HalfLifePreferredTts(
            halfLifeVoice = halfLifeVoice
        )

    async def __parseMicrosoftSamPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> MicrosoftSamPreferredTts:
        return MicrosoftSamPreferredTts()

    async def __parseSingingDecTalkPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> SingingDecTalkPreferredTts:
        return SingingDecTalkPreferredTts()

    async def __parseStreamElementsPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> StreamElementsPreferredTts:
        return StreamElementsPreferredTts()

    async def __parseTtsMonsterPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> TtsMonsterPreferredTts:
        if isinstance(configurationJson, dict):
            ttsMonsterVoiceString = configurationJson.get('ttsMonsterVoice', None)

        return TtsMonsterPreferredTts(ttsMonsterVoiceString)

    async def parsePreferredTts(
        self,
        configurationJson: dict[str, Any],
        provider: TtsProvider
    ) -> AbsPreferredTts:
        if not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        match provider:
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

    async def __serializeDecTalkPreferredTts(
        self,
        preferredTts: DecTalkPreferredTts
    ) -> dict[str, Any]:
        return dict()

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

        configurationJson['halfLifeVoice'] = preferredTts.halfLifeVoiceEntry.keyName

        return configurationJson

    async def __serializeMicrosoftSamPreferredTts(
        self,
        preferredTts: MicrosoftSamPreferredTts
    ) -> dict[str, Any]:
        return dict()

    async def __serializeSingingDecTalkPreferredTts(
        self,
        preferredTts: SingingDecTalkPreferredTts
    ) -> dict[str, Any]:
        return dict()

    async def __serializeStreamElementsPreferredTts(
        self,
        preferredTts: StreamElementsPreferredTts
    ) -> dict[str, Any]:
        return dict()

    async def __serializeTtsMonsterPreferredTts(
        self,
        preferredTts: TtsMonsterPreferredTts
    ) -> dict[str, Any]:
        configurationJson: dict[str, Any] = dict()

        if preferredTts.ttsMonsterVoiceEntry is not None:
            configurationJson['ttsMonsterVoice'] = preferredTts.ttsMonsterVoiceEntry

        return configurationJson

    async def serializePreferredTts(
        self,
        preferredTts: AbsPreferredTts
    ) -> dict[str, Any]:
        if not isinstance(preferredTts, AbsPreferredTts):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        if isinstance(preferredTts, DecTalkPreferredTts):
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
