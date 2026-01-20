from dataclasses import dataclass

from ..actions.crowdControlAction import CrowdControlAction


@dataclass(frozen = True, slots = True)
class CrowdControlMessage:
    originatingAction: CrowdControlAction
    messageId: str

    @property
    def twitchChannel(self) -> str:
        return self.originatingAction.twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.originatingAction.twitchChannelId

    @property
    def twitchChatMessageId(self) -> str | None:
        return self.originatingAction.twitchChatMessageId
