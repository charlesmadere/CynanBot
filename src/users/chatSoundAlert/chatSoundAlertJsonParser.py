from typing import Any

from frozenlist import FrozenList

from .absChatSoundAlert import AbsChatSoundAlert
from .chatSoundAlertJsonParserInterface import ChatSoundAlertJsonParserInterface
from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType
from .directoryPathChatSoundAlert import DirectoryPathChatSoundAlert
from .filePathChatSoundAlert import FilePathChatSoundAlert
from .soundAlertChatSoundAlert import SoundAlertChatSoundAlert
from ...misc import utils as utils
from ...soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface


class ChatSoundAlertJsonParser(ChatSoundAlertJsonParserInterface):

    def __init__(
        self,
        soundAlertJsonMapper: SoundAlertJsonMapperInterface
    ):
        if not isinstance(soundAlertJsonMapper, SoundAlertJsonMapperInterface):
            raise TypeError(f'soundAlertJsonMapper argument is malformed: \"{soundAlertJsonMapper}\"')

        self.__soundAlertJsonMapper: SoundAlertJsonMapperInterface = soundAlertJsonMapper

    def parseAlertQualifier(
        self,
        alertQualifier: str
    ) -> ChatSoundAlertQualifer:
        if not utils.isValidStr(alertQualifier):
            raise TypeError(f'alertQualifier argument is malformed: \"{alertQualifier}\"')

        alertQualifier = alertQualifier.lower()

        match alertQualifier:
            case 'contains': return ChatSoundAlertQualifer.CONTAINS
            case 'exact': return ChatSoundAlertQualifer.EXACT
            case _: raise ValueError(f'Encountered unexpected AlertQualifier value: \"{alertQualifier}\"')

    def parseAlertType(
        self,
        alertType: str
    ) -> ChatSoundAlertType:
        if not utils.isValidStr(alertType):
            raise TypeError(f'alertType argument is malformed: \"{alertType}\"')

        alertType = alertType.lower()

        match alertType:
            case 'directory_path': return ChatSoundAlertType.DIRECTORY_PATH
            case 'file_path': return ChatSoundAlertType.FILE_PATH
            case 'sound_alert': return ChatSoundAlertType.SOUND_ALERT
            case _: raise ValueError(f'Encountered unknown ChatSoundAlertType value: \"{alertType}\"')

    def parseChatSoundAlert(
        self,
        jsonContents: dict[str, Any]
    ) -> AbsChatSoundAlert:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        qualifier = self.parseAlertQualifier(utils.getStrFromDict(jsonContents, 'qualifier'))
        alertType = self.parseAlertType(utils.getStrFromDict(jsonContents, 'alertType'))
        message = utils.getStrFromDict(jsonContents, 'message')

        volume: int | None = None
        if 'volume' in jsonContents and utils.isValidInt(jsonContents.get('volume')):
            volume = utils.getIntFromDict(jsonContents, 'volume')

        match alertType:
            case ChatSoundAlertType.DIRECTORY_PATH:
                return self.__parseDirectoryPathChatSoundAlert(
                    qualifier = qualifier,
                    jsonContents = jsonContents,
                    message = message,
                    volume = volume
                )

            case ChatSoundAlertType.FILE_PATH:
                return self.__parseFilePathChatSoundAlert(
                    qualifier = qualifier,
                    jsonContents = jsonContents,
                    message = message,
                    volume = volume
                )

            case ChatSoundAlertType.SOUND_ALERT:
                return self.__parseSoundAlertChatSoundAlert(
                    qualifier = qualifier,
                    jsonContents = jsonContents,
                    message = message,
                    volume = volume
                )

            case _:
                raise ValueError(f'Encountered unknown ChatSoundAlertType value: \"{alertType}\"')

    def parseChatSoundAlerts(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> FrozenList[AbsChatSoundAlert] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        alerts: list[AbsChatSoundAlert] = list()

        for alertJson in jsonContents:
            alert = self.parseChatSoundAlert(alertJson)
            alerts.append(alert)

        # elements with a qualifier of EXACT should be sorted to the front of the list
        alerts.sort(key = lambda alert: (alert.qualifier is not ChatSoundAlertQualifer.EXACT, alert.message.casefold()))
        frozenAlerts: FrozenList[AbsChatSoundAlert] = FrozenList(alerts)
        frozenAlerts.freeze()

        return frozenAlerts

    def __parseDirectoryPathChatSoundAlert(
        self,
        qualifier: ChatSoundAlertQualifer,
        jsonContents: dict[str, Any],
        message: str,
        volume: int | None
    ) -> DirectoryPathChatSoundAlert:
        directoryPath = utils.getStrFromDict(jsonContents, 'directoryPath')

        return DirectoryPathChatSoundAlert(
            qualifier = qualifier,
            directoryPath = directoryPath,
            message = message,
            volume = volume
        )

    def __parseFilePathChatSoundAlert(
        self,
        qualifier: ChatSoundAlertQualifer,
        jsonContents: dict[str, Any],
        message: str,
        volume: int | None
    ) -> FilePathChatSoundAlert:
        filePath = utils.getStrFromDict(jsonContents, 'filePath')

        return FilePathChatSoundAlert(
            qualifier = qualifier,
            filePath = filePath,
            message = message,
            volume = volume
        )

    def __parseSoundAlertChatSoundAlert(
        self,
        qualifier: ChatSoundAlertQualifer,
        jsonContents: dict[str, Any],
        message: str,
        volume: int | None
    ) -> SoundAlertChatSoundAlert:
        soundAlertString = utils.getStrFromDict(jsonContents, 'soundAlert')
        soundAlert = self.__soundAlertJsonMapper.requireSoundAlert(soundAlertString)

        return SoundAlertChatSoundAlert(
            qualifier = qualifier,
            soundAlert = soundAlert,
            message = message,
            volume = volume
        )
