from abc import ABC, abstractmethod
from enum import Enum, auto

from ..models.requestGashaponRewardAction import RequestGashaponRewardAction


class GashaponRewardUseCaseInterface(ABC):

    class Result(Enum):

        NOT_FOLLOWING = auto()
        NOT_READY = auto()
        NOT_SUBSCRIBED = auto()
        READY = auto()

    @abstractmethod
    async def invoke(
        self,
        action: RequestGashaponRewardAction,
        twitchAccessToken: str,
    ) -> Result:
        pass
