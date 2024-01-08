from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface
from CynanBot.twitch.websocket.websocketCommunitySubGift import \
    WebsocketCommunitySubGift
from CynanBot.twitch.websocket.websocketCondition import WebsocketCondition
from CynanBot.twitch.websocket.websocketConnectionStatus import \
    WebsocketConnectionStatus
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketMessageType import WebsocketMessageType
from CynanBot.twitch.websocket.websocketMetadata import WebsocketMetadata
from CynanBot.twitch.websocket.websocketNoticeType import WebsocketNoticeType
from CynanBot.twitch.websocket.websocketOutcome import WebsocketOutcome
from CynanBot.twitch.websocket.websocketOutcomeColor import \
    WebsocketOutcomeColor
from CynanBot.twitch.websocket.websocketOutcomePredictor import \
    WebsocketOutcomePredictor
from CynanBot.twitch.websocket.websocketPayload import WebsocketPayload
from CynanBot.twitch.websocket.websocketReward import WebsocketReward
from CynanBot.twitch.websocket.websocketSession import WebsocketSession
from CynanBot.twitch.websocket.websocketSubGift import WebsocketSubGift
from CynanBot.twitch.websocket.websocketSubscription import \
    WebsocketSubscription
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.twitch.websocket.websocketTransport import WebsocketTransport
from CynanBot.twitch.websocket.websocketTransportMethod import \
    WebsocketTransportMethod


