from dataclasses import dataclass

from .editCheerActionResult import EditCheerActionResult
from ..absCheerAction import AbsCheerAction


@dataclass(frozen = True, slots = True)
class SuccessfullyEnabledEditCheerActionResult(EditCheerActionResult):
    cheerAction: AbsCheerAction

    @property
    def getBits(self) -> int:
        return self.cheerAction.getBits()

    @property
    def getTwitchChannelId(self) -> str:
        return self.cheerAction.getTwitchChannelId()
