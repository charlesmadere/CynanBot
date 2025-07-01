from dataclasses import dataclass

from .twitchConduitShard import TwitchConduitShard


# This class intends to directly correspond to Twitch's "Verifying a conduit" API:
# https://dev.twitch.tv/docs/eventsub/handling-conduit-events/#verifying-a-conduit
@dataclass(frozen = True)
class TwitchConduitChallengeResponse:
    challenge: str
    conduitShard: TwitchConduitShard
