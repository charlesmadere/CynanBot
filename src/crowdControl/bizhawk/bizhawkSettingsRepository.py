from typing import Any

from .bizhawkKey import BizhawkKey
from .bizhawkKeyMapperInterface import BizhawkKeyMapperInterface
from .bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from ..actions.crowdControlButton import CrowdControlButton
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class BizhawkSettingsRepository(BizhawkSettingsRepositoryInterface):

    def __init__(
        self,
        bizhawkKeyMapper: BizhawkKeyMapperInterface,
        settingsJsonReader: JsonReaderInterface
    ):
        if not isinstance(bizhawkKeyMapper, BizhawkKeyMapperInterface):
            raise TypeError(f'bizhawkKeyMapper argument is malformed: \"{bizhawkKeyMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__bizhawkKeyMapper: BizhawkKeyMapperInterface = bizhawkKeyMapper
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getButtonKeyBind(
        self,
        button: CrowdControlButton
    ) -> BizhawkKey | None:
        if not isinstance(button, CrowdControlButton):
            raise TypeError(f'button argument is malformed: \"{button}\"')

        jsonContents = await self.__readJson()
        keyBindString: str | None = None

        match button:
            case CrowdControlButton.BUTTON_A:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonA',
                    fallback = ''
                )

            case CrowdControlButton.BUTTON_B:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonB',
                    fallback = ''
                )

            case CrowdControlButton.BUTTON_X:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonX',
                    fallback = ''
                )

            case CrowdControlButton.BUTTON_Y:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonY',
                    fallback = ''
                )

            case CrowdControlButton.DPAD_DOWN:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadDown',
                    fallback = ''
                )

            case CrowdControlButton.DPAD_LEFT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadLeft',
                    fallback = ''
                )

            case CrowdControlButton.DPAD_RIGHT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadRight',
                    fallback = ''
                )

            case CrowdControlButton.DPAD_UP:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadUp',
                    fallback = ''
                )

            case CrowdControlButton.SELECT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindSelect',
                    fallback = ''
                )

            case CrowdControlButton.START:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindStart',
                    fallback = ''
                )

            case CrowdControlButton.TRIGGER_LEFT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindTriggerLeft',
                    fallback = ''
                )

            case CrowdControlButton.TRIGGER_RIGHT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindTriggerRight',
                    fallback = ''
                )

        if not utils.isValidStr(keyBindString):
            return None

        return await self.__bizhawkKeyMapper.fromString(keyBindString)

    async def getGameShuffleKeyBind(self) -> BizhawkKey | None:
        jsonContents = await self.__readJson()

        keyBindString = utils.getStrFromDict(
            d = jsonContents,
            key = 'keyBindGameShuffle',
            fallback = ''
        )

        if not utils.isValidStr(keyBindString):
            return None

        return await self.__bizhawkKeyMapper.fromString(keyBindString)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from bizhawk settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
