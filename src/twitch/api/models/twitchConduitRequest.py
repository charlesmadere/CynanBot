from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchConduitRequest:
    shardCount: int
