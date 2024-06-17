from dataclasses import dataclass

from CynanBot.cheerActions.timeout.timeoutCheerActionEntry import \
    TimeoutCheerActionEntry


@dataclass(frozen = True)
class TimeoutCheerActionHistory():
    totalTimeouts: int
    entries: list[TimeoutCheerActionEntry] | None
    chatterUserId: str
    chatterUserName: str
    twitchChannel: str
    twitchChannelId: str
