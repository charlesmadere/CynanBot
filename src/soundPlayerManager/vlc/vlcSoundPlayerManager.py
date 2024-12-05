import asyncio
import traceback
from enum import Enum, auto
from typing import Collection

import aiofiles.ospath
import vlc
from frozenlist import FrozenList

from ..playSessionIdGenerator.playSessionIdGeneratorInterface import PlaySessionIdGeneratorInterface
from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...chatBand.chatBandInstrument import ChatBandInstrument
from ...chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class VlcSoundPlayerManager(SoundPlayerManagerInterface):

    class PlaybackState(Enum):
        ERROR = auto()
        PLAYING = auto()
        STOPPED = auto()

        @classmethod
        def fromVlcState(cls, state: vlc.State):
            if not isinstance(state, vlc.State):
                return VlcSoundPlayerManager.PlaybackState.ERROR

            # VLC State documentation:
            # 0 is "NothingSpecial"
            # 1 is "Opening"
            # 2 is "Buffering"
            # 3 is "Playing"
            # 4 is "Paused"
            # 5 is "Stopped"
            # 6 is "Ended"
            # 7 is "Error"

            match state:
                case 0: return VlcSoundPlayerManager.PlaybackState.STOPPED
                case 1: return VlcSoundPlayerManager.PlaybackState.PLAYING
                case 2: return VlcSoundPlayerManager.PlaybackState.PLAYING
                case 3: return VlcSoundPlayerManager.PlaybackState.PLAYING
                case 4: return VlcSoundPlayerManager.PlaybackState.STOPPED
                case 5: return VlcSoundPlayerManager.PlaybackState.STOPPED
                case 6: return VlcSoundPlayerManager.PlaybackState.STOPPED
                case 7: return VlcSoundPlayerManager.PlaybackState.ERROR
                case _: raise ValueError(f'Encountered unexpected vlc.State value: \"{state}\"')

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None,
        playSessionIdGenerator: PlaySessionIdGeneratorInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        playlistSleepTimeSeconds: float = 0.15
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif chatBandInstrumentSoundsRepository is not None and not isinstance(chatBandInstrumentSoundsRepository, ChatBandInstrumentSoundsRepositoryInterface):
            raise TypeError(f'chatBandInstrumentSoundsRepository argument is malformed: \"{chatBandInstrumentSoundsRepository}\"')
        elif not isinstance(playSessionIdGenerator, PlaySessionIdGeneratorInterface):
            raise TypeError(f'playSessionIdGenerator argument is malformed: \"{playSessionIdGenerator}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(playlistSleepTimeSeconds):
            raise TypeError(f'playlistSleepTimeSeconds argument is malformed: \"{playlistSleepTimeSeconds}\"')
        elif playlistSleepTimeSeconds < 0.1 or playlistSleepTimeSeconds > 8:
            raise ValueError(f'playlistSleepTimeSeconds argument is out of bounds: {playlistSleepTimeSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None = chatBandInstrumentSoundsRepository
        self.__playSessionIdGenerator: PlaySessionIdGeneratorInterface = playSessionIdGenerator
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber
        self.__playlistSleepTimeSeconds: float = playlistSleepTimeSeconds

        self.__isProgressingThroughPlaylist: bool = False
        self.__currentPlaySessionId: str | None = None
        self.__mediaPlayer: vlc.MediaPlayer | None = None

    async def __applyNewPlaySessionId(self) -> str:
        newPlaySessionId = await self.__playSessionIdGenerator.generatePlaySessionId()
        self.__currentPlaySessionId = newPlaySessionId
        return newPlaySessionId

    def __clearCurrentPlaySession(self):
        self.__isProgressingThroughPlaylist = False
        self.__currentPlaySessionId = None

    async def getCurrentPlaySessionId(self) -> str | None:
        return self.__currentPlaySessionId

    async def isPlaying(self) -> bool:
        if self.__isProgressingThroughPlaylist:
            return True

        mediaPlayer = self.__mediaPlayer
        return mediaPlayer is not None and mediaPlayer.is_playing()

    async def playChatBandInstrument(
        self,
        instrument: ChatBandInstrument,
        volume: int | None = None
    ) -> str | None:
        if not isinstance(instrument, ChatBandInstrument):
            raise TypeError(f'instrument argument is malformed: \"{instrument}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume is not None and (volume < 0 or volume > 100):
            raise ValueError(f'volume argument is out of bounds: {volume}')

        chatBandInstrumentSoundsRepository = self.__chatBandInstrumentSoundsRepository

        if chatBandInstrumentSoundsRepository is None:
            return None
        elif not await self.__soundPlayerSettingsRepository.isEnabled():
            return None
        elif await self.isPlaying():
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return None

        filePath = await chatBandInstrumentSoundsRepository.getRandomSound(instrument)

        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'No file path available for chat band instrument ({instrument=}) ({filePath=})')
            return None

        filePaths: FrozenList[str] = FrozenList()
        filePaths.append(filePath)
        filePaths.freeze()

        return await self.playPlaylist(
            filePaths = filePaths,
            volume = volume
        )

    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> str | None:
        if not isinstance(filePaths, Collection):
            raise TypeError(f'filePaths argument is malformed: \"{filePaths}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume is not None and (volume < 0 or volume > 100):
            raise ValueError(f'volume argument is out of bounds: {volume}')

        frozenFilePaths: FrozenList[str] = FrozenList(filePaths)
        frozenFilePaths.freeze()

        if len(frozenFilePaths) == 0:
            self.__timber.log('VlcSoundPlayerManager', f'filePaths argument has no elements: \"{filePaths}\"')
            return None

        for index, filePath in enumerate(frozenFilePaths):
            if not utils.isValidStr(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} is not a valid string: \"{filePath}\"')
                return None
            elif not await aiofiles.ospath.exists(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} does not exist: \"{filePath}\"')
                return None
            elif not await aiofiles.ospath.isfile(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} is not a file: \"{filePath}\"')
                return None

        mediaList: vlc.MediaList | None = None
        addResults: dict[str, int] = dict()
        exception: Exception | None = None

        try:
            mediaList = vlc.MediaList()

            if not isinstance(mediaList, vlc.MediaList):
                return None

            mediaList.lock()

            for filePath in frozenFilePaths:
                addResult = mediaList.add_media(filePath)
                addResults[filePath] = addResult
        except Exception as e:
            exception = e

        if mediaList is None or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to load sounds from file paths: \"{filePaths}\" ({mediaList=}) ({exception=})', exception, traceback.format_exc())
            return None

        for filePath, addResult in addResults.items():
            if addResult != 0:
                self.__timber.log('VlcSoundPlayerManager', f'Encountered bad result code ({addResult}) when trying to add sound \"{filePath}\" from file paths: \"{filePaths}\" ({mediaList=}) ({exception=})', exception, traceback.format_exc())
                return None

        if not utils.isValidInt(volume):
            volume = await self.__soundPlayerSettingsRepository.getMediaPlayerVolume()

        mediaPlayer = await self.__retrieveMediaPlayer()
        newPlaySessionId = await self.__applyNewPlaySessionId()

        self.__backgroundTaskHelper.createTask(self.__progressThroughPlaylist(
            playlistFilePaths = frozenFilePaths,
            volume = volume,
            playSessionId = newPlaySessionId,
            mediaPlayer = mediaPlayer
        ))

        self.__timber.log('VlcSoundPlayerManager', f'Started playing playlist ({newPlaySessionId=}) ({filePaths=}) ({volume=}) ({mediaList=}) ({mediaPlayer=})')
        return newPlaySessionId

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> str | None:
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume is not None and (volume < 0 or volume > 100):
            raise ValueError(f'volume argument is out of bounds: {volume}')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return None
        elif await self.isPlaying():
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return None

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(alert)

        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'No file path available for sound alert ({alert=}) ({filePath=})')
            return None

        return await self.playSoundFile(
            filePath = filePath,
            volume = volume
        )

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> str | None:
        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'filePath argument is malformed: \"{filePath}\"')
            return None
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume is not None and (volume < 0 or volume > 100):
            raise ValueError(f'volume argument is out of bounds: {volume}')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return None
        elif await self.isPlaying():
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return None

        filePaths: FrozenList[str] = FrozenList()
        filePaths.append(filePath)
        filePaths.freeze()

        return await self.playPlaylist(
            filePaths = filePaths,
            volume = volume
        )

    async def __progressThroughPlaylist(
        self,
        playlistFilePaths: FrozenList[str],
        volume: int,
        playSessionId: str,
        mediaPlayer: vlc.MediaPlayer
    ):
        if not isinstance(playlistFilePaths, FrozenList) or len(playlistFilePaths) == 0:
            raise TypeError(f'playlist argument is malformed: \"{playlistFilePaths}\"')
        elif not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume < 0 or volume > 100:
            raise ValueError(f'volume argument is out of bounds: {volume}')
        elif not utils.isValidStr(playSessionId):
            raise TypeError(f'playSessionId argument is malformed: \"{playSessionId}\"')
        elif not isinstance(mediaPlayer, vlc.MediaPlayer):
            raise TypeError(f'mediaPlayer argument is malformed: \"{mediaPlayer}\"')

        self.__isProgressingThroughPlaylist = True
        playlistSleepTimeSeconds = self.__playlistSleepTimeSeconds
        currentPlaylistIndex: int | None = -1

        try:
            while currentPlaylistIndex != None and currentPlaylistIndex < len(playlistFilePaths):
                mediaPlayerState = VlcSoundPlayerManager.PlaybackState.fromVlcState(mediaPlayer.get_state())

                match mediaPlayerState:
                    case VlcSoundPlayerManager.PlaybackState.ERROR:
                        currentPlaylistIndex = None

                    case VlcSoundPlayerManager.PlaybackState.PLAYING:
                        # intentionally empty
                        pass

                    case VlcSoundPlayerManager.PlaybackState.STOPPED:
                        currentPlaylistIndex += 1

                        if currentPlaylistIndex >= len(playlistFilePaths):
                            currentPlaylistIndex = None
                        else:
                            currentFilePath = playlistFilePaths[currentPlaylistIndex]
                            mediaPlayer.set_media(vlc.Media(currentFilePath))
                            volumeResult = mediaPlayer.audio_set_volume(volume)
                            playbackResult = mediaPlayer.play()

                            if playbackResult != 0:
                                self.__timber.log('VlcSoundPlayerManager', f'Received bad playback result when attempting to play media element at playlist index ({volumeResult=}) ({playbackResult=}) ({currentPlaylistIndex=}) ({currentFilePath=}) ({playlistFilePaths=}) ({playSessionId=}) ({mediaPlayer=})')
                                currentPlaylistIndex = None

                if currentPlaylistIndex is not None:
                    await asyncio.sleep(playlistSleepTimeSeconds)
        except Exception as e:
            self.__timber.log('VlcSoundPlayerManager', f'Encountered exception when progressing through playlist ({currentPlaylistIndex=}) ({playlistFilePaths=}) ({playSessionId=}) ({mediaPlayer=}): {e}', e, traceback.format_exc())

        self.__clearCurrentPlaySession()

    async def __retrieveMediaPlayer(self) -> vlc.MediaPlayer:
        mediaPlayer = self.__mediaPlayer

        if mediaPlayer is None:
            mediaPlayer = vlc.MediaPlayer()
            self.__mediaPlayer = mediaPlayer
            self.__timber.log('VlcSoundPlayerManager', f'Created new vlc.MediaPlayer instance: \"{mediaPlayer}\"')

        if not isinstance(mediaPlayer, vlc.MediaPlayer):
            # this scenario should definitely be impossible, but the Python type checking was
            # getting angry without this check
            exception = RuntimeError(f'Failed to instantiate vlc.MediaPlayer: \"{mediaPlayer}\"')
            self.__timber.log('VlcSoundPlayerManager', f'Failed to instantiate vlc.MediaPlayer: \"{mediaPlayer}\" ({exception=})', exception, traceback.format_exc())
            raise exception

        return mediaPlayer

    async def stop(self) -> bool:
        currentPlaySessionId = await self.getCurrentPlaySessionId()

        if not utils.isValidStr(currentPlaySessionId):
            self.__timber.log('VlcSoundPlayerManager', f'There is no current play session ID, so no need to try to stop any media playback ({currentPlaySessionId=})')
            return False

        mediaPlayer = await self.__retrieveMediaPlayer()
        exception: Exception | None = None

        try:
            mediaPlayer.stop()
        except Exception as e:
            exception = e

        self.__clearCurrentPlaySession()

        if exception is None:
            self.__timber.log('VlcSoundPlayerManager', f'Stopped ({currentPlaySessionId=}) ({mediaPlayer=})')
            return True
        else:
            self.__timber.log('VlcSoundPlayerManager', f'Attempted to stop but an exception occurred ({currentPlaySessionId=}) ({mediaPlayer=}): {exception}', exception, traceback.format_exc())
            return False

    async def stopPlaySessionId(self, playSessionId: str | None) -> bool:
        if playSessionId is not None and not isinstance(playSessionId, str):
            raise TypeError(f'playSessionId argument is malformed: \"{playSessionId}\"')
        elif not utils.isValidStr(playSessionId):
            return False

        currentPlaySessionId = await self.getCurrentPlaySessionId()

        if playSessionId == currentPlaySessionId:
            return await self.stop()
        else:
            self.__timber.log('VlcSoundPlayerManager', f'Attempted to stop but the given playSessionId is not what is currently playing ({playSessionId=}) ({currentPlaySessionId=})')
            return False
