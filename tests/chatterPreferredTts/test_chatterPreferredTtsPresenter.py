import pytest

from src.chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.models.google.googlePreferredTts import GooglePreferredTts
from src.chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from src.language.languageEntry import LanguageEntry


class TestChatterPreferredTtsPresenter:

    presenter = ChatterPreferredTtsPresenter()

    @pytest.mark.asyncio
    async def test_printOut_withDecTalkPreferredTts(self):
        decTalkPreferredTts = DecTalkPreferredTts()

        chatterPreferredTts = ChatterPreferredTts(
            preferredTts = decTalkPreferredTts,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'DECtalk'

    @pytest.mark.asyncio
    async def test_printOut_withGooglePreferredTts(self):
        googlePreferredTts = GooglePreferredTts(
            languageEntry = None
        )

        chatterPreferredTts = ChatterPreferredTts(
            preferredTts = googlePreferredTts,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'Google'

    @pytest.mark.asyncio
    async def test_printOut_withGooglePreferredTtsAndJapaneseLanguageEntry(self):
        googlePreferredTts = GooglePreferredTts(
            languageEntry = LanguageEntry.JAPANESE
        )

        chatterPreferredTts = ChatterPreferredTts(
            preferredTts = googlePreferredTts,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'Google (Japanese 🇯🇵)'

    @pytest.mark.asyncio
    async def test_printOut_withGooglePreferredTtsAndKoreanLanguageEntry(self):
        googlePreferredTts = GooglePreferredTts(
            languageEntry = LanguageEntry.KOREAN
        )

        chatterPreferredTts = ChatterPreferredTts(
            preferredTts = googlePreferredTts,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'Google (Korean 🇰🇷)'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, ChatterPreferredTtsPresenter)
