from typing import Any, Dict, Optional

from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.decTalk.decTalkManager import DecTalkManager
from CynanBot.tts.google.googleTtsManager import GoogleTtsManager
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.tts.ttsMonster.ttsMonsterManager import TtsMonsterManager
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface


class TtsManager(TtsManagerInterface):

    def __init__(
        self,
        decTalkManager: Optional[DecTalkManager],
        googleTtsManager: Optional[GoogleTtsManager],
        timber: TimberInterface,
        ttsMonsterManager: Optional[TtsMonsterManager],
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if decTalkManager is not None and not isinstance(decTalkManager, DecTalkManager):
            raise TypeError(f'decTalkManager argument is malformed: \"{decTalkManager}\"')
        elif googleTtsManager is not None and not isinstance(googleTtsManager, GoogleTtsManager):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsMonsterManager is not None and not isinstance(ttsMonsterManager, TtsMonsterManager):
            raise TypeError(f'ttsMonsterManager argument is malformed: \"{googleTtsManager}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__decTalkManager: Optional[TtsManagerInterface] = decTalkManager
        self.__googleTtsManager: Optional[TtsManagerInterface] = googleTtsManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterManager: Optional[TtsMonsterManager] = ttsMonsterManager
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__currentTtsManager: Optional[TtsManagerInterface] = None

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

        provider = event.getProvider()
        decTalkManager = self.__decTalkManager
        googleTtsManager = self.__googleTtsManager
        ttsMonsterManager = self.__ttsMonsterManager

        if provider is TtsProvider.DEC_TALK and decTalkManager is not None:
            if await decTalkManager.playTtsEvent(event):
                self.__currentTtsManager = decTalkManager
                return True
        elif provider is TtsProvider.GOOGLE and googleTtsManager is not None:
            if await googleTtsManager.playTtsEvent(event):
                self.__currentTtsManager = googleTtsManager
                return True
        elif provider is TtsProvider.TTS_MONSTER and ttsMonsterManager is not None:
            if await ttsMonsterManager.playTtsEvent(event):
                self.__currentTtsManager = ttsMonsterManager
                return True

        self.__timber.log('TtsManager', f'Unable to play the given TTS event via the requested TTS provider ({event=}) ({provider=})')
        return False

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'currentTtsManager': self.__currentTtsManager
        }
