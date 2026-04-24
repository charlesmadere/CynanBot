from dataclasses import dataclass

from .editCheerActionResult import EditCheerActionResult
from ..absCheerAction import AbsCheerAction


@dataclass(frozen = True, slots = True)
class AlreadyEnabledEditCheerActionResult(EditCheerActionResult):
    cheerAction: AbsCheerAction

    def getBits(self) -> int:
        return self.cheerAction.getBits()

    def getTwitchChannelId(self) -> str:
        return self.cheerAction.getTwitchChannelId()
