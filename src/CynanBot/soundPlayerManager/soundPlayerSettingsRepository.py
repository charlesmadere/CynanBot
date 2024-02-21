from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface


class SoundPlayerSettingsRepository(SoundPlayerSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        assert isinstance(settingsJsonReader, JsonReaderInterface), f"malformed {settingsJsonReader=}"

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: Optional[Dict[str, Any]] = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getFilePathFor(self, soundAlert: SoundAlert) -> Optional[str]:
        assert isinstance(soundAlert, SoundAlert), f"malformed {soundAlert=}"

        jsonContents = await self.__readJson()
        filePath: Optional[str] = None

        if soundAlert is SoundAlert.CHEER:
            filePath = utils.getStrFromDict(
                d = jsonContents,
                key = 'cheerFilePath',
                fallback = 'Cheer Alert.mp3'
            )
        elif soundAlert is SoundAlert.RAID:
            filePath = utils.getStrFromDict(
                d = jsonContents,
                key = 'raidFilePath',
                fallback = 'Raid Alert.mp3'
            )
        elif soundAlert is SoundAlert.SUBSCRIBE:
            filePath = utils.getStrFromDict(
                d = jsonContents,
                key = 'subscribeFilePath',
                fallback = 'Subscribe Alert.mp3'
            )
        else:
            raise RuntimeError(f'Sound path for SoundAlert \"{soundAlert}\" is undefined!')

        if not utils.isValidStr(filePath):
            return None

        return utils.cleanPath(filePath)

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'enabled', fallback = True)

    async def __readJson(self) -> Dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: Optional[Dict[str, Any]] = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from Sound Player settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
