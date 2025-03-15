from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChatBadge:
    badgeId: str
    info: str | None
    setId: str
