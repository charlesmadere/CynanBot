from src.ttsMonster.models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice


class TestTtsMonsterWebsiteVoice:

    def test_voiceId_withBrian(self):
        voiceId = TtsMonsterWebsiteVoice.BRIAN.voiceId
        assert voiceId == '0993f688-6719-4cf6-9769-fee7b77b1df5'

    def test_voiceId_withGeralt(self):
        voiceId = TtsMonsterWebsiteVoice.GERALT.voiceId
        assert voiceId == 'c5d9224a-60d1-48db-9dfd-3146842a931c'

    def test_voiceId_withHal9000(self):
        voiceId = TtsMonsterWebsiteVoice.HAL_9000.voiceId
        assert voiceId == '105e3e7d-ec3e-47a3-a3d3-86345feed23d'

    def test_voiceId_withJohnny(self):
        voiceId = TtsMonsterWebsiteVoice.JOHNNY.voiceId
        assert voiceId == '24e1a8ff-e5c7-464f-a708-c4fe92c59b28'

    def test_voiceId_withKkona(self):
        voiceId = TtsMonsterWebsiteVoice.KKONA.voiceId
        assert voiceId == '50570964-9672-4927-ac7d-40575e9112d3'

    def test_voiceId_withMegan(self):
        voiceId = TtsMonsterWebsiteVoice.MEGAN.voiceId
        assert voiceId == '1364bd06-f252-433e-9eac-f9a9a964a77b'

    def test_voiceId_withNarrator(self):
        voiceId = TtsMonsterWebsiteVoice.NARRATOR.voiceId
        assert voiceId == '7dfab21a-da07-4474-b7df-dcbbd7c7c69c'

    def test_voiceId_withShadow(self):
        voiceId = TtsMonsterWebsiteVoice.SHADOW.voiceId
        assert voiceId == '67dbd94d-a097-4676-af2f-1db67c1eb8dd'

    def test_voiceId_withZeroTwo(self):
        voiceId = TtsMonsterWebsiteVoice.ZERO_TWO.voiceId
        assert voiceId == '32a369aa-5485-4039-beb6-4c757e93a197'

    def test_websiteName_withBrian(self):
        websiteName = TtsMonsterWebsiteVoice.BRIAN.websiteName
        assert websiteName == 'brian'

    def test_websiteName_withGeralt(self):
        websiteName = TtsMonsterWebsiteVoice.GERALT.websiteName
        assert websiteName == 'geralt'

    def test_websiteName_withHal9000(self):
        websiteName = TtsMonsterWebsiteVoice.HAL_9000.websiteName
        assert websiteName == 'hal9000'

    def test_websiteName_withJohnny(self):
        websiteName = TtsMonsterWebsiteVoice.JOHNNY.websiteName
        assert websiteName == 'johnny'

    def test_websiteName_withKkona(self):
        websiteName = TtsMonsterWebsiteVoice.KKONA.websiteName
        assert websiteName == 'kkona'

    def test_websiteName_withMegan(self):
        websiteName = TtsMonsterWebsiteVoice.MEGAN.websiteName
        assert websiteName == 'megan'

    def test_websiteName_withNarrator(self):
        websiteName = TtsMonsterWebsiteVoice.NARRATOR.websiteName
        assert websiteName == 'narrator'

    def test_websiteName_withShadow(self):
        websiteName = TtsMonsterWebsiteVoice.SHADOW.websiteName
        assert websiteName == 'shadow'

    def test_websiteName_withZeroTwo(self):
        websiteName = TtsMonsterWebsiteVoice.ZERO_TWO.websiteName
        assert websiteName == 'zerotwo'
