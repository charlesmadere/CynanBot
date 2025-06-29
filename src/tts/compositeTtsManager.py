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
from .models.ttsEvent import TtsEvent
from .models.ttsProvider import TtsProvider
from .models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from .settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from .shotgun.shotgunTtsManagerInterface import ShotgunTtsManagerInterface
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
        googleTtsManager: GoogleTtsManagerInterface | None,
        halfLifeTtsManager: HalfLifeTtsManagerInterface | None,
        microsoftTtsManager: MicrosoftTtsManagerInterface | None,
        microsoftSamTtsManager: MicrosoftSamTtsManagerInterface | None,
        shotgunTtsManager: ShotgunTtsManagerInterface | None,
        singingDecTalkTtsManager: DecTalkTtsManagerInterface | None,
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
        elif googleTtsManager is not None and not isinstance(googleTtsManager, GoogleTtsManagerInterface):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif halfLifeTtsManager is not None and not isinstance(halfLifeTtsManager, HalfLifeTtsManagerInterface):
            raise TypeError(f'halfLifeTtsManager argument is malformed: \"{halfLifeTtsManager}\"')
        elif microsoftTtsManager is not None and not isinstance(microsoftTtsManager, MicrosoftTtsManagerInterface):
            raise TypeError(f'microsoftTtsManager argument is malformed: \"{microsoftTtsManager}\"')
        elif microsoftSamTtsManager is not None and not isinstance(microsoftSamTtsManager, MicrosoftSamTtsManagerInterface):
            raise TypeError(f'microsoftSamTtsManager argument is malformed: \"{microsoftSamTtsManager}\"')
        elif shotgunTtsManager is not None and not isinstance(shotgunTtsManager, ShotgunTtsManagerInterface):
            raise TypeError(f'shotgunTtsManager argument is malformed: \"{shotgunTtsManager}\"')
        elif singingDecTalkTtsManager is not None and not isinstance(singingDecTalkTtsManager, DecTalkTtsManagerInterface):
            raise TypeError(f'singingDecTalkTtsManager argument is malformed: \"{singingDecTalkTtsManager}\"')
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
            TtsProvider.SHOTGUN_TTS: shotgunTtsManager,
            TtsProvider.SINGING_DEC_TALK: singingDecTalkTtsManager,
            TtsProvider.STREAM_ELEMENTS: streamElementsTtsManager,
            TtsProvider.TTS_MONSTER: ttsMonsterTtsManager,
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

            for key, value in self.__ttsProviderToManagerMap.items():
                if key is TtsProvider.GOOGLE:
                    # not allowing Google for this as it potentially has financial concerns
                    continue
                elif value is None:
                    continue
                else:
                    availableProviders.add(key)

            if len(availableProviders) >= 1:
                chosenProvider = random.choice(list(availableProviders))
                self.__timber.log('CompositeTtsManager', f'Chatter uses random preferred TTS ({chosenProvider=}) ({preferredTts=}) ({event=})')
                return chosenProvider

        self.__timber.log('CompositeTtsManager', f'Chatter has a preferred TTS ({preferredTts=}) ({event=})')
        return preferredTts.properties.provider

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

        ttsProvider = await self.__determineTtsProvider(event)
        ttsManager = self.__ttsProviderToManagerMap.get(ttsProvider, None)

        if ttsManager is None:
            self.__currentTtsManager = None
            return False
        else:
            self.__currentTtsManager = ttsManager
            self.__backgroundTaskHelper.createTask(ttsManager.playTtsEvent(event))
            return True

    async def stopTtsEvent(self):
        currentTtsManager = self.__currentTtsManager

        if currentTtsManager is not None:
            await currentTtsManager.stopTtsEvent()
            self.__currentTtsManager = None
