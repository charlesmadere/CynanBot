from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchWebsocketChannelPointsVoting():
    isEnabled: bool
    amountPerVote: int
