from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterVoice:

    def test_humanName(self):
        humanNames: set[str] = set()

        for voice in TtsMonsterVoice:
            humanNames.add(voice.humanName)

        assert len(humanNames) == len(TtsMonsterVoice)

    def test_humanName_withAdam(self):
        result = TtsMonsterVoice.ADAM.humanName
        assert result == 'Adam'

    def test_humanName_withKkona(self):
        result = TtsMonsterVoice.KKONA.humanName
        assert result == 'Kkona'

    def test_humanName_withShadow(self):
        result = TtsMonsterVoice.SHADOW.humanName
        assert result == 'Shadow'

    def test_humanName_withZeroTwo(self):
        result = TtsMonsterVoice.ZERO_TWO.humanName
        assert result == 'Zero Two'

    def test_inMessageName(self):
        inMessageNames: set[str] = set()

        for voice in TtsMonsterVoice:
            inMessageNames.add(voice.inMessageName)

        assert len(inMessageNames) == len(TtsMonsterVoice)

    def test_inMessageName_withAdam(self):
        result = TtsMonsterVoice.ADAM.inMessageName
        assert result == 'adam'

    def test_inMessageName_withKkona(self):
        result = TtsMonsterVoice.KKONA.inMessageName
        assert result == 'kkona'

    def test_inMessageName_withShadow(self):
        result = TtsMonsterVoice.SHADOW.inMessageName
        assert result == 'shadow'

    def test_inMessageName_withZeroTwo(self):
        result = TtsMonsterVoice.ZERO_TWO.inMessageName
        assert result == 'zerotwo'
