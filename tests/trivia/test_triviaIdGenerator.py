import re
from typing import Pattern

import pytest

from src.trivia.triviaIdGenerator import TriviaIdGenerator
from src.trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface


class TestTriviaIdGenerator:

    actionIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    idGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    @pytest.mark.asyncio
    async def test_generateActionId(self):
        for _ in range(100):
            actionId = await self.idGenerator.generateActionId()
            assert isinstance(actionId, str)
            assert self.actionIdRegEx.fullmatch(actionId) is not None

    @pytest.mark.asyncio
    async def test_generateEventId(self):
        for _ in range(100):
            eventId = await self.idGenerator.generateEventId()
            assert isinstance(eventId, str)
            assert self.actionIdRegEx.fullmatch(eventId) is not None

    @pytest.mark.asyncio
    async def test_generateGameId(self):
        for _ in range(100):
            gameId = await self.idGenerator.generateGameId()
            assert isinstance(gameId, str)
            assert self.actionIdRegEx.fullmatch(gameId) is not None

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, TriviaIdGeneratorInterface)
        assert isinstance(self.idGenerator, TriviaIdGenerator)
