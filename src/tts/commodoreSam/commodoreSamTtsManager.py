import asyncio
import traceback
from typing import Final

from .commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...commodoreSam.commodoreSamMessageCleanerInterface import CommodoreSamMessageCleanerInterface
from ...commodoreSam.helper.commodoreSamHelperInterface import CommodoreSamHelperInterface
from ...commodoreSam.models.commodoreSamFileReference import CommodoreSamFileReference
from ...commodoreSam.settings.commodoreSamSettingsRepositoryInterface import CommodoreSamSettingsRepositoryInterface
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
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
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

        self.__commodoreSamHelper: Final[CommodoreSamHelperInterface] = commodoreSamHelper
        self.__commodoreSamMessageCleaner: Final[CommodoreSamMessageCleanerInterface] = commodoreSamMessageCleaner
        self.__commodoreSamSettingsRepository: Final[CommodoreSamSettingsRepositoryInterface] = commodoreSamSettingsRepository
        self.__soundPlayerManager: Final[SoundPlayerManagerInterface] = soundPlayerManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __executeTts(self, fileReference: CommodoreSamFileReference):
        volume = await self.__commodoreSamSettingsRepository.getMediaPlayerVolume()
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playSoundFile():
            await self.__soundPlayerManager.playSoundFile(
                filePath = fileReference.filePath,
                volume = volume,
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playSoundFile(), timeout = timeoutSeconds)
        except TimeoutError as e:
            self.__timber.log('CommodoreSamTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()
        except Exception as e:
            self.__timber.log('CommodoreSamTtsManager', f'Stopping TTS event due to unknown exception ({fileReference=}) ({timeoutSeconds=}): {e}', e, traceback.format_exc())
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
            self.__timber.log('CommodoreSamTtsManager', f'There is already an ongoing TTS event!')
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
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        message = await self.__commodoreSamMessageCleaner.clean(event.message)

        return await self.__commodoreSamHelper.generateTts(
            donationPrefix = donationPrefix,
            message = message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId,
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__isLoadingOrPlaying = False
        self.__timber.log('CommodoreSamTtsManager', f'Stopped TTS event')
