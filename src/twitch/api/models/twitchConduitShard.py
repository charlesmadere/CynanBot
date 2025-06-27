from dataclasses import dataclass


# This class intends to directly correspond to the "conduit_shard" field from Twitch's "Verifying
# a Conduit" API: https://dev.twitch.tv/docs/eventsub/handling-conduit-events/#verifying-a-conduit
@dataclass(frozen = True)
class TwitchConduitShard:
    conduitId: str
    shard: str
