from dataclasses import dataclass

from .twitchFetchUserRequest import TwitchFetchUserRequest


@dataclass(frozen = True, slots = True)
class TwitchFetchUserWithIdRequest(TwitchFetchUserRequest):
    userId: str
