from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChatBadge:
    badgeId: str | None
    info: str |  None
    setId: str | None
