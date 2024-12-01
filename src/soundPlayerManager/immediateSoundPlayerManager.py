from typing import Collection

from .soundAlert import SoundAlert
from .soundPlayerManagerInterface import SoundPlayerManagerInterface
from .soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..chatBand.chatBandInstrument import ChatBandInstrument
from ..misc import utils as utils


class ImmediateSoundPlayerManager(SoundPlayerManagerInterface):

    def __init__(
        self,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface
    ):
        if not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')

        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider

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

        soundPlayManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayManager.playChatBandInstrument(
            instrument = instrument,
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

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayerManager.playPlaylist(
            filePaths = filePaths,
            volume = volume
        )

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

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayerManager.playSoundAlert(
            alert = alert,
            volume = volume
        )

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> str | None:
        if filePath is not None and not isinstance(filePath, str):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume is not None and (volume < 0 or volume > 100):
            raise ValueError(f'volume argument is out of bounds: {volume}')

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayerManager.playSoundFile(
            filePath = filePath,
            volume = volume
        )

    async def stop(self) -> str | None:
        # this method is intentionally empty
        return None
