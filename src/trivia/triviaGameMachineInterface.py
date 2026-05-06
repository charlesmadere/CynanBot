from abc import ABC, abstractmethod

from .actions.absTriviaAction import AbsTriviaAction
from ..misc.startable import Startable


class TriviaGameMachineInterface(Startable, ABC):

    @abstractmethod
    def submitAction(self, action: AbsTriviaAction):
        pass
