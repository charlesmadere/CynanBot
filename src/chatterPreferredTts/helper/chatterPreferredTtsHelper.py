import random
from typing import Final

from frozenlist import FrozenList

from .chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from .chatterPreferredTtsUserMessageHelperInterface import ChatterPreferredTtsUserMessageHelperInterface
from ..exceptions import FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, \
    UnableToParseUserMessageIntoTtsException, TtsProviderIsNotEnabledException
from ..models.absTtsProperties import AbsTtsProperties
from ..models.chatterPrefferedTts import ChatterPreferredTts
from ..models.commodoreSam.commodoreSamTtsProperties import CommodoreSamTtsProperties
from ..models.decTalk.decTalkTtsProperties import DecTalkTtsProperties
from ..models.google.googleTtsProperties import GoogleTtsProperties
from ..models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from ..models.microsoft.microsoftTtsTtsProperties import MicrosoftTtsTtsProperties
from ..models.microsoftSam.microsoftSamTtsProperties import MicrosoftSamTtsProperties
from ..models.streamElements.streamElementsTtsProperties import StreamElementsTtsProperties
from ..models.ttsMonster.ttsMonsterTtsProperties import TtsMonsterTtsProperties
from ..repository.chatterPreferredTtsRepositoryInterface import ChatterPreferredTtsRepositoryInterface
from ..settings.chatterPreferredTtsSettingsRepositoryInterface import ChatterPreferredTtsSettingsRepositoryInterface
from ...decTalk.models.decTalkVoice import DecTalkVoice
from ...google.helpers.googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...language.languageEntry import LanguageEntry
from ...microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from ...microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider
from ...ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice
from ...twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier
from ...twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface


