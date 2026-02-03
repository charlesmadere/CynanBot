from dataclasses import dataclass

from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class TwitchChannelPointsMessage:
    rewardCost: int
    eventId: str
    redemptionMessage: str | None
    rewardId: str
    twitchChannelId: str
    userId: str
    userLogin: str
    userName: str
    twitchUser: UserInterface
