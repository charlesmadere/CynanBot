import re
from typing import Pattern

import pytest

from src.voicemail.idGenerator.voicemailIdGenerator import VoicemailIdGenerator
from src.voicemail.idGenerator.voicemailIdGeneratorInterface import VoicemailIdGeneratorInterface


class TestVoicemailIdGenerator:

    idGenerator: VoicemailIdGeneratorInterface = VoicemailIdGenerator()

    @pytest.mark.asyncio
    async def test_generateVoicemailId(self):
        regEx: Pattern = re.compile(r'^[a-z0-9]{3}$')

        for _ in range(100):
            voicemailId = await self.idGenerator.generateVoicemailId()
            match = regEx.fullmatch(voicemailId)
            assert match is not None

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, VoicemailIdGenerator)
        assert isinstance(self.idGenerator, VoicemailIdGeneratorInterface)
