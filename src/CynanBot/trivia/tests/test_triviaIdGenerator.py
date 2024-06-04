import re
from typing import Pattern

import pytest

from CynanBot.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBot.trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface


class TestTriviaIdGenerator():

    actionIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    @pytest.mark.asyncio
    async def test_generateActionId(self):
        for _ in range(100):
            actionId = await self.triviaIdGenerator.generateActionId()
            assert isinstance(actionId, str)
            assert self.actionIdRegEx.fullmatch(actionId) is not None

    @pytest.mark.asyncio
    async def test_generateEventId(self):
        for _ in range(100):
            eventId = await self.triviaIdGenerator.generateEventId()
            assert isinstance(eventId, str)
            assert self.actionIdRegEx.fullmatch(eventId) is not None

    @pytest.mark.asyncio
    async def test_generateGameId(self):
        for _ in range(100):
            gameId = await self.triviaIdGenerator.generateGameId()
            assert isinstance(gameId, str)
            assert self.actionIdRegEx.fullmatch(gameId) is not None

    def test_sanity(self):
        assert self.triviaIdGenerator is not None
        assert isinstance(self.triviaIdGenerator, TriviaIdGeneratorInterface)
        assert isinstance(self.triviaIdGenerator, TriviaIdGenerator)
