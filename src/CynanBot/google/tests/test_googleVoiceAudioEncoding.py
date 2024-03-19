import pytest

from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class TestGoogleVoiceAudioEncoding():

    def test_toStr_withAlaw(self):
        result = GoogleVoiceAudioEncoding.ALAW.toStr()
        assert result == 'ALAW'

    def test_toStr_withLinear16(self):
        result = GoogleVoiceAudioEncoding.LINEAR_16.toStr()
        assert result == 'LINEAR16'

    def test_toStr_withMp3(self):
        result = GoogleVoiceAudioEncoding.MP3.toStr()
        assert result == 'MP3'

    def test_toStr_withMale(self):
        result = GoogleVoiceAudioEncoding.MP3_64_KBPS.toStr()
        assert result == 'MP3_64_KBPS'

    def test_toStr_withMulaw(self):
        result = GoogleVoiceAudioEncoding.MULAW.toStr()
        assert result == 'MULAW'

    def test_toStr_withOggOpus(self):
        result = GoogleVoiceAudioEncoding.OGG_OPUS.toStr()
        assert result == 'OGG_OPUS'

    def test_toStr_withUnspecified(self):
        result: str | None = None

        with pytest.raises(Exception):
            result = GoogleVoiceAudioEncoding.UNSPECIFIED.toStr()

        assert result is None
