import asyncio

import aiofiles.ospath

from .microsoftSamFileManagerInterface import MicrosoftSamFileManagerInterface
from .microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from ..ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...microsoftSam.helper.microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ...microsoftSam.microsoftSamMessageCleanerInterface import MicrosoftSamMessageCleanerInterface
from ...microsoftSam.settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class MicrosoftSamTtsManager(MicrosoftSamTtsManagerInterface):

    def __init__(
        self,
        microsoftSamFileManager: MicrosoftSamFileManagerInterface,
        microsoftSamHelper: MicrosoftSamHelperInterface,
        microsoftSamMessageCleaner: MicrosoftSamMessageCleanerInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(microsoftSamFileManager, MicrosoftSamFileManagerInterface):
            raise TypeError(f'microsoftSamFileManager argument is malformed: \"{microsoftSamFileManager}\"')
        elif not isinstance(microsoftSamHelper, MicrosoftSamHelperInterface):
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

        self.__microsoftSamFileManager: MicrosoftSamFileManagerInterface = microsoftSamFileManager
        self.__microsoftSamHelper: MicrosoftSamHelperInterface = microsoftSamHelper
        self.__microsoftSamMessageCleaner: MicrosoftSamMessageCleanerInterface = microsoftSamMessageCleaner
        self.__microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = microsoftSamSettingsRepository
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __executeTts(self, fileName: str):
        volume = await self.__microsoftSamSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('MicrosoftSamTtsManager', f'Stopping Microsoft Sam TTS event due to timeout ({fileName=}) ({timeoutSeconds=}): {e}', e)
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
        fileName = await self.__processTtsEvent(event)

        if not utils.isValidStr(fileName) or not await aiofiles.ospath.exists(fileName):
            self.__timber.log('MicrosoftSamTtsManager', f'Failed to write TTS speech in \"{event.twitchChannel}\" to a temporary file ({event=}) ({fileName=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('MicrosoftSamTtsManager', f'Playing \"{fileName}\" TTS message in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileName)

    async def __processTtsEvent(self, event: TtsEvent) -> str | None:
        message = await self.__microsoftSamMessageCleaner.clean(event.message)
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

        speechBytes = await self.__microsoftSamHelper.getSpeech(
            message = fullMessage
        )

        if speechBytes is None:
            self.__timber.log('MicrosoftSamTtsManager', f'Failed to fetch TTS speech in \"{event.twitchChannel}\" ({event=}) ({speechBytes=})')
            return None

        return await self.__microsoftSamFileManager.saveSpeechToNewFile(speechBytes)

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('MicrosoftSamTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM
