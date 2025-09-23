from typing import Any, Final

from .pixelsDiceStateMapperInterface import PixelsDiceStateMapperInterface
from ..models.states.absPixelsDiceState import AbsPixelsDiceState
from ..models.states.pixelsDiceBatteryState import PixelsDiceBatteryState
from ..models.states.pixelsDiceRollState import PixelsDiceRollState
from ...misc import utils as utils

BATTERY_STATE: Final[int] = 34
ROLL_STATE: Final[int] = 3

class PixelsDiceStateMapper(PixelsDiceStateMapperInterface):

    async def map(
        self,
        data: bytearray | Any | None,
    ) -> AbsPixelsDiceState | None:
        if not isinstance(data, bytearray):
            return None

        if len(data) == 3 and data[0] == BATTERY_STATE:
            return PixelsDiceBatteryState(
                isCharging = utils.intToBool(data[2]),
                battery = data[1],
            )

        elif len(data) == 3 and data[0] == ROLL_STATE and data[1] == 1:
            return PixelsDiceRollState(
                roll = data[2] + 1,
            )

        else:
            # this is considered an unknown/unimplemented state
            return None
