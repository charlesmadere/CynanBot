from .twitchWebsocketConditionBuilderInterface import TwitchWebsocketConditionBuilderInterface
from ..twitchWebsocketUser import TwitchWebsocketUser
from ...api.models.twitchWebsocketCondition import TwitchWebsocketCondition
from ...api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType


class TwitchWebsocketConditionBuilder(TwitchWebsocketConditionBuilderInterface):

    async def build(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: TwitchWebsocketUser,
    ) -> TwitchWebsocketCondition | None:
        if not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
                userId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_CHEER:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_UPDATE:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.FOLLOW:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
                moderatorUserId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.RAID:
            return TwitchWebsocketCondition(
                toBroadcasterUserId = user.userId,
            )

        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT or \
                subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
            )

        else:
            return None
