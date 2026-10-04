from datetime import datetime, timezone
from typing import Final

import pytest

from src.cuteness.cutenessPresenter import CutenessPresenter
from src.cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from src.cuteness.models.cutenessResult import CutenessResult
from src.cuteness.models.preparedCutenessResult import PreparedCutenessResult


class TestCutenessPresenter:

    presenter: Final[CutenessPresenterInterface] = CutenessPresenter()

    @pytest.mark.asyncio
    async def test_printCuteness_withNoneCuteness(self):
        result = PreparedCutenessResult(
            cutenessResult = CutenessResult(
                cutenessDate = datetime(year = 2022, month = 6, day = 1, tzinfo = timezone.utc),
                cuteness = None,
                chatterUserId = 'abc123',
                twitchChannelId = 'def456',
            ),
            chatterUserLogin = 'stashiocat',
            chatterUserName = 'stashiocat',
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == '😿 stashiocat has no cuteness in Jun 2022'

    @pytest.mark.asyncio
    async def test_printCuteness_with0Cuteness(self):
        result = PreparedCutenessResult(
            cutenessResult = CutenessResult(
                cutenessDate = datetime(year = 2022, month = 6, day = 1, tzinfo = timezone.utc),
                cuteness = None,
                chatterUserId = 'abc123',
                twitchChannelId = 'def456',
            ),
            chatterUserLogin = 'stashiocat',
            chatterUserName = 'stashiocat',
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == '😿 stashiocat has no cuteness in Jun 2022'

    @pytest.mark.asyncio
    async def test_printCuteness_with10Cuteness(self):
        result = PreparedCutenessResult(
            cutenessResult = CutenessResult(
                cutenessDate = datetime(year = 2022, month = 6, day = 1, tzinfo = timezone.utc),
                cuteness = 10,
                chatterUserId = 'abc123',
                twitchChannelId = 'def456',
            ),
            chatterUserLogin = 'stashiocat',
            chatterUserName = 'stashiocat',
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == '✨ stashiocat\'s Jun 2022 cuteness is 10'

    def test_printCutenessDate(self):
        dateTime = datetime(year = 2026, month = 1, day = 1, tzinfo = timezone.utc)
        printOut = self.presenter.printCutenessDate(dateTime)
        assert isinstance(printOut, str)
        assert printOut == 'Jan 2026'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, CutenessPresenter)
        assert isinstance(self.presenter, CutenessPresenterInterface)
