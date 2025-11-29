import asyncio
import os
import traceback
from asyncio import AbstractEventLoop
from typing import Collection, Final

import aiofiles.ospath
from frozenlist import FrozenList

from .audioPlayerMediaPlayer import AudioPlayerMediaPlayer
from ..settings.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ..soundAlert import SoundAlert
from ..soundPlaybackFile import SoundPlaybackFile
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerPlaylist import SoundPlayerPlaylist
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils
from ...timber.timberInterface import TimberInterface


class AudioPlayerSoundPlayerManager(SoundPlayerManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        playbackLoopSleepTimeSeconds: float = 0.25,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidNum(playbackLoopSleepTimeSeconds):
            raise TypeError(f'playbackLoopSleepTimeSeconds argument is malformed: \"{playbackLoopSleepTimeSeconds}\"')
        elif playbackLoopSleepTimeSeconds < 0.125 or playbackLoopSleepTimeSeconds > 1:
            raise ValueError(f'playbackLoopSleepTimeSeconds argument is out of bounds: {playbackLoopSleepTimeSeconds}')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__soundPlayerSettingsRepository: Final[SoundPlayerSettingsRepositoryInterface] = soundPlayerSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__playbackLoopSleepTimeSeconds: Final[float] = playbackLoopSleepTimeSeconds

        self.__isLoadingOrPlaying: bool = False
        self.__mediaPlayer: AudioPlayerMediaPlayer | None = None

    @property
    def isLoadingOrPlaying(self) -> bool:
        if self.__isLoadingOrPlaying:
            return True

        mediaPlayer = self.__mediaPlayer
        return mediaPlayer is not None and mediaPlayer.isPlaying

    async def playPlaylist(
        self,
        playlist: SoundPlayerPlaylist,
    ) -> bool:
        if not isinstance(playlist, SoundPlayerPlaylist):
            raise TypeError(f'playlist argument is malformed: \"{playlist}\"')

        self.__isLoadingOrPlaying = True

        if len(playlist.playlistFiles) == 0:
            self.__timber.log('AudioPlayerSoundPlayerManager', f'filePaths argument has no elements: \"{playlist}\"')
            self.__isLoadingOrPlaying = False
            return False

        for index, playlistFile in enumerate(playlist.playlistFiles):
            if not utils.isValidStr(playlistFile.filePath):
                self.__timber.log('AudioPlayerSoundPlayerManager', f'The given file path at index {index} is not a valid string: ({playlist=}) ({playlistFile=})')
                self.__isLoadingOrPlaying = False
                return False
            elif not await aiofiles.ospath.exists(
                path = playlistFile.filePath,
                loop = self.__eventLoop,
            ):
                self.__timber.log('AudioPlayerSoundPlayerManager', f'The given file path at index {index} does not exist: ({playlist=}) ({playlistFile=})')
                self.__isLoadingOrPlaying = False
                return False
            elif not await aiofiles.ospath.isfile(
                path = playlistFile.filePath,
                loop = self.__eventLoop,
            ):
                self.__timber.log('AudioPlayerSoundPlayerManager', f'The given file path at index {index} is not a file: ({playlist=}) ({playlistFile=})')
                self.__isLoadingOrPlaying = False
                return False

        await self.__progressThroughPlaylist(
            playlist = playlist,
        )

        return True

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None,
    ) -> bool:
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif self.isLoadingOrPlaying:
            self.__timber.log('AudioPlayerSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(alert)

        if not utils.isValidStr(filePath):
            self.__timber.log('AudioPlayerSoundPlayerManager', f'No file path available for sound alert ({alert=}) ({filePath=})')
            return False

        filePath = os.path.normpath(filePath)

        return await self.playSoundFile(
            filePath = filePath,
            volume = volume,
        )

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None,
    ) -> bool:
        if filePath is not None and not isinstance(filePath, str):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        if not utils.isValidStr(filePath):
            self.__timber.log('AudioPlayerSoundPlayerManager', f'The given file path is not a valid string: \"{filePath}\"')
            return False
        elif not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif self.isLoadingOrPlaying:
            self.__timber.log('AudioPlayerSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        playlistFiles: FrozenList[SoundPlaybackFile] = FrozenList()

        playlistFiles.append(SoundPlaybackFile(
            volume = None,
            filePath = filePath,
        ))

        playlistFiles.freeze()

        playlist = SoundPlayerPlaylist(
            playlistFiles = playlistFiles,
            volume = volume,
        )

        return await self.playPlaylist(
            playlist = playlist,
        )

    async def playSoundFiles(
        self,
        filePaths: Collection[str],
        volume: int | None = None,
    ) -> bool:
        if not isinstance(filePaths, Collection):
            raise TypeError(f'filePaths argument is malformed: \"{filePaths}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif self.isLoadingOrPlaying:
            self.__timber.log('AudioPlayerSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        playlistFiles: FrozenList[SoundPlaybackFile] = FrozenList()

        for filePath in filePaths:
            playlistFiles.append(SoundPlaybackFile(
                volume = None,
                filePath = filePath,
            ))

        playlistFiles.freeze()

        if len(playlistFiles) == 0:
            self.__timber.log('AudioPlayerSoundPlayerManager', f'filePaths argument has no elements: \"{filePaths}\"')
            return False

        playlist = SoundPlayerPlaylist(
            playlistFiles = playlistFiles,
            volume = volume,
        )

        return await self.playPlaylist(
            playlist = playlist,
        )

    async def __progressThroughPlaylist(self, playlist: SoundPlayerPlaylist):
        if not isinstance(playlist, SoundPlayerPlaylist):
            raise TypeError(f'playlist argument is malformed: \"{playlist}\"')

        mediaPlayer = await self.__retrieveMediaPlayer()
        baseVolume = playlist.volume

        if not utils.isValidInt(baseVolume):
            baseVolume = await self.__soundPlayerSettingsRepository.getMediaPlayerVolume()

        await mediaPlayer.setVolume(baseVolume)

        playErrorOccurred: bool = False
        currentPlaylistIndex: int = -1
        currentVolume: int | None = None
        currentFile: SoundPlaybackFile | None = None

        self.__timber.log('AudioPlayerSoundPlayerManager', f'Started playing playlist ({playlist=}) ({baseVolume=}) ({mediaPlayer=})')

        try:
            while self.__isLoadingOrPlaying and not playErrorOccurred and (currentPlaylistIndex < len(playlist.playlistFiles) or mediaPlayer.isPlaying):
                if mediaPlayer.isPlaying:
                    pass
                else:
                    if currentPlaylistIndex < 0:
                        currentPlaylistIndex = 0
                    else:
                        currentPlaylistIndex += 1

                    if currentPlaylistIndex < len(playlist.playlistFiles):
                        currentFile = playlist.playlistFiles[currentPlaylistIndex]
                        currentVolume = currentFile.volume

                        if not utils.isValidInt(currentVolume):
                            currentVolume = baseVolume

                        await mediaPlayer.setMedia(currentFile.filePath)
                        await mediaPlayer.setVolume(currentVolume)

                        if not await mediaPlayer.play():
                            self.__timber.log('AudioPlayerSoundPlayerManager', f'Received bad playback result when attempting to play media element at playlist index ({currentPlaylistIndex=}) ({currentFile=}) ({currentVolume=}) ({playlist=}) ({baseVolume=}) ({mediaPlayer=})')
                            playErrorOccurred = True

                await asyncio.sleep(self.__playbackLoopSleepTimeSeconds)
        except Exception as e:
            self.__timber.log('AudioPlayerSoundPlayerManager', f'Encountered exception when progressing through playlist ({playErrorOccurred=}) ({currentPlaylistIndex=}) ({currentFile=}) ({currentVolume=}) ({playlist=}) ({baseVolume=}) ({mediaPlayer=}): {e}', e, traceback.format_exc())

        self.__isLoadingOrPlaying = False

    async def __retrieveMediaPlayer(self) -> AudioPlayerMediaPlayer:
        mediaPlayer = self.__mediaPlayer

        if mediaPlayer is None:
            mediaPlayer = AudioPlayerMediaPlayer(
                eventLoop = self.__eventLoop,
                timber = self.__timber,
                timeZoneRepository = self.__timeZoneRepository,
                playbackLoopSleepTimeSeconds = self.__playbackLoopSleepTimeSeconds,
            )

            self.__mediaPlayer = mediaPlayer
            self.__timber.log('AudioPlayerSoundPlayerManager', f'Created new AudioPlayerMediaPlayer instance: \"{mediaPlayer}\"')

        return mediaPlayer

    async def stop(self):
        mediaPlayer = self.__mediaPlayer

        if mediaPlayer is not None:
            await mediaPlayer.stop()
            self.__isLoadingOrPlaying = False
