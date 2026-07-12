from dataclasses import dataclass

from .globalTwitchConstantsInterface import GlobalTwitchConstantsInterface


@dataclass(frozen = True, slots = True)
class GlobalTwitchConstants(GlobalTwitchConstantsInterface):
    maxMessageSize: int = 498 # the actual max is 500, but let's leave a small buffer
    maxTimeoutSeconds: int = 1209600 # 14 days

    def getMaxMessageSize(self) -> int:
        return self.maxMessageSize

    def getMaxTimeoutSeconds(self) -> int:
        return self.maxTimeoutSeconds
