import hashlib
import re
import uuid
from typing import Optional, Pattern

import CynanBot.misc.utils as utils
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface


class TriviaIdGenerator(TriviaIdGeneratorInterface):

    def __init__(self):
        self.__actionIdRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        actionId = str(uuid.uuid4())
        return self.__actionIdRegEx.sub('', actionId)

    async def generateEventId(self) -> str:
        return await self.generateActionId()

    async def generateGameId(self) -> str:
        return await self.generateActionId()

    async def generateQuestionId(
        self,
        question: str,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> str:
        if not utils.isValidStr(question):
            raise ValueError(f'question argument is malformed: \"{question}\"')

        string = f'{question}'

        if utils.isValidStr(category):
            string = f'{string}:{category}'

        if utils.isValidStr(difficulty):
            string = f'{string}:{difficulty}'

        return hashlib.sha256(string.encode('utf-8')).hexdigest()
