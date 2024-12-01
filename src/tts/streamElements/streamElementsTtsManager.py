import aiofiles.ospath

from .streamElementsFileManagerInterface import StreamElementsFileManagerInterface
from ..tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from ..ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from ...streamElements.settings.streamElementsSettingsRepositoryInterface import \
    StreamElementsSettingsRepositoryInterface
from ...streamElements.streamElementsMessageCleanerInterface import \
    StreamElementsMessageCleanerInterface
from ...timber.timberInterface import TimberInterface


class StreamElementsTtsManager(TtsManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        streamElementsFileManager: StreamElementsFileManagerInterface,
        streamElementsHelper: StreamElementsHelperInterface,
        streamElementsMessageCleaner: StreamElementsMessageCleanerInterface,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface
    ):
        if not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(streamElementsFileManager, StreamElementsFileManagerInterface):
            raise TypeError(f'streamElementsHelper argument is malformed: \"{streamElementsHelper}\"')
        elif not isinstance(streamElementsHelper, StreamElementsHelperInterface):
            raise TypeError(f'streamElementsHelper argument is malformed: \"{streamElementsHelper}\"')
        elif not isinstance(streamElementsMessageCleaner, StreamElementsMessageCleanerInterface):
            raise TypeError(f'streamElementsMessageCleaner argument is malformed: \"{streamElementsMessageCleaner}\"')
        elif not isinstance(streamElementsSettingsRepository, StreamElementsSettingsRepositoryInterface):
            raise TypeError(f'streamElementsSettingsRepository argument is malformed: \"{streamElementsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__streamElementsFileManager: StreamElementsFileManagerInterface = streamElementsFileManager
        self.__streamElementsHelper: StreamElementsHelperInterface = streamElementsHelper
        self.__streamElementsMessageCleaner: StreamElementsMessageCleanerInterface = streamElementsMessageCleaner
        self.__streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface = streamElementsSettingsRepository
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper

        self.__isLoading: bool = False

    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True

        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to Stream
        #  Elements TTS, and yet in this scenario, this method would still return true. So for
        #  the fix for this is probably a way to check if SoundPlayerManager is currently playing,
        #  AND also a check to see specifically what media it is currently playing.
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
        fileName = await self.__processTtsEvent(event)

        if not utils.isValidStr(fileName) or not await aiofiles.ospath.exists(fileName):
            self.__timber.log('StreamElementsTtsManager', f'Failed to write TTS speech in \"{event.twitchChannel}\" to a temporary file ({event=}) ({fileName=})')
            self.__isLoading = False
            return False

        self.__timber.log('StreamElementsTtsManager', f'Playing TTS message in \"{event.twitchChannel}\" from \"{fileName}\"...')

        await self.__soundPlayerManager.playSoundFile(
            filePath = fileName,
            volume = await self.__streamElementsSettingsRepository.getMediaPlayerVolume()
        )

        await self.__ttsTempFileHelper.registerTempFile(fileName)
        self.__isLoading = False

        return False

    async def __processTtsEvent(self, event: TtsEvent) -> str | None:
        message = await self.__streamElementsMessageCleaner.clean(event.message)
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        fullMessage: str

        if utils.isValidStr(message) and utils.isValidStr(donationPrefix):
            fullMessage = f'{donationPrefix} {message}'
        elif utils.isValidStr(message):
            fullMessage = message
        elif utils.isValidStr(donationPrefix):
            fullMessage = donationPrefix
        else:
            return None

        speechBytes = await self.__streamElementsHelper.getSpeech(
            message = fullMessage,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

        if speechBytes is None:
            self.__timber.log('StreamElementsTtsManager', f'Failed to fetch TTS speech in \"{event.twitchChannel}\" ({event=}) ({speechBytes=})')
            return None

        return await self.__streamElementsFileManager.saveSpeechToNewFile(speechBytes)
