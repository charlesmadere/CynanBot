from typing import Any, Final

from . import utils as utils


class GeneralSettingsRepositorySnapshot:

    def __init__(
        self,
        jsonContents: dict[str, Any],
    ):
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        self.__jsonContents: Final[dict[str, Any]] = jsonContents

    def isFuntoonApiEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonApiEnabled', True)

    def isFuntoonTwitchChatFallbackEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonTwitchChatFallbackEnabled', True)

    def isJishoEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'jishoEnabled', True)

    def isPokepediaEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pokepediaEnabled', True)

    def requireAdministrator(self) -> str:
        administrator = self.__jsonContents.get('administrator')

        if not utils.isValidStr(administrator):
            raise ValueError(f'\"administrator\" in General Settings file is malformed: \"{administrator}\"')

        return administrator
