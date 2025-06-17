import hashlib
import re
import uuid
from typing import Final, Pattern

from .triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..misc import utils as utils


class TriviaIdGenerator(TriviaIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        return await self.__generateRandomUuid()

    async def generateEventId(self) -> str:
        return await self.__generateRandomUuid()

    async def generateGameId(self) -> str:
        return await self.__generateRandomUuid()

    async def generateQuestionId(
        self,
        question: str,
        category: str | None = None,
        difficulty: str | None = None
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

    async def __generateRandomUuid(self) -> str:
        triviaId = str(uuid.uuid4())
        return self.__idRegEx.sub('', triviaId)
