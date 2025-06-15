import pytest

from src.chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from src.chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from src.chatterPreferredTts.models.decTalk.decTalkTtsProperties import DecTalkTtsProperties
from src.chatterPreferredTts.models.google.googleTtsProperties import GoogleTtsProperties
from src.decTalk.models.decTalkVoice import DecTalkVoice
from src.language.languageEntry import LanguageEntry


class TestChatterPreferredTtsPresenter:

    presenter = ChatterPreferredTtsPresenter()

    @pytest.mark.asyncio
    async def test_printOut_withDecTalkPreferredTts(self):
        properties = DecTalkTtsProperties(
            voice = None
        )

        chatterPreferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'DECtalk'

    @pytest.mark.asyncio
    async def test_printOut_withDecTalkPreferredTtsAndWendyVoice(self):
        properties = DecTalkTtsProperties(
            voice = DecTalkVoice.WENDY
        )

        chatterPreferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'DECtalk (Wendy)'

    @pytest.mark.asyncio
    async def test_printOut_withGooglePreferredTts(self):
        properties = GoogleTtsProperties(
            languageEntry = None
        )

        chatterPreferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'Google'

    @pytest.mark.asyncio
    async def test_printOut_withGooglePreferredTtsAndJapaneseLanguageEntry(self):
        properties = GoogleTtsProperties(
            languageEntry = LanguageEntry.JAPANESE
        )

        chatterPreferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'Google (Japanese 🇯🇵)'

    @pytest.mark.asyncio
    async def test_printOut_withGooglePreferredTtsAndKoreanLanguageEntry(self):
        properties = GoogleTtsProperties(
            languageEntry = LanguageEntry.KOREAN
        )

        chatterPreferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = 'abc123',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.printOut(chatterPreferredTts)
        assert result == 'Google (Korean 🇰🇷)'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, ChatterPreferredTtsPresenter)
