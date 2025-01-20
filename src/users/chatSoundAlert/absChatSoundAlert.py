from abc import ABC, abstractmethod

from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType
from ...misc import utils as utils


class AbsChatSoundAlert(ABC):

    def __init__(
        self,
        qualifier: ChatSoundAlertQualifer,
        cooldownSeconds: int | None,
        volume: int | None,
        message: str
    ):
        if not isinstance(qualifier, ChatSoundAlertQualifer):
            raise TypeError(f'qualifier argument is malformed: \"{qualifier}\"')
        elif cooldownSeconds is not None and not utils.isValidInt(cooldownSeconds):
            raise TypeError(f'cooldownSeconds argument is malformed: \"{cooldownSeconds}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        self.__qualifier: ChatSoundAlertQualifer = qualifier
        self.__cooldownSeconds: int | None = cooldownSeconds
        self.__volume: int | None = volume
        self.__message: str = message

    @property
    @abstractmethod
    def alertType(self) -> ChatSoundAlertType:
        pass

    @property
    def cooldownSeconds(self) -> int | None:
        return self.__cooldownSeconds

    @property
    def message(self) -> str:
        return self.__message

    @property
    def qualifier(self) -> ChatSoundAlertQualifer:
        return self.__qualifier

    @property
    def volume(self) -> int | None:
        return self.__volume
