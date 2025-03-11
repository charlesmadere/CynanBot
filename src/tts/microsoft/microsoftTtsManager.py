import asyncio

from .microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.microsoft.microsoftTtsPreferredTts import MicrosoftTtsPreferredTts
from ...microsoft.helper.microsoftTtsHelperInterface import MicrosoftTtsHelperInterface
from ...microsoft.microsoftTtsMessageCleanerInterface import MicrosoftTtsMessageCleanerInterface
from ...microsoft.models.microsoftTtsFileReference import MicrosoftTtsFileReference
from ...microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from ...microsoft.settings.microsoftTtsSettingsRepositoryInterface import MicrosoftTtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class MicrosoftTtsManager(MicrosoftTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        microsoftTtsHelper: MicrosoftTtsHelperInterface,
        microsoftTtsMessageCleaner: MicrosoftTtsMessageCleanerInterface,
        microsoftTtsSettingsRepository: MicrosoftTtsSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(microsoftTtsHelper, MicrosoftTtsHelperInterface):
            raise TypeError(f'microsoftTtsHelper argument is malformed: \"{microsoftTtsHelper}\"')
        elif not isinstance(microsoftTtsMessageCleaner, MicrosoftTtsMessageCleanerInterface):
            raise TypeError(f'microsoftTtsMessageCleaner argument is malformed: \"{microsoftTtsMessageCleaner}\"')
        elif not isinstance(microsoftTtsSettingsRepository, MicrosoftTtsSettingsRepositoryInterface):
            raise TypeError(f'microsoftTtsSettingsRepository argument is malformed: \"{microsoftTtsSettingsRepository}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface = chatterPreferredTtsHelper
        self.__microsoftTtsHelper: MicrosoftTtsHelperInterface = microsoftTtsHelper
        self.__microsoftTtsMessageCleaner: MicrosoftTtsMessageCleanerInterface = microsoftTtsMessageCleaner
        self.__microsoftTtsSettingsRepository: MicrosoftTtsSettingsRepositoryInterface = microsoftTtsSettingsRepository
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoice(self, event: TtsEvent) -> MicrosoftTtsVoice | None:
        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId
        )

        if preferredTts is None:
            return None

        microsoftTtsPreferredTts = preferredTts.preferredTts
        if not isinstance(microsoftTtsPreferredTts, MicrosoftTtsPreferredTts):
            self.__timber.log('MicrosoftTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

        microsoftTtsVoiceEntry = microsoftTtsPreferredTts.voice
        if microsoftTtsVoiceEntry is None:
            return None

        return microsoftTtsVoiceEntry

    async def __executeTts(self, fileReference: MicrosoftTtsFileReference):
        volume = await self.__microsoftTtsSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('MicrosoftTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('MicrosoftTtsManager', f'There is already an ongoing Microsoft TTS event!')
            return

        self.__isLoadingOrPlaying = True
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('MicrosoftTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('MicrosoftTtsManager', f'Playing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> MicrosoftTtsFileReference | None:
        cleanedMessage = await self.__microsoftTtsMessageCleaner.clean(event.message)
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

        voice = await self.__determineVoice(event)

        return await self.__microsoftTtsHelper.generateTts(
            voice = voice,
            message = fullMessage,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('MicrosoftTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT
