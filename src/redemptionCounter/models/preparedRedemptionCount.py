from dataclasses import dataclass

from .redemptionCount import RedemptionCount


@dataclass(frozen = True)
class PreparedRedemptionCount:
    redemptionCount: RedemptionCount
    chatterUserName: str

    @property
    def count(self) -> int:
        return self.redemptionCount.count

    @property
    def countStr(self) -> str:
        return self.redemptionCount.countStr

    @property
    def chatterUserId(self) -> str:
        return self.redemptionCount.chatterUserId

    @property
    def counterName(self) -> str:
        return self.redemptionCount.counterName

    @property
    def twitchChannelId(self) -> str:
        return self.redemptionCount.twitchChannelId
