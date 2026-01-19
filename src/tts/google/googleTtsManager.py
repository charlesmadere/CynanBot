import asyncio
import random
import traceback
from typing import Final

from .googleTtsManagerInterface import GoogleTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.google.googleTtsProperties import GoogleTtsProperties
from ...google.googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from ...google.helpers.googleTtsHelperInterface import GoogleTtsHelperInterface
from ...google.helpers.googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ...google.models.absGoogleVoicePreset import AbsGoogleVoicePreset
from ...google.models.googleTtsFileReference import GoogleTtsFileReference
from ...google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...language.languageEntry import LanguageEntry
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class GoogleTtsManager(GoogleTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsHelper: GoogleTtsHelperInterface,
        googleTtsMessageCleaner: GoogleTtsMessageCleanerInterface,
        googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsHelper, GoogleTtsHelperInterface):
            raise TypeError(f'googleTtsHelper argument is malformed: \"{googleTtsHelper}\"')
        elif not isinstance(googleTtsMessageCleaner, GoogleTtsMessageCleanerInterface):
            raise TypeError(f'googleTtsMessageCleaner argument is malformed: \"{googleTtsMessageCleaner}\"')
        elif not isinstance(googleTtsVoicesHelper, GoogleTtsVoicesHelperInterface):
            raise TypeError(f'googleTtsVoicesHelper argument is malformed: \"{googleTtsVoicesHelper}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__googleSettingsRepository: Final[GoogleSettingsRepositoryInterface] = googleSettingsRepository
        self.__googleTtsHelper: Final[GoogleTtsHelperInterface] = googleTtsHelper
        self.__googleTtsMessageCleaner: Final[GoogleTtsMessageCleanerInterface] = googleTtsMessageCleaner
        self.__googleTtsVoicesHelper: Final[GoogleTtsVoicesHelperInterface] = googleTtsVoicesHelper
        self.__soundPlayerManager: Final[SoundPlayerManagerInterface] = soundPlayerManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoicePreset(self, event: TtsEvent) -> AbsGoogleVoicePreset | None:
        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if preferredTts is None:
            return None
        elif isinstance(preferredTts.properties, GoogleTtsProperties):
            languageEntry = preferredTts.properties.languageEntry

            if languageEntry is None:
                return None
            else:
                return await self.__googleTtsVoicesHelper.getVoiceForLanguage(languageEntry)
        elif preferredTts.provider is TtsProvider.RANDO_TTS:
            languageEntriesWithVoices: list[LanguageEntry] = list()

            for languageEntry in LanguageEntry:
                if await self.__googleTtsVoicesHelper.getVoiceForLanguage(languageEntry) is not None:
                    languageEntriesWithVoices.append(languageEntry)

            chosenLanguageEntry = random.choice(languageEntriesWithVoices)
            return await self.__googleTtsVoicesHelper.getVoiceForLanguage(chosenLanguageEntry)
        else:
            self.__timber.log('GoogleTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

    async def __executeTts(self, fileReference: GoogleTtsFileReference):
        volume = await self.__googleSettingsRepository.getMediaPlayerVolume()
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
            self.__timber.log('GoogleTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()
        except Exception as e:
            self.__timber.log('GoogleTtsManager', f'Stopping TTS event due to unknown exception ({fileReference=}) ({timeoutSeconds=}): {e}', e, traceback.format_exc())
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
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        message = await self.__googleTtsMessageCleaner.clean(event.message)
        voicePreset = await self.__determineVoicePreset(event)

        return await self.__googleTtsHelper.generateTts(
            voicePreset = voicePreset,
            allowMultiSpeaker = False,
            donationPrefix = donationPrefix,
            message = message,
            twitchChannelId = event.twitchChannelId,
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__isLoadingOrPlaying = False
        self.__timber.log('GoogleTtsManager', f'Stopped TTS event')
