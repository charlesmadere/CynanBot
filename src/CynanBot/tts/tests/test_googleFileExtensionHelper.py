import pytest

from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.tts.google.googleFileExtensionHelper import \
    GoogleFileExtensionHelper
from CynanBot.tts.google.googleFileExtensionHelperInterface import \
    GoogleFileExtensionHelperInterface


class TestGoogleFileExtensionHelper():

    fileExtensionHelper: GoogleFileExtensionHelperInterface = GoogleFileExtensionHelper()

    @pytest.mark.asyncio
    async def test_getFileExtension_withAlaw(self):
        result: str | None = None

        with pytest.raises(Exception):
            result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.ALAW)

        assert result is None

    @pytest.mark.asyncio
    async def test_getFileExtension_withLinear16(self):
        result: str | None = None

        with pytest.raises(Exception):
            result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.LINEAR_16)

        assert result is None

    @pytest.mark.asyncio
    async def test_getFileExtension_withMp3(self):
        result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.MP3)
        assert result == 'mp3'

    @pytest.mark.asyncio
    async def test_getFileExtension_withMulaw(self):
        result: str | None = None

        with pytest.raises(Exception):
            result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.MULAW)

        assert result is None

    @pytest.mark.asyncio
    async def test_getFileExtension_withOggOpus(self):
        result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.OGG_OPUS)
        assert result == 'ogg'

    @pytest.mark.asyncio
    async def test_getFileExtension_withUnspecified(self):
        result: str | None = None

        with pytest.raises(Exception):
            result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.UNSPECIFIED)

        assert result is None
