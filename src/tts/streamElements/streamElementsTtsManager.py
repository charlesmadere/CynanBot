import asyncio

import aiofiles.ospath

from .streamElementsFileManagerInterface import StreamElementsFileManagerInterface
from .streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from ...streamElements.settings.streamElementsSettingsRepositoryInterface import \
    StreamElementsSettingsRepositoryInterface
from ...streamElements.streamElementsMessageCleanerInterface import \
    StreamElementsMessageCleanerInterface
from ...timber.timberInterface import TimberInterface


class StreamElementsTtsManager(StreamElementsTtsManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        streamElementsFileManager: StreamElementsFileManagerInterface,
        streamElementsHelper: StreamElementsHelperInterface,
        streamElementsMessageCleaner: StreamElementsMessageCleanerInterface,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
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

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__streamElementsFileManager: StreamElementsFileManagerInterface = streamElementsFileManager
        self.__streamElementsHelper: StreamElementsHelperInterface = streamElementsHelper
        self.__streamElementsMessageCleaner: StreamElementsMessageCleanerInterface = streamElementsMessageCleaner
        self.__streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface = streamElementsSettingsRepository
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __executeTts(self, fileName: str):
        volume = await self.__streamElementsSettingsRepository.getMediaPlayerVolume()
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playSoundFile():
            await self.__soundPlayerManager.playSoundFile(
                filePath = fileName,
                volume = volume
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playSoundFile(), timeout = timeoutSeconds)
        except Exception as e:
            self.__timber.log('StreamElementsTtsManager', f'Stopping Stream Elements TTS event due to timeout ({fileName=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()

    @property
    def isLoadingOrPlaying(self) -> bool:
        return self.__isLoadingOrPlaying

    async def playTtsEvent(self, event: TtsEvent):
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return
        elif self.isLoadingOrPlaying:
            self.__timber.log('StreamElementsTtsManager', f'There is already an ongoing TTS event!')
            return

        self.__isLoadingOrPlaying = True
        fileName = await self.__processTtsEvent(event)

        if not utils.isValidStr(fileName) or not await aiofiles.ospath.exists(fileName):
            self.__timber.log('StreamElementsTtsManager', f'Failed to write TTS speech in \"{event.twitchChannel}\" to a temporary file ({event=}) ({fileName=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('StreamElementsTtsManager', f'Playing \"{fileName}\" TTS message in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileName)

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

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('StreamElementsTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.STREAM_ELEMENTS
