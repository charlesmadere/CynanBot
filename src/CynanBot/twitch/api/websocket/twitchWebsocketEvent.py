from dataclasses import dataclass
from datetime import datetime

from CynanBot.twitch.api.twitchCommunitySubGift import TwitchCommunitySubGift
from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.twitchPollChoice import TwitchPollChoice
from CynanBot.twitch.api.twitchPollStatus import TwitchPollStatus
from CynanBot.twitch.api.twitchResub import TwitchResub
from CynanBot.twitch.api.twitchReward import TwitchReward
from CynanBot.twitch.api.twitchRewardRedemptionStatus import \
    TwitchRewardRedemptionStatus
from CynanBot.twitch.api.twitchSubGift import TwitchSubGift
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.websocket.twitchWebsocketChannelPointsVoting import \
    TwitchWebsocketChannelPointsVoting
from CynanBot.twitch.api.websocket.twitchWebsocketNoticeType import \
    TwitchWebsocketNoticeType


@dataclass(frozen = True)
class TwitchWebsocketEvent():
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
