import asyncio

from frozenlist import FrozenList

from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...halfLife.halfLifeMessageCleanerInterface import HalfLifeMessageCleanerInterface
from ...halfLife.helper.halfLifeHelperInterface import HalfLifeHelperInterface
from ...halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class HalfLifeTtsManager(HalfLifeTtsManagerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        halfLifeHelper: HalfLifeHelperInterface,
        halfLifeMessageCleaner: HalfLifeMessageCleanerInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(halfLifeHelper, HalfLifeHelperInterface):
            raise TypeError(f'halfLifeHelper argument is malformed: \"{halfLifeHelper}\"')
        elif not isinstance(halfLifeMessageCleaner, HalfLifeMessageCleanerInterface):
            raise TypeError(f'halfLifeMessageCleaner argument is malformed: \"{halfLifeMessageCleaner}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__halfLifeHelper: HalfLifeHelperInterface = halfLifeHelper
        self.__halfLifeMessageCleaner: HalfLifeMessageCleanerInterface = halfLifeMessageCleaner
        self.__halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface = halfLifeSettingsRepository
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoading: bool = False
        self.__playSessionId: str | None = None

    async def __executeTts(self, fileNames: FrozenList[str]):
        volume = await self.__halfLifeSettingsRepository.getMediaPlayerVolume()
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playPlaylist():
            self.__playSessionId = await self.__soundPlayerManager.playPlaylist(
                filePaths = fileNames,
                volume = volume
            )

        try:
            await asyncio.wait_for(playPlaylist(), timeout = timeoutSeconds)
        except TimeoutError as e:
            self.__timber.log('HalfLifeTtsManager', f'Stopping Half Life TTS event due to timeout ({fileNames=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()

    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True

        playSessionId = self.__playSessionId
        if not utils.isValidStr(playSessionId):
            return False

        return await self.__soundPlayerManager.getCurrentPlaySessionId() == playSessionId

    async def playTtsEvent(self, event: TtsEvent):
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return
        elif await self.isPlaying():
            self.__timber.log('HalfLifeTtsManager', f'There is already an ongoing Half Life TTS event!')
            return

        self.__isLoading = True
        fileNames = await self.__processTtsEvent(event)

        if fileNames is None or len(fileNames) == 0:
            self.__timber.log('HalfLifeTtsManager', f'Failed to find any TTS files ({event=}) ({fileNames=})')
            self.__isLoading = False
            return

        self.__timber.log('HalfLifeTtsManager', f'Playing {len(fileNames)} TTS message(s) in \"{event.twitchChannel}\"...')
        self.__backgroundTaskHelper.createTask(self.__executeTts(fileNames))
        self.__isLoading = False

    async def __processTtsEvent(self, event: TtsEvent) -> FrozenList[str] | None:
        message = await self.__halfLifeMessageCleaner.clean(event.message)
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

        speechFiles = await self.__halfLifeHelper.getSpeech(fullMessage)

        if speechFiles is None or len(speechFiles) == 0:
            self.__timber.log('HalfLifeTtsManager', f'Failed to fetch TTS speech in \"{event.twitchChannel}\" ({event=}) ({speechFiles=})')
            return None

        return speechFiles

    async def stopTtsEvent(self):
        playSessionId = self.__playSessionId
        if not utils.isValidStr(playSessionId):
            return

        self.__playSessionId = None
        stopResult = await self.__soundPlayerManager.stopPlaySessionId(
            playSessionId = playSessionId
        )

        self.__timber.log('HalfLifeTtsManager', f'Stopped TTS event ({playSessionId=}) ({stopResult=})')

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.HALF_LIFE
