from dataclasses import dataclass

from .chatterItemType import ChatterItemType
from .useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class UseGrenadeItemAction(UseChatterItemAction):
    durationSeconds: int
    actionId: str
    chatterUserId: str
    twitchChannel: str
    twitchChannelId: str

    def getActionId(self) -> str:
        return self.actionId

    def getChatterUserId(self) -> str:
        return self.chatterUserId

    def getItemType(self) -> ChatterItemType:
        return ChatterItemType.GRENADE

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
