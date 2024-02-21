from typing import Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaContestType import PokepediaContestType
from CynanBot.pkmn.pokepediaDamageClass import PokepediaDamageClass
from CynanBot.pkmn.pokepediaGeneration import PokepediaGeneration
from CynanBot.pkmn.pokepediaMachine import PokepediaMachine
from CynanBot.pkmn.pokepediaMoveGeneration import PokepediaMoveGeneration


class PokepediaMove():

    def __init__(
        self,
        contestType: Optional[PokepediaContestType],
        damageClass: PokepediaDamageClass,
        generationMachines: Optional[Dict[PokepediaGeneration, List[PokepediaMachine]]],
        generationMoves: Dict[PokepediaGeneration, PokepediaMoveGeneration],
        critRate: int,
        drain: int,
        flinchChance: int,
        moveId: int,
        initialGeneration: PokepediaGeneration,
        description: str,
        name: str,
        rawName: str
    ):
        assert contestType is None or isinstance(contestType, PokepediaContestType), f"malformed {contestType=}"
        assert isinstance(damageClass, PokepediaDamageClass), f"malformed {damageClass=}"
        if not utils.hasItems(generationMoves):
            raise ValueError(f'generationMoves argument is malformed: \"{generationMoves}\"')
        if not utils.isValidInt(critRate):
            raise ValueError(f'critRate argument is malformed: \"{critRate}\"')
        if not utils.isValidInt(drain):
            raise ValueError(f'drain argument is malformed: \"{drain}\"')
        if not utils.isValidInt(flinchChance):
            raise ValueError(f'flinchChance argument is malformed: \"{flinchChance}\"')
        if not utils.isValidInt(moveId):
            raise ValueError(f'moveId argument is malformed: \"{moveId}\"')
        assert isinstance(initialGeneration, PokepediaGeneration), f"malformed {initialGeneration=}"
        if not utils.isValidStr(description):
            raise ValueError(f'description argument is malformed: \"{description}\"')
        if not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')
        if not utils.isValidStr(rawName):
            raise ValueError(f'rawName argument is malformed: \"{rawName}\"')

        self.__contestType: Optional[PokepediaContestType] = contestType
        self.__damageClass: PokepediaDamageClass = damageClass
        self.__generationMachines: Optional[Dict[PokepediaGeneration, List[PokepediaMachine]]] = generationMachines
        self.__generationMoves: Dict[PokepediaGeneration, PokepediaMoveGeneration] = generationMoves
        self.__critRate: int = critRate
        self.__drain: int = drain
        self.__flinchChance: int = flinchChance
        self.__moveId: int = moveId
        self.__initialGeneration: PokepediaGeneration = initialGeneration
        self.__description: str = description
        self.__name: str = name
        self.__rawName: str = rawName

    def getContestType(self) -> Optional[PokepediaContestType]:
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

    def getGenerationMachines(self) -> Optional[Dict[PokepediaGeneration, List[PokepediaMachine]]]:
        return self.__generationMachines

    def getGenerationMoves(self) -> Dict[PokepediaGeneration, PokepediaMoveGeneration]:
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

    def toStrList(self) -> List[str]:
        strings: List[str] = list()
        strings.append(f'{self.getName()} — {self.getDescription()}')

        for gen in PokepediaGeneration:
            if gen in self.__generationMoves:
                genMove = self.__generationMoves[gen]
                strings.append(genMove.toStr())

        return strings
