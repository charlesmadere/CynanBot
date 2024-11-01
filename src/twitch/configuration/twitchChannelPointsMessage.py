from dataclasses import dataclass

from ...users.userInterface import UserInterface


@dataclass(frozen = True)
class TwitchChannelPointsMessage:
    eventId: str
    redemptionMessage: str | None
    rewardId: str
    twitchUser: UserInterface
    userId: str
    userName: str
