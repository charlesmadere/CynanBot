from datetime import datetime
from typing import Any

from frozenlist import FrozenList

from .twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from ..api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from ..api.models.twitchCheerMetadata import TwitchCheerMetadata
from ..api.models.twitchCommunitySubGift import TwitchCommunitySubGift
from ..api.models.twitchNoticeType import TwitchNoticeType
from ..api.models.twitchOutcome import TwitchOutcome
from ..api.models.twitchOutcomePredictor import TwitchOutcomePredictor
from ..api.models.twitchPollChoice import TwitchPollChoice
from ..api.models.twitchPollStatus import TwitchPollStatus
from ..api.models.twitchPredictionStatus import TwitchPredictionStatus
from ..api.models.twitchRaid import TwitchRaid
from ..api.models.twitchResub import TwitchResub
from ..api.models.twitchReward import TwitchReward
from ..api.models.twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from ..api.models.twitchSubGift import TwitchSubGift
from ..api.models.twitchSubscriberTier import TwitchSubscriberTier
from ..api.models.twitchWebsocketChannelPointsVoting import TwitchWebsocketChannelPointsVoting
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketEvent import TwitchWebsocketEvent
from ..api.models.twitchWebsocketPayload import TwitchWebsocketPayload
from ..api.models.twitchWebsocketSession import TwitchWebsocketSession
from ..api.models.twitchWebsocketSub import TwitchWebsocketSub
from ..api.models.twitchWebsocketSubscription import TwitchWebsocketSubscription
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TwitchWebsocketJsonMapper(TwitchWebsocketJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchJsonMapper: TwitchJsonMapperInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchJsonMapper, TwitchJsonMapperInterface):
            raise TypeError(f'twitchJsonMapper argument is malformed: \"{twitchJsonMapper}\"')

        self.__timber: TimberInterface = timber
        self.__twitchJsonMapper: TwitchJsonMapperInterface = twitchJsonMapper

    async def parseWebsocketPollChoice(
        self,
        choiceJson: dict[str, Any] | None
    ) -> TwitchPollChoice | None:
        if not isinstance(choiceJson, dict) or len(choiceJson) == 0:
            return None

        channelPointsVotes = utils.getIntFromDict(choiceJson, 'channel_points_votes', 0)
        votes = utils.getIntFromDict(choiceJson, 'votes', 0)
        choiceId = utils.getStrFromDict(choiceJson, 'id')
        title = utils.getStrFromDict(choiceJson, 'title')

        return TwitchPollChoice(
            channelPointsVotes = channelPointsVotes,
            votes = votes,
            choiceId = choiceId,
            title = title
        )

    async def parseWebsocketCommunitySubGift(
        self,
        giftJson: dict[str, Any] | Any | None
    ) -> TwitchCommunitySubGift | None:
        if not isinstance(giftJson, dict) or len(giftJson) == 0:
            return None

        cumulativeTotal: int | None = None
        if 'cumulative_total' in giftJson and utils.isValidInt(giftJson.get('cumulative_total')):
            cumulativeTotal = utils.getIntFromDict(giftJson, 'cumulative_total')

        total = utils.getIntFromDict(giftJson, 'total')
        communitySubGiftId = utils.getStrFromDict(giftJson, 'id')
        subTier = await self.__twitchJsonMapper.requireSubscriberTier(utils.getStrFromDict(giftJson, 'sub_tier'))

        return TwitchCommunitySubGift(
            cumulativeTotal = cumulativeTotal,
            total = total,
            communitySubGiftId = communitySubGiftId,
            subTier = subTier
        )

    async def __parsePayload(
        self,
        payloadJson: dict[str, Any] | None
    ) -> TwitchWebsocketPayload | None:
        if not isinstance(payloadJson, dict) or len(payloadJson) == 0:
            return None

        event = await self.parseWebsocketEvent(payloadJson.get('event'))
        session = await self.parseTwitchWebsocketSession(payloadJson.get('session'))
        subscription = await self.parseWebsocketSubscription(payloadJson.get('subscription'))

        return TwitchWebsocketPayload(
            event = event,
            session = session,
            subscription = subscription
        )

    async def parseWebsocketDataBundle(
        self,
        dataBundleJson: dict[str, Any] | None
    ) -> TwitchWebsocketDataBundle | None:
        if not isinstance(dataBundleJson, dict) or len(dataBundleJson) == 0:
            return None

        metadata = await self.__twitchJsonMapper.parseWebsocketMetadata(dataBundleJson.get('metadata'))

        if metadata is None:
            self.__timber.log('TwitchWebsocketJsonMapper', f'Websocket message ({dataBundleJson}) is missing \"metadata\" ({metadata}) field')
            return None

        payload = await self.__parsePayload(dataBundleJson.get('payload'))

        return TwitchWebsocketDataBundle(
            metadata = metadata,
            payload = payload
        )

    async def parseWebsocketEvent(
        self,
        eventJson: dict[str, Any] | None
    ) -> TwitchWebsocketEvent | None:
        if not isinstance(eventJson, dict) or len(eventJson) == 0:
            return None

        isAnonymous: bool | None = None
        if 'is_anonymous' in eventJson and utils.isValidBool(eventJson.get('is_anonymous')):
            isAnonymous = utils.getBoolFromDict(eventJson, 'is_anonymous')

        isChatterAnonymous: bool | None = None
        if 'chatter_is_anonymous' in eventJson and utils.isValidBool(eventJson.get('chatter_is_anonymous')):
            isChatterAnonymous = utils.getBoolFromDict(eventJson, 'chatter_is_anonymous')

        isGift: bool | None = None
        if 'is_gift' in eventJson and eventJson.get('is_gift') is not None:
            isGift = utils.getBoolFromDict(eventJson, 'is_gift')

        followedAt: datetime | None = None
        if 'followed_at' in eventJson and utils.isValidStr(eventJson.get('followed_at')):
            followedAt = utils.getDateTimeFromDict(eventJson, 'followed_at')

        bits: int | None = None
        if 'bits' in eventJson and utils.isValidInt(eventJson.get('bits')):
            bits = utils.getIntFromDict(eventJson, 'bits')

        cumulativeMonths: int | None = None
        if 'cumulative_months' in eventJson and utils.isValidInt(eventJson.get('cumulative_months')):
            cumulativeMonths = utils.getIntFromDict(eventJson, 'cumulative_months')

        cumulativeTotal: int | None = None
        if 'cumulative_total' in eventJson and utils.isValidInt(eventJson.get('cumulative_total')):
            cumulativeTotal = utils.getIntFromDict(eventJson, 'cumulative_total')

        durationMonths: int | None = None
        if 'duration_months' in eventJson and utils.isValidInt(eventJson.get('duration_months')):
            durationMonths = utils.getIntFromDict(eventJson, 'duration_months')

        streakMonths: int | None = None
        if 'streak_months' in eventJson and utils.isValidInt(eventJson.get('streak_months')):
            streakMonths = utils.getIntFromDict(eventJson, 'streak_months')

        total: int | None = None
        if 'total' in eventJson and utils.isValidInt(eventJson.get('total')):
            total = utils.getIntFromDict(eventJson, 'total')

        viewers: int | None = None
        if 'viewers' in eventJson and utils.isValidInt(eventJson.get('viewers')):
            viewers = utils.getIntFromDict(eventJson, 'viewers')

        endedAt: datetime | None = None
        if 'ended_at' in eventJson and utils.isValidStr(eventJson.get('ended_at')):
            endedAt = utils.getDateTimeFromDict(eventJson, 'ended_at')

        endsAt: datetime | None = None
        if 'ends_at' in eventJson and utils.isValidStr(eventJson.get('ends_at')):
            endsAt = utils.getDateTimeFromDict(eventJson, 'ends_at')

        lockedAt: datetime | None = None
        if 'locked_at' in eventJson and utils.isValidStr(eventJson.get('locked_at')):
            lockedAt = utils.getDateTimeFromDict(eventJson, 'locked_at')

        locksAt: datetime | None = None
        if 'locks_at' in eventJson and utils.isValidStr(eventJson.get('locks_at')):
            locksAt = utils.getDateTimeFromDict(eventJson, 'locks_at')

        redeemedAt: datetime | None = None
        if 'redeemed_at' in eventJson and utils.isValidStr(eventJson.get('redeemed_at')):
            redeemedAt = utils.getDateTimeFromDict(eventJson, 'redeemed_at')

        startedAt: datetime | None = None
        if 'started_at' in eventJson and utils.isValidStr(eventJson.get('started_at')):
            startedAt = utils.getDateTimeFromDict(eventJson, 'started_at')

        frozenOutcomes: FrozenList[TwitchOutcome] | None = None
        if 'outcomes' in eventJson:
            outcomesItem: Any | None = eventJson.get('outcomes')

            if isinstance(outcomesItem, list) and len(outcomesItem) >= 1:
                outcomes: list[TwitchOutcome] = list()

                for outcomeItem in outcomesItem:
                    outcome = await self.parseTwitchOutcome(outcomeItem)

                    if outcome is not None:
                        outcomes.append(outcome)

                if len(outcomes) >= 1:
                    outcomes.sort(key = lambda outcome: outcome.outcomeId)
                    frozenOutcomes = FrozenList(outcomes)
                    frozenOutcomes.freeze()

        frozenChoices: FrozenList[TwitchPollChoice] | None = None
        if 'choices' in eventJson:
            choicesItem: Any | None = eventJson.get('choices')

            if isinstance(choicesItem, list) and len(choicesItem) >= 1:
                choices: list[TwitchPollChoice] = list()

                for choiceItem in choicesItem:
                    choice = await self.parseWebsocketPollChoice(choiceItem)

                    if choice is not None:
                        choices.append(choice)

                if len(choices) >= 1:
                    choices.sort(key = lambda choice: choice.choiceId)
                    frozenChoices = FrozenList(choices)
                    frozenChoices.freeze()

        broadcasterUserId: str | None = None
        if 'broadcaster_user_id' in eventJson and utils.isValidStr(eventJson.get('broadcaster_user_id')):
            broadcasterUserId = utils.getStrFromDict(eventJson, 'broadcaster_user_id')

        broadcasterUserLogin: str | None = None
        if 'broadcaster_user_login' in eventJson and utils.isValidStr(eventJson.get('broadcaster_user_login')):
            broadcasterUserLogin = utils.getStrFromDict(eventJson, 'broadcaster_user_login')

        broadcasterUserName: str | None = None
        if 'broadcaster_user_name' in eventJson and utils.isValidStr(eventJson.get('broadcaster_user_name')):
            broadcasterUserName = utils.getStrFromDict(eventJson, 'broadcaster_user_name')

        categoryId: str | None = None
        if 'category_id' in eventJson and utils.isValidStr(eventJson.get('category_id')):
            categoryId = utils.getStrFromDict(eventJson, 'category_id')

        categoryName: str | None = None
        if 'category_name' in eventJson and utils.isValidStr(eventJson.get('category_name')):
            categoryName = utils.getStrFromDict(eventJson, 'category_name')

        chatterUserId: str | None = None
        if 'chatter_user_id' in eventJson and utils.isValidStr(eventJson.get('chatter_user_id')):
            chatterUserId = utils.getStrFromDict(eventJson, 'chatter_user_id')

        chatterUserName: str | None = None
        if 'chatter_user_name' in eventJson and utils.isValidStr(eventJson.get('chatter_user_name')):
            chatterUserName = utils.getStrFromDict(eventJson, 'chatter_user_name')

        clientId: str | None = None
        if 'client_id' in eventJson and utils.isValidStr(eventJson.get('client_id')):
            clientId = utils.getStrFromDict(eventJson, 'client_id')

        color: str | None = None
        if 'color' in eventJson and utils.isValidStr(eventJson.get('color')):
            color = utils.getStrFromDict(eventJson, 'color')

        eventId: str | None = None
        if 'id' in eventJson and utils.isValidStr(eventJson.get('id')):
            eventId = utils.getStrFromDict(eventJson, 'id')

        fromBroadcasterUserId: str | None = None
        if 'from_broadcaster_user_id' in eventJson and utils.isValidStr(eventJson.get('from_broadcaster_user_id')):
            fromBroadcasterUserId = utils.getStrFromDict(eventJson, 'from_broadcaster_user_id')

        fromBroadcasterUserLogin: str | None = None
        if 'from_broadcaster_user_login' in eventJson and utils.isValidStr(eventJson.get('from_broadcaster_user_login')):
            fromBroadcasterUserLogin = utils.getStrFromDict(eventJson, 'from_broadcaster_user_login')

        fromBroadcasterUserName: str | None = None
        if 'from_broadcaster_user_name' in eventJson and utils.isValidStr(eventJson.get('from_broadcaster_user_name')):
            fromBroadcasterUserName = utils.getStrFromDict(eventJson, 'from_broadcaster_user_name')

        message: str | None = None
        if 'message' in eventJson:
            messageElement: str | Any | None = eventJson.get('message')

            if utils.isValidStr(messageElement):
                message = utils.getStrFromDict(eventJson, 'message', clean = True)
            elif isinstance(messageElement, dict) and utils.isValidStr(messageElement.get('text')):
                message = utils.getStrFromDict(messageElement, 'text', clean = True)

        messageId: str | None = None
        if 'message_id' in eventJson and utils.isValidStr(eventJson.get('message_id')):
            messageId = utils.getStrFromDict(eventJson, 'message_id')

        rewardId: str | None = None
        if 'reward_id' in eventJson and utils.isValidStr(eventJson.get('reward_id')):
            rewardId = utils.getStrFromDict(eventJson, 'reward_id')

        systemMessage: str | None = None
        if 'system_message' in eventJson and utils.isValidStr(eventJson.get('system_message')):
            systemMessage = utils.getStrFromDict(eventJson, 'system_message')

        text: str | None = None
        if 'text' in eventJson and utils.isValidStr(eventJson.get('text')):
            text = utils.getStrFromDict(eventJson, 'text')

        title: str | None = None
        if 'title' in eventJson and utils.isValidStr(eventJson.get('title')):
            title = utils.getStrFromDict(eventJson, 'title')

        toBroadcasterUserId: str | None = None
        if 'to_broadcaster_user_id' in eventJson and utils.isValidStr(eventJson.get('to_broadcaster_user_id')):
            toBroadcasterUserId = utils.getStrFromDict(eventJson, 'to_broadcaster_user_id')

        toBroadcasterUserLogin: str | None = None
        if 'to_broadcaster_user_login' in eventJson and utils.isValidStr(eventJson.get('to_broadcaster_user_login')):
            toBroadcasterUserLogin = utils.getStrFromDict(eventJson, 'to_broadcaster_user_login')

        toBroadcasterUserName: str | None = None
        if 'to_broadcaster_user_name' in eventJson and utils.isValidStr(eventJson.get('to_broadcaster_user_name')):
            toBroadcasterUserName = utils.getStrFromDict(eventJson, 'to_broadcaster_user_name')

        userId: str | None = None
        if 'user_id' in eventJson and utils.isValidStr(eventJson.get('user_id')):
            userId = utils.getStrFromDict(eventJson, 'user_id')

        userInput: str | None = None
        if 'user_input' in eventJson and utils.isValidStr(eventJson.get('user_input')):
            userInput = utils.getStrFromDict(eventJson, 'user_input')

        userLogin: str | None = None
        if 'user_login' in eventJson and utils.isValidStr(eventJson.get('user_login')):
            userLogin = utils.getStrFromDict(eventJson, 'user_login')

        userName: str | None = None
        if 'user_name' in eventJson and utils.isValidStr(eventJson.get('user_name')):
            userName = utils.getStrFromDict(eventJson, 'user_name')

        winningOutcomeId: str | None = None
        if 'winning_outcome_id' in eventJson and utils.isValidStr(eventJson.get('winning_outcome_id')):
            winningOutcomeId = utils.getStrFromDict(eventJson, 'winning_outcome_id')

        cheer: TwitchCheerMetadata | None = None
        if 'cheer' in eventJson:
            cheer = await self.__twitchJsonMapper.parseCheerMetadata(eventJson.get('cheer'))

        tier: TwitchSubscriberTier | None = None
        if 'tier' in eventJson and utils.isValidStr(eventJson.get('tier')):
            tier = await self.__twitchJsonMapper.parseSubscriberTier(eventJson.get('tier'))

        channelPointsVoting: TwitchWebsocketChannelPointsVoting | None = None
        if 'channel_points_voting' in eventJson:
            channelPointsVoting = await self.__twitchJsonMapper.parseWebsocketChannelPointsVoting(eventJson.get('channel_points_voting'))

        communitySubGift: TwitchCommunitySubGift | None = None
        if 'community_sub_gift' in eventJson:
            communitySubGift = await self.parseWebsocketCommunitySubGift(eventJson.get('community_sub_gift'))

        pollStatus: TwitchPollStatus | None = None
        predictionStatus: TwitchPredictionStatus | None = None
        rewardRedemptionStatus: TwitchRewardRedemptionStatus | None = None
        if 'status' in eventJson and utils.isValidStr(eventJson.get('status')):
            pollStatus = await self.__twitchJsonMapper.parsePollStatus(utils.getStrFromDict(eventJson, 'status'))
            predictionStatus = await self.__twitchJsonMapper.parsePredictionStatus(utils.getStrFromDict(eventJson, 'status'))
            rewardRedemptionStatus = await self.__twitchJsonMapper.parseRewardRedemptionStatus(utils.getStrFromDict(eventJson, 'status'))

        raid: TwitchRaid | None = None
        if 'raid' in eventJson:
            raid = await self.__twitchJsonMapper.parseRaid(eventJson.get('raid'))

        noticeType: TwitchNoticeType | None = None
        if 'notice_type' in eventJson and utils.isValidStr(eventJson.get('notice_type')):
            noticeType = await self.__twitchJsonMapper.parseNoticeType(utils.getStrFromDict(eventJson, 'notice_type'))

        resub: TwitchResub | None = None
        if 'resub' in eventJson:
            resub = await self.parseWebsocketResub(eventJson.get('resub'))

        reward: TwitchReward | None = None
        if 'reward' in eventJson:
            reward = await self.__twitchJsonMapper.parseReward(eventJson.get('reward'))

        subGift: TwitchSubGift | None = None
        if 'sub_gift' in eventJson:
            subGift = await self.parseWebsocketSubGift(eventJson.get('sub_gift'))

        sub: TwitchWebsocketSub | None = None
        if 'sub' in eventJson:
            sub = await self.__twitchJsonMapper.parseWebsocketSub(eventJson.get('sub'))

        return TwitchWebsocketEvent(
            isAnonymous = isAnonymous,
            isChatterAnonymous = isChatterAnonymous,
            isGift = isGift,
            endedAt = endedAt,
            endsAt = endsAt,
            followedAt = followedAt,
            lockedAt = lockedAt,
            locksAt = locksAt,
            redeemedAt = redeemedAt,
            startedAt = startedAt,
            outcomes = frozenOutcomes,
            choices = frozenChoices,
            bits = bits,
            cumulativeMonths = cumulativeMonths,
            cumulativeTotal = cumulativeTotal,
            durationMonths = durationMonths,
            streakMonths = streakMonths,
            total = total,
            viewers = viewers,
            broadcasterUserId = broadcasterUserId,
            broadcasterUserLogin = broadcasterUserLogin,
            broadcasterUserName = broadcasterUserName,
            categoryId = categoryId,
            categoryName = categoryName,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            clientId = clientId,
            color = color,
            eventId = eventId,
            fromBroadcasterUserId = fromBroadcasterUserId,
            fromBroadcasterUserLogin = fromBroadcasterUserLogin,
            fromBroadcasterUserName = fromBroadcasterUserName,
            message = message,
            messageId = messageId,
            rewardId = rewardId,
            systemMessage = systemMessage,
            text = text,
            title = title,
            toBroadcasterUserId = toBroadcasterUserId,
            toBroadcasterUserLogin = toBroadcasterUserLogin,
            toBroadcasterUserName = toBroadcasterUserName,
            userId = userId,
            userInput = userInput,
            userLogin = userLogin,
            userName = userName,
            winningOutcomeId = winningOutcomeId,
            cheer = cheer,
            tier = tier,
            channelPointsVoting = channelPointsVoting,
            communitySubGift = communitySubGift,
            pollStatus = pollStatus,
            predictionStatus = predictionStatus,
            raid = raid,
            resub = resub,
            rewardRedemptionStatus = rewardRedemptionStatus,
            noticeType = noticeType,
            reward = reward,
            subGift = subGift,
            sub = sub
        )

    async def parseTwitchOutcome(
        self,
        outcomeJson: dict[str, Any] | None
    ) -> TwitchOutcome | None:
        if not isinstance(outcomeJson, dict) or len(outcomeJson) == 0:
            return None

        channelPoints = utils.getIntFromDict(outcomeJson, 'channel_points', fallback = 0)
        users = utils.getIntFromDict(outcomeJson, 'users', fallback = 0)
        outcomeId = utils.getStrFromDict(outcomeJson, 'id')
        title = utils.getStrFromDict(outcomeJson, 'title')
        color = await self.__twitchJsonMapper.requireOutcomeColor(utils.getStrFromDict(outcomeJson, 'color'))

        frozenTopPredictors: FrozenList[TwitchOutcomePredictor] | None = None
        if 'top_predictors' in outcomeJson:
            topPredictorsItem: Any | None = outcomeJson.get('top_predictors')

            if isinstance(topPredictorsItem, list) and len(topPredictorsItem) >= 1:
                topPredictors: list[TwitchOutcomePredictor] = list()

                for topPredictorItem in topPredictorsItem:
                    topPredictor = await self.parseTwitchOutcomePredictor(topPredictorItem)

                    if topPredictor is not None:
                        topPredictors.append(topPredictor)

                if len(topPredictors) >= 1:
                    topPredictors.sort(key = lambda element: element.channelPointsUsed, reverse = True)
                    frozenTopPredictors = FrozenList(topPredictors)
                    frozenTopPredictors.freeze()

        return TwitchOutcome(
            topPredictors = frozenTopPredictors,
            channelPoints = channelPoints,
            users = users,
            outcomeId = outcomeId,
            title = title,
            color = color
        )

    async def parseTwitchOutcomePredictor(
        self,
        predictorJson: dict[str, Any] | Any | None
    ) -> TwitchOutcomePredictor | None:
        if not isinstance(predictorJson, dict) or len(predictorJson) == 0:
            return None

        channelPointsUsed = utils.getIntFromDict(predictorJson, 'channel_points_used')

        channelPointsWon: int | None = None
        if 'channel_points_won' in predictorJson and utils.isValidInt(predictorJson.get('channel_points_won')):
            channelPointsWon = utils.getIntFromDict(predictorJson, 'channel_points_won')

        userId = utils.getStrFromDict(predictorJson, 'user_id')
        userLogin = utils.getStrFromDict(predictorJson, 'user_login')
        userName = utils.getStrFromDict(predictorJson, 'user_name')

        return TwitchOutcomePredictor(
            channelPointsUsed = channelPointsUsed,
            channelPointsWon = channelPointsWon,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parseWebsocketResub(
        self,
        resubJson: dict[str, Any] | None
    ) -> TwitchResub | None:
        if not isinstance(resubJson, dict) or len(resubJson) == 0:
            return None

        gifterIsAnonymous: bool | None = None
        if 'gifter_is_anonymous' in resubJson and utils.isValidBool(resubJson.get('gifter_is_anonymous')):
            gifterIsAnonymous = utils.getBoolFromDict(resubJson, 'gifter_is_anonymous')

        isGift = utils.getBoolFromDict(resubJson, 'is_gift', fallback = False)
        isPrime = utils.getBoolFromDict(resubJson, 'is_prime', fallback = False)
        cumulativeMonths = utils.getIntFromDict(resubJson, 'cumulative_months')
        durationMonths = utils.getIntFromDict(resubJson, 'duration_months')
        streakMonths = utils.getIntFromDict(resubJson, 'streak_months')

        gifterUserId: str | None = None
        if 'gifter_user_id' in resubJson and utils.isValidStr(resubJson.get('gifter_user_id')):
            gifterUserId = utils.getStrFromDict(resubJson, 'gifter_user_id')

        gifterUserLogin: str | None = None
        if 'gifter_user_login' in resubJson and utils.isValidStr(resubJson.get('gifter_user_login')):
            gifterUserLogin = utils.getStrFromDict(resubJson, 'gifter_user_login')

        gifterUserName: str | None = None
        if 'gifter_user_name' in resubJson and utils.isValidStr(resubJson.get('gifter_user_name')):
            gifterUserName = utils.getStrFromDict(resubJson, 'gifter_user_name')

        subTier = await self.__twitchJsonMapper.requireSubscriberTier(utils.getStrFromDict(resubJson, 'sub_tier'))

        return TwitchResub(
            gifterIsAnonymous = gifterIsAnonymous,
            isGift = isGift,
            isPrime = isPrime,
            cumulativeMonths = cumulativeMonths,
            durationMonths = durationMonths,
            streakMonths = streakMonths,
            gifterUserId = gifterUserId,
            gifterUserLogin = gifterUserLogin,
            gifterUserName = gifterUserName,
            subTier = subTier
        )

    async def parseTwitchWebsocketSession(
        self,
        sessionJson: dict[str, Any] | None
    ) -> TwitchWebsocketSession | None:
        if not isinstance(sessionJson, dict) or len(sessionJson) == 0:
            return None

        connectedAt = utils.getDateTimeFromDict(sessionJson, 'connected_at')

        keepAliveTimeoutSeconds: int | None = None
        if 'keepalive_timeout_seconds' in sessionJson and utils.isValidInt(sessionJson.get('keepalive_timeout_seconds')):
            keepAliveTimeoutSeconds = utils.getIntFromDict(sessionJson, 'keepalive_timeout_seconds')

        reconnectUrl: str | None = None
        if 'reconnect_url' in sessionJson and utils.isValidUrl(sessionJson.get('reconnect_url')):
            reconnectUrl = utils.getStrFromDict(sessionJson, 'reconnect_url')

        recoveryUrl: str | None = None
        if 'recovery_url' in sessionJson and utils.isValidUrl(sessionJson.get('recovery_url')):
            recoveryUrl = utils.getStrFromDict(sessionJson, 'recovery_url')

        sessionId = utils.getStrFromDict(sessionJson, 'id')
        status = await self.__twitchJsonMapper.requireConnectionStatus(utils.getStrFromDict(sessionJson, 'status'))

        return TwitchWebsocketSession(
            connectedAt = connectedAt,
            keepAliveTimeoutSeconds = keepAliveTimeoutSeconds,
            reconnectUrl = reconnectUrl,
            recoveryUrl = recoveryUrl,
            sessionId = sessionId,
            status = status
        )

    async def parseWebsocketSubGift(
        self,
        giftJson: dict[str, Any] | None
    ) -> TwitchSubGift | None:
        if not isinstance(giftJson, dict) or len(giftJson) == 0:
            return None

        cumulativeTotal: int | None = None
        if 'cumulative_total' in giftJson and utils.isValidInt(giftJson.get('cumulative_total')):
            cumulativeTotal = utils.getIntFromDict(giftJson, 'cumulative_total')

        durationMonths = utils.getIntFromDict(giftJson, 'duration_months')
        communityGiftId = utils.getStrFromDict(giftJson, 'community_gift_id')
        recipientUserId = utils.getStrFromDict(giftJson, 'recipient_user_id')
        recipientUserLogin = utils.getStrFromDict(giftJson, 'recipient_user_login')
        recipientUserName = utils.getStrFromDict(giftJson, 'recipient_user_name')
        subTier = await self.__twitchJsonMapper.requireSubscriberTier(utils.getStrFromDict(giftJson, 'sub_tier'))

        return TwitchSubGift(
            cumulativeTotal = cumulativeTotal,
            durationMonths = durationMonths,
            communityGiftId = communityGiftId,
            recipientUserId = recipientUserId,
            recipientUserLogin = recipientUserLogin,
            recipientUserName = recipientUserName,
            subTier = subTier
        )

    async def parseWebsocketSubscription(
        self,
        subscriptionJson: dict[str, Any] | None
    ) -> TwitchWebsocketSubscription | None:
        if not isinstance(subscriptionJson, dict) or len(subscriptionJson) == 0:
            return None

        cost = utils.getIntFromDict(subscriptionJson, 'cost')
        createdAt = utils.getDateTimeFromDict(subscriptionJson, 'created_at')
        subscriptionId = utils.getStrFromDict(subscriptionJson, 'id')
        version = utils.getStrFromDict(subscriptionJson, 'version')
        condition = await self.__twitchJsonMapper.parseCondition(subscriptionJson.get('condition'))
        status = await self.__twitchJsonMapper.requireConnectionStatus(utils.getStrFromDict(subscriptionJson, 'status'))
        subscriptionType = await self.__twitchJsonMapper.requireSubscriptionType(utils.getStrFromDict(subscriptionJson, 'type'))
        transport = await self.__twitchJsonMapper.requireTransport(subscriptionJson.get('transport'))

        return TwitchWebsocketSubscription(
            cost = cost,
            createdAt = createdAt,
            subscriptionId = subscriptionId,
            version = version,
            condition = condition,
            status = status,
            subscriptionType = subscriptionType,
            transport = transport
        )
