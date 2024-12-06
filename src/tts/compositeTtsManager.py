from frozendict import frozendict

from .compositeTtsManagerInterface import CompositeTtsManagerInterface
from .decTalk.decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from .google.googleTtsManagerInterface import GoogleTtsManagerInterface
from .halfLife.halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from .streamElements.streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from .ttsEvent import TtsEvent
from .ttsManagerInterface import TtsManagerInterface
from .ttsMonster.ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from .ttsProvider import TtsProvider
from .ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class CompositeTtsManager(CompositeTtsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        decTalkTtsManager: DecTalkTtsManagerInterface | None,
        googleTtsManager: GoogleTtsManagerInterface | None,
        halfLifeTtsManager: HalfLifeTtsManagerInterface | None,
        streamElementsTtsManager: StreamElementsTtsManagerInterface | None,
        timber: TimberInterface,
        ttsMonsterTtsManager: TtsMonsterTtsManagerInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        if decTalkTtsManager is not None and not isinstance(decTalkTtsManager, DecTalkTtsManagerInterface):
            raise TypeError(f'decTalkTtsManager argument is malformed: \"{decTalkTtsManager}\"')
        elif googleTtsManager is not None and not isinstance(googleTtsManager, GoogleTtsManagerInterface):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif halfLifeTtsManager is not None and not isinstance(halfLifeTtsManager, HalfLifeTtsManagerInterface):
            raise TypeError(f'halfLifeTtsManager argument is malformed: \"{halfLifeTtsManager}\"')
        elif streamElementsTtsManager is not None and not isinstance(streamElementsTtsManager, StreamElementsTtsManagerInterface):
            raise TypeError(f'streamElementsTtsManager argument is malformed: \"{streamElementsTtsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsMonsterTtsManager is not None and not isinstance(ttsMonsterTtsManager, TtsMonsterTtsManagerInterface):
            raise TypeError(f'ttsMonsterTtsManager argument is malformed: \"{ttsMonsterTtsManager}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__decTalkTtsManager: TtsManagerInterface | None = decTalkTtsManager
        self.__googleTtsManager: TtsManagerInterface | None = googleTtsManager
        self.__halfLifeTtsManager: TtsManagerInterface | None = halfLifeTtsManager
        self.__streamElementsTtsManager: TtsManagerInterface | None = streamElementsTtsManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterTtsManager: TtsManagerInterface | None = ttsMonsterTtsManager
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__ttsProviderToManagerMap: frozendict[TtsProvider, TtsManagerInterface | None] = self.__createTtsProviderToManagerMap()
        self.__currentTtsManager: TtsManagerInterface | None = None

    def __createTtsProviderToManagerMap(self) -> frozendict[TtsProvider, TtsManagerInterface | None]:
        ttsProviderToManagerMap: dict[TtsProvider, TtsManagerInterface | None] = {
            TtsProvider.DEC_TALK: self.__decTalkTtsManager,
            TtsProvider.GOOGLE: self.__googleTtsManager,
            TtsProvider.HALF_LIFE: self.__halfLifeTtsManager,
            TtsProvider.STREAM_ELEMENTS: self.__streamElementsTtsManager,
            TtsProvider.TTS_MONSTER: self.__ttsMonsterTtsManager
        }

        if len(ttsProviderToManagerMap.keys()) != len(TtsProvider):
            raise RuntimeError(f'ttsProviderToManagerMap is missing some members of TtsProvider! ({ttsProviderToManagerMap=})')

        return frozendict(ttsProviderToManagerMap)

    async def isPlaying(self) -> bool:
        currentTtsManager = self.__currentTtsManager
        return currentTtsManager is not None and await currentTtsManager.isPlaying()

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('TtsManager', f'Will not play the given TTS event as there is one already an ongoing! ({event=})')
            return False

        ttsManager = self.__ttsProviderToManagerMap[event.provider]
        self.__backgroundTaskHelper.createTask(ttsManager.playTtsEvent(event))
        self.__currentTtsManager = ttsManager

        return True

    async def stopTtsEvent(self):
        currentTtsManager = self.__currentTtsManager

        if currentTtsManager is not None:
            await currentTtsManager.stopTtsEvent()
            self.__currentTtsManager = None
