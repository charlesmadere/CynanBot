from dataclasses import dataclass

from .editCheerActionResult import EditCheerActionResult


@dataclass(frozen = True, slots = True)
class NotFoundEditCheerActionResult(EditCheerActionResult):
    bits: int
    twitchChannelId: str

    @property
    def getBits(self) -> int:
        return self.bits

    @property
    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
