from abc import ABC, abstractmethod

from .actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from .actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction


class CrowdControlActionHandler(ABC):

    @abstractmethod
    async def handleButtonPressAction(self, action: ButtonPressCrowdControlAction) -> bool:
        pass

    @abstractmethod
    async def handleGameShuffleAction(self, action: GameShuffleCrowdControlAction) -> bool:
        pass
