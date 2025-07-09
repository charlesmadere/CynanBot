from dataclasses import dataclass

from .twitchContributionType import TwitchContributionType


@dataclass(frozen = True)
class TwitchContribution:
    total: int
    userId: str
    userLogin: str
    userName: str
    contributionType: TwitchContributionType
