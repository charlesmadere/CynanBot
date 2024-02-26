from CynanBot.google.googleVoiceGender import GoogleVoiceGender


class TestGoogleVoiceGender():

    def test_toStr_withFemale(self):
        result = GoogleVoiceGender.FEMALE.toStr()
        assert result == 'FEMALE'

    def test_toStr_withMale(self):
        result = GoogleVoiceGender.MALE.toStr()
        assert result == 'MALE'

    def test_toStr_withUnspecified(self):
        result = GoogleVoiceGender.UNSPECIFIED.toStr()
        assert result == 'SSML_VOICE_GENDER_UNSPECIFIED'
