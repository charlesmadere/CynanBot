from datetime import datetime
from typing import Any, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchCommunitySubGift import TwitchCommunitySubGift
from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.twitchPollChoice import TwitchPollChoice
from CynanBot.twitch.api.twitchPollStatus import TwitchPollStatus
from CynanBot.twitch.api.twitchReward import TwitchReward
from CynanBot.twitch.api.twitchRewardRedemptionStatus import \
    TwitchRewardRedemptionStatus
from CynanBot.twitch.api.twitchSubGift import TwitchSubGift
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.websocket.twitchWebsocketChannelPointsVoting import \
    TwitchWebsocketChannelPointsVoting
from CynanBot.twitch.api.websocket.twitchWebsocketNoticeType import \
    TwitchWebsocketNoticeType


class TwitchWebsocketEvent():

    def __init__(
        self,
        isAnonymous: bool | None = None,
        isGift: bool | None = None,
        endedAt: datetime | None = None,
        endsAt: datetime | None = None,
        followedAt: datetime | None = None,
        lockedAt: datetime | None = None,
        locksAt: datetime | None = None,
        redeemedAt: datetime | None = None,
        startedAt: datetime | None = None,
        bits: Optional[int] = None,
        cumulativeMonths: Optional[int] = None,
        total: Optional[int] = None,
        viewers: Optional[int] = None,
        broadcasterUserId: Optional[str] = None,
        broadcasterUserLogin: Optional[str] = None,
        broadcasterUserName: Optional[str] = None,
        categoryId: Optional[str] = None,
        categoryName: Optional[str] = None,
        eventId: Optional[str] = None,
        fromBroadcasterUserId: Optional[str] = None,
        fromBroadcasterUserLogin: Optional[str] = None,
        fromBroadcasterUserName: Optional[str] = None,
        message: Optional[str] = None,
        rewardId: Optional[str] = None,
        text: Optional[str] = None,
        title: Optional[str] = None,
        toBroadcasterUserId: Optional[str] = None,
        toBroadcasterUserLogin: Optional[str] = None,
        toBroadcasterUserName: Optional[str] = None,
        userId: Optional[str] = None,
        userInput: Optional[str] = None,
        userLogin: Optional[str] = None,
        userName: Optional[str] = None,
        winningOutcomeId: Optional[str] = None,
        tier: Optional[TwitchSubscriberTier] = None,
        channelPointsVoting: Optional[TwitchWebsocketChannelPointsVoting] = None,
        choices: Optional[list[TwitchPollChoice]] = None,
        pollStatus: Optional[TwitchPollStatus] = None,
        rewardRedemptionStatus: Optional[TwitchRewardRedemptionStatus] = None,
        communitySubGift: Optional[TwitchCommunitySubGift] = None,
        noticeType: Optional[TwitchWebsocketNoticeType] = None,
        outcomes: Optional[list[TwitchOutcome]] = None,
        reward: TwitchReward | None = None,
        subGift: Optional[TwitchSubGift] = None
    ):
        if isAnonymous is not None and not utils.isValidBool(isAnonymous):
            raise TypeError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        elif isGift is not None and not utils.isValidBool(isGift):
            raise TypeError(f'isGift argument is malformed: \"{isGift}\'')
        elif endedAt is not None and not isinstance(endedAt, datetime):
            raise TypeError(f'endedAt argument is malformed: \"{endedAt}\"')
        elif endsAt is not None and not isinstance(endsAt, datetime):
            raise TypeError(f'endsAt argument is malformed: \"{endsAt}\"')
        elif followedAt is not None and not isinstance(followedAt, datetime):
            raise TypeError(f'followedAt argument is malformed: \"{followedAt}\"')
        elif lockedAt is not None and not isinstance(lockedAt, datetime):
            raise TypeError(f'lockedAt argument is malformed: \"{lockedAt}\"')
        elif locksAt is not None and not isinstance(locksAt, datetime):
            raise TypeError(f'locksAt argument is malformed: \"{locksAt}\"')
        elif redeemedAt is not None and not isinstance(redeemedAt, datetime):
            raise TypeError(f'redeemedAt argument is malformed: \"{redeemedAt}\"')
        elif startedAt is not None and not isinstance(startedAt, datetime):
            raise TypeError(f'startedAt argument is malformed: \"{startedAt}\"')
        elif bits is not None and not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif cumulativeMonths is not None and not utils.isValidInt(cumulativeMonths):
            raise TypeError(f'cumulativeMonths argument is malformed: \"{cumulativeMonths}\"')
        elif total is not None and not utils.isValidInt(total):
            raise TypeError(f'total argument is malformed: \"{total}\"')
        elif viewers is not None and not utils.isValidInt(viewers):
            raise TypeError(f'viewers argument is malformed: \"{viewers}\"')
        elif broadcasterUserId is not None and not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif broadcasterUserLogin is not None and not utils.isValidStr(broadcasterUserLogin):
            raise TypeError(f'broadcasterUserLogin argument is malformed: \"{broadcasterUserLogin}\"')
        elif broadcasterUserName is not None and not utils.isValidStr(broadcasterUserName):
            raise TypeError(f'broadcasterUserName argument is malformed: \"{broadcasterUserName}\"')
        elif categoryId is not None and not utils.isValidStr(categoryId):
            raise TypeError(f'categoryId argument is malformed: \"{categoryId}\"')
        elif categoryName is not None and not utils.isValidStr(categoryName):
            raise TypeError(f'categoryName argument is malformed: \"{categoryName}\"')
        elif eventId is not None and not utils.isValidStr(eventId):
            raise TypeError(f'eventId argument is malformed: \"{eventId}\"')
        elif fromBroadcasterUserId is not None and not utils.isValidStr(fromBroadcasterUserId):
            raise TypeError(f'fromBroadcasterUserId argument is malformed: \"{fromBroadcasterUserId}\"')
        elif fromBroadcasterUserLogin is not None and not utils.isValidStr(fromBroadcasterUserLogin):
            raise TypeError(f'fromBroadcasterUserLogin argument is malformed: \"{fromBroadcasterUserLogin}\"')
        elif fromBroadcasterUserName is not None and not utils.isValidStr(fromBroadcasterUserName):
            raise TypeError(f'fromBroadcasterUserName argument is malformed: \"{fromBroadcasterUserName}\"')
        elif message is not None and not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif rewardId is not None and not utils.isValidStr(rewardId):
            raise TypeError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif text is not None and not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif title is not None and not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif toBroadcasterUserId is not None and not utils.isValidStr(toBroadcasterUserId):
            raise TypeError(f'toBroadcasterUserId argument is malformed: \"{toBroadcasterUserId}\"')
        elif toBroadcasterUserLogin is not None and not utils.isValidStr(toBroadcasterUserLogin):
            raise TypeError(f'toBroadcasterUserLogin argument is malformed: \"{toBroadcasterUserLogin}\"')
        elif toBroadcasterUserName is not None and not utils.isValidStr(toBroadcasterUserName):
            raise TypeError(f'toBroadcasterUserName argument is malformed: \"{toBroadcasterUserName}\"')
        elif userId is not None and not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif userInput is not None and not utils.isValidStr(userInput):
            raise TypeError(f'userInput argument is malformed: \"{userInput}\"')
        elif userLogin is not None and not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif userName is not None and not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif winningOutcomeId is not None and not utils.isValidStr(winningOutcomeId):
            raise TypeError(f'winningOutcomeId argument is malformed: \"{winningOutcomeId}\"')
        elif tier is not None and not isinstance(tier, TwitchSubscriberTier):
            raise TypeError(f'tier argument is malformed: \"{tier}\"')
        elif channelPointsVoting is not None and not isinstance(channelPointsVoting, TwitchWebsocketChannelPointsVoting):
            raise TypeError(f'channelPointsVoting argument is malformed: \"{channelPointsVoting}\"')
        elif choices is not None and not isinstance(choices, list):
            raise TypeError(f'choices argument is malformed: \"{choices}\"')
        elif pollStatus is not None and not isinstance(pollStatus, TwitchPollStatus):
            raise TypeError(f'pollStatus argument is malformed: \"{pollStatus}\"')
        elif rewardRedemptionStatus is not None and not isinstance(rewardRedemptionStatus, TwitchRewardRedemptionStatus):
            raise TypeError(f'rewardRedemptionStatus argument is malformed: \"{rewardRedemptionStatus}\"')
        elif communitySubGift is not None and not isinstance(communitySubGift, TwitchCommunitySubGift):
            raise TypeError(f'communitySubGift argument is malformed: \"{communitySubGift}\"')
        elif noticeType is not None and not isinstance(noticeType, TwitchWebsocketNoticeType):
            raise TypeError(f'noticeType argument is malformed: \"{noticeType}\"')
        elif outcomes is not None and not isinstance(outcomes, list):
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')
        elif reward is not None and not isinstance(reward, TwitchReward):
            raise TypeError(f'reward argument is malformed: \"{reward}\"')
        elif subGift is not None and not isinstance(subGift, TwitchSubGift):
            raise TypeError(f'subGift argument is malformed: \"{subGift}\"')

        self.__isAnonymous: bool | None = isAnonymous
        self.__isGift: bool | None = isGift
        self.__endedAt: datetime | None = endedAt
        self.__endsAt: datetime | None = endsAt
        self.__followedAt: datetime | None = followedAt
        self.__lockedAt: datetime | None = lockedAt
        self.__locksAt: datetime | None = locksAt
        self.__redeemedAt: datetime | None = redeemedAt
        self.__startedAt: datetime | None = startedAt
        self.__bits: Optional[int] = bits
        self.__cumulativeMonths: Optional[int] = cumulativeMonths
        self.__total: Optional[int] = total
        self.__viewers: Optional[int] = viewers
        self.__broadcasterUserId: Optional[str] = broadcasterUserId
        self.__broadcasterUserLogin: Optional[str] = broadcasterUserLogin
        self.__broadcasterUserName: Optional[str] = broadcasterUserName
        self.__categoryId: Optional[str] = categoryId
        self.__categoryName: Optional[str] = categoryName
        self.__eventId: Optional[str] = eventId
        self.__fromBroadcasterUserId: Optional[str] = fromBroadcasterUserId
        self.__fromBroadcasterUserLogin: Optional[str] = fromBroadcasterUserLogin
        self.__fromBroadcasterUserName: Optional[str] = fromBroadcasterUserName
        self.__message: Optional[str] = message
        self.__rewardId: Optional[str] = rewardId
        self.__text: Optional[str] = text
        self.__title: Optional[str] = title
        self.__toBroadcasterUserId: Optional[str] = toBroadcasterUserId
        self.__toBroadcasterUserLogin: Optional[str] = toBroadcasterUserLogin
        self.__toBroadcasterUserName: Optional[str] = toBroadcasterUserName
        self.__userId: Optional[str] = userId
        self.__userInput: Optional[str] = userInput
        self.__userLogin: Optional[str] = userLogin
        self.__userName: Optional[str] = userName
        self.__winningOutcomeId: Optional[str] = winningOutcomeId
        self.__tier: Optional[TwitchSubscriberTier] = tier
        self.__channelPointsVoting: Optional[TwitchWebsocketChannelPointsVoting] = channelPointsVoting
        self.__choices: Optional[list[TwitchPollChoice]] = choices
        self.__pollStatus: Optional[TwitchPollStatus] = pollStatus
        self.__rewardRedemptionStatus: Optional[TwitchRewardRedemptionStatus] = rewardRedemptionStatus
        self.__communitySubGift: Optional[TwitchCommunitySubGift] = communitySubGift
        self.__noticeType: Optional[TwitchWebsocketNoticeType] = noticeType
        self.__outcomes: Optional[list[TwitchOutcome]] = outcomes
        self.__reward: TwitchReward | None = reward
        self.__subGift: Optional[TwitchSubGift] = subGift

    def getBits(self) -> Optional[int]:
        return self.__bits

    def getBroadcasterUserId(self) -> Optional[str]:
        return self.__broadcasterUserId

    def getBroadcasterUserLogin(self) -> Optional[str]:
        return self.__broadcasterUserLogin

    def getBroadcasterUserName(self) -> Optional[str]:
        return self.__broadcasterUserName

    def getCategoryId(self) -> Optional[str]:
        return self.__categoryId

    def getCategoryName(self) -> Optional[str]:
        return self.__categoryName

    def getChannelPointsVoting(self) -> Optional[TwitchWebsocketChannelPointsVoting]:
        return self.__channelPointsVoting

    def getChoices(self) -> Optional[list[TwitchPollChoice]]:
        return self.__choices

    def getCommunitySubGift(self) -> Optional[TwitchCommunitySubGift]:
        return self.__communitySubGift

    def getCumulativeMonths(self) -> Optional[int]:
        return self.__cumulativeMonths

    def getEndedAt(self) -> datetime | None:
        return self.__endedAt

    def getEndsAt(self) -> datetime | None:
        return self.__endsAt

    def getEventId(self) -> Optional[str]:
        return self.__eventId

    def getFollowedAt(self) -> Optional[datetime]:
        return self.__followedAt

    def getFromBroadcasterUserId(self) -> Optional[str]:
        return self.__fromBroadcasterUserId

    def getFromBroadcasterUserLogin(self) -> Optional[str]:
        return self.__fromBroadcasterUserLogin

    def getFromBroadcasterUserName(self) -> Optional[str]:
        return self.__fromBroadcasterUserName

    def getLockedAt(self) -> datetime | None:
        return self.__lockedAt

    def getLocksAt(self) -> datetime | None:
        return self.__locksAt

    def getMessage(self) -> str | None:
        return self.__message

    def getNoticeType(self) -> Optional[TwitchWebsocketNoticeType]:
        return self.__noticeType

    def getOutcomes(self) -> Optional[list[TwitchOutcome]]:
        return self.__outcomes

    def getPollStatus(self) -> Optional[TwitchPollStatus]:
        return self.__pollStatus

    def getRedeemedAt(self) -> datetime | None:
        return self.__redeemedAt

    def getReward(self) -> TwitchReward | None:
        return self.__reward

    def getRewardId(self) -> Optional[str]:
        return self.__rewardId

    def getRewardRedemptionStatus(self) -> Optional[TwitchRewardRedemptionStatus]:
        return self.__rewardRedemptionStatus

    def getStartedAt(self) -> datetime | None:
        return self.__startedAt

    def getSubGift(self) -> Optional[TwitchSubGift]:
        return self.__subGift

    def getText(self) -> Optional[str]:
        return self.__text

    def getTier(self) -> Optional[TwitchSubscriberTier]:
        return self.__tier

    def getTitle(self) -> Optional[str]:
        return self.__title

    def getToBroadcasterUserId(self) -> Optional[str]:
        return self.__toBroadcasterUserId

    def getToBroadcasterUserLogin(self) -> Optional[str]:
        return self.__toBroadcasterUserLogin

    def getToBroadcasterUserName(self) -> Optional[str]:
        return self.__toBroadcasterUserName

    def getTotal(self) -> Optional[int]:
        return self.__total

    def getUserId(self) -> Optional[str]:
        return self.__userId

    def getUserInput(self) -> Optional[str]:
        return self.__userInput

    def getUserLogin(self) -> Optional[str]:
        return self.__userLogin

    def getUserName(self) -> Optional[str]:
        return self.__userName

    def getViewers(self) -> Optional[int]:
        return self.__viewers

    def getWinningOutcomeId(self) -> Optional[str]:
        return self.__winningOutcomeId

    def isAnonymous(self) -> bool | None:
        return self.__isAnonymous

    def isGift(self) -> bool | None:
        return self.__isGift

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'broadcasterUserId': self.__broadcasterUserId,
            'broadcasterUserLogin': self.__broadcasterUserLogin,
            'broadcasterUserName': self.__broadcasterUserName,
            'categoryId': self.__categoryId,
            'categoryName': self.__categoryName,
            'channelPointsVoting': self.__channelPointsVoting,
            'choices': self.__choices,
            'communitySubGift': self.__communitySubGift,
            'cumulativeMonths': self.__cumulativeMonths,
            'endedAt': self.__endedAt,
            'endsAt': self.__endsAt,
            'eventId': self.__eventId,
            'followedAt': self.__followedAt,
            'fromBroadcasterUserId': self.__fromBroadcasterUserId,
            'fromBroadcasterUserLogin': self.__fromBroadcasterUserLogin,
            'fromBroadcasterUserName': self.__fromBroadcasterUserName,
            'lockedAt': self.__lockedAt,
            'locksAt': self.__locksAt,
            'message': self.__message,
            'noticeType': self.__noticeType,
            'outcomes': self.__outcomes,
            'pollStatus': self.__pollStatus,
            'redeemedAt': self.__redeemedAt,
            'reward': self.__reward,
            'rewardId': self.__rewardId,
            'rewardRedemptionStatus': self.__rewardRedemptionStatus,
            'startedAt': self.__startedAt,
            'subGift': self.__subGift,
            'text': self.__text,
            'tier': self.__tier,
            'title': self.__title,
            'toBroadcasterUserId': self.__toBroadcasterUserId,
            'toBroadcasterUserLogin': self.__toBroadcasterUserLogin,
            'toBroadcasterUserName': self.__toBroadcasterUserName,
            'total': self.__total,
            'userId': self.__userId,
            'userInput': self.__userInput,
            'userLogin': self.__userLogin,
            'userName': self.__userName,
            'viewers': self.__viewers,
            'winningOutcomeId': self.__winningOutcomeId,
            'isAnonymous': self.__isAnonymous,
            'isGift': self.__isGift
        }
