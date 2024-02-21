from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.api.twitchCommunitySubGift import TwitchCommunitySubGift
from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.twitchPollChoice import TwitchPollChoice
from CynanBot.twitch.api.twitchPollStatus import TwitchPollStatus
from CynanBot.twitch.api.twitchReward import TwitchReward
from CynanBot.twitch.api.twitchRewardRedemptionStatus import \
    TwitchRewardRedemptionStatus
from CynanBot.twitch.api.twitchSubGift import TwitchSubGift
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.twitchWebsocketChannelPointsVoting import \
    TwitchChannelPointsVoting
from CynanBot.twitch.api.websocket.twitchWebsocketNoticeType import \
    TwitchWebsocketNoticeType


class TwitchWebsocketEvent():

    def __init__(
        self,
        isAnonymous: Optional[bool] = None,
        isGift: Optional[bool] = None,
        bits: Optional[int] = None,
        cumulativeMonths: Optional[int] = None,
        total: Optional[int] = None,
        viewers: Optional[int] = None,
        endedAt: Optional[SimpleDateTime] = None,
        endsAt: Optional[SimpleDateTime] = None,
        followedAt: Optional[SimpleDateTime] = None,
        lockedAt: Optional[SimpleDateTime] = None,
        locksAt: Optional[SimpleDateTime] = None,
        redeemedAt: Optional[SimpleDateTime] = None,
        startedAt: Optional[SimpleDateTime] = None,
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
        channelPointsVoting: Optional[TwitchChannelPointsVoting] = None,
        choices: Optional[List[TwitchPollChoice]] = None,
        pollStatus: Optional[TwitchPollStatus] = None,
        rewardRedemptionStatus: Optional[TwitchRewardRedemptionStatus] = None,
        communitySubGift: Optional[TwitchCommunitySubGift] = None,
        noticeType: Optional[TwitchWebsocketNoticeType] = None,
        outcomes: Optional[List[TwitchOutcome]] = None,
        reward: Optional[TwitchReward] = None,
        subGift: Optional[TwitchSubGift] = None
    ):
        if isAnonymous is not None and not utils.isValidBool(isAnonymous):
            raise ValueError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        if isGift is not None and not utils.isValidBool(isGift):
            raise ValueError(f'isGift argument is malformed: \"{isGift}\'')
        if bits is not None and not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        if cumulativeMonths is not None and not utils.isValidInt(cumulativeMonths):
            raise ValueError(f'cumulativeMonths argument is malformed: \"{cumulativeMonths}\"')
        if total is not None and not utils.isValidInt(total):
            raise ValueError(f'total argument is malformed: \"{total}\"')
        if viewers is not None and not utils.isValidInt(viewers):
            raise ValueError(f'viewers argument is malformed: \"{viewers}\"')
        assert endedAt is None or isinstance(endedAt, SimpleDateTime), f"malformed {endedAt=}"
        assert endsAt is None or isinstance(endsAt, SimpleDateTime), f"malformed {endsAt=}"
        assert followedAt is None or isinstance(followedAt, SimpleDateTime), f"malformed {followedAt=}"
        assert lockedAt is None or isinstance(lockedAt, SimpleDateTime), f"malformed {lockedAt=}"
        assert locksAt is None or isinstance(locksAt, SimpleDateTime), f"malformed {locksAt=}"
        assert redeemedAt is None or isinstance(redeemedAt, SimpleDateTime), f"malformed {redeemedAt=}"
        assert startedAt is None or isinstance(startedAt, SimpleDateTime), f"malformed {startedAt=}"
        if broadcasterUserId is not None and not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        if broadcasterUserLogin is not None and not utils.isValidStr(broadcasterUserLogin):
            raise ValueError(f'broadcasterUserLogin argument is malformed: \"{broadcasterUserLogin}\"')
        if broadcasterUserName is not None and not utils.isValidStr(broadcasterUserName):
            raise ValueError(f'broadcasterUserName argument is malformed: \"{broadcasterUserName}\"')
        if categoryId is not None and not utils.isValidStr(categoryId):
            raise ValueError(f'categoryId argument is malformed: \"{categoryId}\"')
        if categoryName is not None and not utils.isValidStr(categoryName):
            raise ValueError(f'categoryName argument is malformed: \"{categoryName}\"')
        if eventId is not None and not utils.isValidStr(eventId):
            raise ValueError(f'eventId argument is malformed: \"{eventId}\"')
        if fromBroadcasterUserId is not None and not utils.isValidStr(fromBroadcasterUserId):
            raise ValueError(f'fromBroadcasterUserId argument is malformed: \"{fromBroadcasterUserId}\"')
        if fromBroadcasterUserLogin is not None and not utils.isValidStr(fromBroadcasterUserLogin):
            raise ValueError(f'fromBroadcasterUserLogin argument is malformed: \"{fromBroadcasterUserLogin}\"')
        if fromBroadcasterUserName is not None and not utils.isValidStr(fromBroadcasterUserName):
            raise ValueError(f'fromBroadcasterUserName argument is malformed: \"{fromBroadcasterUserName}\"')
        if message is not None and not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        if rewardId is not None and not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        if text is not None and not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')
        if title is not None and not utils.isValidStr(title):
            raise ValueError(f'title argument is malformed: \"{title}\"')
        if toBroadcasterUserId is not None and not utils.isValidStr(toBroadcasterUserId):
            raise ValueError(f'toBroadcasterUserId argument is malformed: \"{toBroadcasterUserId}\"')
        if toBroadcasterUserLogin is not None and not utils.isValidStr(toBroadcasterUserLogin):
            raise ValueError(f'toBroadcasterUserLogin argument is malformed: \"{toBroadcasterUserLogin}\"')
        if toBroadcasterUserName is not None and not utils.isValidStr(toBroadcasterUserName):
            raise ValueError(f'toBroadcasterUserName argument is malformed: \"{toBroadcasterUserName}\"')
        if userId is not None and not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if userInput is not None and not utils.isValidStr(userInput):
            raise ValueError(f'userInput argument is malformed: \"{userInput}\"')
        if userLogin is not None and not utils.isValidStr(userLogin):
            raise ValueError(f'userLogin argument is malformed: \"{userLogin}\"')
        if userName is not None and not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        if winningOutcomeId is not None and not utils.isValidStr(winningOutcomeId):
            raise ValueError(f'winningOutcomeId argument is malformed: \"{winningOutcomeId}\"')
        assert tier is None or isinstance(tier, TwitchSubscriberTier), f"malformed {tier=}"
        assert channelPointsVoting is None or isinstance(channelPointsVoting, TwitchChannelPointsVoting), f"malformed {channelPointsVoting=}"
        assert choices is None or isinstance(choices, List), f"malformed {choices=}"
        assert pollStatus is None or isinstance(pollStatus, TwitchPollStatus), f"malformed {pollStatus=}"
        assert rewardRedemptionStatus is None or isinstance(rewardRedemptionStatus, TwitchRewardRedemptionStatus), f"malformed {rewardRedemptionStatus=}"
        assert communitySubGift is None or isinstance(communitySubGift, TwitchCommunitySubGift), f"malformed {communitySubGift=}"
        assert noticeType is None or isinstance(noticeType, TwitchWebsocketNoticeType), f"malformed {noticeType=}"
        assert outcomes is None or isinstance(outcomes, List), f"malformed {outcomes=}"
        assert reward is None or isinstance(reward, TwitchReward), f"malformed {reward=}"
        assert subGift is None or isinstance(subGift, TwitchSubGift), f"malformed {subGift=}"

        self.__isAnonymous: Optional[bool] = isAnonymous
        self.__isGift: Optional[bool] = isGift
        self.__bits: Optional[int] = bits
        self.__cumulativeMonths: Optional[int] = cumulativeMonths
        self.__total: Optional[int] = total
        self.__viewers: Optional[int] = viewers
        self.__endedAt: Optional[SimpleDateTime] = endedAt
        self.__endsAt: Optional[SimpleDateTime] = endsAt
        self.__followedAt: Optional[SimpleDateTime] = followedAt
        self.__lockedAt: Optional[SimpleDateTime] = lockedAt
        self.__locksAt: Optional[SimpleDateTime] = locksAt
        self.__redeemedAt: Optional[SimpleDateTime] = redeemedAt
        self.__startedAt: Optional[SimpleDateTime] = startedAt
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
        self.__channelPointsVoting: Optional[TwitchChannelPointsVoting] = channelPointsVoting
        self.__choices: Optional[List[TwitchPollChoice]] = choices
        self.__pollStatus: Optional[TwitchPollStatus] = pollStatus
        self.__rewardRedemptionStatus: Optional[TwitchRewardRedemptionStatus] = rewardRedemptionStatus
        self.__communitySubGift: Optional[TwitchCommunitySubGift] = communitySubGift
        self.__noticeType: Optional[TwitchWebsocketNoticeType] = noticeType
        self.__outcomes: Optional[List[TwitchOutcome]] = outcomes
        self.__reward: Optional[TwitchReward] = reward
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

    def getChannelPointsVoting(self) -> Optional[TwitchChannelPointsVoting]:
        return self.__channelPointsVoting

    def getChoices(self) -> Optional[List[TwitchPollChoice]]:
        return self.__choices

    def getCommunitySubGift(self) -> Optional[TwitchCommunitySubGift]:
        return self.__communitySubGift

    def getCumulativeMonths(self) -> Optional[int]:
        return self.__cumulativeMonths

    def getEndedAt(self) -> Optional[SimpleDateTime]:
        return self.__endedAt

    def getEndsAt(self) -> Optional[SimpleDateTime]:
        return self.__endsAt

    def getEventId(self) -> Optional[str]:
        return self.__eventId

    def getFollowedAt(self) -> Optional[SimpleDateTime]:
        return self.__followedAt

    def getFromBroadcasterUserId(self) -> Optional[str]:
        return self.__fromBroadcasterUserId

    def getFromBroadcasterUserLogin(self) -> Optional[str]:
        return self.__fromBroadcasterUserLogin

    def getFromBroadcasterUserName(self) -> Optional[str]:
        return self.__fromBroadcasterUserName

    def getLockedAt(self) -> Optional[SimpleDateTime]:
        return self.__lockedAt

    def getLocksAt(self) -> Optional[SimpleDateTime]:
        return self.__locksAt

    def getMessage(self) -> Optional[str]:
        return self.__message

    def getNoticeType(self) -> Optional[TwitchWebsocketNoticeType]:
        return self.__noticeType

    def getOutcomes(self) -> Optional[List[TwitchOutcome]]:
        return self.__outcomes

    def getPollStatus(self) -> Optional[TwitchPollStatus]:
        return self.__pollStatus

    def getRedeemedAt(self) -> Optional[SimpleDateTime]:
        return self.__redeemedAt

    def getReward(self) -> Optional[TwitchReward]:
        return self.__reward

    def getRewardId(self) -> Optional[str]:
        return self.__rewardId

    def getRewardRedemptionStatus(self) -> Optional[TwitchRewardRedemptionStatus]:
        return self.__rewardRedemptionStatus

    def getStartedAt(self) -> Optional[SimpleDateTime]:
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

    def isAnonymous(self) -> Optional[bool]:
        return self.__isAnonymous

    def isGift(self) -> Optional[bool]:
        return self.__isGift

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
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
