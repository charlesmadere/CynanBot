import re
from typing import Any, Collection, Final, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ..actions.crowdControlButton import CrowdControlButton
from ...misc import utils as utils


class CrowdControlUserInputUtils(CrowdControlUserInputUtilsInterface):

    def __init__(self):
        self.__buttonRegExes: Final[frozendict[CrowdControlButton, Collection[Pattern]]] = self.__buildButtonRegExes()

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
            CrowdControlButton.TRIGGER_LEFT: frozenset({ 'left trigger', 'left_trigger', 'l trigger', 'l_trigger', 'trigger_left', 'trigger-left', 'trigger left' }),
            CrowdControlButton.TRIGGER_RIGHT: frozenset({ 'right trigger', 'right_trigger', 'r trigger', 'r_trigger', 'trigger_right', 'trigger-right', 'trigger right' }),
        })

    def __buildButtonRegExes(self) -> frozendict[CrowdControlButton, Collection[Pattern]]:
        buttonA: FrozenList[Pattern] = FrozenList()
        buttonA.append(re.compile(r'^\s*a\s*$', re.IGNORECASE))
        buttonA.freeze()

        buttonB: FrozenList[Pattern] = FrozenList()
        buttonB.append(re.compile(r'^\s*b\s*$', re.IGNORECASE))
        buttonB.freeze()

        buttonC: FrozenList[Pattern] = FrozenList()
        buttonC.append(re.compile(r'^\s*c\s*$', re.IGNORECASE))
        buttonC.freeze()

        buttonX: FrozenList[Pattern] = FrozenList()
        buttonX.append(re.compile(r'^\s*x\s*$', re.IGNORECASE))
        buttonX.freeze()

        buttonY: FrozenList[Pattern] = FrozenList()
        buttonY.append(re.compile(r'^\s*y\s*$', re.IGNORECASE))
        buttonY.freeze()

        buttonZ: FrozenList[Pattern] = FrozenList()
        buttonZ.append(re.compile(r'^\s*z\s*$', re.IGNORECASE))
        buttonZ.freeze()

        dpadDown: FrozenList[Pattern] = FrozenList()
        dpadDown.append(re.compile(r'^\s*d(?:ow)?n\s*$', re.IGNORECASE))
        dpadDown.append(re.compile(r'^\s*dpad(?:\s+|_|-)?d(?:ow)?n\s*$', re.IGNORECASE))
        dpadDown.append(re.compile(r'^\s*d(?:ow)?n(?:\s+|_|-)?dpad\s*$', re.IGNORECASE))
        dpadDown.freeze()

        dpadLeft: FrozenList[Pattern] = FrozenList()
        dpadLeft.append(re.compile(r'^\s*left\s*$', re.IGNORECASE))
        dpadLeft.append(re.compile(r'^\s*dpad(?:\s+|_|-)?left\s*$', re.IGNORECASE))
        dpadLeft.append(re.compile(r'^\s*left(?:\s+|_|-)?dpad\s*$', re.IGNORECASE))
        dpadLeft.freeze()

        dpadRight: FrozenList[Pattern] = FrozenList()
        dpadRight.append(re.compile(r'^\s*right\s*$', re.IGNORECASE))
        dpadRight.append(re.compile(r'^\s*dpad(?:\s+|_|-)?right\s*$', re.IGNORECASE))
        dpadRight.append(re.compile(r'^\s*right(?:\s+|_|-)?dpad\s*$', re.IGNORECASE))
        dpadRight.freeze()

        dpadUp: FrozenList[Pattern] = FrozenList()
        dpadUp.append(re.compile(r'^\s*up\s*$', re.IGNORECASE))
        dpadUp.append(re.compile(r'^\s*dpad(?:\s+|_|-)?up\s*$', re.IGNORECASE))
        dpadUp.append(re.compile(r'^\s*up(?:\s+|_|-)?dpad\s*$', re.IGNORECASE))
        dpadUp.freeze()

        buttonSelect: FrozenList[Pattern] = FrozenList()
        buttonSelect.append(re.compile(r'^\s*sel(?:ect)?\s*$', re.IGNORECASE))
        buttonSelect.freeze()

        buttonStart: FrozenList[Pattern] = FrozenList()
        buttonStart.append(re.compile(r'^\s*start?\s*$', re.IGNORECASE))
        buttonStart.append(re.compile(r'^\s*pause?\s*$', re.IGNORECASE))
        buttonStart.freeze()

        triggerLeft: FrozenList[Pattern] = FrozenList()
        triggerLeft.append(re.compile(r'^\s*l(?:eft)?(?:\s+|_|-)?trigger\s*$', re.IGNORECASE))
        triggerLeft.append(re.compile(r'^\s*trigger(?:\s+|_|-)?l(?:eft)?\s*$', re.IGNORECASE))
        triggerLeft.freeze()

        triggerRight: FrozenList[Pattern] = FrozenList()
        triggerRight.append(re.compile(r'^\s*r(?:ight)?(?:\s+|_|-)?trigger\s*$', re.IGNORECASE))
        triggerRight.append(re.compile(r'^\s*trigger(?:\s+|_|-)?r(?:ight)?\s*$', re.IGNORECASE))
        triggerRight.freeze()

        return frozendict({
            CrowdControlButton.BUTTON_A: buttonA,
            CrowdControlButton.BUTTON_B: buttonB,
            CrowdControlButton.BUTTON_C: buttonC,
            CrowdControlButton.BUTTON_X: buttonX,
            CrowdControlButton.BUTTON_Y: buttonY,
            CrowdControlButton.BUTTON_Z: buttonZ,
            CrowdControlButton.DPAD_DOWN: dpadDown,
            CrowdControlButton.DPAD_LEFT: dpadLeft,
            CrowdControlButton.DPAD_RIGHT: dpadRight,
            CrowdControlButton.DPAD_UP: dpadUp,
            CrowdControlButton.SELECT: buttonSelect,
            CrowdControlButton.START: buttonStart,
            CrowdControlButton.TRIGGER_LEFT: triggerLeft,
            CrowdControlButton.TRIGGER_RIGHT: triggerRight,
        })

    async def parseButtonFromUserInput(
        self,
        userInput: str | Any | None,
    ) -> CrowdControlButton | None:
        if not utils.isValidStr(userInput):
            return None

        userInput = utils.cleanStr(userInput)
        if not utils.isValidStr(userInput):
            return None

        for button, buttonRegExes in self.__buttonRegExes.items():
            for buttonRegEx in buttonRegExes:
                if buttonRegEx.fullmatch(userInput) is not None:
                    return button

        return None
