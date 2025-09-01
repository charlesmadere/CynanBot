from dataclasses import dataclass


@dataclass(frozen = True)
class GlobalTwitchConstants:
    maxMessageSize: int = 498 # the actual max is 500, but let's leave a small buffer
    maxTimeoutSeconds: int = 1209600 # 14 days
