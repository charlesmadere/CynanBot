import locale

from .pokepediaDamageClass import PokepediaDamageClass
from .pokepediaElementType import PokepediaElementType
from .pokepediaGeneration import PokepediaGeneration
from ..misc import utils as utils


class PokepediaMoveGeneration():

    def __init__(
        self,
        accuracy: int | None,
        power: int | None,
        pp: int,
        damageClass: PokepediaDamageClass,
        elementType: PokepediaElementType,
        generation: PokepediaGeneration
    ):
        if not utils.isValidInt(pp):
            raise TypeError(f'pp argument is malformed: \"{pp}\"')
        elif not isinstance(damageClass, PokepediaDamageClass):
            raise TypeError(f'damageClass argument is malformed: \"{damageClass}\"')
        elif not isinstance(elementType, PokepediaElementType):
            raise TypeError(f'elementType argument is malformed: \"{elementType}\"')
        elif not isinstance(generation, PokepediaGeneration):
            raise TypeError(f'generation argument is malformed: \"{generation}\"')

        self.__accuracy: int | None = accuracy
        self.__power: int | None = power
        self.__pp: int = pp
        self.__damageClass: PokepediaDamageClass = damageClass
        self.__elementType: PokepediaElementType = elementType
        self.__generation: PokepediaGeneration = generation

    def getAccuracy(self) -> int | None:
        return self.__accuracy

    def getAccuracyStr(self) -> str:
        if self.hasAccuracy():
            formattedAccuracy = locale.format_string("%d", self.__accuracy, grouping = True)
            return f'{formattedAccuracy}%'
        else:
            raise RuntimeError(f'This PokepediaGenerationMove ({self}) does not have an accuracy value!')

    def getDamageClass(self) -> PokepediaDamageClass:
        return self.__damageClass

    def getElementType(self) -> PokepediaElementType:
        return self.__elementType

    def getGeneration(self) -> PokepediaGeneration:
        return self.__generation

    def getPower(self) -> int | None:
        return self.__power

    def getPowerStr(self) -> str:
        if self.hasPower():
            return locale.format_string("%d", self.__power, grouping = True)
        else:
            raise RuntimeError(f'This PokepediaGenerationMove ({self}) does not have a power value!')

    def getPp(self) -> int:
        return self.__pp

    def getPpStr(self) -> str:
        formattedPp = locale.format_string("%d", self.__pp, grouping = True)
        return f'{formattedPp}pp'

    def hasAccuracy(self) -> bool:
        return utils.isValidNum(self.__accuracy)

    def hasPower(self) -> bool:
        return utils.isValidNum(self.__power)

    def toStr(self) -> str:
        powerStr = ''
        if self.hasPower():
            powerStr = f'💪 {self.getPowerStr()}, '

        accuracyStr = ''
        if self.hasAccuracy():
            accuracyStr = f'🎯 {self.getAccuracyStr()}, '

        return f'{self.__generation.toShortStr()}: {powerStr}{accuracyStr}{self.getPpStr()}, {self.__elementType.getEmojiOrStr().lower()} type, {self.__damageClass.toStr().lower()}'
