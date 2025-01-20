from .absChatSoundAlert import AbsChatSoundAlert
from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType
from ...misc import utils as utils


class DirectoryPathChatSoundAlert(AbsChatSoundAlert):

    def __init__(
        self,
        qualifier: ChatSoundAlertQualifer,
        cooldownSeconds: int | None,
        volume: int | None,
        directoryPath: str,
        message: str
    ):
        super().__init__(
            qualifier = qualifier,
            cooldownSeconds = cooldownSeconds,
            volume = volume,
            message = message
        )

        if not utils.isValidStr(directoryPath):
            raise TypeError(f'directoryPath argument is malformed: \"{directoryPath}\"')

        self.__directoryPath: str = directoryPath

    @property
    def alertType(self) -> ChatSoundAlertType:
        return ChatSoundAlertType.DIRECTORY_PATH

    @property
    def directoryPath(self) -> str:
        return self.__directoryPath
