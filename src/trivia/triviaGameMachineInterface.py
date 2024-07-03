from abc import ABC, abstractmethod

from .actions.absTriviaAction import AbsTriviaAction
from .triviaEventListener import TriviaEventListener


class TriviaGameMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: TriviaEventListener | None):
        pass

    @abstractmethod
    def startMachine(self):
        pass

    @abstractmethod
    def submitAction(self, action: AbsTriviaAction):
        pass
