from dataclasses import dataclass

from .twitchWebsocketTransport import TwitchWebsocketTransport


@dataclass(frozen = True, slots = True)
class TwitchUpdateConduitShardsRequestEntry:
    shardId: str
    transport: TwitchWebsocketTransport
