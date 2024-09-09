import pytest
from frozenlist import FrozenList

from src.ttsMonster.messageToVoicesHelper.ttsMonsterMessageToVoicesHelper import TtsMonsterMessageToVoicesHelper
from src.ttsMonster.messageToVoicesHelper.ttsMonsterMessageToVoicesHelperInterface import \
    TtsMonsterMessageToVoicesHelperInterface
from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice
from src.ttsMonster.models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice


class TestTtsMonsterMessageToVoicesHelper:

    helper: TtsMonsterMessageToVoicesHelperInterface = TtsMonsterMessageToVoicesHelper()

    brian = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Brian',
        sample = None,
        voiceId = 'brianId',
        websiteVoice = TtsMonsterWebsiteVoice.BRIAN
    )

    kkona = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'KKona',
        sample = None,
        voiceId = 'kkonaId',
        websiteVoice = TtsMonsterWebsiteVoice.KKONA
    )

    shadow = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Spectre',
        sample = None,
        voiceId = 'shadowId',
        websiteVoice = TtsMonsterWebsiteVoice.SHADOW
    )

    @pytest.mark.asyncio
    async def test_build_withBasicBrianMessage(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.brian })

        result = await self.helper.build(
            voices = voices,
            message = 'Brian: Hello, World!'
        )

        assert isinstance(result, FrozenList)
        assert len(result) == 1

        entry = result[0]
        assert entry.message == 'Hello, World!'
        assert entry.voice == self.brian

    @pytest.mark.asyncio
    async def test_build_withBasicBrianMessageButNoBrianVoiceIsAvailable(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.kkona })

        result = await self.helper.build(
            voices = voices,
            message = 'Brian: Hello, World!'
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withBlankChunkMessages1(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.brian, self.kkona, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = 'Brian: Shadow: Hello, World! Brian: Hello shadow: kkona: metroid'
        )

        assert isinstance(result, FrozenList)
        assert len(result) == 3

        entry = result[0]
        assert entry.message == 'Hello, World!'
        assert entry.voice == self.shadow

        entry = result[1]
        assert entry.message == 'Hello'
        assert entry.voice == self.brian

        entry = result[2]
        assert entry.message == 'metroid'
        assert entry.voice == self.kkona

    @pytest.mark.asyncio
    async def test_build_withBlankChunkMessages2(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.brian, self.kkona, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = 'Brian: Shadow: Brian: shadow: kkona:'
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withEmptyMessage(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.kkona, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = ''
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withEmptyVoicesAndEmptyMessage(self):
        result = await self.helper.build(
            voices = frozenset(),
            message = ''
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withEmptyVoicesAndWhitespaceMessage(self):
        result = await self.helper.build(
            voices = frozenset(),
            message = ' '
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withJohnnyMessageButNoJohnnyVoiceAvailable(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.brian, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = 'Johnny: Hello, World!'
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withRandomNoiseText1(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.brian, self.kkona, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = 'qXV3Lbsdvi5Tj41STSKIA9qdZbtkc6vrSO1U1bgdk1D0XZmkG9dMtWwFwRi1S0B'
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withRandomNoiseText2(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.brian, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = 'OrVniSn8oglwzVqD0tfal5n2ggBKVqsGljXZzAncZulyJvJzAmOX3vpIZhrXGJW'
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withRandomNoiseText3(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.kkona, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = 'OrVniSn8oglwzVqD0shadow:n2ggBpirate:shadow:cZulyJvJzAmOX3vpIZhrXGJWshadow:'
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_build_withShadowBgram(self):
        voices: frozenset[TtsMonsterVoice] = frozenset({ self.brian, self.shadow })

        result = await self.helper.build(
            voices = voices,
            message = 'shadow: bgram Shadow: bgram'
        )

        assert isinstance(result, FrozenList)
        assert len(result) == 2

        entry = result[0]
        assert entry.message == 'bgram'
        assert entry.voice == self.shadow

        entry = result[1]
        assert entry.message == 'bgram'
        assert entry.voice == self.shadow
