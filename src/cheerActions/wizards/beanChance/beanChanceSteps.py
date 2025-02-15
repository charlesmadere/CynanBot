from .beanChanceStep import BeanChanceStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class BeanChanceSteps(AbsSteps):

    def __init__(self):
        self.__step = BeanChanceStep.BITS

    def getStep(self) -> BeanChanceStep:
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
