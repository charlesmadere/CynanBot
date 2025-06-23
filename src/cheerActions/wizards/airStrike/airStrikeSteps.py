from .airStrikeStep import AirStrikeStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...cheerActionType import CheerActionType


class AirStrikeSteps(AbsSteps):

    def __init__(self):
        self.__step = AirStrikeStep.BITS

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.AIR_STRIKE

    @property
    def currentStep(self) -> AirStrikeStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case AirStrikeStep.BITS:
                self.__step = AirStrikeStep.MINIMUM_DURATION_SECONDS
                return StepResult.NEXT

            case AirStrikeStep.MAXIMUM_CHATTERS:
                return StepResult.DONE

            case AirStrikeStep.MAXIMUM_DURATION_SECONDS:
                self.__step = AirStrikeStep.MINIMUM_CHATTERS
                return StepResult.NEXT

            case AirStrikeStep.MINIMUM_CHATTERS:
                self.__step = AirStrikeStep.MAXIMUM_CHATTERS
                return StepResult.NEXT

            case AirStrikeStep.MINIMUM_DURATION_SECONDS:
                self.__step = AirStrikeStep.MAXIMUM_DURATION_SECONDS
                return StepResult.NEXT

            case _:
                raise RuntimeError(f'unknown next AirStrikeStep: \"{currentStep}\"')
