import re
from typing import Pattern

import pytest

from src.crowdControl.idGenerator.crowdControlIdGenerator import CrowdControlIdGenerator
from src.crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface


class TestCrowdControlIdGenerator:

    actionIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    messageIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    idGenerator: CrowdControlIdGeneratorInterface = CrowdControlIdGenerator()

    @pytest.mark.asyncio
    async def test_generateActionId(self):
        for _ in range(100):
            actionId = await self.idGenerator.generateActionId()
            assert isinstance(actionId, str)
            assert self.actionIdRegEx.fullmatch(actionId) is not None

    @pytest.mark.asyncio
    async def test_generateMessageId(self):
        for _ in range(100):
            messageId = await self.idGenerator.generateMessageId()
            assert isinstance(messageId, str)
            assert self.messageIdRegEx.fullmatch(messageId) is not None

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, CrowdControlIdGeneratorInterface)
        assert isinstance(self.idGenerator, CrowdControlIdGenerator)
