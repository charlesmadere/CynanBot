import re
from typing import Pattern

import pytest

from src.timeout.idGenerator.timeoutIdGenerator import TimeoutIdGenerator
from src.timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface


class TestTimeoutIdGenerator:

    actionIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    eventIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    idGenerator: TimeoutIdGeneratorInterface = TimeoutIdGenerator()

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
            assert self.eventIdRegEx.fullmatch(eventId) is not None

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, TimeoutIdGenerator)
        assert isinstance(self.idGenerator, TimeoutIdGeneratorInterface)
