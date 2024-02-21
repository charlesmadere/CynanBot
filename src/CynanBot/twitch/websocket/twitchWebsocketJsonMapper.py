from typing import Any, Dict, List, Optional

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
from CynanBot.twitch.api.twitchWebsocketChannelPointsVoting import \
    TwitchChannelPointsVoting
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
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__timber: TimberInterface = timber

    async def parseWebsocketChannelPointsVoting(self, channelPointsVotingJson: Optional[Dict[str, Any]]) -> Optional[TwitchChannelPointsVoting]:
        if not isinstance(channelPointsVotingJson, Dict) or len(channelPointsVotingJson) == 0:
            return None

        isEnabled = utils.getBoolFromDict(channelPointsVotingJson, 'is_enabled')
        amountPerVote = utils.getIntFromDict(channelPointsVotingJson, 'amount_per_vote')

        return TwitchChannelPointsVoting(
            isEnabled = isEnabled,
            amountPerVote = amountPerVote
        )

    async def parseWebsocketPollChoice(self, choiceJson: Optional[Dict[str, Any]]) -> Optional[TwitchPollChoice]:
        if not isinstance(choiceJson, Dict) or len(choiceJson) == 0:
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

    async def parseWebsocketCommunitySubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[TwitchCommunitySubGift]:
        if not isinstance(giftJson, Dict) or len(giftJson) == 0:
            return None

        cumulativeTotal: Optional[int] = None
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

    async def parseWebsocketCondition(self, conditionJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketCondition]:
        if not isinstance(conditionJson, Dict):
            return None

        broadcasterUserId: Optional[str] = None
        if 'broadcaster_user_id' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_id')):
            broadcasterUserId = utils.getStrFromDict(conditionJson, 'broadcaster_user_id')

        broadcasterUserLogin: Optional[str] = None
        if 'broadcaster_user_login' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_login')):
            broadcasterUserLogin = utils.getStrFromDict(conditionJson, 'broadcaster_user_login')

        broadcasterUserName: Optional[str] = None
        if 'broadcaster_user_name' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_name')):
            broadcasterUserName = utils.getStrFromDict(conditionJson, 'broadcaster_user_name')

        clientId: Optional[str] = None
        if 'client_id' in conditionJson and utils.isValidStr(conditionJson.get('client_id')):
            clientId = utils.getStrFromDict(conditionJson, 'client_id')

        fromBroadcasterUserId: Optional[str] = None
        if 'from_broadcaster_user_id' in conditionJson and utils.isValidStr(conditionJson.get('from_broadcaster_user_id')):
            fromBroadcasterUserId = utils.getStrFromDict(conditionJson, 'from_broadcaster_user_id')

        fromBroadcasterUserLogin: Optional[str] = None
        if 'from_broadcaster_user_login' in conditionJson and utils.isValidStr(conditionJson.get('from_broadcaster_user_login')):
            fromBroadcasterUserLogin = utils.getStrFromDict(conditionJson, 'from_broadcaster_user_login')

        fromBroadcasterUserName: Optional[str] = None
        if 'from_broadcaster_user_name' in conditionJson and utils.isValidStr(conditionJson.get('from_broadcaster_user_name')):
            fromBroadcasterUserName = utils.getStrFromDict(conditionJson, 'from_broadcaster_user_name')

        moderatorUserId: Optional[str] = None
        if 'moderator_user_id' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_id')):
            moderatorUserId = utils.getStrFromDict(conditionJson, 'moderator_user_id')

        moderatorUserLogin: Optional[str] = None
        if 'moderator_user_login' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_login')):
            moderatorUserLogin = utils.getStrFromDict(conditionJson, 'moderator_user_login')

        moderatorUserName: Optional[str] = None
        if 'moderator_user_name' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_name')):
            moderatorUserName = utils.getStrFromDict(conditionJson, 'moderator_user_name')

        rewardId: Optional[str] = None
        if 'reward_id' in conditionJson and utils.isValidStr(conditionJson.get('reward_id')):
            rewardId = utils.getStrFromDict(conditionJson, 'reward_id')

        toBroadcasterUserId: Optional[str] = None
        if 'to_broadcaster_user_id' in conditionJson and utils.isValidStr(conditionJson.get('to_broadcaster_user_id')):
            toBroadcasterUserId = utils.getStrFromDict(conditionJson, 'to_broadcaster_user_id')

        toBroadcasterUserLogin: Optional[str] = None
        if 'to_broadcaster_user_login' in conditionJson and utils.isValidStr(conditionJson.get('to_broadcaster_user_login')):
            toBroadcasterUserLogin = utils.getStrFromDict(conditionJson, 'to_broadcaster_user_login')

        toBroadcasterUserName: Optional[str] = None
        if 'to_broadcaster_user_name' in conditionJson and utils.isValidStr(conditionJson.get('to_broadcaster_user_name')):
            toBroadcasterUserName = utils.getStrFromDict(conditionJson, 'to_broadcaster_user_name')

        userId: Optional[str] = None
        if 'user_id' in conditionJson and utils.isValidStr(conditionJson.get('user_id')):
            userId = utils.getStrFromDict(conditionJson, 'user_id')

        userLogin: Optional[str] = None
        if 'user_login' in conditionJson and utils.isValidStr(conditionJson.get('user_login')):
            userLogin = utils.getStrFromDict(conditionJson, 'user_login')

        userName: Optional[str] = None
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

    async def __parseMetadata(self, metadataJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketMetadata]:
        if not isinstance(metadataJson, Dict) or len(metadataJson) == 0:
            return None

        messageTimestamp = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(metadataJson, 'message_timestamp')))
        messageId = utils.getStrFromDict(metadataJson, 'message_id')
        messageType = TwitchWebsocketMessageType.fromStr(utils.getStrFromDict(metadataJson, 'message_type'))

        subscriptionVersion: Optional[str] = None
        if 'subscription_version' in metadataJson and utils.isValidStr(metadataJson.get('subscription_version')):
            subscriptionVersion = utils.getStrFromDict(metadataJson, 'subscription_version')

        subscriptionType: Optional[TwitchWebsocketSubscriptionType] = None
        if 'subscription_type' in metadataJson and utils.isValidStr(metadataJson.get('subscription_type')):
            subscriptionType = TwitchWebsocketSubscriptionType.fromStr(utils.getStrFromDict(metadataJson, 'subscription_type'))

        return TwitchWebsocketMetadata(
            messageTimestamp = messageTimestamp,
            messageId = messageId,
            subscriptionVersion = subscriptionVersion,
            messageType = messageType,
            subscriptionType = subscriptionType
        )

    async def __parsePayload(self, payloadJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketPayload]:
        if not isinstance(payloadJson, Dict) or len(payloadJson) == 0:
            return None

        event = await self.parseWebsocketEvent(payloadJson.get('event'))
        session = await self.parseTwitchWebsocketSession(payloadJson.get('session'))
        subscription = await self.parseWebsocketSubscription(payloadJson.get('subscription'))

        return TwitchWebsocketPayload(
            event = event,
            session = session,
            subscription  = subscription
        )

    async def __parseTransport(self, transportJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketTransport]:
        if not isinstance(transportJson, Dict) or len(transportJson) == 0:
            return None

        connectedAt: Optional[SimpleDateTime] = None
        if 'connected_at' in transportJson and utils.isValidStr(transportJson.get('connected_at')):
            connectedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(transportJson, 'connected_at')))

        disconnectedAt: Optional[SimpleDateTime] = None
        if 'disconnected_at' in transportJson and utils.isValidStr(transportJson.get('disconnected_at')):
            disconnectedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(transportJson, 'disconnected_at')))

        secret: Optional[str] = None
        if 'secret' in transportJson and utils.isValidStr(transportJson.get('secret')):
            secret = utils.getStrFromDict(transportJson, 'secret')

        sessionId: Optional[str] = None
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

    async def parseWebsocketDataBundle(self, dataBundleJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketDataBundle]:
        if not isinstance(dataBundleJson, Dict) or len(dataBundleJson) == 0:
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

    async def parseWebsocketEvent(self, eventJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketEvent]:
        if not isinstance(eventJson, Dict) or len(eventJson) == 0:
            return None

        isAnonymous: Optional[bool] = None
        if 'is_anonymous' in eventJson and eventJson.get('is_anonymous') is not None:
            isAnonymous = utils.getBoolFromDict(eventJson, 'is_anonymous')

        isGift: Optional[bool] = None
        if 'is_gift' in eventJson and eventJson.get('is_gift') is not None:
            isGift = utils.getBoolFromDict(eventJson, 'is_gift')

        bits: Optional[int] = None
        if 'bits' in eventJson and utils.isValidInt(eventJson.get('bits')):
            bits = utils.getIntFromDict(eventJson, 'bits')

        cumulativeMonths: Optional[int] = None
        if 'cumulative_months' in eventJson and utils.isValidInt(eventJson.get('cumulative_months')):
            cumulativeMonths = utils.getIntFromDict(eventJson, 'cumulative_months')

        total: Optional[int] = None
        if 'total' in eventJson and utils.isValidInt(eventJson.get('total')):
            total = utils.getIntFromDict(eventJson, 'total')

        viewers: Optional[int] = None
        if 'viewers' in eventJson and utils.isValidInt(eventJson.get('viewers')):
            viewers = utils.getIntFromDict(eventJson, 'viewers')

        endedAt: Optional[SimpleDateTime] = None
        if 'ended_at' in eventJson and utils.isValidStr(eventJson.get('ended_at')):
            endedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'ended_at')))

        endsAt: Optional[SimpleDateTime] = None
        if 'ends_at' in eventJson and utils.isValidStr(eventJson.get('ends_at')):
            endsAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'ends_at')))

        followedAt: Optional[SimpleDateTime] = None
        if 'followed_at' in eventJson and utils.isValidStr(eventJson.get('followed_at')):
            followedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'followed_at')))

        lockedAt: Optional[SimpleDateTime] = None
        if 'locked_at' in eventJson and utils.isValidStr(eventJson.get('locked_at')):
            lockedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'locked_at')))

        locksAt: Optional[SimpleDateTime] = None
        if 'locks_at' in eventJson and utils.isValidStr(eventJson.get('locks_at')):
            locksAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'locks_at')))

        redeemedAt: Optional[SimpleDateTime] = None
        if 'redeemed_at' in eventJson and utils.isValidStr(eventJson.get('redeemed_at')):
            redeemedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'redeemed_at')))

        startedAt: Optional[SimpleDateTime] = None
        if 'started_at' in eventJson and utils.isValidStr(eventJson.get('started_at')):
            startedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(eventJson, 'started_at')))

        broadcasterUserId: Optional[str] = None
        if 'broadcaster_user_id' in eventJson and utils.isValidStr(eventJson.get('broadcaster_user_id')):
            broadcasterUserId = utils.getStrFromDict(eventJson, 'broadcaster_user_id')

        broadcasterUserLogin: Optional[str] = None
        if 'broadcaster_user_login' in eventJson and utils.isValidStr(eventJson.get('broadcaster_user_login')):
            broadcasterUserLogin = utils.getStrFromDict(eventJson, 'broadcaster_user_login')

        broadcasterUserName: Optional[str] = None
        if 'broadcaster_user_name' in eventJson and utils.isValidStr(eventJson.get('broadcaster_user_name')):
            broadcasterUserName = utils.getStrFromDict(eventJson, 'broadcaster_user_name')

        categoryId: Optional[str] = None
        if 'category_id' in eventJson and utils.isValidStr(eventJson.get('category_id')):
            categoryId = utils.getStrFromDict(eventJson, 'category_id')

        categoryName: Optional[str] = None
        if 'category_name' in eventJson and utils.isValidStr(eventJson.get('category_name')):
            categoryName = utils.getStrFromDict(eventJson, 'category_name')

        eventId: Optional[str] = None
        if 'id' in eventJson and utils.isValidStr(eventJson.get('id')):
            eventId = utils.getStrFromDict(eventJson, 'id')

        fromBroadcasterUserId: Optional[str] = None
        if 'from_broadcaster_user_id' in eventJson and utils.isValidStr(eventJson.get('from_broadcaster_user_id')):
            fromBroadcasterUserId = utils.getStrFromDict(eventJson, 'from_broadcaster_user_id')

        fromBroadcasterUserLogin: Optional[str] = None
        if 'from_broadcaster_user_login' in eventJson and utils.isValidStr(eventJson.get('from_broadcaster_user_login')):
            fromBroadcasterUserLogin = utils.getStrFromDict(eventJson, 'from_broadcaster_user_login')

        fromBroadcasterUserName: Optional[str] = None
        if 'from_broadcaster_user_name' in eventJson and utils.isValidStr(eventJson.get('from_broadcaster_user_name')):
            fromBroadcasterUserName = utils.getStrFromDict(eventJson, 'from_broadcaster_user_name')

        message: Optional[str] = None
        if 'message' in eventJson:
            messageItem: Any = eventJson.get('message')

            if utils.isValidStr(messageItem):
                message = utils.getStrFromDict(eventJson, 'message')
            elif isinstance(messageItem, Dict) and utils.isValidStr(messageItem.get('text')):
                message = utils.getStrFromDict(messageItem, 'text')

        rewardId: Optional[str] = None
        if 'reward_id' in eventJson and utils.isValidStr(eventJson.get('reward_id')):
            rewardId = utils.getStrFromDict(eventJson, 'reward_id')

        text: Optional[str] = None
        if 'text' in eventJson and utils.isValidStr(eventJson.get('text')):
            text = utils.getStrFromDict(eventJson, 'text')

        title: Optional[str] = None
        if 'title' in eventJson and utils.isValidStr(eventJson.get('title')):
            title = utils.getStrFromDict(eventJson, 'title')

        toBroadcasterUserId: Optional[str] = None
        if 'to_broadcaster_user_id' in eventJson and utils.isValidStr(eventJson.get('to_broadcaster_user_id')):
            toBroadcasterUserId = utils.getStrFromDict(eventJson, 'to_broadcaster_user_id')

        toBroadcasterUserLogin: Optional[str] = None
        if 'to_broadcaster_user_login' in eventJson and utils.isValidStr(eventJson.get('to_broadcaster_user_login')):
            toBroadcasterUserLogin = utils.getStrFromDict(eventJson, 'to_broadcaster_user_login')

        toBroadcasterUserName: Optional[str] = None
        if 'to_broadcaster_user_name' in eventJson and utils.isValidStr(eventJson.get('to_broadcaster_user_name')):
            toBroadcasterUserName = utils.getStrFromDict(eventJson, 'to_broadcaster_user_name')

        userId: Optional[str] = None
        if 'user_id' in eventJson and utils.isValidStr(eventJson.get('user_id')):
            userId = utils.getStrFromDict(eventJson, 'user_id')

        userInput: Optional[str] = None
        if 'user_input' in eventJson and utils.isValidStr(eventJson.get('user_input')):
            userInput = utils.getStrFromDict(eventJson, 'user_input')

        userLogin: Optional[str] = None
        if 'user_login' in eventJson and utils.isValidStr(eventJson.get('user_login')):
            userLogin = utils.getStrFromDict(eventJson, 'user_login')

        userName: Optional[str] = None
        if 'user_name' in eventJson and utils.isValidStr(eventJson.get('user_name')):
            userName = utils.getStrFromDict(eventJson, 'user_name')

        winningOutcomeId: Optional[str] = None
        if 'winning_outcome_id' in eventJson and utils.isValidStr(eventJson.get('winning_outcome_id')):
            winningOutcomeId = utils.getStrFromDict(eventJson, 'winning_outcome_id')

        tier: Optional[TwitchSubscriberTier] = None
        if 'tier' in eventJson and utils.isValidStr(eventJson.get('tier')):
            tier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(eventJson, 'tier'))

        channelPointsVoting: Optional[TwitchChannelPointsVoting] = None
        if 'channel_points_voting' in eventJson:
            channelPointsVoting = await self.parseWebsocketChannelPointsVoting(eventJson.get('channel_points_voting'))

        choices: Optional[List[TwitchPollChoice]] = None
        if 'choices' in eventJson:
            choicesItem: Any = eventJson.get('choices')

            if isinstance(choicesItem, List) and len(choicesItem) >= 1:
                choices = list()

                for choiceItem in choicesItem:
                    choice = await self.parseWebsocketPollChoice(choiceItem)

                    if choice is not None:
                        choices.append(choice)

                if len(choices) == 0:
                    choices = None

        pollStatus: Optional[TwitchPollStatus] = None
        rewardRedemptionStatus: Optional[TwitchRewardRedemptionStatus] = None
        if 'status' in eventJson and utils.isValidStr(eventJson.get('status')):
            pollStatus = TwitchPollStatus.fromStr(utils.getStrFromDict(eventJson, 'status'))
            rewardRedemptionStatus = TwitchRewardRedemptionStatus.fromStr(utils.getStrFromDict(eventJson, 'status'))

        communitySubGift: Optional[TwitchCommunitySubGift] = None
        if 'community_sub_gift' in eventJson:
            communitySubGift = await self.parseWebsocketCommunitySubGift(eventJson.get('community_sub_gift'))

        noticeType: Optional[TwitchWebsocketNoticeType] = None
        if 'notice_type' in eventJson and utils.isValidStr(eventJson.get('notice_type')):
            noticeType = TwitchWebsocketNoticeType.fromStr(utils.getStrFromDict(eventJson, 'notice_type'))

        outcomes: Optional[List[TwitchOutcome]] = None
        if 'outcomes' in eventJson:
            outcomesItem: Any = eventJson.get('outcomes')

            if isinstance(outcomesItem, List) and len(outcomesItem) >= 1:
                outcomes = list()

                for outcomeItem in outcomesItem:
                    outcome = await self.parseTwitchOutcome(outcomeItem)

                    if outcome is not None:
                        outcomes.append(outcome)

                if len(outcomes) == 0:
                    outcomes = None

        reward: Optional[TwitchReward] = None
        if 'reward' in eventJson:
            reward = await self.parseWebsocketReward(eventJson.get('reward'))

        subGift: Optional[TwitchSubGift] = None
        if 'sub_gift' in eventJson:
            subGift = await self.parseWebsocketSubGift(eventJson.get('sub_gift'))

        return TwitchWebsocketEvent(
            isAnonymous = isAnonymous,
            isGift = isGift,
            bits = bits,
            cumulativeMonths = cumulativeMonths,
            total = total,
            viewers = viewers,
            endedAt = endedAt,
            endsAt = endsAt,
            followedAt = followedAt,
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

    async def parseTwitchOutcome(self, outcomeJson: Optional[Dict[str, Any]]) -> Optional[TwitchOutcome]:
        if not isinstance(outcomeJson, Dict) or len(outcomeJson) == 0:
            return None

        channelPoints = utils.getIntFromDict(outcomeJson, 'channel_points', fallback = 0)
        users = utils.getIntFromDict(outcomeJson, 'users', fallback = 0)
        outcomeId = utils.getStrFromDict(outcomeJson, 'id')
        title = utils.getStrFromDict(outcomeJson, 'title')
        color = TwitchOutcomeColor.fromStr(utils.getStrFromDict(outcomeJson, 'color'))

        topPredictors: Optional[List[TwitchOutcomePredictor]] = None
        if 'top_predictors' in outcomeJson:
            topPredictorsItem: Any = outcomeJson.get('top_predictors')

            if isinstance(topPredictorsItem, List) and len(topPredictorsItem) >= 1:
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

    async def parseTwitchOutcomePredictor(self, predictorJson: Optional[Dict[str, Any]]) -> Optional[TwitchOutcomePredictor]:
        if not isinstance(predictorJson, Dict) or len(predictorJson) == 0:
            return None

        channelPointsUsed = utils.getIntFromDict(predictorJson, 'channel_points_used')

        channelPointsWon: Optional[int] = None
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

    async def parseWebsocketReward(self, rewardJson: Optional[Dict[str, Any]]) -> Optional[TwitchReward]:
        if not isinstance(rewardJson, Dict) or len(rewardJson) == 0:
            return None

        cost = utils.getIntFromDict(rewardJson, 'cost')

        prompt: Optional[str] = None
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

    async def parseTwitchWebsocketSession(self, sessionJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketSession]:
        if not isinstance(sessionJson, Dict) or len(sessionJson) == 0:
            return None

        keepAliveTimeoutSeconds = utils.getIntFromDict(sessionJson, 'keepalive_timeout_seconds')
        connectedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(sessionJson, 'connected_at')))
        sessionId = utils.getStrFromDict(sessionJson, 'id')
        status = TwitchWebsocketConnectionStatus.fromStr(utils.getStrFromDict(sessionJson, 'status'))

        reconnectUrl: Optional[str] = None
        if 'reconnect_url' in sessionJson and utils.isValidUrl(sessionJson.get('reconnect_url')):
            reconnectUrl = utils.getStrFromDict(sessionJson, 'reconnect_url')

        return TwitchWebsocketSession(
            keepAliveTimeoutSeconds = keepAliveTimeoutSeconds,
            connectedAt = connectedAt,
            reconnectUrl = reconnectUrl,
            sessionId = sessionId,
            status = status
        )

    async def parseWebsocketSubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[TwitchSubGift]:
        if not isinstance(giftJson, Dict) or len(giftJson) == 0:
            return None

        cumulativeTotal: Optional[int] = None
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

    async def parseWebsocketSubscription(self, subscriptionJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketSubscription]:
        if not isinstance(subscriptionJson, Dict) or len(subscriptionJson) == 0:
            return None

        cost = utils.getIntFromDict(subscriptionJson, 'cost')
        createdAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(subscriptionJson, 'created_at')))
        subscriptionId = utils.getStrFromDict(subscriptionJson, 'id')
        version = utils.getStrFromDict(subscriptionJson, 'version')
        condition = await self.parseWebsocketCondition(subscriptionJson.get('condition'))
        status = TwitchWebsocketConnectionStatus.fromStr(utils.getStrFromDict(subscriptionJson, 'status'))
        subscriptionType = TwitchWebsocketSubscriptionType.fromStr(utils.getStrFromDict(subscriptionJson, 'type'))
        transport = await self.__parseTransport(subscriptionJson.get('transport'))

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
