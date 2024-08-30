import re
from typing import Pattern

from frozendict import frozendict

from .crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ..actions.crowdControlButton import CrowdControlButton
from ...misc import utils as utils


class CrowdControlUserInputUtils(CrowdControlUserInputUtilsInterface):

    def __init__(self):
        self.__buttonToUserInputs: frozendict[CrowdControlButton, frozenset[str]] = frozendict({
            CrowdControlButton.BUTTON_A: frozenset({ 'a' }),
            CrowdControlButton.BUTTON_B: frozenset({ 'b' }),
            CrowdControlButton.BUTTON_X: frozenset({ 'x' }),
            CrowdControlButton.BUTTON_Y: frozenset({ 'y' }),
            CrowdControlButton.DPAD_DOWN: frozenset({ 'dn', 'down', 'dpad_dn', 'dpad dn', 'dpad_down', 'dpad down', 'down dpad' }),
            CrowdControlButton.DPAD_LEFT: frozenset({ 'left', 'dpad_left', 'dpad left', 'left dpad' }),
            CrowdControlButton.DPAD_RIGHT: frozenset({ 'right', 'dpad_right', 'dpad right', 'right dpad' }),
            CrowdControlButton.DPAD_UP: frozenset({ 'up', 'dpad_up', 'dpad up', 'up dpad' }),
            CrowdControlButton.SELECT: frozenset({ 'select', 'sel' }),
            CrowdControlButton.START: frozenset({ 'start', 'pause' }),
            CrowdControlButton.TRIGGER_LEFT: frozenset({ 'left trigger', 'left_trigger', 'trigger_left', 'trigger left' }),
            CrowdControlButton.TRIGGER_RIGHT: frozenset({ 'right trigger', 'right_trigger', 'trigger_right', 'trigger right' })
        })

        self.__cheerRegEx: Pattern = re.compile(r'^cheer\d+\s+', re.IGNORECASE)
        self.__extraWhitespaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    async def parseButtonFromUserInput(
        self,
        userInput: str | None
    ) -> CrowdControlButton | None:
        if not utils.isValidStr(userInput):
            return None

        userInput = userInput.strip().lower()
        userInput = self.__cheerRegEx.sub('', userInput).strip()
        userInput = self.__extraWhitespaceRegEx.sub(' ', userInput).strip()

        for button, userInputs in self.__buttonToUserInputs.items():
            if userInput in userInputs:
                return button

        return None
