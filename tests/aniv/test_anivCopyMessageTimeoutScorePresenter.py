import pytest

from src.aniv.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from src.aniv.anivCopyMessageTimeoutScorePresenter import \
    AnivCopyMessageTimeoutScorePresenter
from src.aniv.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface


class TestAnivCopyMessageTimeoutScorePresenter():

    presenter: AnivCopyMessageTimeoutScorePresenterInterface = AnivCopyMessageTimeoutScorePresenter()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    @pytest.mark.asyncio
    async def test_toString_with0Dodges0TimeoutsScore(self):
        score = AnivCopyMessageTimeoutScore(
            mostRecentDodge = None,
            mostRecentTimeout = None,
            dodgeScore = 0,
            timeoutScore = 0,
            chatterUserId = 'abc123',
            chatterUserName = 'stashiocat',
            twitchChannel = 'smCharles',
            twitchChannelId = 'def456'
        )

        printOut = await self.presenter.toString(score)
        assert printOut == f'ⓘ @{score.chatterUserName} has no aniv timeouts'
