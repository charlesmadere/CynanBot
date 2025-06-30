from typing import Any

from frozenlist import FrozenList

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.jsonMapper.ttsJsonMapper import TtsJsonMapper
from src.tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.models.ttsProvider import TtsProvider
from src.users.tts.ttsBoosterPack import TtsBoosterPack
from src.users.tts.ttsBoosterPackParser import TtsBoosterPackParser
from src.users.tts.ttsBoosterPackParserInterface import TtsBoosterPackParserInterface


class TestTtsBoosterPackParser:

    timber: TimberInterface = TimberStub()

    ttsJsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
        timber = timber,
    )

    parser: TtsBoosterPackParserInterface = TtsBoosterPackParser(
        ttsJsonMapper = ttsJsonMapper,
    )

    def test_parseBoosterPack(self):
        boosterPack = TtsBoosterPack(
            cheerAmount = 100,
            ttsProvider = TtsProvider.DEC_TALK,
        )

        result = self.parser.parseBoosterPack({
            'cheerAmount': boosterPack.cheerAmount,
            'ttsProvider': self.ttsJsonMapper.serializeProvider(boosterPack.ttsProvider),
        })

        assert isinstance(result, TtsBoosterPack)
        assert result == boosterPack
        assert result.cheerAmount == 100
        assert result.ttsProvider is TtsProvider.DEC_TALK

    def test_parseBoosterPacks(self):
        jsonContents: list[dict[str, Any]] = [
            {
                'cheerAmount': 50,
                'ttsProvider': self.ttsJsonMapper.serializeProvider(TtsProvider.DEC_TALK),
            },
            {
                'cheerAmount': 150,
                'ttsProvider': self.ttsJsonMapper.serializeProvider(TtsProvider.TTS_MONSTER),
            },
            {
                'cheerAmount': 100,
                'ttsProvider': self.ttsJsonMapper.serializeProvider(TtsProvider.STREAM_ELEMENTS),
            },
            {
                'cheerAmount': 500,
                'ttsProvider': self.ttsJsonMapper.serializeProvider(TtsProvider.SHOTGUN_TTS),
            },
        ]

        results = self.parser.parseBoosterPacks(jsonContents)
        assert isinstance(results, FrozenList)
        assert len(results) == 4

        entry = results[0]
        assert entry.cheerAmount == 500
        assert entry.ttsProvider is TtsProvider.SHOTGUN_TTS

        entry = results[1]
        assert entry.cheerAmount == 150
        assert entry.ttsProvider is TtsProvider.TTS_MONSTER

        entry = results[2]
        assert entry.cheerAmount == 100
        assert entry.ttsProvider is TtsProvider.STREAM_ELEMENTS

        entry = results[3]
        assert entry.cheerAmount == 50
        assert entry.ttsProvider is TtsProvider.DEC_TALK

    def test_parseBoosterPacks_withEmptyList(self):
        result = self.parser.parseBoosterPacks(list())
        assert result is None

    def test_parseBoosterPacks_withNone(self):
        result = self.parser.parseBoosterPacks(None)
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, TtsBoosterPackParser)
        assert isinstance(self.parser, TtsBoosterPackParserInterface)
