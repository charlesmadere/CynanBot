from .gameShuffleStep import GameShuffleStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...cheerActionType import CheerActionType


class GameShuffleSteps(AbsSteps):

    def __init__(self):
        self.__step = GameShuffleStep.BITS

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.GAME_SHUFFLE

    @property
    def currentStep(self) -> GameShuffleStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case GameShuffleStep.BITS:
                self.__step = GameShuffleStep.GIGA_SHUFFLE_CHANCE
                return StepResult.NEXT

            case GameShuffleStep.GIGA_SHUFFLE_CHANCE:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next GameShuffleStep: \"{currentStep}\"')
