from datetime import datetime
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchCommunitySubGift import TwitchCommunitySubGift
from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.twitchOutcomeColor import TwitchOutcomeColor
from CynanBot.twitch.api.twitchOutcomePredictor import TwitchOutcomePredictor
from CynanBot.twitch.api.twitchPollChoice import TwitchPollChoice
from CynanBot.twitch.api.twitchPollStatus import TwitchPollStatus
from CynanBot.twitch.api.twitchReward import TwitchReward
from CynanBot.twitch.api.twitchRewardRedemptionStatus import \
    TwitchRewardRedemptionStatus
from CynanBot.twitch.api.twitchSubGift import TwitchSubGift
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.websocket.twitchWebsocketChannelPointsVoting import \
    TwitchWebsocketChannelPointsVoting
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.api.websocket.twitchWebsocketMessageType import \
    TwitchWebsocketMessageType
from CynanBot.twitch.api.websocket.twitchWebsocketMetadata import \
    TwitchWebsocketMetadata
from CynanBot.twitch.api.websocket.twitchWebsocketNoticeType import \
    TwitchWebsocketNoticeType
from CynanBot.twitch.api.websocket.twitchWebsocketPayload import \
    TwitchWebsocketPayload
from CynanBot.twitch.api.websocket.twitchWebsocketSession import \
    TwitchWebsocketSession
from CynanBot.twitch.api.websocket.twitchWebsocketSubscription import \
    TwitchWebsocketSubscription
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport
from CynanBot.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod
from CynanBot.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface


