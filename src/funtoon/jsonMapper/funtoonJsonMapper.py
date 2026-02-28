from typing import Any

from .funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from ..funtoonPkmnCatchType import FuntoonPkmnCatchType
from ..funtoonTriviaQuestion import FuntoonTriviaQuestion
from ...misc import utils as utils


class FuntoonJsonMapper(FuntoonJsonMapperInterface):

    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> FuntoonTriviaQuestion | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        categoryId = utils.getIntFromDict(jsonContents, 'category_id')
        triviaId = utils.getIntFromDict(jsonContents, 'id')
        answer = utils.getStrFromDict(jsonContents, 'answer')
        category = utils.getStrFromDict(jsonContents, 'category')
        clue = utils.getStrFromDict(jsonContents, 'clue')

        return FuntoonTriviaQuestion(
            categoryId = categoryId,
            triviaId = triviaId,
            answer = answer,
            category = category,
            clue = clue,
        )

    async def serializePkmnCatchType(
        self,
        pkmnCatchType: FuntoonPkmnCatchType,
    ) -> str:
        if not isinstance(pkmnCatchType, FuntoonPkmnCatchType):
            raise TypeError(f'pkmnCatchType argument is malformed: \"{pkmnCatchType}\"')

        match pkmnCatchType:
            case FuntoonPkmnCatchType.GREAT: return 'great'
            case FuntoonPkmnCatchType.NORMAL: return 'normal'
            case FuntoonPkmnCatchType.ULTRA: return 'ultra'
            case _: raise ValueError(f'unknown FuntoonPkmnCatchType: \"{self}\"')
