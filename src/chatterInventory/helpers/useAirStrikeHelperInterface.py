from abc import ABC, abstractmethod

from ..models.useAirStrikeItemAction import UseAirStrikeItemAction


class UseAirStrikeHelperInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def use(self, action: UseAirStrikeItemAction):
        pass
