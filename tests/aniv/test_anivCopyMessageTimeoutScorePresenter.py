import pytest

from src.aniv.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from src.aniv.anivCopyMessageTimeoutScorePresenter import AnivCopyMessageTimeoutScorePresenter
from src.aniv.anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface


class TestAnivCopyMessageTimeoutScorePresenter:

    presenter: AnivCopyMessageTimeoutScorePresenterInterface = AnivCopyMessageTimeoutScorePresenter()

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
