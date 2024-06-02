import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from CynanBot.pkmn.pokepediaJsonMapperInterface import \
    PokepediaJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface


class PokepediaJsonMapper(PokepediaJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor | None:
        if not utils.isValidInt(jsonNumber):
            return None

        match jsonNumber:
            case 1: return PokepediaBerryFlavor.SPICY
            case 2: return PokepediaBerryFlavor.DRY
            case 3: return PokepediaBerryFlavor.SWEET
            case 4: return PokepediaBerryFlavor.BITTER
            case 5: return PokepediaBerryFlavor.SOUR
            case _:
                self.__timber.log('PokepediaJsonMapper', f'Encountered unknown PokepediaBerryFlavor value: \"{jsonNumber}\"')
                return None

    async def requireBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor:
        berryFlavor = await self.parseBerryFlavor(jsonNumber)

        if berryFlavor is None:
            raise ValueError(f'Unable to parse \"{jsonNumber}\" into PokepediaBerryFlavor value!')

        return berryFlavor
