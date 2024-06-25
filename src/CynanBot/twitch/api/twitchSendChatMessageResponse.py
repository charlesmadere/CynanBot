from dataclasses import dataclass

from CynanBot.twitch.api.twitchSendChatDropReason import \
    TwitchSendChatDropReason


@dataclass(frozen = True)
class TwitchSendChatMessageResponse():
    isSent: bool
    messageId: str
    dropReason: TwitchSendChatDropReason | None
