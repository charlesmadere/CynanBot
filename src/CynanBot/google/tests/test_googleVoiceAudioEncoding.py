from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class TestGoogleVoiceAudioEncoding():

    def test_toStr_withMp3(self):
        result = GoogleVoiceAudioEncoding.MP3.toStr()
        assert result == 'MP3'

    def test_toStr_withMale(self):
        result = GoogleVoiceAudioEncoding.MP3_64_KBPS.toStr()
        assert result == 'MP3_64_KBPS'

    def test_toStr_withOggOpus(self):
        result = GoogleVoiceAudioEncoding.OGG_OPUS.toStr()
        assert result == 'OGG_OPUS'
