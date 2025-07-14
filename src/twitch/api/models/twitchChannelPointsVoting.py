from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChannelPointsVoting:
    isEnabled: bool
    amountPerVote: int
