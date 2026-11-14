import re
from typing import Final, Pattern

import pytest

from src.chatterInventory.idGenerator.chatterInventoryIdGenerator import ChatterInventoryIdGenerator
from src.chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from src.misc.randomUtils import RandomUtils
from src.misc.randomUtilsInterface import RandomUtilsInterface


class TestChatterInventoryIdGenerator:

    actionIdRegEx: Final[Pattern] = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)

    eventIdRegEx: Final[Pattern] = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)

    requestIdRegEx: Final[Pattern] = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)

    randomUtils: Final[RandomUtilsInterface] = RandomUtils()

    idGenerator: Final[ChatterInventoryIdGeneratorInterface] = ChatterInventoryIdGenerator(
        randomUtils = randomUtils,
    )

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
