import aiofiles.ospath

from .streamElementsFileManagerInterface import StreamElementsFileManagerInterface
from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from ...timber.timberInterface import TimberInterface


class StreamElementsTtsManager(TtsManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        streamElementsFileManager: StreamElementsFileManagerInterface,
        streamElementsHelper: StreamElementsHelperInterface,
        timber: Timber,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        if not isinstance(streamElementsFileManager, StreamElementsFileManagerInterface):
            raise TypeError(f'streamElementsHelper argument is malformed: \"{streamElementsHelper}\"')
        if not isinstance(streamElementsHelper, StreamElementsHelperInterface):
            raise TypeError(f'streamElementsHelper argument is malformed: \"{streamElementsHelper}\"')
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__streamElementsFileManager: StreamElementsFileManagerInterface = streamElementsFileManager
        self.__streamElementsHelper: StreamElementsHelperInterface = streamElementsHelper
        self.__timber: TimberInterface = timber
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoading: bool = False

    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True

        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to Google TTS,
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
            self.__timber.log('StreamElementsTtsManager', f'There is already an ongoing Stream Elements TTS event!')
            return False

        self.__isLoading = True

        speechBytes = await self.__streamElementsHelper.getSpeech(
            message = event.message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

        if speechBytes is None:
            self.__timber.log('StreamElementsTtsManager', f'Failed to fetch TTS speech in \"{event.twitchChannel}\" ({event=}) ({speechBytes=})')
            self.__isLoading = False
            return False

        fileName = await self.__streamElementsFileManager.saveSpeechToNewFile(speechBytes)
        if not utils.isValidStr(fileName) or not aiofiles.ospath.exists(fileName):
            self.__timber.log('StreamElementsTtsManager', f'Failed to write TTS speech in \"{event.twitchChannel}\" to a temporary file ({event=}) ({fileName=})')
            self.__isLoading = False
            return False

        self.__timber.log('StreamElementsTtsManager', f'Playing TTS message in \"{event.twitchChannel}\" from \"{fileName}\"...')
        await self.__soundPlayerManager.playSoundFile(fileName)
        self.__isLoading = False

        return False

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'isLoading': self.__isLoading
        }
