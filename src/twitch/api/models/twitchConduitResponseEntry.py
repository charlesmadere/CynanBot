from dataclasses import dataclass


# This class intends to directly correspond to the "data" field from Twitch's "Creating a
# Conduit" API: https://dev.twitch.tv/docs/eventsub/handling-conduit-events/#creating-a-conduit
@dataclass(frozen = True, slots = True)
class TwitchConduitResponseEntry:
    shardCount: int
    shardId: str
