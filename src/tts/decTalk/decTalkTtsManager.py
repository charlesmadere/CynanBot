import asyncio

from .decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from ...decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from ...decTalk.helper.decTalkHelperInterface import DecTalkHelperInterface
from ...decTalk.models.decTalkFileReference import DecTalkFileReference
from ...decTalk.models.decTalkVoice import DecTalkVoice
from ...decTalk.settings.decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class DecTalkTtsManager(DecTalkTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        decTalkHelper: DecTalkHelperInterface,
        decTalkMessageCleaner: DecTalkMessageCleanerInterface,
        decTalkSettingsRepository: DecTalkSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(decTalkHelper, DecTalkHelperInterface):
            raise TypeError(f'decTalkHelper argument is malformed: \"{decTalkHelper}\"')
        elif not isinstance(decTalkMessageCleaner, DecTalkMessageCleanerInterface):
            raise TypeError(f'decTalkMessageCleaner argument is malformed: \"{decTalkMessageCleaner}\"')
        elif not isinstance(decTalkSettingsRepository, DecTalkSettingsRepositoryInterface):
            raise TypeError(f'decTalkSettingsRepository argument is malformed: \"{decTalkSettingsRepository}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface = chatterPreferredTtsHelper
        self.__decTalkHelper: DecTalkHelperInterface = decTalkHelper
        self.__decTalkMessageCleaner: DecTalkMessageCleanerInterface = decTalkMessageCleaner
        self.__decTalkSettingsRepository: DecTalkSettingsRepositoryInterface = decTalkSettingsRepository
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoice(self, event: TtsEvent) -> DecTalkVoice | None:
        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId
        )

        if preferredTts is None:
            return None

        decTalkPreferredTts = preferredTts.preferredTts
        if not isinstance(decTalkPreferredTts, DecTalkPreferredTts):
            self.__timber.log('DecTalkTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

        return decTalkPreferredTts.voice

    async def __executeTts(self, fileReference: DecTalkFileReference):
        volume = await self.__decTalkSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('DecTalkTtsManager', f'Stopping DecTalk TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('DecTalkTtsManager', f'There is already an ongoing DecTalk event!')
            return

        self.__isLoadingOrPlaying = True
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('DecTalkTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('DecTalkTtsManager', f'Executing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> DecTalkFileReference | None:
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        message = await self.__decTalkMessageCleaner.clean(event.message)
        voice = await self.__determineVoice(event)

        return await self.__decTalkHelper.generateTts(
            voice = voice,
            donationPrefix = donationPrefix,
            message = message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('DecTalkTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK
