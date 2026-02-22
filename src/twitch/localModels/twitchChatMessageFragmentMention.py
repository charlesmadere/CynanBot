from dataclasses import dataclass

from .twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class TwitchChatMessageFragmentMention(TwitchUserInterface):
    userId: str
    userLogin: str
    userName: str

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName
