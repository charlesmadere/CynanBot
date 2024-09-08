from typing import Collection

import pytest

from src.ttsMonster.messageToVoicesHelper.ttsMonsterMessageToVoicesHelper import TtsMonsterMessageToVoicesHelper
from src.ttsMonster.messageToVoicesHelper.ttsMonsterMessageToVoicesHelperInterface import \
    TtsMonsterMessageToVoicesHelperInterface
from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterMessageToVoicesHelper:

    helper: TtsMonsterMessageToVoicesHelperInterface = TtsMonsterMessageToVoicesHelper()

    pirate = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Pirate',
        sample = None,
        voiceId = 'pirateId'
    )

    shadow = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Shadow',
        sample = None,
        voiceId = 'shadowId'
    )

    @pytest.mark.asyncio
    async def test_build_bgram(self):
        # TODO this is a work in progress

        # voices: list[TtsMonsterVoice] = [ self.pirate, self.shadow ]
        #
        # result = await self.helper.build(
        #     voices = voices,
        #     message = 'shadow: bgram shadow: bgram'
        # )
        #
        # assert isinstance(result, Collection)
        # assert len(result) == 2
        #
        # entry = result[0]
        # assert entry.message == 'bgram'
        # assert entry.voice == self.shadow
        #
        # entry = result[1]
        # assert entry.message == 'bgram'
        # assert entry.voice == self.shadow

        pass

    @pytest.mark.asyncio
    async def test_build_withEmptyMessage(self):
        voices: list[TtsMonsterVoice] = [ self.pirate, self.shadow ]

        result = await self.helper.build(
            voices = voices,
            message = ''
        )

        assert isinstance(result, Collection)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_build_withEmptyVoicesAndEmptyMessage(self):
        result = await self.helper.build(
            voices = list(),
            message = ''
        )

        assert isinstance(result, Collection)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_build_withEmptyVoicesAndWhitespaceMessage(self):
        result = await self.helper.build(
            voices = list(),
            message = ' '
        )

        assert isinstance(result, Collection)
        assert len(result) == 0
