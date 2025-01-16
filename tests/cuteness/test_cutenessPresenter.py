import pytest

from src.cuteness.cutenessDate import CutenessDate
from src.cuteness.cutenessPresenter import CutenessPresenter
from src.cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from src.cuteness.cutenessResult import CutenessResult


class TestCutenessPresenter:

    presenter: CutenessPresenterInterface = CutenessPresenter()

    @pytest.mark.asyncio
    async def test_printCuteness_withNoneCuteness(self):
        result = CutenessResult(
            cutenessDate = CutenessDate("2022-06"),
            cuteness = None,
            userId = 'abc',
            userName = 'stashiocat'
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == 'stashiocat has no cuteness in Jun 2022'

    @pytest.mark.asyncio
    async def test_printCuteness_with0Cuteness(self):
        result = CutenessResult(
            cutenessDate = CutenessDate("2022-06"),
            cuteness = None,
            userId = 'abc',
            userName = 'stashiocat'
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == 'stashiocat has no cuteness in Jun 2022'

    @pytest.mark.asyncio
    async def test_printCuteness_with10Cuteness(self):
        result = CutenessResult(
            cutenessDate = CutenessDate("2022-06"),
            cuteness = 10,
            userId = 'abc',
            userName = 'stashiocat'
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == 'stashiocat\'s Jun 2022 cuteness is 10 ✨'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, CutenessPresenterInterface)
        assert isinstance(self.presenter, CutenessPresenter)
