from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterVoice:

    def test_humanName_withAll(self):
        humanNames: list[str] = list()

        for voice in TtsMonsterVoice:
            humanNames.append(voice.humanName)

        assert len(humanNames) == len(list(TtsMonsterVoice))
