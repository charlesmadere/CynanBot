import random
from typing import Final

from frozendict import frozendict

from .commodoreSam.commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from .compositeTtsManagerInterface import CompositeTtsManagerInterface
from .decTalk.decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from .google.googleTtsManagerInterface import GoogleTtsManagerInterface
from .halfLife.halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from .microsoft.microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from .microsoftSam.microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from .models.shotgun.useAllShotgunParameters import UseAllShotgunParameters
from .models.shotgun.useExactAmountShotgunParameters import UseExactAmountShotgunParameters
from .models.shotgun.useRandomAmountShotgunParameters import UseRandomAmountShotgunParameters
from .models.ttsEvent import TtsEvent
from .models.ttsProvider import TtsProvider
from .models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from .settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from .streamElements.streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from .ttsManagerInterface import TtsManagerInterface
from .ttsMonster.ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class CompositeTtsManager(CompositeTtsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface | None,
        commodoreSamTtsManager: CommodoreSamTtsManagerInterface | None,
        decTalkTtsManager: DecTalkTtsManagerInterface | None,
        unrestrictedDecTalkTtsManager: DecTalkTtsManagerInterface | None,
        googleTtsManager: GoogleTtsManagerInterface | None,
        halfLifeTtsManager: HalfLifeTtsManagerInterface | None,
        microsoftTtsManager: MicrosoftTtsManagerInterface | None,
        microsoftSamTtsManager: MicrosoftSamTtsManagerInterface | None,
        streamElementsTtsManager: StreamElementsTtsManagerInterface | None,
        timber: TimberInterface,
        ttsMonsterTtsManager: TtsMonsterTtsManagerInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif chatterPreferredTtsHelper is not None and not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif commodoreSamTtsManager is not None and not isinstance(commodoreSamTtsManager, CommodoreSamTtsManagerInterface):
            raise TypeError(f'commodoreSamTtsManager argument is malformed: \"{commodoreSamTtsManager}\"')
        elif decTalkTtsManager is not None and not isinstance(decTalkTtsManager, DecTalkTtsManagerInterface):
            raise TypeError(f'decTalkTtsManager argument is malformed: \"{decTalkTtsManager}\"')
        elif unrestrictedDecTalkTtsManager is not None and not isinstance(unrestrictedDecTalkTtsManager, DecTalkTtsManagerInterface):
            raise TypeError(f'unrestrictedDecTalkTtsManager argument is malformed: \"{unrestrictedDecTalkTtsManager}\"')
        elif googleTtsManager is not None and not isinstance(googleTtsManager, GoogleTtsManagerInterface):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif halfLifeTtsManager is not None and not isinstance(halfLifeTtsManager, HalfLifeTtsManagerInterface):
            raise TypeError(f'halfLifeTtsManager argument is malformed: \"{halfLifeTtsManager}\"')
        elif microsoftTtsManager is not None and not isinstance(microsoftTtsManager, MicrosoftTtsManagerInterface):
            raise TypeError(f'microsoftTtsManager argument is malformed: \"{microsoftTtsManager}\"')
        elif microsoftSamTtsManager is not None and not isinstance(microsoftSamTtsManager, MicrosoftSamTtsManagerInterface):
            raise TypeError(f'microsoftSamTtsManager argument is malformed: \"{microsoftSamTtsManager}\"')
        elif streamElementsTtsManager is not None and not isinstance(streamElementsTtsManager, StreamElementsTtsManagerInterface):
            raise TypeError(f'streamElementsTtsManager argument is malformed: \"{streamElementsTtsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsMonsterTtsManager is not None and not isinstance(ttsMonsterTtsManager, TtsMonsterTtsManagerInterface):
            raise TypeError(f'ttsMonsterTtsManager argument is malformed: \"{ttsMonsterTtsManager}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface | None] = chatterPreferredTtsHelper
        self.__timber: Final[TimberInterface] = timber
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__ttsProviderToManagerMap: Final[frozendict[TtsProvider, TtsManagerInterface | None]] = frozendict({
            TtsProvider.COMMODORE_SAM: commodoreSamTtsManager,
            TtsProvider.DEC_TALK: decTalkTtsManager,
            TtsProvider.GOOGLE: googleTtsManager,
            TtsProvider.HALF_LIFE: halfLifeTtsManager,
            TtsProvider.MICROSOFT: microsoftTtsManager,
            TtsProvider.MICROSOFT_SAM: microsoftSamTtsManager,
            TtsProvider.STREAM_ELEMENTS: streamElementsTtsManager,
            TtsProvider.TTS_MONSTER: ttsMonsterTtsManager,
            TtsProvider.UNRESTRICTED_DEC_TALK: unrestrictedDecTalkTtsManager,
        })

        self.__currentTtsManager: TtsManagerInterface | None = None

    async def __determineTtsProvider(self, event: TtsEvent) -> TtsProvider:
        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return event.provider
        elif self.__chatterPreferredTtsHelper is None:
            return event.provider

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if preferredTts is None:
            return event.provider

        if preferredTts.provider is TtsProvider.RANDO_TTS:
            availableProviders: set[TtsProvider] = set()
            randoEnabledProviders = await self.__ttsSettingsRepository.getRandoEnabledProviders()

            for provider, manager in self.__ttsProviderToManagerMap.items():
                if provider in randoEnabledProviders and manager is not None:
                    availableProviders.add(provider)

            if len(availableProviders) >= 1:
                chosenProvider = random.choice(list(availableProviders))
                self.__timber.log('CompositeTtsManager', f'Chatter uses random preferred TTS ({chosenProvider=}) ({preferredTts=}) ({event=})')
                return chosenProvider

        self.__timber.log('CompositeTtsManager', f'Chatter has a preferred TTS ({preferredTts=}) ({event=})')
        return preferredTts.properties.provider

    async def __handleShotgunTtsEvent(self, event: TtsEvent) -> bool:
        parameters = await self.__ttsSettingsRepository.getShotgunProviderUseParameters()

        if isinstance(parameters, UseAllShotgunParameters):
            return await self.__handleShotgunUseAllTtsEvent(
                event = event,
                parameters = parameters,
            )

        elif isinstance(parameters, UseExactAmountShotgunParameters):
            return await self.__handleShotgunUseExactAmountTtsEvent(
                event = event,
                parameters = parameters,
            )

        elif isinstance(parameters, UseRandomAmountShotgunParameters):
            return await self.__handleShotgunUseRandomAmountTtsEvent(
                event = event,
                parameters = parameters,
            )

        else:
            self.__timber.log('CompositeTtsManager', f'Encountered unknown shotgun parameters ({parameters=}) ({event=})')
            return False

    async def __handleShotgunUseAllTtsEvent(
        self,
        event: TtsEvent,
        parameters: UseAllShotgunParameters,
    ) -> bool:
        if not isinstance(parameters, UseAllShotgunParameters):
            raise TypeError(f'parameters argument is malformed: \"{parameters}\"')

        enabledProviders = await self.__ttsSettingsRepository.getShotgunEnabledProviders()
        chosenProviders: dict[TtsProvider, TtsManagerInterface] = dict()

        for provider, manager in self.__ttsProviderToManagerMap.items():
            if provider in enabledProviders and manager is not None:
                chosenProviders[provider] = manager

        if len(chosenProviders) == 0:
            self.__timber.log('CompositeTtsManager', f'This shotgun TTS event was unable to find any available TTS Providers ({chosenProviders=}) ({event=}) ({parameters=})')
            return False

        eventCopy = TtsEvent(
            message = event.message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId,
            userId = event.userId,
            userName = event.userName,
            donation = event.donation,
            provider = TtsProvider.SHOTGUN_TTS,
            providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
            raidInfo = event.raidInfo,
        )

        self.__timber.log('CompositeTtsManager', f'This shotgun TTS event is using all available TTS Providers ({chosenProviders.keys()=}) ({event=}) ({eventCopy=}) ({parameters=})')

        for provider, manager in chosenProviders.items():
            self.__backgroundTaskHelper.createTask(manager.playTtsEvent(eventCopy))

        return True

    async def __handleShotgunUseExactAmountTtsEvent(
        self,
        event: TtsEvent,
        parameters: UseExactAmountShotgunParameters,
    ) -> bool:
        if not isinstance(parameters, UseExactAmountShotgunParameters):
            raise TypeError(f'parameters argument is malformed: \"{parameters}\"')

        enabledProviders = await self.__ttsSettingsRepository.getShotgunEnabledProviders()
        availableProviders: list[TtsProvider] = list()

        for provider, manager in self.__ttsProviderToManagerMap.items():
            if provider in enabledProviders and manager is not None:
                availableProviders.append(provider)

        chosenProviders: list[TtsProvider] = list()

        while len(chosenProviders) < parameters.amount and len(availableProviders) >= 1:
            chosenProvider = random.choice(availableProviders)
            chosenProviders.append(chosenProvider)
            availableProviders.remove(chosenProvider)

        if len(chosenProviders) == 0:
            self.__timber.log('CompositeTtsManager', f'This shotgun TTS event was unable to find any available TTS Providers ({chosenProviders=}) ({event=}) ({parameters=})')
            return False

        self.__timber.log('CompositeTtsManager', f'This shotgun TTS event is using {len(chosenProviders)} available TTS Provider(s) ({chosenProviders=}) ({event=}) ({parameters=})')

        for chosenProvider in chosenProviders:
            manager = self.__ttsProviderToManagerMap.get(chosenProvider, None)

            if manager is not None:
                self.__backgroundTaskHelper.createTask(manager.playTtsEvent(event))

        return True

    async def __handleShotgunUseRandomAmountTtsEvent(
        self,
        event: TtsEvent,
        parameters: UseRandomAmountShotgunParameters,
    ) -> bool:
        if not isinstance(parameters, UseRandomAmountShotgunParameters):
            raise TypeError(f'parameters argument is malformed: \"{parameters}\"')

        enabledProviders = await self.__ttsSettingsRepository.getShotgunEnabledProviders()
        availableProviders: list[TtsProvider] = list()

        for provider, manager in self.__ttsProviderToManagerMap.items():
            if provider in enabledProviders and manager is not None:
                availableProviders.append(provider)

        chosenProviders: list[TtsProvider] = list()
        chosenAmount = random.randint(parameters.minAmount, parameters.maxAmount)

        while len(chosenProviders) < chosenAmount and len(availableProviders) >= 1:
            chosenProvider = random.choice(availableProviders)
            chosenProviders.append(chosenProvider)
            availableProviders.remove(chosenProvider)

        if len(chosenProviders) == 0:
            self.__timber.log('CompositeTtsManager', f'This shotgun TTS event was unable to find any available TTS Providers ({chosenAmount=}) ({chosenProviders=}) ({event=}) ({parameters=})')
            return False

        self.__timber.log('CompositeTtsManager', f'This shotgun TTS event is using {len(chosenProviders)} available TTS Provider(s) ({chosenAmount=}) ({chosenProviders=}) ({event=}) ({parameters=})')

        for chosenProvider in chosenProviders:
            manager = self.__ttsProviderToManagerMap.get(chosenProvider, None)

            if manager is not None:
                self.__backgroundTaskHelper.createTask(manager.playTtsEvent(event))

        return True

    @property
    def isLoadingOrPlaying(self) -> bool:
        currentTtsManager = self.__currentTtsManager

        if currentTtsManager is None:
            return False
        elif currentTtsManager.isLoadingOrPlaying:
            return True
        else:
            self.__currentTtsManager = None
            return False

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif self.isLoadingOrPlaying:
            self.__timber.log('CompositeTtsManager', f'Will not play the given TTS event as there is one already an ongoing! ({event=})')
            return False

        provider = await self.__determineTtsProvider(event)
        manager = self.__ttsProviderToManagerMap.get(provider, None)

        if provider is TtsProvider.SHOTGUN_TTS:
            return await self.__handleShotgunTtsEvent(event)
        elif manager is None:
            self.__currentTtsManager = None
            return False
        else:
            self.__currentTtsManager = manager
            self.__backgroundTaskHelper.createTask(manager.playTtsEvent(event))
            return True

    async def stopTtsEvent(self):
        currentTtsManager = self.__currentTtsManager

        if currentTtsManager is not None:
            await currentTtsManager.stopTtsEvent()
            self.__currentTtsManager = None
