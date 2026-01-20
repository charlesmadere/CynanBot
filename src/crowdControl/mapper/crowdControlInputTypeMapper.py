from .crowdControlInputTypeMapperInterface import CrowdControlInputTypeMapperInterface
from ..actions.crowdControlButton import CrowdControlButton
from ...users.crowdControl.crowdControlInputType import CrowdControlInputType


class CrowdControlInputTypeMapper(CrowdControlInputTypeMapperInterface):

    async def toButton(
        self,
        inputType: CrowdControlInputType | None,
    ) -> CrowdControlButton | None:
        if inputType is None:
            return None
        elif not isinstance(inputType, CrowdControlInputType):
            raise TypeError(f'inputType argument is malformed: \"{inputType}\"')

        match inputType:
            case CrowdControlInputType.BUTTON_A: return CrowdControlButton.BUTTON_A
            case CrowdControlInputType.BUTTON_B: return CrowdControlButton.BUTTON_B
            case CrowdControlInputType.BUTTON_C: return CrowdControlButton.BUTTON_C
            case CrowdControlInputType.BUTTON_X: return CrowdControlButton.BUTTON_X
            case CrowdControlInputType.BUTTON_Y: return CrowdControlButton.BUTTON_Y
            case CrowdControlInputType.BUTTON_Z: return CrowdControlButton.BUTTON_Z
            case CrowdControlInputType.DPAD_DOWN: return CrowdControlButton.DPAD_DOWN
            case CrowdControlInputType.DPAD_LEFT: return CrowdControlButton.DPAD_LEFT
            case CrowdControlInputType.DPAD_RIGHT: return CrowdControlButton.DPAD_RIGHT
            case CrowdControlInputType.DPAD_UP: return CrowdControlButton.DPAD_UP
            case CrowdControlInputType.GAME_SHUFFLE: raise ValueError(f'Encountered unsupported CrowdControlInputType: \"{inputType}\"')
            case CrowdControlInputType.SELECT: return CrowdControlButton.SELECT
            case CrowdControlInputType.START: return CrowdControlButton.START
            case CrowdControlInputType.TRIGGER_LEFT: return CrowdControlButton.TRIGGER_LEFT
            case CrowdControlInputType.TRIGGER_RIGHT: return CrowdControlButton.TRIGGER_RIGHT
            case CrowdControlInputType.USER_INPUT_BUTTON: raise ValueError(f'Encountered unsupported CrowdControlInputType: \"{inputType}\"')
            case _: raise ValueError(f'Encountered unknown CrowdControlInputType: \"{inputType}\"')
