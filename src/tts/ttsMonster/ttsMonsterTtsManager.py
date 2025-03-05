import asyncio

from .ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.ttsMonster.ttsMonsterPreferredTts import TtsMonsterPreferredTts
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ...ttsMonster.models.ttsMonsterFileReference import TtsMonsterFileReference
from ...ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice
from ...ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...ttsMonster.ttsMonsterMessageCleanerInterface import TtsMonsterMessageCleanerInterface


class TtsMonsterTtsManager(TtsMonsterTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsMonsterHelper: TtsMonsterHelperInterface,
        ttsMonsterMessageCleaner: TtsMonsterMessageCleanerInterface,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        loudVoices: frozenset[TtsMonsterVoice] | None = frozenset({ TtsMonsterVoice.SHADOW})
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterHelper, TtsMonsterHelperInterface):
            raise TypeError(f'ttsMonsterHelper argument is malformed: \"{ttsMonsterHelper}\"')
        elif not isinstance(ttsMonsterMessageCleaner, TtsMonsterMessageCleanerInterface):
            raise TypeError(f'ttsMonsterMessageCleaner argument is malformed: \"{ttsMonsterMessageCleaner}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not loudVoices is not None and not isinstance(loudVoices, frozenset):
            raise TypeError(f'loudVoices argument is malformed: \"{loudVoices}\"')

        self.__chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface = chatterPreferredTtsHelper
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterMessageCleaner: TtsMonsterMessageCleanerInterface = ttsMonsterMessageCleaner
        self.__ttsMonsterHelper: TtsMonsterHelperInterface = ttsMonsterHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__loudVoices: frozenset[TtsMonsterVoice] | None = loudVoices

        self.__isLoadingOrPlaying: bool = False

    async def __containsLoudVoices(self, fileReference: TtsMonsterFileReference) -> bool:
        loudVoices = self.__loudVoices

        if loudVoices is None or len(loudVoices) == 0:
            return False

        for louderVoice in loudVoices:
            if louderVoice in fileReference.allVoices:
                return True

        return False

    async def __determineVoice(self, event: TtsEvent) -> TtsMonsterVoice | None:
        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId
        )

        if preferredTts is None:
            return None

        ttsMonsterPreferredTts = preferredTts.preferredTts
        if not isinstance(ttsMonsterPreferredTts, TtsMonsterPreferredTts):
            self.__timber.log('TtsMonsterTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

        ttsMonsterVoiceEntry = ttsMonsterPreferredTts.ttsMonsterVoiceEntry
        if ttsMonsterVoiceEntry is None:
            return None

        return ttsMonsterVoiceEntry

    async def __determineVolume(self, fileReference: TtsMonsterFileReference) -> int | None:
        volume: int | None = None

        if await self.__containsLoudVoices(fileReference):
            volume = await self.__ttsMonsterSettingsRepository.getReducedMediaPlayerVolume()

        if volume is None:
            volume = await self.__ttsMonsterSettingsRepository.getMediaPlayerVolume()

        return volume

    async def __executeTts(self, fileReference: TtsMonsterFileReference):
        volume = await self.__determineVolume(fileReference)
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playPlaylist():
            await self.__soundPlayerManager.playSoundFile(
                filePath = fileReference.filePath,
                volume = volume
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playPlaylist(), timeout = timeoutSeconds)
        except TimeoutError as e:
            self.__timber.log('TtsMonsterTtsManager', f'Stopping TTS event due to timeout ({fileReference=}) ({timeoutSeconds=}): {e}', e)
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
            self.__timber.log('TtsMonsterTtsManager', f'There is already an ongoing TTS event!')
            return

        self.__isLoadingOrPlaying = True
        fileReference = await self.__processTtsEvent(event)

        if fileReference is None:
            self.__timber.log('TtsMonsterTtsManager', f'Failed to generate TTS ({event=}) ({fileReference=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('TtsMonsterTtsManager', f'Playing TTS in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileReference)

    async def __processTtsEvent(self, event: TtsEvent) -> TtsMonsterFileReference | None:
        cleanedMessage = await self.__ttsMonsterMessageCleaner.clean(event.message)
        voice = await self.__determineVoice(event)

        if voice is not None:
            cleanedMessage = f'{voice.inMessageName}: {cleanedMessage}'

        return await self.__ttsMonsterHelper.generateTts(
            message = cleanedMessage,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('TtsMonsterTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
