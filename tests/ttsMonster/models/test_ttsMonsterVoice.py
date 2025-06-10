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

    def test_humanName_withAsmr(self):
        result = TtsMonsterVoice.ASMR.humanName
        assert result == 'ASMR'

    def test_humanName_withBrian(self):
        result = TtsMonsterVoice.BRIAN.humanName
        assert result == 'Brian'

    def test_humanName_withGlados(self):
        result = TtsMonsterVoice.GLADOS.humanName
        assert result == 'Glados'

    def test_humanName_withHikari(self):
        result = TtsMonsterVoice.HIKARI.humanName
        assert result == 'Hikari'

    def test_humanName_withJazz(self):
        result = TtsMonsterVoice.JAZZ.humanName
        assert result == 'Jazz'

    def test_humanName_withKkona(self):
        result = TtsMonsterVoice.KKONA.humanName
        assert result == 'Kkona'

    def test_humanName_withNarrator(self):
        result = TtsMonsterVoice.NARRATOR.humanName
        assert result == 'Narrator'

    def test_humanName_withShadow(self):
        result = TtsMonsterVoice.SHADOW.humanName
        assert result == 'Shadow'

    def test_humanName_withSpongebob(self):
        result = TtsMonsterVoice.SPONGEBOB.humanName
        assert result == 'Spongebob'

    def test_humanName_withVomit(self):
        result = TtsMonsterVoice.VOMIT.humanName
        assert result == 'Vomit'

    def test_humanName_withWitch(self):
        result = TtsMonsterVoice.WITCH.humanName
        assert result == 'Witch'

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

    def test_inMessageName_withAsmr(self):
        result = TtsMonsterVoice.ASMR.inMessageName
        assert result == 'asmr'

    def test_inMessageName_withBrian(self):
        result = TtsMonsterVoice.BRIAN.inMessageName
        assert result == 'brian'

    def test_inMessageName_withGlados(self):
        result = TtsMonsterVoice.GLADOS.inMessageName
        assert result == 'glados'

    def test_inMessageName_withHikari(self):
        result = TtsMonsterVoice.HIKARI.inMessageName
        assert result == 'hikari'

    def test_inMessageName_withJazz(self):
        result = TtsMonsterVoice.JAZZ.inMessageName
        assert result == 'jazz'

    def test_inMessageName_withKkona(self):
        result = TtsMonsterVoice.KKONA.inMessageName
        assert result == 'kkona'

    def test_inMessageName_withNarrator(self):
        result = TtsMonsterVoice.NARRATOR.inMessageName
        assert result == 'narrator'

    def test_inMessageName_withPirate(self):
        result = TtsMonsterVoice.PIRATE.inMessageName
        assert result == 'pirate'

    def test_inMessageName_withShadow(self):
        result = TtsMonsterVoice.SHADOW.inMessageName
        assert result == 'shadow'

    def test_inMessageName_withSpongebob(self):
        result = TtsMonsterVoice.SPONGEBOB.inMessageName
        assert result == 'spongebob'

    def test_inMessageName_withVomit(self):
        result = TtsMonsterVoice.VOMIT.inMessageName
        assert result == 'vomit'

    def test_inMessageName_withWitch(self):
        result = TtsMonsterVoice.WITCH.inMessageName
        assert result == 'witch'

    def test_inMessageName_withZeroTwo(self):
        result = TtsMonsterVoice.ZERO_TWO.inMessageName
        assert result == 'zerotwo'
