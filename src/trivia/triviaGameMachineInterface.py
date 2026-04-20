from abc import ABC, abstractmethod

from .actions.absTriviaAction import AbsTriviaAction
from .triviaEventListener import TriviaEventListener
from ..misc.startable import Startable


class TriviaGameMachineInterface(Startable, ABC):

    @abstractmethod
    def setEventListener(self, listener: TriviaEventListener | None):
        pass

    @abstractmethod
    def submitAction(self, action: AbsTriviaAction):
        pass
