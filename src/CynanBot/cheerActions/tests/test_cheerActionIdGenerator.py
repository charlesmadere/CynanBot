import re
from typing import Pattern

import pytest

from CynanBot.cheerActions.cheerActionIdGenerator import CheerActionIdGenerator
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface


class TestCheerActionIdGenerator():

    cheerActionIdGenerator: CheerActionIdGeneratorInterface = CheerActionIdGenerator()
    actionIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)

    @pytest.mark.asyncio
    async def test_generateActionId_containsOnlyAlphanumericCharacters(self):
        for _ in range(100):
            actionId = await self.cheerActionIdGenerator.generateActionId()
            assert isinstance(actionId, str)
            assert self.actionIdRegEx.fullmatch(actionId) is not None

    @pytest.mark.asyncio
    async def test_generateActionId_isProperLength(self):
        for _ in range(100):
            actionId = await self.cheerActionIdGenerator.generateActionId()
            assert isinstance(actionId, str)
            assert len(actionId) == 3
