from src.streamElements.models.streamElementsVoice import StreamElementsVoice


class TestStreamElementsVoice:

    def test_jsonValue_withBrian(self):
        result = StreamElementsVoice.BRIAN.jsonValue
        assert result == 'brian'

    def test_jsonValue_withJoey(self):
        result = StreamElementsVoice.JOEY.jsonValue
        assert result == 'joey'

    def test_urlValue_withBrian(self):
        result = StreamElementsVoice.BRIAN.urlValue
        assert result == 'Brian'

    def test_urlValue_withJoey(self):
        result = StreamElementsVoice.JOEY.urlValue
        assert result == 'Joey'
