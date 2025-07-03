from frozendict import frozendict

from src.users.decTalkSongs.decTalkSongBoosterPack import DecTalkSongBoosterPack
from src.users.decTalkSongs.decTalkSongBoosterPackParser import DecTalkSongBoosterPackParser
from src.users.decTalkSongs.decTalkSongBoosterPackParserInterface import DecTalkSongBoosterPackParserInterface


class TestDecTalkSongBoosterPackParser:

    parser: DecTalkSongBoosterPackParserInterface = DecTalkSongBoosterPackParser()

    def test_parseBoosterPacks(self):
        boosterPack = DecTalkSongBoosterPack(
            rewardId = 'abc123',
            song = 'The Final Countdown'
        )

        result = self.parser.parseBoosterPacks([
            {
                'rewardId': boosterPack.rewardId,
                'song': boosterPack.song,
            },
        ])

        assert isinstance(result, frozendict)
        assert len(result) == 1

        entry = result.get(boosterPack.rewardId, None)
        assert isinstance(entry, DecTalkSongBoosterPack)
        assert entry == boosterPack
        assert entry.rewardId == boosterPack.rewardId
        assert entry.song == boosterPack.song

    def test_parseBoosterPacks_withEmptyList(self):
        result = self.parser.parseBoosterPacks(list())
        assert result is None

    def test_parseBoosterPacks_withNone(self):
        result = self.parser.parseBoosterPacks(None)
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, DecTalkSongBoosterPackParser)
        assert isinstance(self.parser, DecTalkSongBoosterPackParserInterface)
