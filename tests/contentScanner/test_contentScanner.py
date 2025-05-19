import pytest

from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from src.contentScanner.contentCode import ContentCode
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.storage.linesStaticReader import LinesStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestContentScanner:

    timber: TimberInterface = TimberStub()

    bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
        bannedWordsLinesReader = LinesStaticReader(
            lines = [ '\"meth\"', 'Nintendo', 'SONY', '\"QAnon\"', 'sony' ]
        ),
        timber = timber
    )

    contentScanner: ContentScannerInterface = ContentScanner(
        bannedWordsRepository = bannedWordsRepository,
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_scan_withBannedPhrase1(self):
        result = await self.contentScanner.scan('qanonbelievers need help')
        assert result is ContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withBannedPhrase2(self):
        result = await self.contentScanner.scan('qanon believers need help')
        assert result is ContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_scan_withBannedWord1(self):
        result = await self.contentScanner.scan('im pretty sure Nintendo hates Melee lol')
        assert result is ContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_scan_withBannedWord2(self):
        result = await self.contentScanner.scan('but do you hate sONY')
        assert result is ContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_scan_withBlankString(self):
        result = await self.contentScanner.scan(' ')
        assert result is ContentCode.IS_BLANK

    @pytest.mark.asyncio
    async def test_scan_withEmptyString(self):
        result = await self.contentScanner.scan('')
        assert result is ContentCode.IS_EMPTY

    @pytest.mark.asyncio
    async def test_scan_withHelloWorld(self):
        result = await self.contentScanner.scan('Hello, World!')
        assert result is ContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withNone(self):
        result = await self.contentScanner.scan(None)
        assert result is ContentCode.IS_NONE

    @pytest.mark.asyncio
    async def test_scan_withSomething(self):
        # the word "something" contains the word "meth" which is a banned word
        result = await self.contentScanner.scan('something')
        assert result is ContentCode.OK

    @pytest.mark.asyncio
    async def test_scan_withUrl(self):
        result = await self.contentScanner.scan('Hello https://google.com/ World!')
        assert result is ContentCode.CONTAINS_URL

    @pytest.mark.asyncio
    async def test_updatePhrasesContent(self):
        # TODO
        pass

    @pytest.mark.asyncio
    async def test_updateWordsContent(self):
        # TODO
        pass

    def test_sanity(self):
        assert self.contentScanner is not None
        assert isinstance(self.contentScanner, ContentScanner)
        assert isinstance(self.contentScanner, ContentScannerInterface)
