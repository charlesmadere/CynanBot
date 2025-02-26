import pytest

from src.tts.directoryProvider.ttsDirectoryProvider import TtsDirectoryProvider
from src.tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from src.tts.models.ttsProvider import TtsProvider


class TestTtsDirectoryProvider:

    directoryProvider: TtsDirectoryProviderInterface = TtsDirectoryProvider()

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withDecTalk(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    @pytest.mark.asyncio
    async def test_getTtsDirectoryFor_withMicrosoftSam(self):
        result = await self.directoryProvider.getTtsDirectoryFor(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    def test_sanity(self):
        assert self.directoryProvider is not None
        assert isinstance(self.directoryProvider, TtsDirectoryProvider)
        assert isinstance(self.directoryProvider, TtsDirectoryProviderInterface)
