from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterVoice:

    def test_humanName_withAll(self):
        humanNames: list[str] = list()

        for voice in TtsMonsterVoice:
            humanNames.append(voice.humanName)

        assert len(humanNames) == len(list(TtsMonsterVoice))

    def test_inMessageName_withAll(self):
        inMessageNames: list[str] = list()

        for voice in TtsMonsterVoice:
            inMessageNames.append(voice.inMessageName)

        assert len(inMessageNames) == len(list(TtsMonsterVoice))
