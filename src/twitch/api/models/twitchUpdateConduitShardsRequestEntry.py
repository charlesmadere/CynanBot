from dataclasses import dataclass

from .twitchWebsocketTransport import TwitchWebsocketTransport


@dataclass(frozen = True)
class TwitchUpdateConduitShardsRequestEntry:
    shardId: str
    transport: TwitchWebsocketTransport
