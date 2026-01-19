from typing import Any, Final

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
        settingsJsonReader: JsonReaderInterface,
        defaultGameShuffleKeyBind: BizhawkKey = BizhawkKey.F15,
    ):
        if not isinstance(bizhawkKeyMapper, BizhawkKeyMapperInterface):
            raise TypeError(f'bizhawkKeyMapper argument is malformed: \"{bizhawkKeyMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultGameShuffleKeyBind, BizhawkKey):
            raise TypeError(f'defaultGameShuffleKeyBind argument is malformed: \"{defaultGameShuffleKeyBind}\"')

        self.__bizhawkKeyMapper: Final[BizhawkKeyMapperInterface] = bizhawkKeyMapper
        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultGameShuffleKeyBind: Final[BizhawkKey] = defaultGameShuffleKeyBind

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getButtonKeyBind(
        self,
        button: CrowdControlButton,
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
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.X),
                )

            case CrowdControlButton.BUTTON_B:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonB',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.Z),
                )

            case CrowdControlButton.BUTTON_C:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonC',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.C),
                )

            case CrowdControlButton.BUTTON_X:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonX',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.S),
                )

            case CrowdControlButton.BUTTON_Y:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonY',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.A),
                )

            case CrowdControlButton.BUTTON_Z:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindButtonZ',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.D),
                )

            case CrowdControlButton.DPAD_DOWN:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadDown',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.ARROW_DOWN),
                )

            case CrowdControlButton.DPAD_LEFT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadLeft',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.ARROW_LEFT),
                )

            case CrowdControlButton.DPAD_RIGHT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadRight',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.ARROW_RIGHT),
                )

            case CrowdControlButton.DPAD_UP:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindDpadUp',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.ARROW_UP),
                )

            case CrowdControlButton.SELECT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindSelect',
                    fallback = '',
                )

            case CrowdControlButton.START:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindStart',
                    fallback = await self.__bizhawkKeyMapper.toString(BizhawkKey.ENTER),
                )

            case CrowdControlButton.TRIGGER_LEFT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindTriggerLeft',
                    fallback = '',
                )

            case CrowdControlButton.TRIGGER_RIGHT:
                keyBindString = utils.getStrFromDict(
                    d = jsonContents,
                    key = 'keyBindTriggerRight',
                    fallback = '',
                )

        if not utils.isValidStr(keyBindString):
            return None

        return await self.__bizhawkKeyMapper.fromString(keyBindString)

    async def getGameShuffleKeyBind(self) -> BizhawkKey | None:
        jsonContents = await self.__readJson()

        keyBindString = utils.getStrFromDict(
            d = jsonContents,
            key = 'keyBindGameShuffle',
            fallback = await self.__bizhawkKeyMapper.toString(self.__defaultGameShuffleKeyBind),
        )

        if not utils.isValidStr(keyBindString):
            return None

        return await self.__bizhawkKeyMapper.fromString(keyBindString)

    async def getProcessName(self) -> str:
        jsonContents = await self.__readJson()

        return utils.getStrFromDict(
            d = jsonContents,
            key = 'processName',
            fallback = 'EmuHawk',
        )

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from bizhawk settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
