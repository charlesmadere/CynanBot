import re
from typing import Pattern

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from CynanBot.pkmn.pokepediaJsonMapperInterface import \
    PokepediaJsonMapperInterface
from CynanBot.pkmn.pokepediaMachineType import PokepediaMachineType
from CynanBot.timber.timberInterface import TimberInterface


class PokepediaJsonMapper(PokepediaJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__machineTypeRegEx: Pattern = re.compile(r'^(HM|TM|TR)\d*$', re.IGNORECASE)

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

    async def parseMachineType(
        self,
        machineTypeString: str | None
    ) -> PokepediaMachineType | None:
        if not utils.isValidStr(machineTypeString):
            return None

        machineTypeMatch = self.__machineTypeRegEx.fullmatch(machineTypeString)

        if machineTypeMatch is None:
            return None

        machineTypePrefix = machineTypeMatch.group(1).upper()

        match machineTypePrefix:
            case 'HM': return PokepediaMachineType.HM
            case 'TM': return PokepediaMachineType.TM
            case 'TR': return PokepediaMachineType.TR
            case _:
                self.__timber.log('PokepediaJsonMapper', f'Encountered unknown PokepediaMachineType value: \"{machineTypeString}\"')
                return None

    async def requireBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor:
        berryFlavor = await self.parseBerryFlavor(jsonNumber)

        if berryFlavor is None:
            raise ValueError(f'Unable to parse \"{jsonNumber}\" into PokepediaBerryFlavor value!')

        return berryFlavor

    async def requireMachineType(
        self,
        machineTypeString: str | None
    ) -> PokepediaMachineType:
        machineType = await self.parseMachineType(machineTypeString)

        if machineType is None:
            raise ValueError(f'Unable to parse \"{machineTypeString}\" into PokepediaMachineType value!')
        
        return machineType
