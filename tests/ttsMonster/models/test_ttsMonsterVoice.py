from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterVoice:

    def test_humanName_withAll(self):
        humanNames: list[str] = list()

        for voice in TtsMonsterVoice:
            humanNames.append(voice.humanName)

        assert len(humanNames) == len(list(TtsMonsterVoice))

    def test_humanName_withKkona(self):
        result = TtsMonsterVoice.KKONA.humanName
        assert result == 'Kkona'

    def test_humanName_withShadow(self):
        result = TtsMonsterVoice.SHADOW.humanName
        assert result == 'Shadow'

    def test_humanName_withZeroTwo(self):
        result = TtsMonsterVoice.ZERO_TWO.humanName
        assert result == 'Zero Two'

    def test_inMessageName_withAll(self):
        inMessageNames: list[str] = list()

        for voice in TtsMonsterVoice:
            inMessageNames.append(voice.inMessageName)

        assert len(inMessageNames) == len(list(TtsMonsterVoice))

    def test_inMessageName_withKkona(self):
        result = TtsMonsterVoice.KKONA.inMessageName
        assert result == 'kkona'

    def test_inMessageName_withShadow(self):
        result = TtsMonsterVoice.SHADOW.inMessageName
        assert result == 'shadow'

    def test_inMessageName_withZeroTwo(self):
        result = TtsMonsterVoice.ZERO_TWO.inMessageName
        assert result == 'zerotwo'
