from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchSendChatMessageResponseEntry import TwitchSendChatMessageResponseEntry


# This class intends to directly correspond to Twitch's "Send Chat Message" API:
# https://dev.twitch.tv/docs/api/reference/#send-chat-message
@dataclass(frozen = True, slots = True)
class TwitchSendChatMessageResponse:
    data: FrozenList[TwitchSendChatMessageResponseEntry]
