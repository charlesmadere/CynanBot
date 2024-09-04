import pytest

from src.beanStats.beanStatsPresenter import BeanStatsPresenter
from src.beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from src.beanStats.chatterBeanStats import ChatterBeanStats


class TestBeanStatsPresenter:

    presenter: BeanStatsPresenterInterface = BeanStatsPresenter()

    @pytest.mark.asyncio
    async def test_toString_with0Successes0FailsStats(self):
        beanStats = ChatterBeanStats(
            mostRecentBean = None,
            failedBeanAttempts = 0,
            successfulBeans = 0,
            chatterUserId = 'abc123',
            chatterUserName = 'stashiocat',
            twitchChannel = 'smCharles',
            twitchChannelId = 'def456'
        )

        result = await self.presenter.toString(beanStats)
        assert result == '@stashiocat has no bean attempts'
