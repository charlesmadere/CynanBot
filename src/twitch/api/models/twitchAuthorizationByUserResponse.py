from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchAuthorizationByUser import TwitchAuthorizationByUser


@dataclass(frozen = True, slots = True)
class TwitchAuthorizationByUserResponse:
    data: FrozenList[TwitchAuthorizationByUser]
