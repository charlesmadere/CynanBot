from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketChannelPointsVoting import TwitchWebsocketChannelPointsVoting
from .twitchWebsocketNoticeType import TwitchWebsocketNoticeType
from ..twitchCommunitySubGift import TwitchCommunitySubGift
from ..twitchOutcome import TwitchOutcome
from ..twitchPollChoice import TwitchPollChoice
from ..twitchPollStatus import TwitchPollStatus
from ..twitchResub import TwitchResub
from ..twitchReward import TwitchReward
from ..twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from ..twitchSubGift import TwitchSubGift
from ..twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TwitchWebsocketEvent:
    isAnonymous: bool | None = None
    isGift: bool | None = None
    endedAt: datetime | None = None
    endsAt: datetime | None = None
    followedAt: datetime | None = None
    lockedAt: datetime | None = None
    locksAt: datetime | None = None
    redeemedAt: datetime | None = None
    startedAt: datetime | None = None
    bits: int | None = None
    cumulativeMonths: int | None = None
    total: int | None = None
    viewers: int | None = None
    broadcasterUserId: str | None = None
    broadcasterUserLogin: str | None = None
    broadcasterUserName: str | None = None
    categoryId: str | None = None
    categoryName: str | None = None
    eventId: str | None = None
    fromBroadcasterUserId: str | None = None
    fromBroadcasterUserLogin: str | None = None
    fromBroadcasterUserName: str | None = None
    message: str | None = None
    rewardId: str | None = None
    text: str | None = None
    title: str | None = None
    toBroadcasterUserId: str | None = None
    toBroadcasterUserLogin: str | None = None
    toBroadcasterUserName: str | None = None
    userId: str | None = None
    userInput: str | None = None
    userLogin: str | None = None
    userName: str | None = None
    winningOutcomeId: str | None = None
    tier: TwitchSubscriberTier | None = None
    channelPointsVoting: TwitchWebsocketChannelPointsVoting | None = None
    choices: list[TwitchPollChoice] | None = None
    pollStatus: TwitchPollStatus | None = None
    resub: TwitchResub | None = None
    rewardRedemptionStatus: TwitchRewardRedemptionStatus | None = None
    communitySubGift: TwitchCommunitySubGift | None = None
    noticeType: TwitchWebsocketNoticeType | None = None
    outcomes: list[TwitchOutcome] | None = None
    reward: TwitchReward | None = None
    subGift: TwitchSubGift | None = None
