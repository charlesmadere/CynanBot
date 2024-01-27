from typing import Optional

from CynanBot.soundPlayerHelper.soundReferenceInterface import \
    SoundReferenceInterface
from CynanBot.timber.timberInterface import TimberInterface


class SoundReferenceStub(SoundReferenceInterface):

    def __init__(
        self,
        filePath: Optional[str],
        timber: TimberInterface
    ):
        if filePath is not None and not isinstance(filePath, str):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__filePath: Optional[str] = filePath
        self.__timber: TimberInterface = timber

    async def getDurationMillis(self) -> int:
        return 0

    async def play(self):
        self.__timber.log('SoundReferenceStub', f'Attempted to play \"{self.__filePath}\", but this is just a stub, so nothing will play')
