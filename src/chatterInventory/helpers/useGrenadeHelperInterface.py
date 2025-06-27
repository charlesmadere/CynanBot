from abc import ABC, abstractmethod

from ..models.useGrenadeItemAction import UseGrenadeItemAction


class UseGrenadeHelperInterface(ABC):

    @abstractmethod
    async def use(self, action: UseGrenadeItemAction):
        pass
