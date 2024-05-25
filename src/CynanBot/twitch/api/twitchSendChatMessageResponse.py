from dataclasses import dataclass

from CynanBot.twitch.api.twitchChatDropReason import TwitchChatDropReason


@dataclass(frozen = True)
class TwitchSendChatMessageResponse():
    isSent: bool
    messageId: str
    dropReason: TwitchChatDropReason | None
