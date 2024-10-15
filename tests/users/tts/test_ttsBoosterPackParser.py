from src.timber.timberStub import TimberStub
from src.timber.timberInterface import TimberInterface
from src.tts.ttsJsonMapper import TtsJsonMapper
from src.tts.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.ttsProvider import TtsProvider
from src.users.tts.ttsBoosterPackParser import TtsBoosterPackParser
from src.users.tts.ttsBoosterPackParserInterface import TtsBoosterPackParserInterface


class TestTtsBoosterPackParser:

    timber: TimberInterface = TimberStub()

    ttsJsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
        timber = timber
    )

    parser: TtsBoosterPackParserInterface = TtsBoosterPackParser(
        ttsJsonMapper = ttsJsonMapper
    )

    def test_parseBoosterPack(self):
        result = self.parser.parseBoosterPack({
            'cheerAmount': 100,
            'ttsProvider': self.ttsJsonMapper.serializeProvider(TtsProvider.DEC_TALK)
        })

        assert result.cheerAmount == 100
        assert result.ttsProvider is TtsProvider.DEC_TALK
