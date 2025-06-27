from abc import ABC, abstractmethod

from ..models.useAirStrikeItemAction import UseAirStrikeItemAction


class UseAirStrikeHelperInterface(ABC):

    @abstractmethod
    async def use(self, action: UseAirStrikeItemAction):
        pass
