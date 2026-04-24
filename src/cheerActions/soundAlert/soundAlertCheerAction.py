from dataclasses import dataclass

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType


@dataclass(frozen = True, slots = True)
class SoundAlertCheerAction(AbsCheerAction):
    enabled: bool
    streamStatusRequirement: CheerActionStreamStatusRequirement
    bits: int
    directory: str
    twitchChannelId: str

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.SOUND_ALERT

    def getBits(self) -> int:
        return self.bits

    def getStreamStatusRequirement(self) -> CheerActionStreamStatusRequirement:
        return self.streamStatusRequirement

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def isEnabled(self) -> bool:
        return self.enabled

    def printOut(self) -> str:
        return f'isEnabled={self.enabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, directory={self.directory}'
