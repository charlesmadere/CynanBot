from abc import ABC, abstractmethod

from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType
from ...misc import utils as utils


class AbsChatSoundAlert(ABC):

    def __init__(
        self,
        qualifier: ChatSoundAlertQualifer,
        message: str,
        volume: int | None
    ):
        if not isinstance(qualifier, ChatSoundAlertQualifer):
            raise TypeError(f'qualifier argument is malformed: \"{qualifier}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        self.__qualifier: ChatSoundAlertQualifer = qualifier
        self.__message: str = message
        self.__volume: int | None = volume

    @property
    @abstractmethod
    def alertType(self) -> ChatSoundAlertType:
        pass

    @property
    def message(self) -> str:
        return self.__message

    @property
    def qualifier(self) -> ChatSoundAlertQualifer:
        return self.__qualifier

    @property
    def volume(self) -> int | None:
        return self.__volume
