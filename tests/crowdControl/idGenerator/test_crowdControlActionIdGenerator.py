import re
from typing import Final, Pattern

import pytest

from src.crowdControl.idGenerator.crowdControlIdGenerator import CrowdControlIdGenerator
from src.crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from src.misc.randomUtils import RandomUtils
from src.misc.randomUtilsInterface import RandomUtilsInterface


class TestCrowdControlIdGenerator:

    actionIdRegEx: Final[Pattern] = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)

    messageIdRegEx: Final[Pattern] = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)

    randomUtils: Final[RandomUtilsInterface] = RandomUtils()

    idGenerator: Final[CrowdControlIdGeneratorInterface] = CrowdControlIdGenerator(
        randomUtils = randomUtils,
    )

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
        assert isinstance(self.idGenerator, CrowdControlIdGenerator)
        assert isinstance(self.idGenerator, CrowdControlIdGeneratorInterface)
