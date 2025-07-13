from datetime import datetime
from typing import Any

from frozenlist import FrozenList

from .twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from .twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from ..api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from ..api.models.twitchChatBadge import TwitchChatBadge
from ..api.models.twitchChatMessage import TwitchChatMessage
from ..api.models.twitchChatMessageType import TwitchChatMessageType
from ..api.models.twitchCheerMetadata import TwitchCheerMetadata
from ..api.models.twitchCommunitySubGift import TwitchCommunitySubGift
from ..api.models.twitchContribution import TwitchContribution
from ..api.models.twitchHypeTrainType import TwitchHypeTrainType
from ..api.models.twitchNoticeType import TwitchNoticeType
from ..api.models.twitchOutcome import TwitchOutcome
from ..api.models.twitchOutcomePredictor import TwitchOutcomePredictor
from ..api.models.twitchPollChoice import TwitchPollChoice
from ..api.models.twitchPollStatus import TwitchPollStatus
from ..api.models.twitchPowerUp import TwitchPowerUp
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

    async def parseLoggingLevel(
        self,
        loggingLevel: str | Any | None
    ) -> TwitchWebsocketJsonLoggingLevel:
        if not utils.isValidStr(loggingLevel):
            raise TypeError(f'loggingLevel argument is malformed: \"{loggingLevel}\"')

        loggingLevel = loggingLevel.lower()

        match loggingLevel:
            case 'all': return TwitchWebsocketJsonLoggingLevel.ALL
            case 'limited': return TwitchWebsocketJsonLoggingLevel.LIMITED
            case 'none': return TwitchWebsocketJsonLoggingLevel.NONE
            case _: raise ValueError(f'Unknown TwitchWebsocketJsonLoggingLevel value: \"{loggingLevel}\"')

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
        if 'is_gift' in eventJson and utils.isValidBool(eventJson.get('is_gift')):
            isGift = utils.getBoolFromDict(eventJson, 'is_gift')

        isSharedTrain: bool | None = None
        if 'is_shared_train' in eventJson and utils.isValidBool(eventJson.get('is_shared_train')):
            isSharedTrain = utils.getBoolFromDict(eventJson, 'is_shared_train')

        isSourceOnly: bool | None = None
        if 'is_source_only' in eventJson and utils.isValidBool(eventJson.get('is_source_only')):
            isSourceOnly = utils.getBoolFromDict(eventJson, 'is_source_only')

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

        goal: int | None = None
        if 'goal' in eventJson and utils.isValidInt(eventJson.get('goal')):
            goal = utils.getIntFromDict(eventJson, 'goal')

        level: int | None = None
        if 'level' in eventJson and utils.isValidInt(eventJson.get('level')):
            level = utils.getIntFromDict(eventJson, 'level')

        progress: int | None = None
        if 'progress' in eventJson and utils.isValidInt(eventJson.get('progress')):
            progress = utils.getIntFromDict(eventJson, 'progress')

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

        expiresAt: datetime | None = None
        if 'expires_at' in eventJson and utils.isValidStr(eventJson.get('expires_at')):
            expiresAt = utils.getDateTimeFromDict(eventJson, 'expires_at')

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

        frozenBadges: FrozenList[TwitchChatBadge] | None = None
        if 'badges' in eventJson:
            badgesItem: Any | None = eventJson.get('badges')

            if isinstance(badgesItem, list) and len(badgesItem) >= 1:
                badges: list[TwitchChatBadge] = list()

                for badgeItem in badgesItem:
                    badge = await self.__twitchJsonMapper.parseChatBadge(badgeItem)

                    if badge is not None:
                        badges.append(badge)

                if len(badges) >= 1:
                    badges.sort(key = lambda badge: badge.badgeId)
                    frozenBadges = FrozenList(badges)
                    frozenBadges.freeze()

        frozenTopContributions: FrozenList[TwitchContribution] | None = None
        if 'top_contributions' in eventJson:
            topContributionsItem: Any | None = eventJson.get('top_contributions')

            if isinstance(topContributionsItem, list) and len(topContributionsItem) >= 1:
                topContributions: list[TwitchContribution] = list()

                for topContributionItem in topContributionsItem:
                    topContribution = await self.__twitchJsonMapper.parseContribution(topContributionItem)

                    if topContribution is not None:
                        topContributions.append(topContribution)

                if len(topContributions) >= 1:
                    topContributions.sort(key = lambda topContribution: topContribution.userName.casefold())
                    frozenTopContributions = FrozenList(topContributions)
                    frozenTopContributions.freeze()

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
                    choice = await self.__twitchJsonMapper.parsePollChoice(choiceItem)

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

        channelPointsCustomRewardId: str | None = None
        if 'channel_points_custom_reward_id' in eventJson and utils.isValidStr(eventJson.get('channel_points_custom_reward_id')):
            channelPointsCustomRewardId = utils.getStrFromDict(eventJson, 'channel_points_custom_reward_id')

        chatterUserId: str | None = None
        if 'chatter_user_id' in eventJson and utils.isValidStr(eventJson.get('chatter_user_id')):
            chatterUserId = utils.getStrFromDict(eventJson, 'chatter_user_id')

        chatterUserLogin: str | None = None
        if 'chatter_user_login' in eventJson and utils.isValidStr(eventJson.get('chatter_user_login')):
            chatterUserLogin = utils.getStrFromDict(eventJson, 'chatter_user_login')

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

        sourceBroadcasterUserId: str | None = None
        if 'source_broadcaster_user_id' in eventJson and utils.isValidStr(eventJson.get('source_broadcaster_user_id')):
            sourceBroadcasterUserId = utils.getStrFromDict(eventJson, 'source_broadcaster_user_id')

        sourceBroadcasterUserLogin: str | None = None
        if 'source_broadcaster_user_login' in eventJson and utils.isValidStr(eventJson.get('source_broadcaster_user_login')):
            sourceBroadcasterUserLogin = utils.getStrFromDict(eventJson, 'source_broadcaster_user_login')

        sourceBroadcasterUserName: str | None = None
        if 'source_broadcaster_user_name' in eventJson and utils.isValidStr(eventJson.get('source_broadcaster_user_name')):
            sourceBroadcasterUserName = utils.getStrFromDict(eventJson, 'source_broadcaster_user_name')

        sourceMessageId: str | None = None
        if 'source_message_id' in eventJson and utils.isValidStr(eventJson.get('source_message_id')):
            sourceMessageId = utils.getStrFromDict(eventJson, 'source_message_id')

        systemMessage: str | None = None
        if 'system_message' in eventJson and utils.isValidStr(eventJson.get('system_message')):
            systemMessage = utils.getStrFromDict(eventJson, 'system_message')

        text: str | None = None
        if 'text' in eventJson and utils.isValidStr(eventJson.get('text')):
            text = utils.getStrFromDict(eventJson, 'text', clean = True)

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

        chatMessage: TwitchChatMessage | None = None
        if 'message' in eventJson:
            chatMessage = await self.__twitchJsonMapper.parseChatMessage(eventJson.get('message'))

        chatMessageType: TwitchChatMessageType | None = None
        if 'message_type' in eventJson:
            chatMessageType = await self.__twitchJsonMapper.parseChatMessageType(eventJson.get('message_type'))

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
            communitySubGift = await self.__twitchJsonMapper.parseCommunitySubGift(eventJson.get('community_sub_gift'))

        hypeTrainType: TwitchHypeTrainType | None = None
        if 'type' in eventJson and utils.isValidStr(eventJson.get('type')):
            typeString = utils.getStrFromDict(eventJson, 'type')
            hypeTrainType = await self.__twitchJsonMapper.parseHypeTrainType(typeString)

        pollStatus: TwitchPollStatus | None = None
        predictionStatus: TwitchPredictionStatus | None = None
        rewardRedemptionStatus: TwitchRewardRedemptionStatus | None = None
        if 'status' in eventJson and utils.isValidStr(eventJson.get('status')):
            statusString = utils.getStrFromDict(eventJson, 'status')
            pollStatus = await self.__twitchJsonMapper.parsePollStatus(statusString)
            predictionStatus = await self.__twitchJsonMapper.parsePredictionStatus(statusString)
            rewardRedemptionStatus = await self.__twitchJsonMapper.parseRewardRedemptionStatus(statusString)

        raid: TwitchRaid | None = None
        if 'raid' in eventJson:
            raid = await self.__twitchJsonMapper.parseRaid(eventJson.get('raid'))

        noticeType: TwitchNoticeType | None = None
        if 'notice_type' in eventJson and utils.isValidStr(eventJson.get('notice_type')):
            noticeType = await self.__twitchJsonMapper.parseNoticeType(utils.getStrFromDict(eventJson, 'notice_type'))

        powerUp: TwitchPowerUp | None = None
        if 'power_up' in eventJson:
            powerUp = await self.__twitchJsonMapper.parsePowerUp(eventJson.get('power_up'))

        resub: TwitchResub | None = None
        if 'resub' in eventJson:
            resub = await self.__twitchJsonMapper.parseResub(eventJson.get('resub'))

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
            isSharedTrain = isSharedTrain,
            isSourceOnly = isSourceOnly,
            endedAt = endedAt,
            endsAt = endsAt,
            expiresAt = expiresAt,
            followedAt = followedAt,
            lockedAt = lockedAt,
            locksAt = locksAt,
            redeemedAt = redeemedAt,
            startedAt = startedAt,
            badges = frozenBadges,
            topContributions = frozenTopContributions,
            outcomes = frozenOutcomes,
            choices = frozenChoices,
            bits = bits,
            cumulativeMonths = cumulativeMonths,
            cumulativeTotal = cumulativeTotal,
            durationMonths = durationMonths,
            goal = goal,
            level = level,
            progress = progress,
            streakMonths = streakMonths,
            total = total,
            viewers = viewers,
            broadcasterUserId = broadcasterUserId,
            broadcasterUserLogin = broadcasterUserLogin,
            broadcasterUserName = broadcasterUserName,
            categoryId = categoryId,
            categoryName = categoryName,
            channelPointsCustomRewardId = channelPointsCustomRewardId,
            chatterUserId = chatterUserId,
            chatterUserLogin = chatterUserLogin,
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
            sourceBroadcasterUserId = sourceBroadcasterUserId,
            sourceBroadcasterUserLogin = sourceBroadcasterUserLogin,
            sourceBroadcasterUserName = sourceBroadcasterUserName,
            sourceMessageId = sourceMessageId,
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
            chatMessage = chatMessage,
            chatMessageType = chatMessageType,
            cheer = cheer,
            hypeTrainType = hypeTrainType,
            tier = tier,
            channelPointsVoting = channelPointsVoting,
            communitySubGift = communitySubGift,
            pollStatus = pollStatus,
            predictionStatus = predictionStatus,
            raid = raid,
            resub = resub,
            rewardRedemptionStatus = rewardRedemptionStatus,
            noticeType = noticeType,
            powerUp = powerUp,
            reward = reward,
            subGift = subGift,
            sub = sub,
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
                    topPredictor = await self.__twitchJsonMapper.parseOutcomePredictor(topPredictorItem)

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

    async def serializeLoggingLevel(
        self,
        loggingLevel: TwitchWebsocketJsonLoggingLevel
    ) -> str:
        if not isinstance(loggingLevel, TwitchWebsocketJsonLoggingLevel):
            raise TypeError(f'loggingLevel argument is malformed: \"{loggingLevel}\"')

        match loggingLevel:
            case TwitchWebsocketJsonLoggingLevel.ALL: return 'all'
            case TwitchWebsocketJsonLoggingLevel.LIMITED: return 'limited'
            case TwitchWebsocketJsonLoggingLevel.NONE: return 'none'
            case _: raise ValueError(f'Unknown TwitchWebsocketJsonLoggingLevel value: \"{loggingLevel}\"')
