import traceback
from typing import Collection

import aiofiles.ospath
from frozenlist import FrozenList

from .vlcMediaPlayer import VlcMediaPlayer
from ..playSessionIdGenerator.playSessionIdGeneratorInterface import PlaySessionIdGeneratorInterface
from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...chatBand.chatBandInstrument import ChatBandInstrument
from ...chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class VlcSoundPlayerManager(SoundPlayerManagerInterface):

    def __init__(
        self,
        chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None,
        playSessionIdGenerator: PlaySessionIdGeneratorInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if chatBandInstrumentSoundsRepository is not None and not isinstance(chatBandInstrumentSoundsRepository, ChatBandInstrumentSoundsRepositoryInterface):
            raise TypeError(f'chatBandInstrumentSoundsRepository argument is malformed: \"{chatBandInstrumentSoundsRepository}\"')
        elif not isinstance(playSessionIdGenerator, PlaySessionIdGeneratorInterface):
            raise TypeError(f'playSessionIdGenerator argument is malformed: \"{playSessionIdGenerator}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None = chatBandInstrumentSoundsRepository
        self.__playSessionIdGenerator: PlaySessionIdGeneratorInterface = playSessionIdGenerator
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber

        self.__isProgressingThroughPlaylist: bool = False
        self.__currentPlaySessionId: str | None = None
        self.__mediaPlayer: VlcMediaPlayer | None = None

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
        return mediaPlayer is not None and mediaPlayer.isPlaying

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

        if not utils.isValidInt(volume):
            volume = await self.__soundPlayerSettingsRepository.getMediaPlayerVolume()

        mediaPlayer = await self.__retrieveMediaPlayer()
        newPlaySessionId = await self.__applyNewPlaySessionId()

        await self.__progressThroughPlaylist(
            playlistFilePaths = frozenFilePaths,
            volume = volume,
            playSessionId = newPlaySessionId,
            mediaPlayer = mediaPlayer
        )

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
        mediaPlayer: VlcMediaPlayer
    ):
        if not isinstance(playlistFilePaths, FrozenList) or len(playlistFilePaths) == 0:
            raise TypeError(f'playlist argument is malformed: \"{playlistFilePaths}\"')
        elif not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume < 0 or volume > 100:
            raise ValueError(f'volume argument is out of bounds: {volume}')
        elif not utils.isValidStr(playSessionId):
            raise TypeError(f'playSessionId argument is malformed: \"{playSessionId}\"')
        elif not isinstance(mediaPlayer, VlcMediaPlayer):
            raise TypeError(f'mediaPlayer argument is malformed: \"{mediaPlayer}\"')

        self.__isProgressingThroughPlaylist = True
        playErrorOccurred: bool = False
        currentPlaylistIndex: int = -1
        currentFilePath: str | None = None

        await mediaPlayer.setVolume(volume)

        self.__timber.log('VlcSoundPlayerManager', f'Started playing playlist ({playlistFilePaths=}) ({volume=}) ({playSessionId=}) ({mediaPlayer=})')

        try:
            while not playErrorOccurred and currentPlaylistIndex < len(playlistFilePaths):
                match mediaPlayer.playbackState:
                    case VlcMediaPlayer.PlaybackState.ERROR:
                        playErrorOccurred = True

                    case VlcMediaPlayer.PlaybackState.PLAYING:
                        # intentionally empty
                        pass

                    case VlcMediaPlayer.PlaybackState.STOPPED:
                        if currentPlaylistIndex == -1:
                            currentPlaylistIndex = 0
                        else:
                            currentPlaylistIndex += 1

                        if currentPlaylistIndex < len(playlistFilePaths):
                            currentFilePath = playlistFilePaths[currentPlaylistIndex]
                            await mediaPlayer.setMedia(currentFilePath)

                            if not await mediaPlayer.play():
                                self.__timber.log('VlcSoundPlayerManager', f'Received bad playback result when attempting to play media element at playlist index ({currentPlaylistIndex=}) ({currentFilePath=}) ({playlistFilePaths=}) ({playSessionId=}) ({mediaPlayer=})')
                                playErrorOccurred = True
        except Exception as e:
            self.__timber.log('VlcSoundPlayerManager', f'Encountered exception when progressing through playlist ({playErrorOccurred=}) ({currentPlaylistIndex=}) ({currentFilePath=}) ({playlistFilePaths=}) ({playSessionId=}) ({mediaPlayer=}): {e}', e, traceback.format_exc())

        self.__clearCurrentPlaySession()

    async def __retrieveMediaPlayer(self) -> VlcMediaPlayer:
        mediaPlayer = self.__mediaPlayer

        if mediaPlayer is None:
            mediaPlayer = VlcMediaPlayer(timber = self.__timber)
            self.__mediaPlayer = mediaPlayer
            self.__timber.log('VlcSoundPlayerManager', f'Created new VlcMediaPlayer instance: \"{mediaPlayer}\"')

        return mediaPlayer

    async def stop(self):
        currentPlaySessionId = await self.getCurrentPlaySessionId()

        if not utils.isValidStr(currentPlaySessionId):
            self.__timber.log('VlcSoundPlayerManager', f'There is no current play session ID, so no need to try to stop any media playback ({currentPlaySessionId=})')
            return False

        mediaPlayer = await self.__retrieveMediaPlayer()
        await mediaPlayer.stop()

        self.__clearCurrentPlaySession()
        return True

    async def stopPlaySessionId(self, playSessionId: str | None) -> bool:
        if playSessionId is not None and not isinstance(playSessionId, str):
            raise TypeError(f'playSessionId argument is malformed: \"{playSessionId}\"')
        elif not utils.isValidStr(playSessionId):
            return False

        currentPlaySessionId = await self.getCurrentPlaySessionId()

        if playSessionId == currentPlaySessionId:
            await self.stop()
            return True
        else:
            self.__timber.log('VlcSoundPlayerManager', f'Attempted to stop but the given playSessionId is not what is currently playing ({playSessionId=}) ({currentPlaySessionId=})')
            return False
