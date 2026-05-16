from abc import ABC, abstractmethod

from .actions.crowdControlAction import CrowdControlAction
from ..misc.startable import Startable


class CrowdControlMachineInterface(Startable, ABC):

    @property
    @abstractmethod
    def isPaused(self) -> bool:
        pass

    @abstractmethod
    def pause(self) -> bool:
        pass

    @abstractmethod
    def resume(self) -> bool:
        pass

    @abstractmethod
    def submitAction(self, action: CrowdControlAction):
        pass
