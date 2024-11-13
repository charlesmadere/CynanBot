from .gameShuffleStep import GameShuffleStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult


class GameShuffleSteps(AbsSteps):

    def __init__(self):
        self.__step = GameShuffleStep.BITS

    def getStep(self) -> GameShuffleStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case GameShuffleStep.BITS:
                self.__step = GameShuffleStep.SUPER_SHUFFLE_CHANCE
                return StepResult.NEXT

            case GameShuffleStep.SUPER_SHUFFLE_CHANCE:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next GameShuffleStep: \"{currentStep}\"')
