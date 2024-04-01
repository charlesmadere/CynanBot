import pytest

from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.tts.google.googleFileExtensionHelper import \
    GoogleFileExtensionHelper
from CynanBot.tts.google.googleFileExtensionHelperInterface import \
    GoogleFileExtensionHelperInterface


class TestGoogleFileExtensionHelper():

    fileExtensionHelper: GoogleFileExtensionHelperInterface = GoogleFileExtensionHelper()

    @pytest.mark.asyncio
    async def text_getFileExtension_withMp3(self):
        result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.MP3)
        assert result == 'mp3'

    @pytest.mark.asyncio
    async def text_getFileExtension_withOggOpus(self):
        result = await self.fileExtensionHelper.getFileExtension(GoogleVoiceAudioEncoding.OGG_OPUS)
        assert result == 'ogg'
