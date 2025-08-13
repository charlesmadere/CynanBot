from dataclasses import dataclass

from .absTimeoutTarget import AbsTimeoutTarget


@dataclass(frozen = True)
class BananaTimeoutTarget(AbsTimeoutTarget):
    targetUserId: str
    targetUserName: str

    def getTargetUserId(self) -> str:
        return self.targetUserId

    def getTargetUserName(self) -> str:
        return self.targetUserName
