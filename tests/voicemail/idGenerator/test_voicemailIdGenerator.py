import re
from typing import Final, Pattern

import pytest

from src.misc.randomUtils import RandomUtils
from src.misc.randomUtilsInterface import RandomUtilsInterface
from src.voicemail.idGenerator.voicemailIdGenerator import VoicemailIdGenerator
from src.voicemail.idGenerator.voicemailIdGeneratorInterface import VoicemailIdGeneratorInterface


class TestVoicemailIdGenerator:

    voicemailIdRegEx: Final[Pattern] = re.compile(r'^[a-z0-9]{3}$', re.IGNORECASE)

    randomUtils: Final[RandomUtilsInterface] = RandomUtils()

    idGenerator: Final[VoicemailIdGeneratorInterface] = VoicemailIdGenerator(
        randomUtils = randomUtils,
    )

    @pytest.mark.asyncio
    async def test_generateVoicemailId(self):
        for _ in range(100):
            voicemailId = await self.idGenerator.generateVoicemailId()
            assert isinstance(voicemailId, str)
            assert self.voicemailIdRegEx.fullmatch(voicemailId) is not None

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, VoicemailIdGenerator)
        assert isinstance(self.idGenerator, VoicemailIdGeneratorInterface)
