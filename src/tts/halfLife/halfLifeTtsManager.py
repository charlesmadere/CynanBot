import asyncio
import traceback
from typing import Final

from frozenlist import FrozenList

from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..models.ttsEvent import TtsEvent
from ..models.ttsProvider import TtsProvider
from ..models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...chatterPreferredTts.models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from ...halfLife.halfLifeMessageCleanerInterface import HalfLifeMessageCleanerInterface
from ...halfLife.helper.halfLifeTtsHelperInterface import HalfLifeTtsHelperInterface
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...soundPlayerManager.soundPlaybackFile import SoundPlaybackFile
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...soundPlayerManager.soundPlayerPlaylist import SoundPlayerPlaylist
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
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
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

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__halfLifeMessageCleaner: Final[HalfLifeMessageCleanerInterface] = halfLifeMessageCleaner
        self.__halfLifeSettingsRepository: Final[HalfLifeSettingsRepositoryInterface] = halfLifeSettingsRepository
        self.__halfLifeTtsHelper: Final[HalfLifeTtsHelperInterface] = halfLifeTtsHelper
        self.__soundPlayerManager: Final[SoundPlayerManagerInterface] = soundPlayerManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__isLoadingOrPlaying: bool = False

    async def __determineVoice(self, event: TtsEvent) -> HalfLifeVoice | None:
        if event.provider is TtsProvider.SHOTGUN_TTS:
            return HalfLifeVoice.ALL
        elif event.providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return None

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if preferredTts is None:
            return None
        elif isinstance(preferredTts.properties, HalfLifeTtsProperties):
            return preferredTts.properties.voice
        elif preferredTts.provider is TtsProvider.RANDO_TTS:
            return HalfLifeVoice.ALL
        else:
            self.__timber.log('HalfLifeTtsManager', f'Encountered bizarre incorrect preferred TTS provider ({event=}) ({preferredTts=})')
            return None

    async def __executeTts(self, playlist: SoundPlayerPlaylist):
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playPlaylist():
            await self.__soundPlayerManager.playPlaylist(
                playlist = playlist,
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playPlaylist(), timeout = timeoutSeconds)
        except TimeoutError as e:
            self.__timber.log('HalfLifeTtsManager', f'Stopping TTS event due to timeout ({playlist=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()
        except Exception as e:
            self.__timber.log('HalfLifeTtsManager', f'Stopping TTS event due to unknown exception ({playlist=}) ({timeoutSeconds=}): {e}', e, traceback.format_exc())
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
        playlist = await self.__processTtsEvent(event)

        if playlist is None or len(playlist.playlistFiles) == 0:
            self.__timber.log('HalfLifeTtsManager', f'Failed to find any TTS files ({event=}) ({playlist=})')
            self.__isLoadingOrPlaying = False
            return

        self.__timber.log('HalfLifeTtsManager', f'Playing {len(playlist.playlistFiles)} TTS message(s) in \"{event.twitchChannel}\"...')
        await self.__executeTts(playlist)

    async def __processTtsEvent(self, event: TtsEvent) -> SoundPlayerPlaylist | None:
        cleanedMessage = await self.__halfLifeMessageCleaner.clean(event.message)
        voice = await self.__determineVoice(event)

        soundFiles = await self.__halfLifeTtsHelper.generateTts(
            voice = voice,
            message = cleanedMessage,
        )

        if soundFiles is None or len(soundFiles) == 0:
            return None

        playlistFiles: FrozenList[SoundPlaybackFile] = FrozenList()
        voiceVolumes = await self.__halfLifeSettingsRepository.getVoiceVolumes()

        for soundFile in soundFiles:
            playlistFiles.append(SoundPlaybackFile(
                volume = voiceVolumes.get(soundFile.voice, None),
                filePath = soundFile.path,
            ))

        playlistFiles.freeze()

        return SoundPlayerPlaylist(
            playlistFiles = playlistFiles,
            volume = await self.__halfLifeSettingsRepository.getMediaPlayerVolume(),
        )

    async def stopTtsEvent(self):
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__isLoadingOrPlaying = False
        self.__timber.log('HalfLifeTtsManager', f'Stopped TTS event')
