import asyncio
import random
import traceback
from typing import Final

from .microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.microsoftSam.microsoftSamTtsProperties import MicrosoftSamTtsProperties
from ...microsoftSam.helper.microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ...microsoftSam.microsoftSamMessageCleanerInterface import MicrosoftSamMessageCleanerInterface
from ...microsoftSam.models.microsoftSamFileReference import MicrosoftSamFileReference
from ...microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ...microsoftSam.settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class MicrosoftSamTtsManager(MicrosoftSamTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        microsoftSamHelper: MicrosoftSamHelperInterface,
        microsoftSamMessageCleaner: MicrosoftSamMessageCleanerInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
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

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__microsoftSamHelper: Final[MicrosoftSamHelperInterface] = microsoftSamHelper
        self.__microsoftSamMessageCleaner: Final[MicrosoftSamMessageCleanerInterface] = microsoftSamMessageCleaner
        self.__microsoftSamSettingsRepository: Final[MicrosoftSamSettingsRepositoryInterface] = microsoftSamSettingsRepository
        self.__soundPlayerManager: Final[SoundPlayerManagerInterface] = soundPlayerManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoice(self, event: TtsEvent) -> MicrosoftSamVoice | None:
        if event.provider is TtsProvider.SHOTGUN_TTS:
            return random.choice(list(MicrosoftSamVoice))
        elif event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if preferredTts is None:
            return None
        elif isinstance(preferredTts.properties, MicrosoftSamTtsProperties):
            return preferredTts.properties.voice
        elif preferredTts.provider is TtsProvider.RANDO_TTS:
            return random.choice(list(MicrosoftSamVoice))
        else:
            self.__timber.log('MicrosoftSamTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

    async def __executeTts(self, fileReference: MicrosoftSamFileReference):
        volume = await self.__microsoftSamSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('MicrosoftSamTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=})', e)
            await self.stopTtsEvent()
        except Exception as e:
            self.__timber.log('MicrosoftSamTtsManager', f'Stopping TTS event due to unknown exception ({fileReference=}) ({timeoutSeconds=})', e, traceback.format_exc())
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
            self.__timber.log('MicrosoftSamTtsManager', f'There is already an ongoing TTS event!')
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
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        message = await self.__microsoftSamMessageCleaner.clean(event.message)
        voice = await self.__determineVoice(event)

        return await self.__microsoftSamHelper.generateTts(
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
        self.__timber.log('MicrosoftSamTtsManager', f'Stopped TTS event')
