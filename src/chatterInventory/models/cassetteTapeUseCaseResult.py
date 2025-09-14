from dataclasses import dataclass


@dataclass(frozen = True)
class CassetteTapeUseCaseResult:
    targetUserId: str
    targetUserName: str
