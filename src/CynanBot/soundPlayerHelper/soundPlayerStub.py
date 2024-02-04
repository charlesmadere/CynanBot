from typing import Optional

from CynanBot.soundPlayerHelper.soundPlayerInterface import \
    SoundPlayerInterface
from CynanBot.soundPlayerHelper.soundReferenceInterface import \
    SoundReferenceInterface
from CynanBot.soundPlayerHelper.soundReferenceStub import SoundReferenceStub
from CynanBot.timber.timberInterface import TimberInterface


class SoundPlayerStub(SoundPlayerInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def load(self, filePath: Optional[str]) -> SoundReferenceInterface:
        if filePath is not None and not isinstance(filePath, str):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        return SoundReferenceStub(
            filePath = filePath,
            timber = self.__timber
        )
