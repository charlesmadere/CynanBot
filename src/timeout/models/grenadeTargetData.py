from dataclasses import dataclass


@dataclass(frozen = True)
class GrenadeTargetData:
    targetUserId: str
    targetUserName: str
