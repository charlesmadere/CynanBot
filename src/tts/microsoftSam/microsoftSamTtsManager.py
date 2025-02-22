import asyncio

from .microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...microsoftSam.helper.microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ...microsoftSam.microsoftSamMessageCleanerInterface import MicrosoftSamMessageCleanerInterface
from ...microsoftSam.models.microsoftSamFileReference import MicrosoftSamFileReference
from ...microsoftSam.settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class MicrosoftSamTtsManager(MicrosoftSamTtsManagerInterface):

    def __init__(
        self,
        microsoftSamHelper: MicrosoftSamHelperInterface,
        microsoftSamMessageCleaner: MicrosoftSamMessageCleanerInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(microsoftSamHelper, MicrosoftSamHelperInterface):
            raise TypeError(f'microsoftSamHelper argument is malformed: \"{microsoftSamHelper}\"')
        elif not isinstance(microsoftSamMessageCleaner, MicrosoftSamMessageCleanerInterface):
            raise TypeError(f'microsoftSamMessageCleaner argument is malformed: \"{microsoftSamMessageCleaner}\"')
        elif not isinstance(microsoftSamSettingsRepository, MicrosoftSamSettingsRepositoryInterface):
            raise TypeError(f'microsoftSamSettingsRepository argument is malformed: \"{microsoftSamSettingsRepository}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__microsoftSamHelper: MicrosoftSamHelperInterface = microsoftSamHelper
        self.__microsoftSamMessageCleaner: MicrosoftSamMessageCleanerInterface = microsoftSamMessageCleaner
        self.__microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = microsoftSamSettingsRepository
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __executeTts(self, fileReference: MicrosoftSamFileReference):
        volume = await self.__microsoftSamSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('MicrosoftSamTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('MicrosoftSamTtsManager', f'There is already an ongoing Microsoft Sam TTS event!')
            return

        self.__isLoadingOrPlaying = True
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('MicrosoftSamTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('MicrosoftSamTtsManager', f'Playing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> MicrosoftSamFileReference | None:
        cleanedMessage = await self.__microsoftSamMessageCleaner.clean(
            message = event.message
        )

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

        return await self.__microsoftSamHelper.generateTts(
            message = fullMessage,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('MicrosoftSamTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM
