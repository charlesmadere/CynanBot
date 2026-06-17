from dataclasses import dataclass

from .twitchApiScope import TwitchApiScope
from ...localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class TwitchAuthorizationByUser(TwitchUserInterface):
    scopes: frozenset[TwitchApiScope]
    userId: str
    userLogin: str
    userName: str

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName
