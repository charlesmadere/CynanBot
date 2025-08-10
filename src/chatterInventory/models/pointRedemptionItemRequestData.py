from dataclasses import dataclass


@dataclass(frozen = True)
class PointRedemptionItemRequestData:
    eventId: str
    message: str | None
    rewardId: str
