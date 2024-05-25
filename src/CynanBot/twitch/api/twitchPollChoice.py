from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchPollChoice():
    channelPointsVotes: int
    votes: int
    choiceId: str
    title: str
