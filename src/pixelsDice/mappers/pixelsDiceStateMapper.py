from typing import Any, Final

from .pixelsDiceStateMapperInterface import PixelsDiceStateMapperInterface
from ..models.states.absPixelsDiceState import AbsPixelsDiceState
from ..models.states.pixelsDiceRollState import PixelsDiceRollState

FINISHED_ROLL_STATE: Final[int] = 1
ROLL_EVENT: Final[int] = 3

class PixelsDiceStateMapper(PixelsDiceStateMapperInterface):

    async def map(
        self,
        rawData: bytearray | Any | None,
    ) -> AbsPixelsDiceState | None:
        if not isinstance(rawData, bytearray) or len(rawData) == 0:
            return None

        if rawData[0] == ROLL_EVENT and rawData[1] == FINISHED_ROLL_STATE:
            return PixelsDiceRollState(
                rawData = rawData,
                roll = rawData[2] + 1,
            )

        else:
            # this is considered an unknown/currently unimplemented state
            return None
