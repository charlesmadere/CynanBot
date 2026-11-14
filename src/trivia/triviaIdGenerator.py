import hashlib
from typing import Final

from .triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..misc import utils as utils
from ..misc.randomUtilsInterface import RandomUtilsInterface


class TriviaIdGenerator(TriviaIdGeneratorInterface):

    def __init__(
        self,
        randomUtils: RandomUtilsInterface,
    ):
        if not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')

        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils

    async def generateActionId(self) -> str:
        return self.__randomUtils.uuid()

    async def generateEventId(self) -> str:
        return self.__randomUtils.uuid()

    async def generateGameId(self) -> str:
        return self.__randomUtils.uuid()

    async def generateQuestionId(
        self,
        question: str,
        category: str | None = None,
        difficulty: str | None = None,
    ) -> str:
        if not utils.isValidStr(question):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif category is not None and not isinstance(category, str):
            raise TypeError(f'category argument is malformed: \"{category}\"')
        elif difficulty is not None and not isinstance(difficulty, str):
            raise TypeError(f'difficulty argument is malformed: \"{difficulty}\"')

        string = f'{question}'

        if utils.isValidStr(category):
            string = f'{string}:{category}'

        if utils.isValidStr(difficulty):
            string = f'{string}:{difficulty}'

        encodedString = string.encode('utf-8')
        return hashlib.sha256(encodedString).hexdigest()
