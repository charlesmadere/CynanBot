import pytest

from CynanBot.aniv.anivContentCode import AnivContentCode
from CynanBot.aniv.anivContentScanner import AnivContentScanner
from CynanBot.aniv.anivContentScannerInterface import \
    AnivContentScannerInterface
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.storage.linesStaticReader import LinesStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


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
    async def test_scan_withBadParens(self):
        result = await self.anivContentScanner.scan('(insanefirebat')
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
    async def test_scan_withEmptyString(self):
        result = await self.anivContentScanner.scan('')
        assert result is AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK

    @pytest.mark.asyncio
    async def test_scan_withGoodParens(self):
        result = await self.anivContentScanner.scan('(insanefirebat)')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withGoodQuotes(self):
        result = await self.anivContentScanner.scan('\"insanefirebat\"')
        assert result is AnivContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withHelloWorld(self):
        result = await self.anivContentScanner.scan('Hello, World!')
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
