from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchUpdateConduitShardsRequestEntry import TwitchUpdateConduitShardsRequestEntry


# This class intends to directly correspond to Twitch's "Update Conduit Shards" API:
# https://dev.twitch.tv/docs/api/reference/#update-conduit-shards
@dataclass(frozen = True, slots = True)
class TwitchUpdateConduitShardsRequest:
    shards: FrozenList[TwitchUpdateConduitShardsRequestEntry]
    conduitId: str