class ChatterPreferredTtsHelper(ChatterPreferredTtsHelperInterface):

    def __init__(
        self,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        chatterPreferredTtsUserMessageHelper: ChatterPreferredTtsUserMessageHelperInterface,
        googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface,
        timber: TimberInterface,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
    ):
        if not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(chatterPreferredTtsUserMessageHelper, ChatterPreferredTtsUserMessageHelperInterface):
            raise TypeError(f'chatterPreferredTtsUserMessageHelper argument is malformed: \"{chatterPreferredTtsUserMessageHelper}\"')
        elif not isinstance(googleTtsVoicesHelper, GoogleTtsVoicesHelperInterface):
            raise TypeError(f'googleTtsVoicesHelper argument is malformed: \"{googleTtsVoicesHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')

        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__chatterPreferredTtsUserMessageHelper: Final[ChatterPreferredTtsUserMessageHelperInterface] = chatterPreferredTtsUserMessageHelper
        self.__googleTtsVoicesHelper: Final[GoogleTtsVoicesHelperInterface] = googleTtsVoicesHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchSubscriptionsRepository: Final[TwitchSubscriptionsRepositoryInterface] = twitchSubscriptionsRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository

    async def applyRandomPreferredTts(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredTts:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        randomChoiceEnabledTtsProviders: FrozenList[TtsProvider] = FrozenList()

        for ttsProvider in TtsProvider:
            if ttsProvider in await self.__chatterPreferredTtsSettingsRepository.getHighTierTtsProviders():
                continue
            elif ttsProvider in await self.__chatterPreferredTtsSettingsRepository.getEnabledTtsProviders():
                randomChoiceEnabledTtsProviders.append(ttsProvider)

        randomChoiceEnabledTtsProviders.freeze()

        if len(randomChoiceEnabledTtsProviders) == 0:
            raise NoEnabledTtsProvidersException(f'Can\'t randomly apply a preferred TTS as there are no random choice TTS Providers available ({randomChoiceEnabledTtsProviders=}) ({chatterUserId=}) ({twitchChannelId=})')

        ttsProvider = random.choice(randomChoiceEnabledTtsProviders)
        properties: AbsTtsProperties | None = None

        match ttsProvider:
            case TtsProvider.COMMODORE_SAM:
                properties = await self.__chooseCommodoreSamProperties()

            case TtsProvider.DEC_TALK:
                properties = await self.__chooseRandomDecTalkProperties()

            case TtsProvider.GOOGLE:
                properties = await self.__chooseRandomGoogleProperties()

            case TtsProvider.HALF_LIFE:
                properties = await self.__chooseRandomHalfLifeProperties()

            case TtsProvider.MICROSOFT:
                properties = await self.__chooseRandomMicrosoftProperties()

            case TtsProvider.MICROSOFT_SAM:
                properties = await self.__chooseRandomMicrosoftSamProperties()

            case TtsProvider.RANDO_TTS:
                properties = None

            case TtsProvider.SHOTGUN_TTS:
                properties = None

            case TtsProvider.STREAM_ELEMENTS:
                properties = await self.__chooseRandomStreamElementsProperties()

            case TtsProvider.TTS_MONSTER:
                properties = await self.__chooseRandomTtsMonsterProperties()

            case TtsProvider.UNRESTRICTED_DEC_TALK:
                properties = None

            case _:
                raise ValueError(f'The given TTS Provider is unknown ({properties=}) ({ttsProvider=}) ({randomChoiceEnabledTtsProviders=}) ({chatterUserId=}) ({twitchChannelId=})')

        if properties is None or properties.provider not in randomChoiceEnabledTtsProviders:
            raise FailedToChooseRandomTtsException(f'Failed to choose a random preferred TTS ({properties=}) ({ttsProvider=}) ({randomChoiceEnabledTtsProviders=}) ({chatterUserId=}) ({twitchChannelId=})')

        preferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        await self.__chatterPreferredTtsRepository.set(
            preferredTts = preferredTts,
        )

        self.__timber.log('ChatterPreferredTtsHelper', f'Randomly chose and assigned new TTS ({preferredTts=}) ({chatterUserId=}) ({twitchChannelId=})')
        return preferredTts

    async def applyUserMessagePreferredTts(
        self,
        chatterUserId: str,
        twitchChannelId: str,
        userMessage: str | None,
    ) -> ChatterPreferredTts:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif userMessage is not None and not isinstance(userMessage, str):
            raise TypeError(f'userMessage argument is malformed: \"{userMessage}\"')

        properties = await self.__chatterPreferredTtsUserMessageHelper.parseUserMessage(
            userMessage = userMessage,
        )

        if properties is None:
            raise UnableToParseUserMessageIntoTtsException(f'Failed to parse user message into TTS ({properties=}) ({chatterUserId=}) ({twitchChannelId=}) ({userMessage=})')
        elif properties.provider not in await self.__chatterPreferredTtsSettingsRepository.getEnabledTtsProviders():
            raise TtsProviderIsNotEnabledException(f'The TtsProvider specified in the given user message is not enabled ({properties=}) ({chatterUserId=}) ({twitchChannelId=}) ({userMessage=})')

        if properties.provider in await self.__chatterPreferredTtsSettingsRepository.getHighTierTtsProviders():
            if await self.__isHighTierEligibleChatter(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            ):
                self.__timber.log('ChatterPreferredTtsHelper', f'Confirmed user\'s permissions for the given high tier TtsProvider ({properties=}) ({chatterUserId=}) ({twitchChannelId=})')
            else:
                raise TtsProviderIsNotEnabledException(f'The given TtsProvider is high tier, but the user does not have the required permissions ({properties=}) ({chatterUserId=}) ({twitchChannelId=})')

        preferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        await self.__chatterPreferredTtsRepository.set(
            preferredTts = preferredTts,
        )

        self.__timber.log('ChatterPreferredTtsHelper', f'Assigned TTS from user message ({preferredTts=}) ({properties=}) ({chatterUserId=}) ({twitchChannelId=}) ({userMessage=})')
        return preferredTts

    async def __chooseCommodoreSamProperties(self) -> CommodoreSamTtsProperties:
        return CommodoreSamTtsProperties()

    async def __chooseRandomDecTalkProperties(self) -> DecTalkTtsProperties:
        voices: list[DecTalkVoice] = list(DecTalkVoice)
        voice = random.choice(voices)

        return DecTalkTtsProperties(
            voice = voice,
        )

    async def __chooseRandomGoogleProperties(self) -> GoogleTtsProperties:
        languageEntries: list[LanguageEntry] = list()

        for languageEntry in LanguageEntry:
            googleVoicePreset = await self.__googleTtsVoicesHelper.getVoiceForLanguage(languageEntry)

            if googleVoicePreset is not None:
                languageEntries.append(languageEntry)

        if len(languageEntries) == 0:
            raise RuntimeError(f'Failed to find any LanguageEntry with an associated GoogleVoicePreset ({languageEntries=})')

        languageEntry = random.choice(languageEntries)

        return GoogleTtsProperties(
            languageEntry = languageEntry,
        )

    async def __chooseRandomHalfLifeProperties(self) -> HalfLifeTtsProperties:
        voices: list[HalfLifeVoice] = list(HalfLifeVoice)
        voice = random.choice(voices)

        return HalfLifeTtsProperties(
            voice = voice,
        )

    async def __chooseRandomMicrosoftProperties(self) -> MicrosoftTtsTtsProperties:
        voices: list[MicrosoftTtsVoice] = list(MicrosoftTtsVoice)
        voice = random.choice(voices)

        return MicrosoftTtsTtsProperties(
            voice = voice,
        )

    async def __chooseRandomMicrosoftSamProperties(self) -> MicrosoftSamTtsProperties:
        voices: list[MicrosoftSamVoice] = list(MicrosoftSamVoice)
        voice = random.choice(voices)

        return MicrosoftSamTtsProperties(
            voice = voice,
        )

    async def __chooseRandomStreamElementsProperties(self) -> StreamElementsTtsProperties:
        voices: list[StreamElementsVoice] = list(StreamElementsVoice)
        voice = random.choice(voices)

        return StreamElementsTtsProperties(
            voice = voice,
        )

    async def __chooseRandomTtsMonsterProperties(self) -> TtsMonsterTtsProperties:
        voices: list[TtsMonsterVoice] = list(TtsMonsterVoice)
        voice = random.choice(voices)

        return TtsMonsterTtsProperties(
            voice = voice,
        )

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredTts | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return None

        preferredTts = await self.__chatterPreferredTtsRepository.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        if preferredTts is None:
            return None
        elif preferredTts.provider not in await self.__chatterPreferredTtsSettingsRepository.getEnabledTtsProviders():
            return None
        elif preferredTts.provider in await self.__chatterPreferredTtsSettingsRepository.getHighTierTtsProviders():
            if not await self.__isHighTierEligibleChatter(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            ):
                return None

        return preferredTts

    async def __isHighTierEligibleChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('ChatterPreferredTtsHelper', f'Unable to check the given user\'s high tier TTS permissions, as no Twitch access token is available ({chatterUserId=}) ({twitchChannelId=}) ({twitchAccessToken=})')
            return False

        subscriptionStatus = await self.__twitchSubscriptionsRepository.fetchSubscription(
            chatterUserId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        return subscriptionStatus is not None and subscriptionStatus.tier is TwitchSubscriberTier.TIER_THREE
