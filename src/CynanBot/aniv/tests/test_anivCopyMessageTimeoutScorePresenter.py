import pytest

from CynanBot.aniv.anivCopyMessageTimeoutScore import \
    AnivCopyMessageTimeoutScore
from CynanBot.aniv.anivCopyMessageTimeoutScorePresenter import \
    AnivCopyMessageTimeoutScorePresenter
from CynanBot.aniv.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import \
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
