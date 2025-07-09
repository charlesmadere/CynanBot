from dataclasses import dataclass
from datetime import datetime

from frozenlist import FrozenList

from .twitchChatBadge import TwitchChatBadge
from .twitchChatMessage import TwitchChatMessage
from .twitchChatMessageType import TwitchChatMessageType
from .twitchCheerMetadata import TwitchCheerMetadata
from .twitchCommunitySubGift import TwitchCommunitySubGift
from .twitchNoticeType import TwitchNoticeType
from .twitchOutcome import TwitchOutcome
from .twitchPollChoice import TwitchPollChoice
from .twitchPollStatus import TwitchPollStatus
from .twitchPowerUp import TwitchPowerUp
from .twitchPredictionStatus import TwitchPredictionStatus
from .twitchRaid import TwitchRaid
from .twitchResub import TwitchResub
from .twitchReward import TwitchReward
from .twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from .twitchSubGift import TwitchSubGift
from .twitchSubscriberTier import TwitchSubscriberTier
from .twitchWebsocketChannelPointsVoting import TwitchWebsocketChannelPointsVoting
from .twitchWebsocketSub import TwitchWebsocketSub


@dataclass(frozen = True)
class TwitchWebsocketEvent:
    isAnonymous: bool | None = None
    isChatterAnonymous: bool | None = None
    isGift: bool | None = None
    isGoldenKappaTrain: bool | None = None
    isSourceOnly: bool | None = None
    endedAt: datetime | None = None
    endsAt: datetime | None = None
    followedAt: datetime | None = None
    lockedAt: datetime | None = None
    locksAt: datetime | None = None
    redeemedAt: datetime | None = None
    startedAt: datetime | None = None
    badges: FrozenList[TwitchChatBadge] | None = None
    outcomes: FrozenList[TwitchOutcome] | None = None
    choices: FrozenList[TwitchPollChoice] | None = None
    bits: int | None = None
    cumulativeMonths: int | None = None
    cumulativeTotal: int | None = None
    durationMonths: int | None = None
    level: int | None = None
    streakMonths: int | None = None
    total: int | None = None
    viewers: int | None = None
    broadcasterUserId: str | None = None
    broadcasterUserLogin: str | None = None
    broadcasterUserName: str | None = None
    categoryId: str | None = None
    categoryName: str | None = None
    channelPointsCustomRewardId: str | None = None
    chatterUserId: str | None = None
    chatterUserLogin: str | None = None
    chatterUserName: str | None = None
    clientId: str | None = None
    color: str | None = None
    eventId: str | None = None
    fromBroadcasterUserId: str | None = None
    fromBroadcasterUserLogin: str | None = None
    fromBroadcasterUserName: str | None = None
    message: str | None = None
    messageId: str | None = None
    rewardId: str | None = None
    sourceBroadcasterUserId: str | None = None
    sourceBroadcasterUserLogin: str | None = None
    sourceBroadcasterUserName: str | None = None
    sourceMessageId: str | None = None
    systemMessage: str | None = None
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
    chatMessage: TwitchChatMessage | None = None
    chatMessageType: TwitchChatMessageType | None = None
    cheer: TwitchCheerMetadata | None = None
    tier: TwitchSubscriberTier | None = None
    channelPointsVoting: TwitchWebsocketChannelPointsVoting | None = None
    communitySubGift: TwitchCommunitySubGift | None = None
    pollStatus: TwitchPollStatus | None = None
    predictionStatus: TwitchPredictionStatus | None = None
    raid: TwitchRaid | None = None
    resub: TwitchResub | None = None
    rewardRedemptionStatus: TwitchRewardRedemptionStatus | None = None
    noticeType: TwitchNoticeType | None = None
    powerUp: TwitchPowerUp | None = None
    reward: TwitchReward | None = None
    subGift: TwitchSubGift | None = None
    sub: TwitchWebsocketSub | None = None
