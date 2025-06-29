import asyncio
import random
import traceback
from typing import Final

from .streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.streamElements.streamElementsTtsProperties import StreamElementsTtsProperties
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from ...streamElements.models.streamElementsFileReference import StreamElementsFileReference
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...streamElements.settings.streamElementsSettingsRepositoryInterface import \
    StreamElementsSettingsRepositoryInterface
from ...streamElements.streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from ...timber.timberInterface import TimberInterface


class StreamElementsTtsManager(StreamElementsTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        streamElementsHelper: StreamElementsHelperInterface,
        streamElementsMessageCleaner: StreamElementsMessageCleanerInterface,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
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

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__soundPlayerManager: Final[SoundPlayerManagerInterface] = soundPlayerManager
        self.__streamElementsHelper: Final[StreamElementsHelperInterface] = streamElementsHelper
        self.__streamElementsMessageCleaner: Final[StreamElementsMessageCleanerInterface] = streamElementsMessageCleaner
        self.__streamElementsSettingsRepository: Final[StreamElementsSettingsRepositoryInterface] = streamElementsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoice(self, event: TtsEvent) -> StreamElementsVoice | None:
        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if preferredTts is None:
            return None
        elif isinstance(preferredTts.properties, StreamElementsTtsProperties):
            return preferredTts.properties.voice
        elif preferredTts.provider is TtsProvider.RANDO_TTS:
            return random.choice(list(StreamElementsVoice))
        else:
            self.__timber.log('StreamElementsTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

    async def __executeTts(self, fileReference: StreamElementsFileReference):
        volume = await self.__streamElementsSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('StreamElementsTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()
        except Exception as e:
            self.__timber.log('StreamElementsTtsManager', f'Stopping TTS event due to unknown exception ({fileReference=}) ({timeoutSeconds=}): {e}', e, traceback.format_exc())
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
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('StreamElementsTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('StreamElementsTtsManager', f'Playing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> StreamElementsFileReference | None:
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        message = await self.__streamElementsMessageCleaner.clean(event.message)
        voice = await self.__determineVoice(event)

        return await self.__streamElementsHelper.generateTts(
            donationPrefix = donationPrefix,
            message = message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId,
            voice = voice,
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__isLoadingOrPlaying = False
        self.__timber.log('StreamElementsTtsManager', f'Stopped TTS event')
