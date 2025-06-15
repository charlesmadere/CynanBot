import random
from typing import Final

from frozenlist import FrozenList

from .chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..exceptions import NoEnabledTtsProvidersException
from ..models.absTtsProperties import AbsTtsProperties
from ..models.chatterPrefferedTts import ChatterPreferredTts
from ..models.commodoreSam.commodoreSamPreferredTts import CommodoreSamTtsProperties
from ..models.decTalk.decTalkPreferredTts import DecTalkTtsProperties
from ..models.google.googlePreferredTts import GoogleTtsProperties
from ..models.ttsMonster.ttsMonsterPreferredTts import TtsMonsterTtsProperties
from ..repository.chatterPreferredTtsRepositoryInterface import ChatterPreferredTtsRepositoryInterface
from ..settings.chatterPreferredTtsSettingsRepositoryInterface import ChatterPreferredTtsSettingsRepositoryInterface
from ...decTalk.models.decTalkVoice import DecTalkVoice
from ...google.helpers.googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ...language.languageEntry import LanguageEntry
from ...misc import utils as utils
from ...tts.models.ttsProvider import TtsProvider
from ...ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class ChatterPreferredTtsHelper(ChatterPreferredTtsHelperInterface):

    def __init__(
        self,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface
    ):
        if not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(googleTtsVoicesHelper, GoogleTtsVoicesHelperInterface):
            raise TypeError(f'googleTtsVoicesHelper argument is malformed: \"{googleTtsVoicesHelper}\"')

        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__googleTtsVoicesHelper: Final[GoogleTtsVoicesHelperInterface] = googleTtsVoicesHelper

    async def applyRandomPreferredTts(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        enabledTtsProviders: FrozenList[TtsProvider] = FrozenList()

        for ttsProvider in TtsProvider:
            if await self.__chatterPreferredTtsSettingsRepository.isTtsProviderEnabled(ttsProvider):
                enabledTtsProviders.append(ttsProvider)

        enabledTtsProviders.freeze()

        if len(enabledTtsProviders) == 0:
            raise NoEnabledTtsProvidersException(f'Can\'t randomly apply a preferred TTS as there are no TTS Providers enabled ({enabledTtsProviders=}) ({chatterUserId=}) ({twitchChannelId=})')

        ttsProvider = random.choice(enabledTtsProviders)
        properties: AbsTtsProperties

        match ttsProvider:
            case TtsProvider.COMMODORE_SAM:
                properties = await self.__chooseCommodoreSamProperties()

            case TtsProvider.DEC_TALK:
                properties = await self.__chooseRandomDecTalkProperties()

            case TtsProvider.GOOGLE:
                properties = await self.__chooseRandomGoogleProperties()

            case TtsProvider.TTS_MONSTER:
                properties = await self.__chooseRandomTtsMonsterProperties()

            case _:
                raise ValueError(f'The given TTS Provider is unknown ({ttsProvider=}) ({enabledTtsProviders=}) ({chatterUserId=}) ({twitchChannelId=})')

        preferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        await self.__chatterPreferredTtsRepository.set(preferredTts = preferredTts)
        return preferredTts

    async def __chooseCommodoreSamProperties(self) -> CommodoreSamTtsProperties:
        return CommodoreSamTtsProperties()

    async def __chooseRandomDecTalkProperties(self) -> DecTalkTtsProperties:
        voices: list[DecTalkVoice] = list(DecTalkVoice)
        voice = random.choice(voices)

        return DecTalkTtsProperties(
            voice = voice
        )

    async def __chooseRandomGoogleProperties(self) -> GoogleTtsProperties:
        languageEntries: list[LanguageEntry] = list()

        for languageEntry in LanguageEntry:
            googleVoicePreset = self.__googleTtsVoicesHelper.getVoiceForLanguage(languageEntry)

            if googleVoicePreset is not None:
                languageEntries.append(languageEntry)

        languageEntry = random.choice(languageEntries)

        return GoogleTtsProperties(
            languageEntry = languageEntry
        )

    async def __chooseRandomTtsMonsterProperties(self) -> TtsMonsterTtsProperties:
        voices: list[TtsMonsterVoice] = list(TtsMonsterVoice)
        voice = random.choice(voices)

        return TtsMonsterTtsProperties(
            voice = voice
        )

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return None

        preferredTts = await self.__chatterPreferredTtsRepository.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        if preferredTts is None:
            return None
        elif not await self.__chatterPreferredTtsSettingsRepository.isTtsProviderEnabled(
            provider = preferredTts.properties.provider
        ):
            return None
        else:
            return preferredTts
