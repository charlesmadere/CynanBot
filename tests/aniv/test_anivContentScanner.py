import pytest

from src.aniv.anivContentCode import AnivContentCode
from src.aniv.anivContentScanner import AnivContentScanner
from src.aniv.anivContentScannerInterface import AnivContentScannerInterface
from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.storage.linesStaticReader import LinesStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestAnivContentScanner():

    timber: TimberInterface = TimberStub()

    bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
        bannedWordsLinesReader = LinesStaticReader(
            lines = [ 'Nintendo', 'SONY', '"QAnon"', 'sony' ]
        ),
        timber = timber
    )

    contentScanner: ContentScannerInterface = ContentScanner(
        bannedWordsRepository = bannedWordsRepository,
        timber = timber
    )

    anivContentScanner: AnivContentScannerInterface = AnivContentScanner(
        contentScanner = contentScanner,
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_scan_withBadParens1(self):
        result = await self.anivContentScanner.scan('(insanefirebat')
        assert result is AnivContentCode.OPEN_PAREN

    @pytest.mark.asyncio
    async def test_scan_withBadParens2(self):
        result = await self.anivContentScanner.scan(')insanefirebat')
        assert result is AnivContentCode.OPEN_PAREN

    @pytest.mark.asyncio
    async def test_scan_withBadParens3(self):
        result = await self.anivContentScanner.scan(')insanefirebat(')
        assert result is AnivContentCode.OPEN_PAREN

    @pytest.mark.asyncio
    async def test_scan_withBadParens4(self):
        result = await self.anivContentScanner.scan(')insanefirebat)')
        assert result is AnivContentCode.OPEN_PAREN

    @pytest.mark.asyncio
    async def test_scan_withBadParens5(self):
        result = await self.anivContentScanner.scan('()insanefirebat))')
        assert result is AnivContentCode.OPEN_PAREN

    @pytest.mark.asyncio
    async def test_scan_withBadTwitchEmojiParens1(self):
        result = await self.anivContentScanner.scan('b)')
        assert result is AnivContentCode.OPEN_PAREN

        result = await self.anivContentScanner.scan('b-)')
        assert result is AnivContentCode.OPEN_PAREN

    @pytest.mark.asyncio
    async def test_scan_withBadQuotes(self):
        result = await self.anivContentScanner.scan('\"insanefirebat')
        assert result is AnivContentCode.OPEN_QUOTES

    @pytest.mark.asyncio
    async def test_scan_withBannedPhrase1(self):
        result = await self.anivContentScanner.scan('qanonbelievers need help')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withBannedPhrase2(self):
        result = await self.anivContentScanner.scan('qanon believers need help')
        assert result is AnivContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_scan_withBlankString(self):
        result = await self.anivContentScanner.scan(' ')
        assert result is AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK

    @pytest.mark.asyncio
    async def test_scan_withExclamationMarkOnly(self):
        result = await self.anivContentScanner.scan('!')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withExclamationMarkThenNonWordCharacters(self):
        result = await self.anivContentScanner.scan('! hello test')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withEmptyString(self):
        result = await self.anivContentScanner.scan('')
        assert result is AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK

    @pytest.mark.asyncio
    async def test_scan_withGoodParens1(self):
        result = await self.anivContentScanner.scan('(insanefirebat)')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodParens2(self):
        result = await self.anivContentScanner.scan('(insanefirebat)()()')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodParens3(self):
        result = await self.anivContentScanner.scan('[](insanefirebat)[]')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodParens4(self):
        result = await self.anivContentScanner.scan('[](insanefirebat)[] :) Hello!')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodQuotes(self):
        result = await self.anivContentScanner.scan('\"insanefirebat\"')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodTwitchEmojiParen1(self):
        result = await self.anivContentScanner.scan('B)')
        assert result is AnivContentCode.OK

        result = await self.anivContentScanner.scan('B-)')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodTwitchEmojiParen2(self):
        result = await self.anivContentScanner.scan('B) :) ;-) ')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodTwitchEmojiParen3(self):
        result = await self.anivContentScanner.scan(':|')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodTwitchEmojiParen4(self):
        result = await self.anivContentScanner.scan(':-D :(')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withHelloWorld(self):
        result = await self.anivContentScanner.scan('Hello, World!')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withLessThanThree(self):
        result = await self.anivContentScanner.scan('<3')
        assert result is AnivContentCode.OK

        result = await self.anivContentScanner.scan('GL!! <3')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withNone(self):
        result = await self.anivContentScanner.scan(None)
        assert result is AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK

    @pytest.mark.asyncio
    async def test_scan_withUrl(self):
        result = await self.anivContentScanner.scan('Hello https://google.com/ World!')
        assert result is AnivContentCode.CONTAINS_URL

    def test_sanity(self):
        assert self.anivContentScanner is not None
        assert isinstance(self.anivContentScanner, AnivContentScannerInterface)
