import pytest

from src.contentScanner.bannedPhrase import BannedPhrase
from src.contentScanner.bannedWord import BannedWord
from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from src.storage.linesReaderInterface import LinesReaderInterface
from src.storage.linesStaticReader import LinesStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestBannedWordsRepository:

    timber: TimberInterface = TimberStub()

    bannedWordsLinesReader: LinesReaderInterface = LinesStaticReader(
        lines = [ 'Hello', 'WORLD', '"QAnon"', 'world' ]
    )

    emptyBannedWordsLinesReader: LinesReaderInterface = LinesStaticReader(
        lines = None
    )

    def test_getBannedWords(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.bannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = bannedWordsRepository.getBannedWords()
        assert len(bannedWords) == 3

        assert BannedPhrase('hello') in bannedWords
        assert BannedPhrase('world') in bannedWords
        assert BannedWord('qanon') in bannedWords

    @pytest.mark.asyncio
    async def test_getBannedWordsAsync(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.bannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = await bannedWordsRepository.getBannedWordsAsync()
        assert len(bannedWords) == 3

        assert BannedPhrase('hello') in bannedWords
        assert BannedPhrase('world') in bannedWords
        assert BannedWord('qanon') in bannedWords

    def test_getBannedWords_withEmptyBannedWordsLinesReader(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.emptyBannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = bannedWordsRepository.getBannedWords()
        assert len(bannedWords) == 0

    @pytest.mark.asyncio
    async def test_getBannedWordsAsync_withEmptyBannedWordsLinesReader(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.emptyBannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = await bannedWordsRepository.getBannedWordsAsync()
        assert len(bannedWords) == 0
