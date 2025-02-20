import pytest

from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelper import ChatterPreferredTtsUserMessageHelper
from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import \
    ChatterPreferredTtsUserMessageHelperInterface
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.models.google.googlePreferredTts import GooglePreferredTts
from src.chatterPreferredTts.models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from src.language.languageEntry import LanguageEntry
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface


class TestChatterPreferredTtsUserMessageHelper:

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    helper: ChatterPreferredTtsUserMessageHelperInterface = ChatterPreferredTtsUserMessageHelper(
        languagesRepository = languagesRepository
    )

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkStrings(self):
        result = await self.helper.parseUserMessage('dectalk')
        assert isinstance(result, DecTalkPreferredTts)

        result = await self.helper.parseUserMessage('dec talk')
        assert isinstance(result, DecTalkPreferredTts)

        result = await self.helper.parseUserMessage('dec_talk')
        assert isinstance(result, DecTalkPreferredTts)

        result = await self.helper.parseUserMessage('dec-talk')
        assert isinstance(result, DecTalkPreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withEmptyString(self):
        result = await self.helper.parseUserMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleStrings(self):
        result = await self.helper.parseUserMessage('goog')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

        result = await self.helper.parseUserMessage('googl')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

        result = await self.helper.parseUserMessage('google')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndEnglish(self):
        result = await self.helper.parseUserMessage('goog english')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.ENGLISH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndGarbledText(self):
        result = await self.helper.parseUserMessage('google fdsiklahfkldsajlfdklsflad')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndJapanese(self):
        result = await self.helper.parseUserMessage('googl ja')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.JAPANESE

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndSwedish(self):
        result = await self.helper.parseUserMessage('google sweden')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.SWEDISH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamStrings(self):
        result = await self.helper.parseUserMessage('microsoftsam')
        assert isinstance(result, MicrosoftSamPreferredTts)

        result = await self.helper.parseUserMessage('microsoft sam')
        assert isinstance(result, MicrosoftSamPreferredTts)

        result = await self.helper.parseUserMessage('microsoft_sam')
        assert isinstance(result, MicrosoftSamPreferredTts)

        result = await self.helper.parseUserMessage('microsoft-sam')
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
