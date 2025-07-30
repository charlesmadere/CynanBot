from dataclasses import dataclass


@dataclass(frozen = True)
class AirStrikeTargetData:
    targetUserId: str
    targetUserName: str
