import pytest

from src.glacialTtsStorage.idGenerator.glacialTtsIdGenerator import GlacialTtsIdGenerator
from src.glacialTtsStorage.idGenerator.glacialTtsIdGeneratorInterface import GlacialTtsIdGeneratorInterface
from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from src.microsoftSam.parser.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from src.tts.models.ttsProvider import TtsProvider


class TestGlacialTtsIdGenerator:

    idGenerator: GlacialTtsIdGeneratorInterface = GlacialTtsIdGenerator()
    microsoftSamJsonParser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

    @pytest.mark.asyncio
    async def test_generateId_voiceComparisons_withMicrosoftSam(self):
        withVoice = await self.idGenerator.generateId(
            message = 'Hello, World!',
            voice = await self.microsoftSamJsonParser.serializeVoice(MicrosoftSamVoice.BONZI_BUDDY),
            provider = TtsProvider.MICROSOFT_SAM
        )

        withoutVoice = await self.idGenerator.generateId(
            message = 'Hello, World!',
            voice = None,
            provider = TtsProvider.MICROSOFT_SAM
        )

        assert withVoice != withoutVoice

    @pytest.mark.asyncio
    async def test_generateId_withMicrosoftSam(self):
        results: set[str] = set()

        for _ in range(100):
            result = await self.idGenerator.generateId(
                message = 'Hello, World!',
                voice = await self.microsoftSamJsonParser.serializeVoice(MicrosoftSamVoice.SAM),
                provider = TtsProvider.MICROSOFT_SAM
            )

            results.add(result)

        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_generateId_withTtsMonster(self):
        results: set[str] = set()

        for _ in range(100):
            result = await self.idGenerator.generateId(
                message = 'Hello, World!',
                voice = None,
                provider = TtsProvider.TTS_MONSTER
            )

            results.add(result)

        assert len(results) == 1

    def test_sanity(self):
        assert self.idGenerator is not None
        assert isinstance(self.idGenerator, GlacialTtsIdGenerator)
        assert isinstance(self.idGenerator, GlacialTtsIdGeneratorInterface)
