from src.google.models.googleVoicePreset import GoogleVoicePreset


class TestGoogleVoicePreset:

    def test_fullName_withAll(self):
        fullNames: set[str] = set()

        for voicePreset in GoogleVoicePreset:
            fullNames.add(voicePreset.fullName)

        assert len(fullNames) == len(GoogleVoicePreset)

    def test_languageCode_withAll(self):
        for voicePreset in GoogleVoicePreset:
            languageCode = voicePreset.languageCode
            assert isinstance(languageCode, str)
            assert len(languageCode) >= 1
            assert not languageCode.isspace()

    def test_languageCode_withAllJapanesePresets(self):
        presets: set[GoogleVoicePreset] = {
            GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A,
            GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_B,
            GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_C,
            GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_D,
        }

        languageCodes: set[str] = set()

        for preset in presets:
            languageCodes.add(preset.languageCode)

        assert len(languageCodes) == 1

    def test_languageCode_withAllSwedishPresets(self):
        presets: set[GoogleVoicePreset] = {
            GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A,
            GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_B,
            GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_C,
            GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D,
            GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_E,
            GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_F,
            GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_G,
        }

        languageCodes: set[str] = set()

        for preset in presets:
            languageCodes.add(preset.languageCode)

        assert len(languageCodes) == 1

    def test_languageCode_withEnglishUkStandardA(self):
        languageCode = GoogleVoicePreset.ENGLISH_UK_STANDARD_A.languageCode
        assert languageCode == 'en-GB'

    def test_languageCode_withEnglishUsStandardA(self):
        languageCode = GoogleVoicePreset.ENGLISH_US_STANDARD_A.languageCode
        assert languageCode == 'en-US'

    def test_languageCode_withJapaneseJapanStandardA(self):
        languageCode = GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A.languageCode
        assert languageCode == 'ja-JP'

    def test_languageCode_withKoreanKoreaStandardA(self):
        languageCode = GoogleVoicePreset.KOREAN_KOREA_STANDARD_A.languageCode
        assert languageCode == 'ko-KR'
