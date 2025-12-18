from .itemUseStep import ItemUseStep
from ..absSteps import AbsSteps
from ..stepResult import StepResult
from ...cheerActionType import CheerActionType


class ItemUseSteps(AbsSteps):

    def __init__(self):
        self.__step = ItemUseStep.ITEM_TYPE

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.ITEM_USE

    @property
    def currentStep(self) -> ItemUseStep:
        return self.__step

    def stepForward(self) -> StepResult:
        currentStep = self.__step

        match currentStep:
            case ItemUseStep.BITS:
                self.__step = ItemUseStep.ITEM_TYPE
                return StepResult.NEXT

            case ItemUseStep.ITEM_TYPE:
                return StepResult.DONE

            case _:
                raise RuntimeError(f'unknown next itemUseStep: \"{currentStep}\"')
