import asyncio

from .commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...commodoreSam.commodoreSamMessageCleanerInterface import CommodoreSamMessageCleanerInterface
from ...commodoreSam.helper.commodoreSamHelperInterface import CommodoreSamHelperInterface
from ...commodoreSam.models.commodoreSamFileReference import CommodoreSamFileReference
from ...commodoreSam.settings.commodoreSamSettingsRepositoryInterface import CommodoreSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class CommodoreSamTtsManager(CommodoreSamTtsManagerInterface):

    def __init__(
        self,
        commodoreSamHelper: CommodoreSamHelperInterface,
        commodoreSamMessageCleaner: CommodoreSamMessageCleanerInterface,
        commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(commodoreSamHelper, CommodoreSamHelperInterface):
            raise TypeError(f'commodoreSamHelper argument is malformed: \"{commodoreSamHelper}\"')
        elif not isinstance(commodoreSamMessageCleaner, CommodoreSamMessageCleanerInterface):
            raise TypeError(f'commodoreSamMessageCleaner argument is malformed: \"{commodoreSamMessageCleaner}\"')
        elif not isinstance(commodoreSamSettingsRepository, CommodoreSamSettingsRepositoryInterface):
            raise TypeError(f'commodoreSamSettingsRepository argument is malformed: \"{commodoreSamSettingsRepository}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__commodoreSamHelper: CommodoreSamHelperInterface = commodoreSamHelper
        self.__commodoreSamMessageCleaner: CommodoreSamMessageCleanerInterface = commodoreSamMessageCleaner
        self.__commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface = commodoreSamSettingsRepository
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __executeTts(self, fileReference: CommodoreSamFileReference):
        volume = await self.__commodoreSamSettingsRepository.getMediaPlayerVolume()
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playSoundFile():
            await self.__soundPlayerManager.playSoundFile(
                filePath = fileReference.filePath,
                volume = volume
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playSoundFile(), timeout = timeoutSeconds)
        except Exception as e:
            self.__timber.log('CommodoreSamTtsManager', f'Stopping Commodore SAM TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('CommodoreSamTtsManager', f'There is already an ongoing Commodore SAM event!')
            return

        self.__isLoadingOrPlaying = True
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('CommodoreSamTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('CommodoreSamTtsManager', f'Executing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> CommodoreSamFileReference | None:
        cleanedMessage = await self.__commodoreSamMessageCleaner.clean(event.message)
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        fullMessage: str

        if utils.isValidStr(cleanedMessage) and utils.isValidStr(donationPrefix):
            fullMessage = f'{donationPrefix} {cleanedMessage}'
        elif utils.isValidStr(cleanedMessage):
            fullMessage = cleanedMessage
        elif utils.isValidStr(donationPrefix):
            fullMessage = donationPrefix
        else:
            return None

        return await self.__commodoreSamHelper.generateTts(
            message = fullMessage,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('CommodoreSamTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.COMMODORE_SAM
