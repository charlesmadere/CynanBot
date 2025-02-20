from typing import Any

from .chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from ..models.absPreferredTts import AbsPreferredTts
from ..models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from ..models.google.googlePreferredTts import GooglePreferredTts
from ..models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from ..models.preferredTtsProvider import PreferredTtsProvider
from ...language.languageEntry import LanguageEntry
from ...language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ...misc import utils as utils


class ChatterPreferredTtsJsonMapper(ChatterPreferredTtsJsonMapperInterface):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')

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
            languageEntryString = configurationJson.get('language_entry', None)

            if utils.isValidStr(languageEntryString):
                languageEntry = await self.__languagesRepository.getLanguageForIso6391Code(
                    iso6391Code = languageEntryString
                )

        return GooglePreferredTts(
            languageEntry = languageEntry
        )

    async def __parseMicrosoftSamPreferredTts(
        self,
        configurationJson: dict[str, Any]
    ) -> MicrosoftSamPreferredTts:
        return MicrosoftSamPreferredTts()

    async def parsePreferredTts(
        self,
        configurationJson: dict[str, Any],
        provider: PreferredTtsProvider
    ) -> AbsPreferredTts:
        if not isinstance(provider, PreferredTtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        match provider:
            case PreferredTtsProvider.DEC_TALK:
                return await self.__parseDecTalkPreferredTts(
                    configurationJson = configurationJson
                )

            case PreferredTtsProvider.GOOGLE:
                return await self.__parseGooglePreferredTts(
                    configurationJson = configurationJson
                )

            case PreferredTtsProvider.MICROSOFT_SAM:
                return await self.__parseMicrosoftSamPreferredTts(
                    configurationJson = configurationJson
                )

            case _:
                raise ValueError(f'Encountered unknown PreferredTtsProvider: \"{provider}\"')

    async def parsePreferredTtsProvider(
        self,
        string: str | Any | None
    ) -> PreferredTtsProvider:
        if not utils.isValidStr(string):
            raise TypeError(f'string argument is malformed: \"{string}\"')

        string = string.lower()

        match string:
            case 'dec_talk': return PreferredTtsProvider.DEC_TALK
            case 'google': return PreferredTtsProvider.GOOGLE
            case 'microsoft_sam': return PreferredTtsProvider.MICROSOFT_SAM
            case _: raise ValueError(f'Encountered unknown string value: \"{string}\"')

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
            configurationJson['language_entry'] = preferredTts.languageEntry.iso6391Code

        return configurationJson

    async def __serializeMicrosoftSamPreferredTts(
        self,
        preferredTts: MicrosoftSamPreferredTts
    ) -> dict[str, Any]:
        return dict()

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

        elif isinstance(preferredTts, MicrosoftSamPreferredTts):
            return await self.__serializeMicrosoftSamPreferredTts(
                preferredTts = preferredTts
            )

        else:
            raise ValueError(f'preferredTts is an unknown type: \"{preferredTts}\"')

    async def serializePreferredTtsProvider(
        self,
        provider: PreferredTtsProvider
    ) -> str:
        match provider:
            case PreferredTtsProvider.DEC_TALK: return 'dec_talk'
            case PreferredTtsProvider.GOOGLE: return 'google'
            case PreferredTtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case _: raise ValueError(f'Encountered unknown PreferredTtsProvider value: \"{provider}\"')
