import re
from typing import Pattern

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaUtilsInterface import PokepediaUtilsInterface


class PokepediaUtils(PokepediaUtilsInterface):

    def __init__(self):
        self.__machineNumberRegEx: Pattern = re.compile(r'^(hm|tm|tr)(\d+)$', re.IGNORECASE)

    async def getMachineNumber(self, machineName: str) -> int:
        if not utils.isValidStr(machineName):
            raise ValueError(f'machineName argument is malformed: \"{machineName}\"')

        machineNumberMatch = self.__machineNumberRegEx.fullmatch(machineName)

        if machineNumberMatch is None or not utils.isValidStr(machineNumberMatch.group(2)):
            raise RuntimeError(f'Unable to convert machine name (\"{machineName}\") into a machine number ({machineNumberMatch=})')

        return int(machineNumberMatch.group(2))
