import asyncio
import traceback

from frozenlist import FrozenList

from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from ...halfLife.halfLifeMessageCleanerInterface import HalfLifeMessageCleanerInterface
from ...halfLife.helper.halfLifeTtsHelperInterface import HalfLifeTtsHelperInterface
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class HalfLifeTtsManager(HalfLifeTtsManagerInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        halfLifeMessageCleaner: HalfLifeMessageCleanerInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        halfLifeTtsHelper: HalfLifeTtsHelperInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(halfLifeMessageCleaner, HalfLifeMessageCleanerInterface):
            raise TypeError(f'halfLifeMessageCleaner argument is malformed: \"{halfLifeMessageCleaner}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(halfLifeTtsHelper, HalfLifeTtsHelperInterface):
            raise TypeError(f'halfLifeTtsHelper argument is malformed: \"{halfLifeTtsHelper}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface = chatterPreferredTtsHelper
        self.__halfLifeMessageCleaner: HalfLifeMessageCleanerInterface = halfLifeMessageCleaner
        self.__halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface = halfLifeSettingsRepository
        self.__halfLifeTtsHelper: HalfLifeTtsHelperInterface = halfLifeTtsHelper
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoice(self, event: TtsEvent) -> HalfLifeVoice | None:
        if event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId
        )

        if preferredTts is None:
            return None

        if not isinstance(preferredTts.properties, HalfLifeTtsProperties):
            self.__timber.log('HalfLifeTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

        return preferredTts.properties.voice

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
            self.__timber.log('HalfLifeTtsManager', f'Stopping TTS event due to timeout ({fileNames=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()
        except Exception as e:
            self.__timber.log('HalfLifeTtsManager', f'Stopping TTS event due to unknown exception ({fileNames=}) ({timeoutSeconds=}): {e}', e, traceback.format_exc())
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
            self.__timber.log('HalfLifeTtsManager', f'There is already an ongoing TTS event!')
            return

        self.__isLoadingOrPlaying = True
        fileNames = await self.__processTtsEvent(event)

        if fileNames is None or len(fileNames) == 0:
            self.__timber.log('HalfLifeTtsManager', f'Failed to find any TTS files ({event=}) ({fileNames=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('HalfLifeTtsManager', f'Playing {len(fileNames)} TTS message(s) in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileNames)

    async def __processTtsEvent(self, event: TtsEvent) -> FrozenList[str] | None:
        cleanedMessage = await self.__halfLifeMessageCleaner.clean(event.message)
        voice = await self.__determineVoice(event)

        return await self.__halfLifeTtsHelper.generateTts(
            voice = voice,
            message = cleanedMessage,
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__isLoadingOrPlaying = False
        self.__timber.log('HalfLifeTtsManager', f'Stopped TTS event')
