from typing import Any, Final

from ...misc import utils as utils


class PygameMediaPlaybackTask:

    def __init__(
        self,
        volume: float,
        filePath: str,
    ):
        if not utils.isValidNum(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume < float(0) or volume > float(100):
            raise ValueError(f'volume argument is out of bounds: {volume}')
        elif not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        self.__volume: Final[float] = volume
        self.__filePath: Final[str] = filePath

        self.__isCanceled: bool = False

    def cancel(self):
        self.__isCanceled = True

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
            'filePath': self.__filePath,
            'isCanceled': self.__isCanceled,
            'volume': self.__volume,
        }

    @property
    def volume(self) -> float:
        return self.__volume
