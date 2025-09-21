from abc import ABC, abstractmethod
from typing import Any, Final

from .absStep import AbsStep
from .absSteps import AbsSteps
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class AbsWizard(ABC):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId

    @property
    @abstractmethod
    def cheerActionType(self) -> CheerActionType:
        pass

    @property
    @abstractmethod
    def currentStep(self) -> AbsStep:
        pass

    @abstractmethod
    def printOut(self) -> str:
        pass

    def __repr__(self):
        dictionary = self.toDictionary()
        return str(dictionary)

    @property
    @abstractmethod
    def steps(self) -> AbsSteps:
        pass

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
