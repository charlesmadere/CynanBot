import locale
from dataclasses import dataclass

from .pokepediaDamageClass import PokepediaDamageClass
from .pokepediaElementType import PokepediaElementType
from .pokepediaGeneration import PokepediaGeneration
from ..misc import utils as utils


@dataclass(frozen = True, slots = True)
class PokepediaMoveGeneration:
    accuracy: int | None
    power: int | None
    pp: int
    damageClass: PokepediaDamageClass
    elementType: PokepediaElementType
    generation: PokepediaGeneration

    def getAccuracyStr(self) -> str:
        if self.hasAccuracy():
            formattedAccuracy = locale.format_string("%d", self.accuracy, grouping = True)
            return f'{formattedAccuracy}%'
        else:
            raise RuntimeError(f'This PokepediaGenerationMove ({self}) does not have an accuracy value!')

    def getPowerStr(self) -> str:
        if self.hasPower():
            return locale.format_string("%d", self.power, grouping = True)
        else:
            raise RuntimeError(f'This PokepediaGenerationMove ({self}) does not have a power value!')

    def getPpStr(self) -> str:
        formattedPp = locale.format_string("%d", self.pp, grouping = True)
        return f'{formattedPp}pp'

    def hasAccuracy(self) -> bool:
        return utils.isValidInt(self.accuracy)

    def hasPower(self) -> bool:
        return utils.isValidInt(self.power)

    def toStr(self) -> str:
        powerStr = ''
        if self.hasPower():
            powerStr = f'💪 {self.getPowerStr()}, '

        accuracyStr = ''
        if self.hasAccuracy():
            accuracyStr = f'🎯 {self.getAccuracyStr()}, '

        return f'{self.generation.toShortStr()}: {powerStr}{accuracyStr}{self.getPpStr()}, {self.elementType.getEmojiOrStr().lower()} type, {self.damageClass.toStr().lower()}'
