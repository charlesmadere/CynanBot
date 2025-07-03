import pytest

from src.tts.directoryProvider.ttsDirectoryProvider import TtsDirectoryProvider
from src.tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from src.tts.models.ttsProvider import TtsProvider


class TestTtsDirectoryProvider:

    directoryProvider: TtsDirectoryProviderInterface = TtsDirectoryProvider()

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withAll(self):
        results: set[str] = set()

        for provider in TtsProvider:
            results.add(await self.directoryProvider.getTtsDirectoryFor(provider))

        assert len(results) == len(TtsProvider)

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withCommodoreSam(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.COMMODORE_SAM)
        assert result == 'commodore_sam'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withDecTalk(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withGoogle(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.GOOGLE)
        assert result == 'google'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withHalfLife(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.HALF_LIFE)
        assert result == 'half_life'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withMicrosoft(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.MICROSOFT)
        assert result == 'microsoft'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withMicrosoftSam(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withRandoTts(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.RANDO_TTS)
        assert result == 'rando_tts'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withShotgunTts(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.SHOTGUN_TTS)
        assert result == 'shotgun_tts'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withStreamElements(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withTtsMonster(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withUnrestrictedDecTalk(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.UNRESTRICTED_DEC_TALK)
        assert result == 'unrestricted_dec_talk'

    def test_sanity(self):
        assert self.directoryProvider is not None
        assert isinstance(self.directoryProvider, TtsDirectoryProvider)
        assert isinstance(self.directoryProvider, TtsDirectoryProviderInterface)
