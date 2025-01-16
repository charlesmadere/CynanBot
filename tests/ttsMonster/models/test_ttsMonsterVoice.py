from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice
from src.ttsMonster.models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice


class TestTtsMonsterVoice:

    pirate = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Pirate',
        sample = None,
        voiceId = 'pirateId',
        websiteVoice = None
    )

    shadow = TtsMonsterVoice(
        language = None,
        metadata = None,
        name = 'Shade',
        sample = None,
        voiceId = 'shadowId',
        websiteVoice = TtsMonsterWebsiteVoice.SHADOW
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
            voiceId = 'shadowId',
            websiteVoice = TtsMonsterWebsiteVoice.SHADOW
        )

        assert similarShadow == self.shadow

    def test_hash_withPirate(self):
        assert hash(self.pirate.voiceId) == hash(self.pirate)

    def test_hash_withPirateAndShadow(self):
        assert hash(self.pirate) != hash(self.shadow)

    def test_hash_withShadow(self):
        assert hash(self.shadow.voiceId) == hash(self.shadow)

    def test_hash_withSimilarPirate(self):
        similarPirate = TtsMonsterVoice(
            language = 'en',
            metadata = 'metadata',
            name = 'Jack Sparrow',
            sample = None,
            voiceId = 'pirateId',
            websiteVoice = None
        )

        assert hash(similarPirate) == hash(self.pirate)
