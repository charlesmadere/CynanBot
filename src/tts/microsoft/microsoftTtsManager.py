import asyncio
import random
import traceback
from typing import Final

from .microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.microsoft.microsoftTtsTtsProperties import MicrosoftTtsTtsProperties
from ...microsoft.helper.microsoftTtsHelperInterface import MicrosoftTtsHelperInterface
from ...microsoft.microsoftTtsMessageCleanerInterface import MicrosoftTtsMessageCleanerInterface
from ...microsoft.models.microsoftTtsFileReference import MicrosoftTtsFileReference
from ...microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from ...microsoft.settings.microsoftTtsSettingsRepositoryInterface import MicrosoftTtsSettingsRepositoryInterface
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
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
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

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__microsoftTtsHelper: Final[MicrosoftTtsHelperInterface] = microsoftTtsHelper
        self.__microsoftTtsMessageCleaner: Final[MicrosoftTtsMessageCleanerInterface] = microsoftTtsMessageCleaner
        self.__microsoftTtsSettingsRepository: Final[MicrosoftTtsSettingsRepositoryInterface] = microsoftTtsSettingsRepository
        self.__soundPlayerManager: Final[SoundPlayerManagerInterface] = soundPlayerManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoice(self, event: TtsEvent) -> MicrosoftTtsVoice | None:
        if event.provider is TtsProvider.SHOTGUN_TTS:
            return random.choice(list(MicrosoftTtsVoice))
        elif event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if preferredTts is None:
            return None
        elif isinstance(preferredTts.properties, MicrosoftTtsTtsProperties):
            return preferredTts.properties.voice
        elif preferredTts.provider is TtsProvider.RANDO_TTS:
            return random.choice(list(MicrosoftTtsVoice))
        else:
            self.__timber.log('MicrosoftTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

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
        except TimeoutError as e:
            self.__timber.log('MicrosoftTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()
        except Exception as e:
            self.__timber.log('MicrosoftTtsManager', f'Stopping TTS event due to unknown exception ({fileReference=}) ({timeoutSeconds=}): {e}', e, traceback.format_exc())
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
            self.__timber.log('MicrosoftTtsManager', f'There is already an ongoing TTS event!')
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
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        message = await self.__microsoftTtsMessageCleaner.clean(event.message)
        voice = await self.__determineVoice(event)

        return await self.__microsoftTtsHelper.generateTts(
            voice = voice,
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
        self.__timber.log('MicrosoftTtsManager', f'Stopped TTS event')
