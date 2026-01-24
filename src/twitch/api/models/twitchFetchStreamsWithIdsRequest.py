from dataclasses import dataclass

from .twitchFetchStreamsRequest import TwitchFetchStreamsRequest


@dataclass(frozen = True, slots = True)
class TwitchFetchStreamsWithIdsRequest(TwitchFetchStreamsRequest):
    userIds: frozenset[str]
