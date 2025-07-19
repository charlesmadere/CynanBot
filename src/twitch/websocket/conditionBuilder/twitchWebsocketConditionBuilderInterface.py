from abc import ABC, abstractmethod

from ..twitchWebsocketUser import TwitchWebsocketUser
from ...api.models.twitchWebsocketCondition import TwitchWebsocketCondition
from ...api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType


class TwitchWebsocketConditionBuilderInterface(ABC):

    @abstractmethod
    async def build(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: TwitchWebsocketUser,
    ) -> TwitchWebsocketCondition | None:
        pass
