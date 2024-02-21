import hashlib
import re
import uuid
from typing import Optional, Pattern

import CynanBot.misc.utils as utils
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface


class TriviaIdGenerator(TriviaIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        return await self.__generateRandomId()

    async def generateEventId(self) -> str:
        return await self.__generateRandomId()

    async def generateGameId(self) -> str:
        return await self.__generateRandomId()

    async def generateQuestionId(
        self,
        question: str,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> str:
        if not utils.isValidStr(question):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        assert category is None or isinstance(category, str), f"malformed {category=}"
        assert difficulty is None or isinstance(difficulty, str), f"malformed {difficulty=}"

        string = f'{question}'

        if utils.isValidStr(category):
            string = f'{string}:{category}'

        if utils.isValidStr(difficulty):
            string = f'{string}:{difficulty}'

        encodedString = string.encode('utf-8')
        return hashlib.sha256(encodedString).hexdigest()

    async def __generateRandomId(self) -> str:
        triviaId = str(uuid.uuid4())
        return self.__idRegEx.sub('', triviaId)
