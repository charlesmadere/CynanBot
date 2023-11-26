import pytest

from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentCode import ContentCode
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.storage.linesStaticReader import LinesStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestContentScanner():

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
    async def test_scan_withUrl(self):
        result = await self.contentScanner.scan('Hello https://google.com/ World!')
        assert result is ContentCode.CONTAINS_URL

    @pytest.mark.asyncio
    async def test_updatePhrasesContent(self):
        pass

    @pytest.mark.asyncio
    async def test_updateWordsContent(self):
        pass
