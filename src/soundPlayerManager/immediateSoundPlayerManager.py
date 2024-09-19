from typing import Collection

from .immediateSoundPlayerManagerInterface import ImmediateSoundPlayerManagerInterface
from .soundAlert import SoundAlert
from .soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class ImmediateSoundPlayerManager(ImmediateSoundPlayerManagerInterface):

    def __init__(
        self,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface
    ):
        if not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__timber: TimberInterface = timber

    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> bool:
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
    ) -> bool:
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
    ) -> bool:
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
