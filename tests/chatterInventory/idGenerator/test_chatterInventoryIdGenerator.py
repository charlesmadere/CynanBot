import re
from typing import Pattern

import pytest

from src.chatterInventory.idGenerator.chatterInventoryIdGenerator import ChatterInventoryIdGenerator
from src.chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface


class TestChatterInventoryIdGenerator:

    actionIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    eventIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    requestIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    idGenerator: ChatterInventoryIdGeneratorInterface = ChatterInventoryIdGenerator()

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

    @pytest.mark.asyncio
    async def test_generateRequestId(self):
        for _ in range(100):
            requestId = await self.idGenerator.generateRequestId()
            assert isinstance(requestId, str)
            assert self.requestIdRegEx.fullmatch(requestId) is not None

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, ChatterInventoryIdGenerator)
        assert isinstance(self.idGenerator, ChatterInventoryIdGeneratorInterface)
