from typing import Any

from .soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ..soundAlert import SoundAlert
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class SoundPlayerSettingsRepository(SoundPlayerSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

    async def areShiniesEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'shiniesEnabled', fallback = True)

    async def clearCaches(self):
        self.__settingsCache = None

    async def getFilePathFor(self, soundAlert: SoundAlert) -> str | None:
        if not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        jsonContents = await self.__readJson()
        filePath: str | None = None

        match soundAlert:
            case SoundAlert.BEAN:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'beanFilePath',
                    fallback = 'Bean Alert.mp3'
                )

            case SoundAlert.CHEER:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'cheerFilePath',
                    fallback = 'Cheer Alert.mp3'
                )

            case SoundAlert.CLICK_NAVIGATION:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'clickNavigationFilePath',
                    fallback = 'Click Navigation.mp3'
                )

            case SoundAlert.GRENADE_1:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'grenade1FilePath',
                    fallback = 'Grenade 1.mp3'
                )

            case SoundAlert.GRENADE_2:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'grenade2FilePath',
                    fallback = 'Grenade 2.mp3'
                )

            case SoundAlert.GRENADE_3:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'grenade3FilePath',
                    fallback = 'Grenade 3.mp3'
                )

            case SoundAlert.JACKPOT:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'jackpotFilePath',
                    fallback = 'Jackpot.mp3'
                )

            case SoundAlert.LAUNCH_TNT:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'launchTntFilePath',
                    fallback = 'Launch TNT.mp3'
                )

            case SoundAlert.MEGA_GRENADE_1:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'megaGrenade1FilePath',
                    fallback = 'Mega Grenade 1.mp3'
                )

            case SoundAlert.MEGA_GRENADE_2:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'megaGrenade2FilePath',
                    fallback = 'Mega Grenade 2.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_01:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption01FilePath',
                    fallback = 'Point Redemption 01.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_02:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption02FilePath',
                    fallback = 'Point Redemption 02.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_03:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption03FilePath',
                    fallback = 'Point Redemption 03.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_04:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption04FilePath',
                    fallback = 'Point Redemption 04.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_05:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption05FilePath',
                    fallback = 'Point Redemption 05.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_06:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption06FilePath',
                    fallback = 'Point Redemption 06.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_07:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption07FilePath',
                    fallback = 'Point Redemption 07.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_08:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption08FilePath',
                    fallback = 'Point Redemption 08.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_09:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption09FilePath',
                    fallback = 'Point Redemption 09.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_10:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption10FilePath',
                    fallback = 'Point Redemption 10.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_11:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption11FilePath',
                    fallback = 'Point Redemption 11.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_12:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption12FilePath',
                    fallback = 'Point Redemption 12.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_13:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption13FilePath',
                    fallback = 'Point Redemption 13.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_14:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption14FilePath',
                    fallback = 'Point Redemption 14.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_15:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption15FilePath',
                    fallback = 'Point Redemption 15.mp3'
                )

            case SoundAlert.POINT_REDEMPTION_16:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'pointRedemption16FilePath',
                    fallback = 'Point Redemption 16.mp3'
                )

            case SoundAlert.RAID:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'raidFilePath',
                    fallback = 'Raid Alert.mp3'
                )

            case SoundAlert.SPLAT:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'splatFilePath',
                    fallback = 'Splat.mp3'
                )

            case SoundAlert.SUBSCRIBE:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'subscribeFilePath',
                    fallback = 'Subscribe Alert.mp3'
                )

            case SoundAlert.TNT:
                filePath = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'tntFilePath',
                    fallback = 'TNT.mp3'
                )

            case _:
                raise RuntimeError(f'Sound path for SoundAlert \"{soundAlert}\" is undefined!')

        if not utils.isValidStr(filePath):
            return None

        return filePath

    async def getMediaPlayerVolume(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'mediaPlayerVolume', fallback = 100)

    async def getShinyProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'shinyProbability', fallback = 0.02)

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'enabled', fallback = True)

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Sound Player settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