class TwitchWebsocketJsonMapper(TwitchWebsocketJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseWebsocketCommunitySubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[WebsocketCommunitySubGift]:
        if not isinstance(giftJson, Dict) or not utils.hasItems(giftJson):
            return None

        cumulativeTotal: Optional[int] = None
        if 'cumulative_total' in giftJson and utils.isValidInt(giftJson.get('cumulative_total')):
            cumulativeTotal = utils.getIntFromDict(giftJson, 'cumulative_total')

        total = utils.getIntFromDict(giftJson, 'total', fallback = 0)
        communitySubGiftId = utils.getStrFromDict(giftJson, 'id')
        subTier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(giftJson, 'sub_tier'))

        return WebsocketCommunitySubGift(
            cumulativeTotal = cumulativeTotal,
            total = total,
            communitySubGiftId = communitySubGiftId,
            subTier = subTier
        )

    async def parseWebsocketCondition(self, conditionJson: Optional[Dict[str, Any]]) -> Optional[WebsocketCondition]:
        if not isinstance(conditionJson, Dict):
            return None

        isAnonymous: Optional[bool] = None
        if 'is_anonymous' in conditionJson and conditionJson.get('is_anonymous') is not None:
            isAnonymous = utils.getBoolFromDict(conditionJson, 'is_anonymous')

        isGift: Optional[bool] = None
        if 'is_gift' in conditionJson and conditionJson.get('is_gift') is not None:
            isGift = utils.getBoolFromDict(conditionJson, 'is_gift')

        isPermanent: Optional[bool] = None
        if 'is_permanent' in conditionJson and conditionJson.get('is_permanent') is not None:
            isPermanent = utils.getBoolFromDict(conditionJson, 'is_permanent')

        bits: Optional[int] = None
        if 'bits' in conditionJson and utils.isValidInt(conditionJson.get('bits')):
            bits = utils.getIntFromDict(conditionJson, 'bits')

        cumulativeTotal: Optional[int] = None
        if 'cumulative_total' in conditionJson and utils.isValidInt(conditionJson.get('cumulative_total')):
            cumulativeTotal = utils.getIntFromDict(conditionJson, 'cumulative_total')

        total: Optional[int] = None
        if 'total' in conditionJson and utils.isValidInt(conditionJson.get('total')):
            total = utils.getIntFromDict(conditionJson, 'total')

        viewers: Optional[int] = None
        if 'viewers' in conditionJson and utils.isValidInt(conditionJson.get('viewers')):
            viewers = utils.getIntFromDict(conditionJson, 'viewers')

        broadcasterUserId: Optional[str] = None
        if 'broadcaster_user_id' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_id')):
            broadcasterUserId = utils.getStrFromDict(conditionJson, 'broadcaster_user_id')

        broadcasterUserLogin: Optional[str] = None
        if 'broadcaster_user_login' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_login')):
            broadcasterUserLogin = utils.getStrFromDict(conditionJson, 'broadcaster_user_login')

        broadcasterUserName: Optional[str] = None
        if 'broadcaster_user_name' in conditionJson and utils.isValidStr(conditionJson.get('broadcaster_user_name')):
            broadcasterUserName = utils.getStrFromDict(conditionJson, 'broadcaster_user_name')

        categoryId: Optional[str] = None
        if 'category_id' in conditionJson and utils.isValidStr(conditionJson.get('category_id')):
            categoryId = utils.getStrFromDict(conditionJson, 'category_id')

        categoryName: Optional[str] = None
        if 'category_name' in conditionJson and utils.isValidStr(conditionJson.get('category_name')):
            categoryName = utils.getStrFromDict(conditionJson, 'category_name')

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

        message: Optional[str] = None
        if 'message' in conditionJson:
            messageItem: Any = conditionJson.get('message')

            if utils.isValidStr(messageItem):
                message = utils.getStrFromDict(conditionJson, 'message')
            elif isinstance(messageItem, Dict) and utils.isValidStr(messageItem.get('text')):
                message = utils.getStrFromDict(messageItem, 'text')

        moderatorUserId: Optional[str] = None
        if 'moderator_user_id' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_id')):
            moderatorUserId = utils.getStrFromDict(conditionJson, 'moderator_user_id')

        moderatorUserLogin: Optional[str] = None
        if 'moderator_user_login' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_login')):
            moderatorUserLogin = utils.getStrFromDict(conditionJson, 'moderator_user_login')

        moderatorUserName: Optional[str] = None
        if 'moderator_user_name' in conditionJson and utils.isValidStr(conditionJson.get('moderator_user_name')):
            moderatorUserName = utils.getStrFromDict(conditionJson, 'moderator_user_name')

        reason: Optional[str] = None
        if 'reason' in conditionJson and utils.isValidBool(conditionJson.get('reason')):
            reason = utils.getStrFromDict(conditionJson, 'reason')

        rewardId: Optional[str] = None
        if 'reward_id' in conditionJson and utils.isValidStr(conditionJson.get('reward_id')):
            rewardId = utils.getStrFromDict(conditionJson, 'reward_id')

        title: Optional[str] = None
        if 'title' in conditionJson and utils.isValidStr(conditionJson.get('title')):
            title = utils.getStrFromDict(conditionJson, 'title')

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

        userInput: Optional[str] = None
        if 'user_input' in conditionJson and utils.isValidStr(conditionJson.get('user_input')):
            userInput = utils.getStrFromDict(conditionJson, 'user_input')

        userLogin: Optional[str] = None
        if 'user_login' in conditionJson and utils.isValidStr(conditionJson.get('user_login')):
            userLogin = utils.getStrFromDict(conditionJson, 'user_login')

        userName: Optional[str] = None
        if 'user_name' in conditionJson and utils.isValidStr(conditionJson.get('user_name')):
            userName = utils.getStrFromDict(conditionJson, 'user_name')

        tier: Optional[TwitchSubscriberTier] = None
        if 'tier' in conditionJson and utils.isValidStr(conditionJson.get('tier')):
            tier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(conditionJson, 'tier'))

        reward: Optional[WebsocketReward] = None
        if 'reward' in conditionJson:
            reward = await self.parseWebsocketReward(conditionJson.get('reward'))

        return WebsocketCondition(
            isAnonymous = isAnonymous,
            isGift = isGift,
            isPermanent = isPermanent,
            bits = bits,
            cumulativeTotal = cumulativeTotal,
            total = total,
            viewers = viewers,
            broadcasterUserId = broadcasterUserId,
            broadcasterUserLogin = broadcasterUserLogin,
            broadcasterUserName = broadcasterUserName,
            categoryId = categoryId,
            categoryName = categoryName,
            clientId = clientId,
            fromBroadcasterUserId = fromBroadcasterUserId,
            fromBroadcasterUserLogin = fromBroadcasterUserLogin,
            fromBroadcasterUserName = fromBroadcasterUserName,
            message = message,
            moderatorUserId = moderatorUserId,
            moderatorUserLogin = moderatorUserLogin,
            moderatorUserName = moderatorUserName,
            reason = reason,
            rewardId = rewardId,
            title = title,
            toBroadcasterUserId = toBroadcasterUserId,
            toBroadcasterUserLogin = toBroadcasterUserLogin,
            toBroadcasterUserName = toBroadcasterUserName,
            userId = userId,
            userInput = userInput,
            userLogin = userLogin,
            userName = userName,
            tier = tier,
            reward = reward
        )

    async def __parseMetadata(self, metadataJson: Optional[Dict[str, Any]]) -> Optional[WebsocketMetadata]:
        if not isinstance(metadataJson, Dict) or not utils.hasItems(metadataJson):
            return None

        messageTimestamp = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(metadataJson, 'message_timestamp')))
        messageId = utils.getStrFromDict(metadataJson, 'message_id')
        messageType = WebsocketMessageType.fromStr(utils.getStrFromDict(metadataJson, 'message_type'))

        subscriptionType: Optional[WebsocketSubscriptionType] = None
        if 'subscription_type' in metadataJson and utils.isValidStr(metadataJson.get('subscription_type')):
            subscriptionType = WebsocketSubscriptionType.fromStr(utils.getStrFromDict(metadataJson, 'subscription_type'))

        subscriptionVersion: Optional[str] = None
        if 'subscription_version' in metadataJson and utils.isValidStr(metadataJson.get('subscription_version')):
            subscriptionVersion = utils.getStrFromDict(metadataJson, 'subscription_version')

        return WebsocketMetadata(
            messageTimestamp = messageTimestamp,
            messageId = messageId,
            subscriptionVersion = subscriptionVersion,
            messageType = messageType,
            subscriptionType = subscriptionType
        )

    async def __parsePayload(self, payloadJson: Optional[Dict[str, Any]]) -> Optional[WebsocketPayload]:
        if not isinstance(payloadJson, Dict) or not utils.hasItems(payloadJson):
            return None

        event = await self.parseWebsocketEvent(payloadJson.get('event'))
        session = await self.parseWebsocketSession(payloadJson.get('session'))
        subscription = await self.parseWebsocketSubscription(payloadJson.get('subscription'))

        return WebsocketPayload(
            event = event,
            session = session,
            subscription  = subscription
        )

    async def __parseTransport(self, transportJson: Optional[Dict[str, Any]]) -> Optional[WebsocketTransport]:
        if not isinstance(transportJson, Dict) or not utils.hasItems(transportJson):
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

        method = WebsocketTransportMethod.fromStr(utils.getStrFromDict(transportJson, 'method'))

        return WebsocketTransport(
            connectedAt = connectedAt,
            disconnectedAt = disconnectedAt,
            secret = secret,
            sessionId = sessionId,
            method = method
        )

    async def parseWebsocketDataBundle(self, dataBundleJson: Optional[Dict[str, Any]]) -> Optional[WebsocketDataBundle]:
        if not isinstance(dataBundleJson, Dict) or not utils.hasItems(dataBundleJson):
            return None

        metadata = await self.__parseMetadata(dataBundleJson.get('metadata'))

        if metadata is None:
            self.__timber.log('TwitchWebsocketJsonMapper', f'Websocket message ({dataBundleJson}) is missing \"metadata\" ({metadata}) field')
            return None

        payload = await self.__parsePayload(dataBundleJson.get('payload'))

        return WebsocketDataBundle(
            metadata = metadata,
            payload = payload
        )

    async def parseWebsocketEvent(self, eventJson: Optional[Dict[str, Any]]) -> Optional[WebsocketEvent]:
        if not isinstance(eventJson, Dict) or not utils.hasItems(eventJson):
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

        tier: Optional[TwitchSubscriberTier] = None
        if 'tier' in eventJson and utils.isValidStr(eventJson.get('tier')):
            tier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(eventJson, 'tier'))

        communitySubGift: Optional[WebsocketCommunitySubGift] = None
        if 'community_sub_gift' in eventJson:
            communitySubGift = await self.parseWebsocketCommunitySubGift(eventJson.get('community_sub_gift'))

        noticeType: Optional[WebsocketNoticeType] = None
        if 'notice_type' in eventJson and utils.isValidStr(eventJson.get('notice_type')):
            noticeType = WebsocketNoticeType.fromStr(utils.getStrFromDict(eventJson, 'notice_type'))

        outcomes: Optional[List[WebsocketOutcome]] = None
        if 'outcomes' in eventJson:
            outcomesItem: Any = eventJson.get('outcomes')

            if isinstance(outcomesItem, List) and utils.hasItems(outcomesItem):
                outcomes = list()

                for outcomeItem in outcomesItem:
                    outcome = await self.parseWebsocketOutcome(outcomeItem)

                    if outcome is not None:
                        outcomes.append(outcome)

                if len(outcomes) == 0:
                    outcomes = None

        reward: Optional[WebsocketReward] = None
        if 'reward' in eventJson:
            reward = await self.parseWebsocketReward(eventJson.get('reward'))

        subGift: Optional[WebsocketSubGift] = None
        if 'sub_gift' in eventJson:
            subGift = await self.parseWebsocketSubGift(eventJson.get('sub_gift'))

        return WebsocketEvent(
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
            tier = tier,
            communitySubGift = communitySubGift,
            noticeType = noticeType,
            outcomes = outcomes,
            reward = reward,
            subGift = subGift
        )

    async def parseWebsocketOutcome(self, outcomeJson: Optional[Dict[str, Any]]) -> Optional[WebsocketOutcome]:
        if not isinstance(outcomeJson, Dict) or not utils.hasItems(outcomeJson):
            return None

        channelPoints = utils.getIntFromDict(outcomeJson, 'channel_points', fallback = 0)
        users = utils.getIntFromDict(outcomeJson, 'users', fallback = 0)
        outcomeId = utils.getStrFromDict(outcomeJson, 'id')
        title = utils.getStrFromDict(outcomeJson, 'title')
        color = WebsocketOutcomeColor.fromStr(utils.getStrFromDict(outcomeJson, 'color'))

        topPredictors: Optional[List[WebsocketOutcomePredictor]] = None
        if 'top_predictors' in outcomeJson:
            topPredictorsItem: Any = outcomeJson.get('top_predictors')

            if isinstance(topPredictorsItem, List) and utils.hasItems(outcomeId):
                topPredictors = list()

                for topPredictorItem in topPredictorsItem:
                    topPredictor = await self.parseWebsocketOutcomePredictor(topPredictorItem)

                    if topPredictor is not None:
                        topPredictors.append(topPredictor)

                if len(topPredictors) == 0:
                    topPredictors = None

        return WebsocketOutcome(
            channelPoints = channelPoints,
            users = users,
            outcomeId = outcomeId,
            title = title,
            color = color,
            topPredictors = topPredictors
        )

    async def parseWebsocketOutcomePredictor(self, predictorJson: Optional[Dict[str, Any]]) -> Optional[WebsocketOutcomePredictor]:
        if not isinstance(predictorJson, Dict) or not utils.hasItems(predictorJson):
            return None

        channelPointsUsed = utils.getIntFromDict(predictorJson, 'channel_points_used')

        channelPointsWon: Optional[int] = None
        if 'channel_points_won' in predictorJson and utils.isValidInt(predictorJson.get('channel_points_won')):
            channelPointsWon = utils.getIntFromDict(predictorJson, 'channel_points_won')

        userId = utils.getStrFromDict(predictorJson, 'user_id')
        userLogin = utils.getStrFromDict(predictorJson, 'user_login')
        userName = utils.getStrFromDict(predictorJson, 'user_name')

        return WebsocketOutcomePredictor(
            channelPointsUsed = channelPointsUsed,
            channelPointsWon = channelPointsWon,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parseWebsocketReward(self, rewardJson: Optional[Dict[str, Any]]) -> Optional[WebsocketReward]:
        if not isinstance(rewardJson, Dict) or not utils.hasItems(rewardJson):
            return None

        cost = utils.getIntFromDict(rewardJson, 'cost')

        prompt: Optional[str] = None
        if 'prompt' in rewardJson and utils.isValidStr(rewardJson.get('prompt')):
            prompt = utils.getStrFromDict(rewardJson, 'prompt')

        rewardId = utils.getStrFromDict(rewardJson, 'id')
        title = utils.getStrFromDict(rewardJson, 'title')

        return WebsocketReward(
            cost = cost,
            prompt = prompt,
            rewardId = rewardId,
            title = title
        )

    async def parseWebsocketSession(self, sessionJson: Optional[Dict[str, Any]]) -> Optional[WebsocketSession]:
        if not isinstance(sessionJson, Dict) or not utils.hasItems(sessionJson):
            return None

        keepAliveTimeoutSeconds = utils.getIntFromDict(sessionJson, 'keepalive_timeout_seconds')
        connectedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(sessionJson, 'connected_at')))
        sessionId = utils.getStrFromDict(sessionJson, 'id')
        status = WebsocketConnectionStatus.fromStr(utils.getStrFromDict(sessionJson, 'status'))

        reconnectUrl: Optional[str] = None
        if 'reconnect_url' in sessionJson and utils.isValidUrl(sessionJson.get('reconnect_url')):
            reconnectUrl = utils.getStrFromDict(sessionJson, 'reconnect_url')

        return WebsocketSession(
            keepAliveTimeoutSeconds = keepAliveTimeoutSeconds,
            connectedAt = connectedAt,
            reconnectUrl = reconnectUrl,
            sessionId = sessionId,
            status = status
        )

    async def parseWebsocketSubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[WebsocketSubGift]:
        if not isinstance(giftJson, Dict) or not utils.hasItems(giftJson):
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

        return WebsocketSubGift(
            cumulativeTotal = cumulativeTotal,
            durationMonths = durationMonths,
            communityGiftId = communityGiftId,
            recipientUserId = recipientUserId,
            recipientUserLogin = recipientUserLogin,
            recipientUserName = recipientUserName,
            subTier = subTier
        )

    async def parseWebsocketSubscription(self, subscriptionJson: Optional[Dict[str, Any]]) -> Optional[WebsocketSubscription]:
        if not isinstance(subscriptionJson, Dict) or not utils.hasItems(subscriptionJson):
            return None

        cost = utils.getIntFromDict(subscriptionJson, 'cost')
        createdAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(subscriptionJson, 'created_at')))
        subscriptionId = utils.getStrFromDict(subscriptionJson, 'id')
        version = utils.getStrFromDict(subscriptionJson, 'version')
        condition = await self.parseWebsocketCondition(subscriptionJson.get('condition'))
        status = WebsocketConnectionStatus.fromStr(utils.getStrFromDict(subscriptionJson, 'status'))
        subscriptionType = WebsocketSubscriptionType.fromStr(utils.getStrFromDict(subscriptionJson, 'type'))
        transport = await self.__parseTransport(subscriptionJson.get('transport'))

        return WebsocketSubscription(
            cost = cost,
            createdAt = createdAt,
            subscriptionId = subscriptionId,
            version = version,
            condition = condition,
            status = status,
            subscriptionType = subscriptionType,
            transport = transport
        )
