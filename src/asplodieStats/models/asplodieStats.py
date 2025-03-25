import locale

from dataclasses import dataclass


@dataclass(frozen = True)
class AsplodieStats:
    totalAsplodies: int
    totalDurationAsplodiedSeconds: int
    chatterUserId: str
    twitchChannelId: str

    @property
    def totalAsplodiesStr(self) -> str:
        return locale.format_string("%d", self.totalAsplodies, grouping = True)

    @property
    def totalDurationAsplodiedSecondsStr(self) -> str:
        return locale.format_string("%d", self.totalDurationAsplodiedSeconds, grouping = True)
