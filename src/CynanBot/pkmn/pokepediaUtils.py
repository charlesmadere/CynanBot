import re
import traceback
from typing import Pattern

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaUtilsInterface import PokepediaUtilsInterface
from CynanBot.timber.timberInterface import TimberInterface


class PokepediaUtils(PokepediaUtilsInterface):

    def __init__(self, timber: TimberInterface):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__timber: TimberInterface = timber

        self.__machineNumberRegEx: Pattern = re.compile(r'^(hm|tm|tr)(\d+)$', re.IGNORECASE)

    async def getMachineNumber(self, machineName: str) -> int:
        if not utils.isValidStr(machineName):
            raise ValueError(f'machineName argument is malformed: \"{machineName}\"')

        machineNumberMatch = self.__machineNumberRegEx.fullmatch(machineName)

        if machineNumberMatch is None or not utils.isValidStr(machineNumberMatch.group(2)):
            raise RuntimeError(f'Unable to convert machine name (\"{machineName}\") into a machine number ({machineNumberMatch=})')

        try:
            return int(machineNumberMatch.group(2))
        except (SyntaxError, TypeError, ValueError) as e:
            self.__timber.log('PkMoveCommand', f'Unable to convert machine name (\"{machineName}\") into a machine number ({machineNumberMatch=}) {e}', e, traceback.format_exc())
            raise RuntimeError(f'Unable to convert machine name (\"{machineName}\") into a machine number ({machineNumberMatch=}): {e}')
