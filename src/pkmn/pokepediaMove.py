from .pokepediaContestType import PokepediaContestType
from .pokepediaDamageClass import PokepediaDamageClass
from .pokepediaGeneration import PokepediaGeneration
from .pokepediaMachine import PokepediaMachine
from .pokepediaMoveGeneration import PokepediaMoveGeneration
from ..misc import utils as utils


class PokepediaMove:

    def __init__(
        self,
        contestType: PokepediaContestType | None,
        damageClass: PokepediaDamageClass,
        generationMachines: dict[PokepediaGeneration, list[PokepediaMachine]] | None,
        generationMoves: dict[PokepediaGeneration, PokepediaMoveGeneration],
        critRate: int,
        drain: int,
        flinchChance: int,
        moveId: int,
        initialGeneration: PokepediaGeneration,
        description: str,
        name: str,
        rawName: str
    ):
        if contestType is not None and not isinstance(contestType, PokepediaContestType):
            raise TypeError(f'contestType argument is malformed: \"{contestType}\"')
        elif not isinstance(damageClass, PokepediaDamageClass):
            raise TypeError(f'damageClass argument is malformed: \"{damageClass}\"')
        elif not utils.hasItems(generationMoves):
            raise TypeError(f'generationMoves argument is malformed: \"{generationMoves}\"')
        elif not utils.isValidInt(critRate):
            raise TypeError(f'critRate argument is malformed: \"{critRate}\"')
        elif not utils.isValidInt(drain):
            raise TypeError(f'drain argument is malformed: \"{drain}\"')
        elif not utils.isValidInt(flinchChance):
            raise TypeError(f'flinchChance argument is malformed: \"{flinchChance}\"')
        elif not utils.isValidInt(moveId):
            raise TypeError(f'moveId argument is malformed: \"{moveId}\"')
        elif not isinstance(initialGeneration, PokepediaGeneration):
            raise TypeError(f'initialGeneration argument is malformed: \"{initialGeneration}\"')
        elif not utils.isValidStr(description):
            raise TypeError(f'description argument is malformed: \"{description}\"')
        elif not utils.isValidStr(name):
            raise TypeError(f'name argument is malformed: \"{name}\"')
        elif not utils.isValidStr(rawName):
            raise TypeError(f'rawName argument is malformed: \"{rawName}\"')

        self.__contestType: PokepediaContestType | None = contestType
        self.__damageClass: PokepediaDamageClass = damageClass
        self.__generationMachines: dict[PokepediaGeneration, list[PokepediaMachine]] | None = generationMachines
        self.__generationMoves: dict[PokepediaGeneration, PokepediaMoveGeneration] = generationMoves
        self.__critRate: int = critRate
        self.__drain: int = drain
        self.__flinchChance: int = flinchChance
        self.__moveId: int = moveId
        self.__initialGeneration: PokepediaGeneration = initialGeneration
        self.__description: str = description
        self.__name: str = name
        self.__rawName: str = rawName

    def getContestType(self) -> PokepediaContestType | None:
        return self.__contestType

    def getCritRate(self) -> int:
        return self.__critRate

    def getDamageClass(self) -> PokepediaDamageClass:
        return self.__damageClass

    def getDescription(self) -> str:
        return self.__description

    def getDrain(self) -> int:
        return self.__drain

    def getFlinchChance(self) -> int:
        return self.__flinchChance

    def getGenerationMachines(self) -> dict[PokepediaGeneration, list[PokepediaMachine]] | None:
        return self.__generationMachines

    def getGenerationMoves(self) -> dict[PokepediaGeneration, PokepediaMoveGeneration]:
        return self.__generationMoves

    def getInitialGeneration(self) -> PokepediaGeneration:
        return self.__initialGeneration

    def getMoveId(self) -> int:
        return self.__moveId

    def getName(self) -> str:
        return self.__name

    def getRawName(self) -> str:
        return self.__rawName

    def hasContestType(self) -> bool:
        return self.__contestType is not None

    def hasMachines(self) -> bool:
        return utils.hasItems(self.__generationMachines)

    def toStrList(self) -> list[str]:
        strings: list[str] = list()
        strings.append(f'{self.getName()} — {self.getDescription()}')

        for gen in PokepediaGeneration:
            if gen in self.__generationMoves:
                genMove = self.__generationMoves[gen]
                strings.append(genMove.toStr())

        return strings
