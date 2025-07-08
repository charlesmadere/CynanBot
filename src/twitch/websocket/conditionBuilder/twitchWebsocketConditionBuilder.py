from typing import Final

from .twitchWebsocketConditionBuilderInterface import TwitchWebsocketConditionBuilderInterface
from ..twitchWebsocketUser import TwitchWebsocketUser
from ...api.models.twitchWebsocketCondition import TwitchWebsocketCondition
from ...api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ...twitchHandleProviderInterface import TwitchHandleProviderInterface
from ....users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchWebsocketConditionBuilder(TwitchWebsocketConditionBuilderInterface):

    def __init__(
        self,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def build(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: TwitchWebsocketUser
    ) -> TwitchWebsocketCondition | None:
        if not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE:
            # TODO we maybe don't need these two lines
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            twitchId = await self.__userIdsRepository.requireUserId(twitchHandle)

            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
                userId = user.userId,
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

        elif subscriptionType is TwitchWebsocketSubscriptionType.CHEER:
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
