import re
from typing import Pattern

import pytest

from src.soundPlayerManager.playSessionIdGenerator.playSessionIdGenerator import PlaySessionIdGenerator
from src.soundPlayerManager.playSessionIdGenerator.playSessionIdGeneratorInterface import \
    PlaySessionIdGeneratorInterface


class TestPlaySessionIdGenerator:

    playSessionIdRegEx: Pattern = re.compile(r'^[a-z0-9]+$', re.IGNORECASE)
    idGenerator: PlaySessionIdGeneratorInterface = PlaySessionIdGenerator()

    @pytest.mark.asyncio
    async def test_generatePlaySessionId(self):
        for _ in range(100):
            actionId = await self.idGenerator.generatePlaySessionId()
            assert isinstance(actionId, str)
            assert self.playSessionIdRegEx.fullmatch(actionId) is not None

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, PlaySessionIdGeneratorInterface)
        assert isinstance(self.idGenerator, PlaySessionIdGenerator)
