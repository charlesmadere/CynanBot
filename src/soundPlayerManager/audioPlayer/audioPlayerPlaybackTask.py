from typing import Any

from ...misc import utils as utils


class AudioPlayerPlaybackTask:

    def __init__(
        self,
        durationSeconds: float,
        volume: int,
        filePath: str
    ):
        if not utils.isValidNum(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 0 or durationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume < 0 or volume > utils.getIntMaxSafeSize():
            raise ValueError(f'volume argument is out of bounds: {volume}')
        elif not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        self.__durationSeconds: float = durationSeconds
        self.__volume: int = volume
        self.__filePath: str = filePath

        self.__isCanceled: bool = False

    def cancel(self):
        self.__isCanceled = True

    @property
    def durationSeconds(self) -> float:
        return self.__durationSeconds

    @property
    def filePath(self) -> str:
        return self.__filePath

    @property
    def isCanceled(self) -> bool:
        return self.__isCanceled

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'durationSeconds': self.__durationSeconds,
            'filePath': self.__filePath,
            'isCanceled': self.__isCanceled,
            'volume': self.__volume
        }

    @property
    def volume(self) -> int:
        return self.__volume
