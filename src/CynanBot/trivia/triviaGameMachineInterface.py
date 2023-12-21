from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.triviaEventListener import TriviaEventListener


class TriviaGameMachineInterface(ABC):

    @abstractmethod
    def setEventListener(self, listener: Optional[TriviaEventListener]):
        pass

    @abstractmethod
    def startMachine(self):
        pass

    @abstractmethod
    def submitAction(self, action: AbsTriviaAction):
        pass
