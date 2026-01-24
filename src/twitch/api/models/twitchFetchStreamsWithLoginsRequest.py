from dataclasses import dataclass

from .twitchFetchStreamsRequest import TwitchFetchStreamsRequest


@dataclass(frozen = True, slots = True)
class TwitchFetchStreamsWithLoginsRequest(TwitchFetchStreamsRequest):
    userLogins: frozenset[str]
