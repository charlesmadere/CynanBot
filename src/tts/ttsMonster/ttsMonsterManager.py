from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from ..tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface


class TtsMonsterManager(TtsManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsMonsterFileManager: TtsMonsterFileManagerInterface,
        ttsMonsterHelper: TtsMonsterHelperInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface
    ):
        if not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterFileManager, TtsMonsterFileManagerInterface):
            raise TypeError(f'ttsMonsterFileManager argument is malformed: \"{ttsMonsterFileManager}\"')
        elif not isinstance(ttsMonsterHelper, TtsMonsterHelperInterface):
            raise TypeError(f'ttsMonsterHelper argument is malformed: \"{ttsMonsterHelper}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterFileManager: TtsMonsterFileManagerInterface = ttsMonsterFileManager
        self.__ttsMonsterHelper: TtsMonsterHelperInterface = ttsMonsterHelper
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper

    async def isPlaying(self) -> bool:
        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to TTS Monster,
        #  and yet in this scenario, this method would still return true. So for the fix for this
        #  is probably a way to check if SoundPlayerManager is currently playing, AND also a check
        #  to see specifically what media it is currently playing.
        return await self.__soundPlayerManager.isPlaying()

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('TtsMonsterManager', f'There is already an ongoing TTS Monster event!')
            return False

        ttsMessageUrls = await self.__ttsMonsterHelper.generateTts(
            message = event.message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

        if ttsMessageUrls is None or len(ttsMessageUrls) == 0:
            self.__timber.log('TtsMonsterManager', f'Failed to generate any TTS messages ({event=}) ({ttsMessageUrls=})')
            return False

        ttsFileNames = await self.__ttsMonsterFileManager.saveTtsUrlsToNewFiles(ttsMessageUrls)

        if ttsFileNames is None or len(ttsFileNames) == 0:
            self.__timber.log('TtsMonsterManager', f'Failed to download/save TTS messages ({event=}) ({ttsMessageUrls=}) ({ttsFileNames=})')
            return False

        # TODO
        return False
