from src.google.models.googleMultiSpeakerVoicePreset import GoogleMultiSpeakerVoicePreset


class TestGoogleMultiSpeakerVoicePreset:

    def test_fullName_withAll(self):
        results: set[str] = set()

        for voicePreset in GoogleMultiSpeakerVoicePreset:
            results.add(voicePreset.fullName)

        assert len(results) == len(GoogleMultiSpeakerVoicePreset)

    def test_languageCode_withAll(self):
        results: set[str] = set()

        for voicePreset in GoogleMultiSpeakerVoicePreset:
            results.add(voicePreset.languageCode)
            assert voicePreset.languageCode == 'en-US'

        assert len(results) == 1

    def test_speakerCharacter_withAll(self):
        results: set[str] = set()

        for voicePreset in GoogleMultiSpeakerVoicePreset:
            results.add(voicePreset.speakerCharacter)

        assert len(results) == len(GoogleMultiSpeakerVoicePreset)
