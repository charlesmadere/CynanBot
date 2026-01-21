import locale

from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AsplodieStats:
    selfAsplodies: int
    totalAsplodies: int
    totalDurationAsplodiedSeconds: int
    chatterUserId: str
    twitchChannelId: str

    @property
    def selfAsplodiesStr(self) -> str:
        return locale.format_string("%d", self.selfAsplodies, grouping = True)

    @property
    def totalAsplodiesStr(self) -> str:
        return locale.format_string("%d", self.totalAsplodies, grouping = True)

    @property
    def totalDurationAsplodiedSecondsStr(self) -> str:
        return locale.format_string("%d", self.totalDurationAsplodiedSeconds, grouping = True)
