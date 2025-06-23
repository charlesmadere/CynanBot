from typing import Any, Final

from .beanChanceStep import BeanChanceStep
from .beanChanceSteps import BeanChanceSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class BeanChanceWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__steps: Final[BeanChanceSteps] = BeanChanceSteps()
        self.__bits: int | None = None
        self.__maximumPerDay: int | None = None
        self.__randomChance: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.BEAN_CHANCE

    @property
    def currentStep(self) -> BeanChanceStep:
        return self.__steps.currentStep

    @property
    def maximumPerDay(self) -> int | None:
        return self.__maximumPerDay

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__maximumPerDay=}, {self.__randomChance=}'

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireBits(self) -> int:
        bits = self.__bits

        if bits is None:
            raise ValueError(f'bits value has not been set: ({self=})')

        return bits

    def requireRandomChance(self) -> int:
        randomChance = self.__randomChance

        if randomChance is None:
            raise ValueError(f'randomChance value has not been set: ({self=})')

        return randomChance

    def setBits(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits = bits

    def setMaximumPerDay(self, maximumPerDay: int | None):
        if maximumPerDay is not None and not utils.isValidInt(maximumPerDay):
            raise TypeError(f'maximumPerDay argument is malformed: \"{maximumPerDay}\"')
        elif maximumPerDay is not None and (maximumPerDay < 1 or maximumPerDay > utils.getIntMaxSafeSize()):
            raise ValueError(f'maximumPerDay argument is out of bounds: {maximumPerDay}')

        self.__maximumPerDay = maximumPerDay

    def setRandomChance(self, randomChance: int):
        if not utils.isValidInt(randomChance):
            raise TypeError(f'randomChance argument is malformed: \"{randomChance}\"')
        elif randomChance < 1 or randomChance > 100:
            raise ValueError(f'randomChance argument is out of bounds: {randomChance}')

        self.__randomChance = randomChance

    @property
    def steps(self) -> BeanChanceSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'currentStep': self.currentStep,
            'maximumPerDay': self.__maximumPerDay,
            'randomChance': self.__randomChance,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
