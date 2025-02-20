import pytest

from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelper import ChatterPreferredTtsUserMessageHelper
from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import ChatterPreferredTtsUserMessageHelperInterface
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.models.google.googlePreferredTts import GooglePreferredTts
from src.chatterPreferredTts.models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestChatterPreferredTtsUserMessageHelper:

    timber: TimberInterface = TimberStub()

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    helper: ChatterPreferredTtsUserMessageHelperInterface = ChatterPreferredTtsUserMessageHelper(
        languagesRepository = languagesRepository
    )

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkStrings(self):
        result = await self.helper.parseUserMessage('dectalk')
        assert isinstance(result, DecTalkPreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withEmptyString(self):
        result = await self.helper.parseUserMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleStrings(self):
        result = await self.helper.parseUserMessage('google')
        assert isinstance(result, GooglePreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamStrings(self):
        result = await self.helper.parseUserMessage('microsoftsam')
        assert isinstance(result, MicrosoftSamPreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withNone(self):
        result = await self.helper.parseUserMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withWhitespaceString(self):
        result = await self.helper.parseUserMessage(' ')
        assert result is None

    def test_sanity(self):
        assert self.helper is not None
        assert isinstance(self.helper, ChatterPreferredTtsUserMessageHelper)
        assert isinstance(self.helper, ChatterPreferredTtsUserMessageHelperInterface)
