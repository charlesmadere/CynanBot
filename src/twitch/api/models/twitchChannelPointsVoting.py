from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchChannelPointsVoting:
    isEnabled: bool
    amountPerVote: int
