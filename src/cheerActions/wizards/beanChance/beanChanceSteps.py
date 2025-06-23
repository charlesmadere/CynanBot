from .beanChanceStep import BeanChanceStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...cheerActionType import CheerActionType


class BeanChanceSteps(AbsSteps):

    def __init__(self):
        self.__step = BeanChanceStep.BITS

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.BEAN_CHANCE

    @property
    def currentStep(self) -> BeanChanceStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case BeanChanceStep.BITS:
                self.__step = BeanChanceStep.RANDOM_CHANCE
                return StepResult.NEXT

            case BeanChanceStep.RANDOM_CHANCE:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next BeanChanceStep: \"{currentStep}\"')
