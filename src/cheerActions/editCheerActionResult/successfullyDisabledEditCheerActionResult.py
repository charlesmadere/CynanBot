from dataclasses import dataclass

from .editCheerActionResult import EditCheerActionResult
from ..absCheerAction import AbsCheerAction


@dataclass(frozen = True, slots = True)
class SuccessfullyDisabledEditCheerActionResult(EditCheerActionResult):
    cheerAction: AbsCheerAction

    @property
    def bits(self) -> int:
        return self.cheerAction.bits

    @property
    def twitchChannelId(self) -> str:
        return self.cheerAction.twitchChannelId
