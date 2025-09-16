from typing import Final

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class SoundAlertCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        directory: str,
        twitchChannelId: str
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__directory: Final[str] = directory

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.SOUND_ALERT

    @property
    def directory(self) -> str:
        return self.__directory

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, directory={self.__directory}'
