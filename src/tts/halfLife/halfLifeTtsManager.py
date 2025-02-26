import asyncio

from frozenlist import FrozenList

from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from ...halfLife.halfLifeMessageCleanerInterface import HalfLifeMessageCleanerInterface
from ...halfLife.helper.halfLifeHelperInterface import HalfLifeHelperInterface
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class HalfLifeTtsManager(HalfLifeTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        halfLifeHelper: HalfLifeHelperInterface,
        halfLifeMessageCleaner: HalfLifeMessageCleanerInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(halfLifeHelper, HalfLifeHelperInterface):
            raise TypeError(f'halfLifeHelper argument is malformed: \"{halfLifeHelper}\"')
        elif not isinstance(halfLifeMessageCleaner, HalfLifeMessageCleanerInterface):
            raise TypeError(f'halfLifeMessageCleaner argument is malformed: \"{halfLifeMessageCleaner}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface = chatterPreferredTtsHelper
        self.__halfLifeHelper: HalfLifeHelperInterface = halfLifeHelper
        self.__halfLifeMessageCleaner: HalfLifeMessageCleanerInterface = halfLifeMessageCleaner
        self.__halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface = halfLifeSettingsRepository
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __executeTts(self, fileNames: FrozenList[str]):
        volume = await self.__halfLifeSettingsRepository.getMediaPlayerVolume()
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playPlaylist():
            await self.__soundPlayerManager.playSoundFiles(
                filePaths = fileNames,
                volume = volume
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playPlaylist(), timeout = timeoutSeconds)
        except TimeoutError as e:
            self.__timber.log('HalfLifeTtsManager', f'Stopping Half Life TTS event due to timeout ({fileNames=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('HalfLifeTtsManager', f'There is already an ongoing Half Life TTS event!')
            return

        self.__isLoadingOrPlaying = True
        fileNames = await self.__processTtsEvent(event)

        if fileNames is None or len(fileNames) == 0:
            self.__timber.log('HalfLifeTtsManager', f'Failed to find any TTS files ({event=}) ({fileNames=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('HalfLifeTtsManager', f'Playing {len(fileNames)} TTS message(s) in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileNames)

    async def __determineVoicePreset(self, event: TtsEvent) -> HalfLifeVoice:

        defaultVoice: HalfLifeVoice = await self.__halfLifeSettingsRepository.getDefaultVoice()

        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return defaultVoice

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId
        )

        if preferredTts is None:
            return defaultVoice

        halfLifePreferredTts = preferredTts.preferredTts
        if not isinstance(halfLifePreferredTts, HalfLifePreferredTts):
            self.__timber.log('HalfLifeTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return defaultVoice

        halfLifeVoiceEntry = halfLifePreferredTts.halfLifeVoiceEntry
        if halfLifeVoiceEntry is None:
            return defaultVoice

        return halfLifeVoiceEntry

    async def __processTtsEvent(self, event: TtsEvent) -> FrozenList[str] | None:
        message = await self.__halfLifeMessageCleaner.clean(event.message)
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

        speechFiles = await self.__halfLifeHelper.getSpeech(
            message = fullMessage,
            voice = await self.__determineVoicePreset(event)
        )

        if speechFiles is None or len(speechFiles) == 0:
            self.__timber.log('HalfLifeTtsManager', f'Failed to fetch TTS speech in \"{event.twitchChannel}\" ({event=}) ({speechFiles=})')
            return None

        return speechFiles

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('HalfLifeTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.HALF_LIFE
