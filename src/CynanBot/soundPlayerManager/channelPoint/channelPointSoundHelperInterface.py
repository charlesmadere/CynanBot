from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.soundPlayerManager.soundAlert import SoundAlert


class ChannelPointSoundHelperInterface(Clearable):

    @abstractmethod
    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        pass
