from src.tts.ttsCommandBuilder import TtsCommandBuilder
from src.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface


class TestTtsCommandBuilder:

    ttsCommandBuilder: TtsCommandBuilderInterface = TtsCommandBuilder()

    def test_sanity(self):
        assert self.ttsCommandBuilder is not None
        assert isinstance(self.ttsCommandBuilder, TtsCommandBuilderInterface)
        assert isinstance(self.ttsCommandBuilder, TtsCommandBuilder)
