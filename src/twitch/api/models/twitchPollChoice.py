import locale
from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchPollChoice:
    channelPointsVotes: int
    votes: int
    choiceId: str
    title: str

    @property
    def channelPointsVotesStr(self) -> str:
        return locale.format_string("%d", self.channelPointsVotes, grouping = True)

    @property
    def votesStr(self) -> str:
        return locale.format_string("%d", self.votes, grouping = True)
