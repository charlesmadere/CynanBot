import pytest

from src.chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter


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

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, ChatterPreferredTtsPresenter)