class TwitchWebsocketJsonMapper(TwitchWebsocketJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseWebsocketChannelPointsVoting(
        self,
        channelPointsVotingJson: dict[str, Any] | None
    ) -> TwitchWebsocketChannelPointsVoting | None:
        if not isinstance(channelPointsVotingJson, dict) or len(channelPointsVotingJson) == 0:
            return None

        isEnabled = utils.getBoolFromDict(channelPointsVotingJson, 'is_enabled')
        amountPerVote = utils.getIntFromDict(channelPointsVotingJson, 'amount_per_vote')

        return TwitchWebsocketChannelPointsVoting(
            isEnabled = isEnabled,
            amountPerVote = amountPerVote
        )

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
        giftJson: dict[str, Any] | None
    ) -> TwitchCommunitySubGift | None:
        if not isinstance(giftJson, dict) or len(giftJson) == 0:
            return None

        cumulativeTotal: int | None = None
        if 'cumulative_total' in giftJson and utils.isValidInt(giftJson.get('cumulative_total')):
            cumulativeTotal = utils.getIntFromDict(giftJson, 'cumulative_total')

        total = utils.getIntFromDict(giftJson, 'total', fallback = 0)
        communitySubGiftId = utils.getStrFromDict(giftJson, 'id')
        subTier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(giftJson, 'sub_tier'))

        return TwitchCommunitySubGift(
            cumulativeTotal = cumulativeTotal,
            total = total,
            communitySubGiftId = communitySubGiftId,
            subTier = subTier
        )

    async def parseWebsocketCondition(
        self,
        conditionJson: dict[str, Any] | None
    ) -> TwitchWebsocketCondition | None:
        if not isinstance(conditionJson, dict):
            return None

        broadcasterUserId: str | None = None
        if 'broadcaster_user_id' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_id')):
            broadcasterUserId = utils.getStrFromDict(conditionJson, 'broadcaster_user_id')

        broadcasterUserLogin: str | None = None
        if 'broadcaster_user_login' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_login')):
            broadcasterUserLogin = utils.getStrFromDict(conditionJson, 'broadcaster_user_login')

        broadcasterUserName: str | None = None
        if 'broadcaster_user_name' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_name')):
            broadcasterUserName = utils.getStrFromDict(conditionJson, 'broadcaster_user_name')

        clientId: str | None = None
        if 'client_id' in conditionJson and utils.isValidStr(conditionJson.get('client_id')):
            clientId = utils.getStrFromDict(conditionJson, 'client_id')

        fromBroadcasterUserId: str | None = None
        if 'from_broadcaster_user_id' in conditionJson and utils.isValidStr(conditionJson.get('from_broadcaster_user_id')):
            fromBroadcasterUserId = utils.getStrFromDict(conditionJson, 'from_broadcaster_user_id')

        fromBroadcasterUserLogin: str | None = None
        if 'from_broadcaster_user_login' in conditionJson and utils.isValidStr(conditionJson.get('from_broadcaster_user_login')):
            fromBroadcasterUserLogin = utils.getStrFromDict(conditionJson, 'from_broadcaster_user_login')

        fromBroadcasterUserName: str | None = None
        if 'from_broadcaster_user_name' in conditionJson and utils.isValidStr(conditionJson.get('from_broadcaster_user_name')):
            fromBroadcasterUserName = utils.getStrFromDict(conditionJson, 'from_broadcaster_user_name')

        moderatorUserId: str | None = None
        if 'moderator_user_id' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_id')):
            moderatorUserId = utils.getStrFromDict(conditionJson, 'moderator_user_id')

        moderatorUserLogin: str | None = None
        if 'moderator_user_login' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_login')):
            moderatorUserLogin = utils.getStrFromDict(conditionJson, 'moderator_user_login')

        moderatorUserName: str | None = None
        if 'moderator_user_name' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_name')):
            moderatorUserName = utils.getStrFromDict(conditionJson, 'moderator_user_name')

        rewardId: str | None = None
        if 'reward_id' in conditionJson and utils.isValidStr(conditionJson.get('reward_id')):
            rewardId = utils.getStrFromDict(conditionJson, 'reward_id')

        toBroadcasterUserId: str | None = None
        if 'to_broadcaster_user_id' in conditionJson and utils.isValidStr(conditionJson.get('to_broadcaster_user_id')):
            toBroadcasterUserId = utils.getStrFromDict(conditionJson, 'to_broadcaster_user_id')

        toBroadcasterUserLogin: str | None = None
        if 'to_broadcaster_user_login' in conditionJson and utils.isValidStr(conditionJson.get('to_broadcaster_user_login')):
            toBroadcasterUserLogin = utils.getStrFromDict(conditionJson, 'to_broadcaster_user_login')

        toBroadcasterUserName: str | None = None
        if 'to_broadcaster_user_name' in conditionJson and utils.isValidStr(conditionJson.get('to_broadcaster_user_name')):
            toBroadcasterUserName = utils.getStrFromDict(conditionJson, 'to_broadcaster_user_name')

        userId: str | None = None
        if 'user_id' in conditionJson and utils.isValidStr(conditionJson.get('user_id')):
            userId = utils.getStrFromDict(conditionJson, 'user_id')

        userLogin: str | None = None
        if 'user_login' in conditionJson and utils.isValidStr(conditionJson.get('user_login')):
            userLogin = utils.getStrFromDict(conditionJson, 'user_login')

        userName: str | None = None
        if 'user_name' in conditionJson and utils.isValidStr(conditionJson.get('user_name')):
            userName = utils.getStrFromDict(conditionJson, 'user_name')

        return TwitchWebsocketCondition(
            broadcasterUserId = broadcasterUserId,
            broadcasterUserLogin = broadcasterUserLogin,
            broadcasterUserName = broadcasterUserName,
            clientId = clientId,
            fromBroadcasterUserId = fromBroadcasterUserId,
            fromBroadcasterUserLogin = fromBroadcasterUserLogin,
            fromBroadcasterUserName = fromBroadcasterUserName,
            moderatorUserId = moderatorUserId,
            moderatorUserLogin = moderatorUserLogin,
            moderatorUserName = moderatorUserName,
            rewardId = rewardId,
            toBroadcasterUserId = toBroadcasterUserId,
            toBroadcasterUserLogin = toBroadcasterUserLogin,
            toBroadcasterUserName = toBroadcasterUserName,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def __parseMetadata(
        self,
        metadataJson: dict[str, Any] | None
    ) -> TwitchWebsocketMetadata | None:
        if not isinstance(metadataJson, dict) or len(metadataJson) == 0:
            return None

        messageTimestamp = datetime.fromisoformat(utils.getStrFromDict(metadataJson, 'message_timestamp'))
        messageId = utils.getStrFromDict(metadataJson, 'message_id')
        messageType = TwitchWebsocketMessageType.fromStr(utils.getStrFromDict(metadataJson, 'message_type'))

        subscriptionVersion: str | None = None
        if 'subscription_version' in metadataJson and utils.isValidStr(metadataJson.get('subscription_version')):
            subscriptionVersion = utils.getStrFromDict(metadataJson, 'subscription_version')

        subscriptionType: TwitchWebsocketSubscriptionType | None = None
        if 'subscription_type' in metadataJson and utils.isValidStr(metadataJson.get('subscription_type')):
            subscriptionType = TwitchWebsocketSubscriptionType.fromStr(utils.getStrFromDict(metadataJson, 'subscription_type'))

        return TwitchWebsocketMetadata(
            messageTimestamp = messageTimestamp,
            messageId = messageId,
            subscriptionVersion = subscriptionVersion,
            messageType = messageType,
            subscriptionType = subscriptionType
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

    async def __parseTransport(
        self,
        transportJson: dict[str, Any] | None
    ) -> TwitchWebsocketTransport | None:
        if not isinstance(transportJson, dict) or len(transportJson) == 0:
            return None

        connectedAt: datetime | None = None
        if 'connected_at' in transportJson and utils.isValidStr(transportJson.get('connected_at')):
            connectedAt = datetime.fromisoformat(utils.getStrFromDict(transportJson, 'connected_at'))

        disconnectedAt: datetime | None = None
        if 'disconnected_at' in transportJson and utils.isValidStr(transportJson.get('disconnected_at')):
            disconnectedAt = datetime.fromisoformat(utils.getStrFromDict(transportJson, 'disconnected_at'))

        secret: str | None = None
        if 'secret' in transportJson and utils.isValidStr(transportJson.get('secret')):
            secret = utils.getStrFromDict(transportJson, 'secret')

        sessionId: str | None = None
        if 'session_id' in transportJson and utils.isValidBool(transportJson.get('session_id')):
            sessionId = utils.getStrFromDict(transportJson, 'session_id')

        method = TwitchWebsocketTransportMethod.fromStr(utils.getStrFromDict(transportJson, 'method'))

        return TwitchWebsocketTransport(
            connectedAt = connectedAt,
            disconnectedAt = disconnectedAt,
            secret = secret,
            sessionId = sessionId,
            method = method
        )

    async def parseWebsocketDataBundle(
        self,
        dataBundleJson: dict[str, Any] | None
    ) -> TwitchWebsocketDataBundle | None:
        if not isinstance(dataBundleJson, dict) or len(dataBundleJson) == 0:
            return None

        metadata = await self.__parseMetadata(dataBundleJson.get('metadata'))

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
        if 'is_anonymous' in eventJson and eventJson.get('is_anonymous') is not None:
            isAnonymous = utils.getBoolFromDict(eventJson, 'is_anonymous')

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

        total: int | None = None
        if 'total' in eventJson and utils.isValidInt(eventJson.get('total')):
            total = utils.getIntFromDict(eventJson, 'total')

        viewers: int | None = None
        if 'viewers' in eventJson and utils.isValidInt(eventJson.get('viewers')):
            viewers = utils.getIntFromDict(eventJson, 'viewers')

        endedAt: SimpleDateTime | None = None
        if 'ended_at' in eventJson and utils.isValidStr(eventJson.get('ended_at')):
            endedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'ended_at')))

        endsAt: SimpleDateTime | None = None
        if 'ends_at' in eventJson and utils.isValidStr(eventJson.get('ends_at')):
            endsAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'ends_at')))

        lockedAt: SimpleDateTime | None = None
        if 'locked_at' in eventJson and utils.isValidStr(eventJson.get('locked_at')):
            lockedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'locked_at')))

        locksAt: SimpleDateTime | None = None
        if 'locks_at' in eventJson and utils.isValidStr(eventJson.get('locks_at')):
            locksAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'locks_at')))

        redeemedAt: SimpleDateTime | None = None
        if 'redeemed_at' in eventJson and utils.isValidStr(eventJson.get('redeemed_at')):
            redeemedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'redeemed_at')))

        startedAt: SimpleDateTime | None = None
        if 'started_at' in eventJson and utils.isValidStr(eventJson.get('started_at')):
            startedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'started_at')))

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
            messageItem: Any | None = eventJson.get('message')

            if utils.isValidStr(messageItem):
                message = utils.getStrFromDict(eventJson, 'message', clean = True)
            elif isinstance(messageItem, dict) and utils.isValidStr(messageItem.get('text')):
                message = utils.getStrFromDict(messageItem, 'text', clean = True)

        rewardId: str | None = None
        if 'reward_id' in eventJson and utils.isValidStr(eventJson.get('reward_id')):
            rewardId = utils.getStrFromDict(eventJson, 'reward_id')

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

        tier: TwitchSubscriberTier | None = None
        if 'tier' in eventJson and utils.isValidStr(eventJson.get('tier')):
            tier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(eventJson, 'tier'))

        channelPointsVoting: TwitchWebsocketChannelPointsVoting | None = None
        if 'channel_points_voting' in eventJson:
            channelPointsVoting = await self.parseWebsocketChannelPointsVoting(eventJson.get('channel_points_voting'))

        choices: list[TwitchPollChoice] | None = None
        if 'choices' in eventJson:
            choicesItem: Any = eventJson.get('choices')

            if isinstance(choicesItem, list) and len(choicesItem) >= 1:
                choices = list()

                for choiceItem in choicesItem:
                    choice = await self.parseWebsocketPollChoice(choiceItem)

                    if choice is not None:
                        choices.append(choice)

                if len(choices) == 0:
                    choices = None

        pollStatus: TwitchPollStatus | None = None
        rewardRedemptionStatus: TwitchRewardRedemptionStatus | None = None
        if 'status' in eventJson and utils.isValidStr(eventJson.get('status')):
            pollStatus = TwitchPollStatus.fromStr(utils.getStrFromDict(eventJson, 'status'))
            rewardRedemptionStatus = TwitchRewardRedemptionStatus.fromStr(utils.getStrFromDict(eventJson, 'status'))

        communitySubGift: TwitchCommunitySubGift | None = None
        if 'community_sub_gift' in eventJson:
            communitySubGift = await self.parseWebsocketCommunitySubGift(eventJson.get('community_sub_gift'))

        noticeType: TwitchWebsocketNoticeType | None = None
        if 'notice_type' in eventJson and utils.isValidStr(eventJson.get('notice_type')):
            noticeType = TwitchWebsocketNoticeType.fromStr(utils.getStrFromDict(eventJson, 'notice_type'))

        outcomes: list[TwitchOutcome] | None = None
        if 'outcomes' in eventJson:
            outcomesItem: Any = eventJson.get('outcomes')

            if isinstance(outcomesItem, list) and len(outcomesItem) >= 1:
                outcomes = list()

                for outcomeItem in outcomesItem:
                    outcome = await self.parseTwitchOutcome(outcomeItem)

                    if outcome is not None:
                        outcomes.append(outcome)

                if len(outcomes) == 0:
                    outcomes = None

        reward: TwitchReward | None = None
        if 'reward' in eventJson:
            reward = await self.parseWebsocketReward(eventJson.get('reward'))

        subGift: TwitchSubGift | None = None
        if 'sub_gift' in eventJson:
            subGift = await self.parseWebsocketSubGift(eventJson.get('sub_gift'))

        return TwitchWebsocketEvent(
            isAnonymous = isAnonymous,
            isGift = isGift,
            followedAt = followedAt,
            bits = bits,
            cumulativeMonths = cumulativeMonths,
            total = total,
            viewers = viewers,
            endedAt = endedAt,
            endsAt = endsAt,
            lockedAt = lockedAt,
            locksAt = locksAt,
            redeemedAt = redeemedAt,
            startedAt = startedAt,
            broadcasterUserId = broadcasterUserId,
            broadcasterUserLogin = broadcasterUserLogin,
            broadcasterUserName = broadcasterUserName,
            categoryId = categoryId,
            categoryName = categoryName,
            eventId = eventId,
            fromBroadcasterUserId = fromBroadcasterUserId,
            fromBroadcasterUserLogin = fromBroadcasterUserLogin,
            fromBroadcasterUserName = fromBroadcasterUserName,
            message = message,
            rewardId = rewardId,
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
            channelPointsVoting = channelPointsVoting,
            choices = choices,
            tier = tier,
            pollStatus = pollStatus,
            rewardRedemptionStatus = rewardRedemptionStatus,
            communitySubGift = communitySubGift,
            noticeType = noticeType,
            outcomes = outcomes,
            reward = reward,
            subGift = subGift
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
        color = TwitchOutcomeColor.fromStr(utils.getStrFromDict(outcomeJson, 'color'))

        topPredictors: list[TwitchOutcomePredictor] | None = None
        if 'top_predictors' in outcomeJson:
            topPredictorsItem: Any = outcomeJson.get('top_predictors')

            if isinstance(topPredictorsItem, list) and len(topPredictorsItem) >= 1:
                topPredictors = list()

                for topPredictorItem in topPredictorsItem:
                    topPredictor = await self.parseTwitchOutcomePredictor(topPredictorItem)

                    if topPredictor is not None:
                        topPredictors.append(topPredictor)

                if len(topPredictors) == 0:
                    topPredictors = None

        return TwitchOutcome(
            channelPoints = channelPoints,
            users = users,
            outcomeId = outcomeId,
            title = title,
            color = color,
            topPredictors = topPredictors
        )

    async def parseTwitchOutcomePredictor(
        self,
        predictorJson: dict[str, Any] | None
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

    async def parseWebsocketReward(
        self,
        rewardJson: dict[str, Any] | None
    ) -> TwitchReward | None:
        if not isinstance(rewardJson, dict) or len(rewardJson) == 0:
            return None

        cost = utils.getIntFromDict(rewardJson, 'cost')

        prompt: str | None = None
        if 'prompt' in rewardJson and utils.isValidStr(rewardJson.get('prompt')):
            prompt = utils.getStrFromDict(rewardJson, 'prompt')

        rewardId = utils.getStrFromDict(rewardJson, 'id')
        title = utils.getStrFromDict(rewardJson, 'title')

        return TwitchReward(
            cost = cost,
            prompt = prompt,
            rewardId = rewardId,
            title = title
        )

    async def parseTwitchWebsocketSession(
        self,
        sessionJson: dict[str, Any] | None
    ) -> TwitchWebsocketSession | None:
        if not isinstance(sessionJson, dict) or len(sessionJson) == 0:
            return None

        keepAliveTimeoutSeconds = utils.getIntFromDict(sessionJson, 'keepalive_timeout_seconds')
        connectedAt = datetime.fromisoformat(utils.getStrFromDict(sessionJson, 'connected_at'))
        sessionId = utils.getStrFromDict(sessionJson, 'id')
        status = TwitchWebsocketConnectionStatus.fromStr(utils.getStrFromDict(sessionJson, 'status'))

        reconnectUrl: str | None = None
        if 'reconnect_url' in sessionJson and utils.isValidUrl(sessionJson.get('reconnect_url')):
            reconnectUrl = utils.getStrFromDict(sessionJson, 'reconnect_url')

        return TwitchWebsocketSession(
            keepAliveTimeoutSeconds = keepAliveTimeoutSeconds,
            connectedAt = connectedAt,
            reconnectUrl = reconnectUrl,
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
        subTier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(giftJson, 'sub_tier'))

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
        createdAt = datetime.fromisoformat(utils.getStrFromDict(subscriptionJson, 'created_at'))
        subscriptionId = utils.getStrFromDict(subscriptionJson, 'id')
        version = utils.getStrFromDict(subscriptionJson, 'version')
        condition = await self.parseWebsocketCondition(subscriptionJson.get('condition'))
        status = TwitchWebsocketConnectionStatus.fromStr(utils.getStrFromDict(subscriptionJson, 'status'))
        subscriptionType = TwitchWebsocketSubscriptionType.fromStr(utils.getStrFromDict(subscriptionJson, 'type'))
        transport = await self.__parseTransport(subscriptionJson.get('transport'))

        assert condition and status and subscriptionType and transport, (
            f"{condition=} {status=} {subscriptionType=} {transport=}"
        )

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
