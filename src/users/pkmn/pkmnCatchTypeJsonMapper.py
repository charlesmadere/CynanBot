from typing import Any

from .pkmnCatchType import PkmnCatchType
from .pkmnCatchTypeJsonMapperInterface import PkmnCatchTypeJsonMapperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class PkmnCatchTypeJsonMapper(PkmnCatchTypeJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    def parse(self, catchType: str | Any | None) -> PkmnCatchType | None:
        if not utils.isValidStr(catchType):
            return None

        catchType = catchType.lower()

        match catchType:
            case 'great': return PkmnCatchType.GREAT
            case 'normal': return PkmnCatchType.NORMAL
            case 'ultra': return PkmnCatchType.ULTRA
            case _:
                self.__timber.log('PkmnCatchTypeJsonMapper', f'Encountered unknown PkmnCatchType: \"{catchType}\"')
                return None

    def require(self, catchType: str | Any | None) -> PkmnCatchType:
        result = self.parse(catchType)

        if result is None:
            raise ValueError(f'Unable to parse \"{catchType}\" into PkmnCatchType value!')

        return result
