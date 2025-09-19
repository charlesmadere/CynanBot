from typing import Final

from frozendict import frozendict

from .crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ..actions.crowdControlButton import CrowdControlButton
from ...misc import utils as utils
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class CrowdControlUserInputUtils(CrowdControlUserInputUtilsInterface):

    def __init__(
        self,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
    ):
        if not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')

        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils

        self.__buttonToUserInputs: Final[frozendict[CrowdControlButton, frozenset[str]]] = frozendict({
            CrowdControlButton.BUTTON_A: frozenset({ 'a' }),
            CrowdControlButton.BUTTON_B: frozenset({ 'b' }),
            CrowdControlButton.BUTTON_C: frozenset({ 'c' }),
            CrowdControlButton.BUTTON_X: frozenset({ 'x' }),
            CrowdControlButton.BUTTON_Y: frozenset({ 'y' }),
            CrowdControlButton.BUTTON_Z: frozenset({ 'z' }),
            CrowdControlButton.DPAD_DOWN: frozenset({ 'dn', 'down', 'dpad_dn', 'dpad dn', 'dpad_down', 'dpad down', 'down dpad' }),
            CrowdControlButton.DPAD_LEFT: frozenset({ 'left', 'dpad_left', 'dpad left', 'left_dpad', 'left dpad' }),
            CrowdControlButton.DPAD_RIGHT: frozenset({ 'right', 'dpad_right', 'dpad right', 'right_dpad', 'right dpad' }),
            CrowdControlButton.DPAD_UP: frozenset({ 'up', 'dpad_up', 'dpad up', 'up dpad' }),
            CrowdControlButton.SELECT: frozenset({ 'select', 'sel' }),
            CrowdControlButton.START: frozenset({ 'start', 'pause' }),
            CrowdControlButton.TRIGGER_LEFT: frozenset({ 'left trigger', 'left_trigger', 'l trigger', 'l_trigger', 'trigger_left', 'trigger left' }),
            CrowdControlButton.TRIGGER_RIGHT: frozenset({ 'right trigger', 'right_trigger', 'r trigger', 'r_trigger', 'trigger_right', 'trigger right' }),
        })

    async def parseButtonFromUserInput(
        self,
        userInput: str | None
    ) -> CrowdControlButton | None:
        if not utils.isValidStr(userInput):
            return None

        userInput = utils.cleanStr(userInput.lower())
        userInput = await self.__twitchMessageStringUtils.removeCheerStrings(userInput)

        for button, userInputs in self.__buttonToUserInputs.items():
            if userInput in userInputs:
                return button

        return None
