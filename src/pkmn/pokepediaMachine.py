from .pokepediaGeneration import PokepediaGeneration
from .pokepediaMachineType import PokepediaMachineType
from ..misc import utils as utils


class PokepediaMachine():

    def __init__(
        self,
        machineId: int,
        machineNumber: int,
        generation: PokepediaGeneration,
        machineType: PokepediaMachineType,
        machineName: str,
        moveName: str
    ):
        if not utils.isValidInt(machineId):
            raise ValueError(f'machineId argument is malformed: \"{machineId}\"')
        elif not utils.isValidInt(machineNumber):
            raise ValueError(f'machineNumber argument is malformed: \"{machineNumber}\"')
        elif not isinstance(generation, PokepediaGeneration):
            raise ValueError(f'generation argument is malformed: \"{generation}\"')
        elif not isinstance(machineType, PokepediaMachineType):
            raise ValueError(f'machineType argment is malformed: \"{machineType}\"')
        elif not utils.isValidStr(machineName):
            raise ValueError(f'machineName argument is malformed: \"{machineName}\"')
        elif not utils.isValidStr(moveName):
            raise ValueError(f'moveName argument is malformed: \"{moveName}\"')

        self.__machineId: int = machineId
        self.__machineNumber: int = machineNumber
        self.__generation: PokepediaGeneration = generation
        self.__machineType: PokepediaMachineType = machineType
        self.__machineName: str = machineName
        self.__moveName: str = moveName

    def getGeneration(self) -> PokepediaGeneration:
        return self.__generation

    def getMachineId(self) -> int:
        return self.__machineId

    def getMachineName(self) -> str:
        return self.__machineName

    def getMachineNumber(self) -> int:
        return self.__machineNumber

    def getMachineType(self) -> PokepediaMachineType:
        return self.__machineType

    def getMoveName(self) -> str:
        return self.__moveName
