from abc import ABC, abstractmethod

from cheerActions.cheerActionType import CheerActionType
from cheerActions.wizards.absSteps import AbsSteps

from ..misc import utils as utils


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

    @property
    @abstractmethod
    def cheerActionType(self) -> CheerActionType:
        pass

    @abstractmethod
    def getSteps(self) -> AbsSteps:
        pass

    @abstractmethod
    def printOut(self) -> str:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
