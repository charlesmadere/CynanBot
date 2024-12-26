from abc import ABC, abstractmethod
from typing import Any

from .absSteps import AbsSteps
from ..actions.recurringActionType import RecurringActionType
from ...misc import utils as utils


class AbsWizard(ABC):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId

    @abstractmethod
    def getSteps(self) -> AbsSteps:
        pass

    @abstractmethod
    def printOut(self) -> str:
        pass

    @property
    @abstractmethod
    def recurringActionType(self) -> RecurringActionType:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
