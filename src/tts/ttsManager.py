from .decTalk.decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from .google.googleTtsManagerInterface import GoogleTtsManagerInterface
from .halfLife.halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from .streamElements.streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from .stub.stubTtsManager import StubTtsManager
from .ttsEvent import TtsEvent
from .ttsManagerInterface import TtsManagerInterface
from .ttsMonster.ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from .ttsProvider import TtsProvider
from .ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class TtsManager(TtsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        decTalkTtsManager: DecTalkTtsManagerInterface | StubTtsManager,
        googleTtsManager: GoogleTtsManagerInterface | StubTtsManager,
        halfLifeTtsManager: HalfLifeTtsManagerInterface | StubTtsManager,
        streamElementsTtsManager: StreamElementsTtsManagerInterface | StubTtsManager,
        timber: TimberInterface,
        ttsMonsterTtsManager: TtsMonsterTtsManagerInterface | StubTtsManager,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        if not isinstance(decTalkTtsManager, DecTalkTtsManagerInterface) and not isinstance(decTalkTtsManager, StubTtsManager):
            raise TypeError(f'decTalkTtsManager argument is malformed: \"{decTalkTtsManager}\"')
        elif not isinstance(googleTtsManager, GoogleTtsManagerInterface) and not isinstance(googleTtsManager, StubTtsManager):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif not isinstance(halfLifeTtsManager, HalfLifeTtsManagerInterface) and not isinstance(halfLifeTtsManager, StubTtsManager):
            raise TypeError(f'halfLifeTtsManager argument is malformed: \"{halfLifeTtsManager}\"')
        elif not isinstance(streamElementsTtsManager, StreamElementsTtsManagerInterface) and not isinstance(streamElementsTtsManager, StubTtsManager):
            raise TypeError(f'streamElementsTtsManager argument is malformed: \"{streamElementsTtsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterTtsManager, TtsMonsterTtsManagerInterface) and not isinstance(ttsMonsterTtsManager, StubTtsManager):
            raise TypeError(f'ttsMonsterTtsManager argument is malformed: \"{ttsMonsterTtsManager}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__decTalkTtsManager: TtsManagerInterface = decTalkTtsManager
        self.__googleTtsManager: TtsManagerInterface = googleTtsManager
        self.__halfLifeTtsManager: TtsManagerInterface = halfLifeTtsManager
        self.__streamElementsTtsManager: TtsManagerInterface = streamElementsTtsManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterTtsManager: TtsManagerInterface = ttsMonsterTtsManager
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__currentTtsManager: TtsManagerInterface | None = None

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

        match event.provider:
            case TtsProvider.DEC_TALK:
                self.__backgroundTaskHelper.createTask(self.__decTalkTtsManager.playTtsEvent(event))
                self.__currentTtsManager = self.__decTalkTtsManager

            case TtsProvider.GOOGLE:
                self.__backgroundTaskHelper.createTask(self.__googleTtsManager.playTtsEvent(event))
                self.__currentTtsManager = self.__googleTtsManager

            case TtsProvider.HALF_LIFE:
                self.__backgroundTaskHelper.createTask(self.__halfLifeTtsManager.playTtsEvent(event))
                self.__currentTtsManager = self.__halfLifeTtsManager

            case TtsProvider.STREAM_ELEMENTS:
                self.__backgroundTaskHelper.createTask(self.__streamElementsTtsManager.playTtsEvent(event))
                self.__currentTtsManager = self.__streamElementsTtsManager

            case TtsProvider.TTS_MONSTER:
                self.__backgroundTaskHelper.createTask(self.__ttsMonsterTtsManager.playTtsEvent(event))
                self.__currentTtsManager = self.__ttsMonsterTtsManager

        return True

    async def stopTtsEvent(self):
        currentTtsManager = self.__currentTtsManager

        if currentTtsManager is not None:
            await currentTtsManager.stopTtsEvent()
            self.__currentTtsManager = None
