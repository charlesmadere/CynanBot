from frozendict import frozendict

from .compositeTtsManagerInterface import CompositeTtsManagerInterface
from .decTalk.decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from .google.googleTtsManagerInterface import GoogleTtsManagerInterface
from .halfLife.halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from .microsoftSam.microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from .streamElements.streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from .ttsEvent import TtsEvent
from .ttsManagerInterface import TtsManagerInterface
from .ttsMonster.ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from .ttsProvider import TtsProvider
from .ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..chatterPreferredTts.models.preferredTtsProvider import PreferredTtsProvider
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class CompositeTtsManager(CompositeTtsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface | None,
        decTalkTtsManager: DecTalkTtsManagerInterface | None,
        googleTtsManager: GoogleTtsManagerInterface | None,
        halfLifeTtsManager: HalfLifeTtsManagerInterface | None,
        microsoftSamTtsManager: MicrosoftSamTtsManagerInterface | None,
        singingDecTalkTtsManager: DecTalkTtsManagerInterface | None,
        streamElementsTtsManager: StreamElementsTtsManagerInterface | None,
        timber: TimberInterface,
        ttsMonsterTtsManager: TtsMonsterTtsManagerInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif chatterPreferredTtsHelper is not None and not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif decTalkTtsManager is not None and not isinstance(decTalkTtsManager, DecTalkTtsManagerInterface):
            raise TypeError(f'decTalkTtsManager argument is malformed: \"{decTalkTtsManager}\"')
        elif googleTtsManager is not None and not isinstance(googleTtsManager, GoogleTtsManagerInterface):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif halfLifeTtsManager is not None and not isinstance(halfLifeTtsManager, HalfLifeTtsManagerInterface):
            raise TypeError(f'halfLifeTtsManager argument is malformed: \"{halfLifeTtsManager}\"')
        elif microsoftSamTtsManager is not None and not isinstance(microsoftSamTtsManager, MicrosoftSamTtsManagerInterface):
            raise TypeError(f'microsoftSamTtsManager argument is malformed: \"{microsoftSamTtsManager}\"')
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

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface | None = chatterPreferredTtsHelper
        self.__decTalkTtsManager: TtsManagerInterface | None = decTalkTtsManager
        self.__googleTtsManager: TtsManagerInterface | None = googleTtsManager
        self.__halfLifeTtsManager: TtsManagerInterface | None = halfLifeTtsManager
        self.__microsoftSamTtsManager: MicrosoftSamTtsManagerInterface | None = microsoftSamTtsManager
        self.__singingDecTalkTtsManager: TtsManagerInterface | None = singingDecTalkTtsManager
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
            TtsProvider.MICROSOFT_SAM: self.__microsoftSamTtsManager,
            TtsProvider.SINGING_DEC_TALK: self.__singingDecTalkTtsManager,
            TtsProvider.STREAM_ELEMENTS: self.__streamElementsTtsManager,
            TtsProvider.TTS_MONSTER: self.__ttsMonsterTtsManager
        }

        if len(ttsProviderToManagerMap.keys()) != len(TtsProvider):
            raise RuntimeError(f'ttsProviderToManagerMap is missing some members of TtsProvider! ({ttsProviderToManagerMap=})')

        return frozendict(ttsProviderToManagerMap)

    async def __determineTtsProvider(self, event: TtsEvent) -> TtsProvider:
        if not event.allowChatterPreferredTts:
            return event.provider

        chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper

        if chatterPreferredTtsHelper is None:
            return event.provider

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId
        )

        if preferredTts is None:
            return event.provider

        self.__timber.log('CompositeTtsManager', f'Chatter has a preferred TTS ({preferredTts=}) ({event=})')

        match preferredTts.preferredTts.preferredTtsProvider:
            case PreferredTtsProvider.DEC_TALK: return TtsProvider.DEC_TALK
            case PreferredTtsProvider.GOOGLE: return TtsProvider.GOOGLE
            case PreferredTtsProvider.MICROSOFT_SAM: return TtsProvider.MICROSOFT_SAM
            case _: return event.provider

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
