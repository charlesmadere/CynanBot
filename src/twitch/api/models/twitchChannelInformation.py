from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True, slots = True)
class TwitchChannelInformation:
    isBrandedContent: bool
    contentClassificationLabels: FrozenList[str]
    tags: FrozenList[str]
    delaySeconds: int | None
    broadcasterId: str
    broadcasterLanguage: str | None
    broadcasterLogin: str
    broadcasterName: str
    gameId: str | None
    gameName: str | None
    title: str | None
