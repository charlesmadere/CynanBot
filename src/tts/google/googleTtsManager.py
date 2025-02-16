import asyncio
import random

from .googleTtsManagerInterface import GoogleTtsManagerInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...google.googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from ...google.helpers.googleTtsHelperInterface import GoogleTtsHelperInterface
from ...google.models.googleTtsFileReference import GoogleTtsFileReference
from ...google.models.googleVoicePreset import GoogleVoicePreset
from ...google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class GoogleTtsManager(GoogleTtsManagerInterface):

    def __init__(
        self,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsHelper: GoogleTtsHelperInterface,
        googleTtsMessageCleaner: GoogleTtsMessageCleanerInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface
    ):
        if not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsHelper, GoogleTtsHelperInterface):
            raise TypeError(f'googleTtsHelper argument is malformed: \"{googleTtsHelper}\"')
        elif not isinstance(googleTtsMessageCleaner, GoogleTtsMessageCleanerInterface):
            raise TypeError(f'googleTtsMessageCleaner argument is malformed: \"{googleTtsMessageCleaner}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__googleSettingsRepository: GoogleSettingsRepositoryInterface = googleSettingsRepository
        self.__googleTtsHelper: GoogleTtsHelperInterface = googleTtsHelper
        self.__googleTtsMessageCleaner: GoogleTtsMessageCleanerInterface = googleTtsMessageCleaner
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoicePreset(self, event: TtsEvent) -> GoogleVoicePreset | None:
        voicePresets: frozenset[GoogleVoicePreset] | None = None

        if event.userId == await self.__twitchFriendsUserIdRepository.getHokkaidoubareUserId():
            voicePresets = frozenset({
                GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A,
                GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_B,
                GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_C,
                GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D
            })
        elif event.userId == await self.__twitchFriendsUserIdRepository.getLucentUserId():
            voicePresets = frozenset({
                GoogleVoicePreset.ITALIAN_ITALY_CHIRP_D,
                GoogleVoicePreset.ITALIAN_ITALY_CHIRP_F,
                GoogleVoicePreset.ITALIAN_ITALY_CHIRP_O
            })
        elif event.userId == await self.__twitchFriendsUserIdRepository.getMerttUserId():
            voicePresets = frozenset({
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_D,
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_F,
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_O
            })
        elif event.userId == await self.__twitchFriendsUserIdRepository.getVolwrathUserId():
            voicePresets = frozenset({
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_D,
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_F,
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_O
            })
        elif event.userId == await self.__twitchFriendsUserIdRepository.getZanianUserId():
            voicePresets = frozenset({
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_D,
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_F,
                GoogleVoicePreset.FRENCH_CANADA_CHIRP_O,
                GoogleVoicePreset.GERMAN_GERMANY_CHIRP_D,
                GoogleVoicePreset.GERMAN_GERMANY_CHIRP_F,
                GoogleVoicePreset.GERMAN_GERMANY_CHIRP_O,
                GoogleVoicePreset.KOREAN_KOREA_STANDARD_A,
                GoogleVoicePreset.KOREAN_KOREA_STANDARD_B,
                GoogleVoicePreset.KOREAN_KOREA_STANDARD_C,
                GoogleVoicePreset.KOREAN_KOREA_STANDARD_D
            })

        if voicePresets is None or len(voicePresets) == 0:
            return None
        else:
            return random.choice(list(voicePresets))

    async def __executeTts(self, fileReference: GoogleTtsFileReference):
        volume = await self.__googleSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('GoogleTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('GoogleTtsManager', f'There is already an ongoing TTS event!')
            return

        self.__isLoadingOrPlaying = True
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('GoogleTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('GoogleTtsManager', f'Playing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> GoogleTtsFileReference | None:
        cleanedMessage = await self.__googleTtsMessageCleaner.clean(
            message = event.message
        )

        voicePreset = await self.__determineVoicePreset(event)

        return await self.__googleTtsHelper.generateTts(
            voicePreset = voicePreset,
            message = cleanedMessage,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('GoogleTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
