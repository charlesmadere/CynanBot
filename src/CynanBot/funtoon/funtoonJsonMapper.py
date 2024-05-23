from CynanBot.funtoon.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from CynanBot.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType


class FuntoonJsonMapper(FuntoonJsonMapperInterface):

    async def serializePkmnCatchType(
        self,
        pkmnCatchType: FuntoonPkmnCatchType
    ) -> str:
        if not isinstance(pkmnCatchType, FuntoonPkmnCatchType):
            raise TypeError(f'pkmnCatchType argument is malformed: \"{pkmnCatchType}\"')

        match pkmnCatchType:
            case FuntoonPkmnCatchType.GREAT: return 'great'
            case FuntoonPkmnCatchType.NORMAL: return 'normal'
            case FuntoonPkmnCatchType.ULTRA: return 'ultra'
            case _: raise ValueError(f'unknown FuntoonPkmnCatchType: \"{self}\"')
