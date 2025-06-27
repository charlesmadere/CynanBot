from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchConduitRequest:
    shardCount: int
