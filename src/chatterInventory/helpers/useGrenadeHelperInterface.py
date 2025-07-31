from abc import ABC, abstractmethod

from ..models.useGrenadeItemAction import UseGrenadeItemAction


class UseGrenadeHelperInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAction(self, action: UseGrenadeItemAction):
        pass
