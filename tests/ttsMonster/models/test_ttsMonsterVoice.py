from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterVoice:

    pirate = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Pirate',
        sample = None,
        voiceId = 'pirateId'
    )

    shadow = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Shadow',
        sample = None,
        voiceId = 'shadowId'
    )

    def test_equals_withPirate(self):
        assert self.pirate == self.pirate

    def test_equals_withPirateAndShadow(self):
        assert self.pirate != self.shadow

    def test_equals_withShadow(self):
        assert self.shadow == self.shadow

    def test_equals_withSimilarShadow(self):
        similarShadow = TtsMonsterVoice(
            language = 'en',
            metadata = 'metadata',
            name = 'Shadow the Hedgehog',
            sample = None,
            voiceId = 'shadowId'
        )

        assert similarShadow == self.shadow

    def test_hash_withPirate(self):
        assert hash(self.pirate.voiceId) == hash(self.pirate)

    def test_hash_withPirateAndShadow(self):
        assert hash(self.pirate) != hash(self.shadow)

    def test_hash_withShadow(self):
        assert hash(self.shadow.voiceId) == hash(self.shadow)
