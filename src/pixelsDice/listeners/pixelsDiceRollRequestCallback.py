from abc import ABC, abstractmethod

from ..models.diceRollResult import DiceRollResult


class PixelsDiceRollRequestCallback(ABC):

    @abstractmethod
    async def onPixelsDiceRolled(self, result: DiceRollResult):
        pass
