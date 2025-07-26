from dataclasses import dataclass


@dataclass(frozen = True)
class PointRedemptionTimeoutData:
    eventId: str
    message: str | None
    rewardId: str
