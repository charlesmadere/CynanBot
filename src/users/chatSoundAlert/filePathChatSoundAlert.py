from .absChatSoundAlert import AbsChatSoundAlert
from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType
from ...misc import utils as utils


class FilePathChatSoundAlert(AbsChatSoundAlert):

    def __init__(
        self,
        qualifier: ChatSoundAlertQualifer,
        filePath: str,
        message: str,
        volume: int | None
    ):
        super().__init__(
            qualifier = qualifier,
            message = message,
            volume = volume
        )

        if not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        self.__filePath: str = filePath

    @property
    def alertType(self) -> ChatSoundAlertType:
        return ChatSoundAlertType.FILE_PATH

    @property
    def filePath(self) -> str:
        return self.__filePath
