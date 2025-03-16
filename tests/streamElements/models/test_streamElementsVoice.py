from src.streamElements.models.streamElementsVoice import StreamElementsVoice


class TestStreamElementsVoice:

    def test_humanName(self):
        results: set[str] = set()

        for voice in StreamElementsVoice:
            results.add(voice.humanName)

        assert len(results) == len(StreamElementsVoice)

    def test_humanName_withAmy(self):
        result = StreamElementsVoice.AMY.humanName
        assert result == 'Amy'

    def test_humanName_withBrian(self):
        result = StreamElementsVoice.BRIAN.humanName
        assert result == 'Brian'

    def test_humanName_withJoey(self):
        result = StreamElementsVoice.JOEY.humanName
        assert result == 'Joey'

    def test_urlValue(self):
        results: set[str] = set()

        for voice in StreamElementsVoice:
            results.add(voice.urlValue)

        assert len(results) == len(StreamElementsVoice)

    def test_urlValue_withAmy(self):
        result = StreamElementsVoice.AMY.urlValue
        assert result == 'Amy'

    def test_urlValue_withBrian(self):
        result = StreamElementsVoice.BRIAN.urlValue
        assert result == 'Brian'

    def test_urlValue_withJoey(self):
        result = StreamElementsVoice.JOEY.urlValue
        assert result == 'Joey'
