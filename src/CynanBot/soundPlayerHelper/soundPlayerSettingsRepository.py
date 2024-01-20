from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface


class SoundPlayerSettingsRepository(SoundPlayerSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise ValueError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: Optional[Dict[str, Any]] = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getFilePathFor(self, soundAlert: SoundAlert) -> Optional[str]:
        if not isinstance(soundAlert, SoundAlert):
            raise ValueError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        jsonContents = await self.__readJson()

        if soundAlert is SoundAlert.CHEER:
            return utils.getStrFromDict(
                d = jsonContents,
                key = 'cheerFileName',
                fallback = 'src/Bit Alert.wav'
            )
        elif soundAlert is SoundAlert.RAID:
            return utils.getStrFromDict(
                d = jsonContents,
                key = 'raidFileName',
                fallback = 'src/Raid Alert.wav'
            )
        elif soundAlert is SoundAlert.SUBSCRIBE:
            return utils.getStrFromDict(
                d = jsonContents,
                key = 'subscribeFileName',
                fallback = 'src/Subscriber Alert.wav'
            )
        else:
            raise RuntimeError(f'Sound path for SoundAlert \"{soundAlert}\" is undefined!')

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
