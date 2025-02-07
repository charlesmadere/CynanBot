import asyncio

from .ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ...ttsMonster.models.ttsMonsterFileReference import TtsMonsterFileReference
from ...ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...ttsMonster.ttsMonsterMessageCleanerInterface import TtsMonsterMessageCleanerInterface
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface


class TtsMonsterTtsManager(TtsMonsterTtsManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsMonsterHelper: TtsMonsterHelperInterface,
        ttsMonsterMessageCleaner: TtsMonsterMessageCleanerInterface,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterHelper, TtsMonsterHelperInterface):
            raise TypeError(f'ttsMonsterHelper argument is malformed: \"{ttsMonsterHelper}\"')
        elif not isinstance(ttsMonsterMessageCleaner, TtsMonsterMessageCleanerInterface):
            raise TypeError(f'ttsMonsterMessageCleaner argument is malformed: \"{ttsMonsterMessageCleaner}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterMessageCleaner: TtsMonsterMessageCleanerInterface = ttsMonsterMessageCleaner
        self.__ttsMonsterHelper: TtsMonsterHelperInterface = ttsMonsterHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__isLoadingOrPlaying: bool = False

    async def __executeTts(self, fileReference: TtsMonsterFileReference):
        volume = await self.__ttsMonsterSettingsRepository.getMediaPlayerVolume()
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playPlaylist():
            await self.__soundPlayerManager.playSoundFile(
                filePath = fileReference.filePath,
                volume = volume
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playPlaylist(), timeout = timeoutSeconds)
        except TimeoutError as e:
            self.__timber.log('TtsMonsterTtsManager', f'Stopping TTS Monster TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('TtsMonsterTtsManager', f'There is already an ongoing TTS Monster event!')
            return

        self.__isLoadingOrPlaying = True
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('TtsMonsterTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('TtsMonsterTtsManager', f'Playing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> TtsMonsterFileReference | None:
        cleanedMessage = await self.__ttsMonsterMessageCleaner.clean(
            message = event.message
        )

        return await self.__ttsMonsterHelper.generateTts(
            message = cleanedMessage,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('TtsMonsterTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
