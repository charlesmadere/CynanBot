from dataclasses import dataclass

from .chatterItemType import ChatterItemType
from .useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class UseAirStrikeItemAction(UseChatterItemAction):
    actionId: str
    chatterUserId: str
    twitchChannel: str
    twitchChannelId: str

    def getActionId(self) -> str:
        return self.actionId

    def getItemType(self) -> ChatterItemType:
        return ChatterItemType.AIR_STRIKE

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
