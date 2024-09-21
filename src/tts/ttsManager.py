from typing import Any

from .decTalk.decTalkManager import DecTalkManager
from .google.googleTtsManager import GoogleTtsManager
from .streamElements.streamElementsTtsManager import StreamElementsTtsManager
from .tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from .ttsEvent import TtsEvent
from .ttsManagerInterface import TtsManagerInterface
from .ttsMonster.ttsMonsterManagerInterface import TtsMonsterManagerInterface
from .ttsProvider import TtsProvider
from .ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..timber.timberInterface import TimberInterface


class TtsManager(TtsManagerInterface):

    def __init__(
        self,
        decTalkManager: DecTalkManager | None,
        googleTtsManager: GoogleTtsManager | None,
        streamElementsTtsManager: StreamElementsTtsManager | None,
        timber: TimberInterface,
        ttsMonsterManager: TtsMonsterManagerInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface
    ):
        if decTalkManager is not None and not isinstance(decTalkManager, DecTalkManager):
            raise TypeError(f'decTalkManager argument is malformed: \"{decTalkManager}\"')
        elif googleTtsManager is not None and not isinstance(googleTtsManager, GoogleTtsManager):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif streamElementsTtsManager is not None and not isinstance(streamElementsTtsManager, StreamElementsTtsManager):
            raise TypeError(f'streamElementsTtsManager argument is malformed: \"{streamElementsTtsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsMonsterManager is not None and not isinstance(ttsMonsterManager, TtsMonsterManagerInterface):
            raise TypeError(f'ttsMonsterManager argument is malformed: \"{ttsMonsterManager}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')

        self.__decTalkManager: TtsManagerInterface | None = decTalkManager
        self.__googleTtsManager: TtsManagerInterface | None = googleTtsManager
        self.__streamElementsTtsManager: StreamElementsTtsManager = streamElementsTtsManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterManager: TtsMonsterManagerInterface | None = ttsMonsterManager
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper

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

        decTalkManager = self.__decTalkManager
        googleTtsManager = self.__googleTtsManager
        streamElementsTtsManager = self.__streamElementsTtsManager
        ttsMonsterManager = self.__ttsMonsterManager
        proceed = False

        if event.provider is TtsProvider.DEC_TALK and decTalkManager is not None:
            if await decTalkManager.playTtsEvent(event):
                self.__currentTtsManager = decTalkManager
                proceed = True
        elif event.provider is TtsProvider.GOOGLE and googleTtsManager is not None:
            if await googleTtsManager.playTtsEvent(event):
                self.__currentTtsManager = googleTtsManager
                proceed = True
        elif event.provider is TtsProvider.STREAM_ELEMENTS and streamElementsTtsManager is not None:
            if await streamElementsTtsManager.playTtsEvent(event):
                self.__currentTtsManager = streamElementsTtsManager
                proceed = True
        elif event.provider is TtsProvider.TTS_MONSTER and ttsMonsterManager is not None:
            if await ttsMonsterManager.playTtsEvent(event):
                self.__currentTtsManager = ttsMonsterManager
                proceed = True

        if proceed:
            await self.__ttsTempFileHelper.deleteOldTempFiles()
            return True
        else:
            self.__timber.log('TtsManager', f'Unable to play the given TTS event via the requested TTS provider ({event=}) ({event.provider=})')
            return False

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'currentTtsManager': self.__currentTtsManager
        }
