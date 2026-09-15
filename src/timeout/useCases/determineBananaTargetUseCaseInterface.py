from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.actions.bananaTimeoutAction import BananaTimeoutAction
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..models.timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from ..models.timeoutTarget import TimeoutTarget
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


class DetermineBananaTargetUseCaseInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class ResultData:
        isReverse: bool
        diceRoll: TimeoutDiceRoll | None
        diceRollFailureData: TimeoutDiceRollFailureData | None
        timeoutTarget: TimeoutTarget

    @abstractmethod
    async def invoke(
        self,
        timeoutAction: BananaTimeoutAction,
        diceRoll: TimeoutDiceRoll | None,
        timeoutTarget: TimeoutTarget,
        instigatorUserData: TwitchUserInterface,
    ) -> ResultData:
        pass
