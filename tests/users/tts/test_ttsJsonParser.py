from src.tts.ttsProvider import TtsProvider
from src.users.tts.ttsJsonParser import TtsJsonParser
from src.users.tts.ttsJsonParserInterface import TtsJsonParserInterface


class TestTtsJsonParser:

    parser: TtsJsonParserInterface = TtsJsonParser()

    def test_parseTtsProvider_withDecTalk(self):
        result = self.parser.parseTtsProvider('dectalk')
        assert result is TtsProvider.DEC_TALK

    def test_parseTtsProvider_withGoogle(self):
        result = self.parser.parseTtsProvider('google')
        assert result is TtsProvider.GOOGLE

    def test_parseTtsProvider_withStreamElements(self):
        result = self.parser.parseTtsProvider('streamelements')
        assert result is TtsProvider.STREAM_ELEMENTS

    def test_parseTtsProvider_withTtsMonster(self):
        result = self.parser.parseTtsProvider('ttsmonster')
        assert result is TtsProvider.TTS_MONSTER
