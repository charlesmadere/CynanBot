from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Final, Collection

import pytest

from src.cuteness.cutenessDate import CutenessDate
from src.cuteness.cutenessPresenter import CutenessPresenter
from src.cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from src.cuteness.cutenessResult import CutenessResult
from src.twitch.localModels.twitchUserInterface import TwitchUserInterface
from src.twitch.userIds.twitchUserData import TwitchUserData
from src.twitch.userIds.twitchUserIdsRepositoryInterface import TwitchUserIdsRepositoryInterface


class TestCutenessPresenter:

    @dataclass(frozen = True, slots = True)
    class FakeTwitchUserData(TwitchUserInterface):
        userId: str
        userLogin: str
        userName: str

        def getUserId(self) -> str:
            return self.userId

        def getUserLogin(self) -> str:
            return self.userLogin

        def getUserName(self) -> str:
            return self.userName

    class FakeTwitchUserIdsRepository(TwitchUserIdsRepositoryInterface):

        async def clearCaches(self):
            pass

        async def getById(
            self,
            userId: str,
        ) -> TwitchUserData | None:
            raise NotImplementedError()

        async def getByLoginOrName(
            self,
            userLoginOrName: str,
        ) -> TwitchUserData | None:
            raise NotImplementedError()

        async def getIdByLoginOrName(
            self,
            userLoginOrName: str,
        ) -> str | None:
            raise NotImplementedError()

        async def requireById(
            self,
            userId: str,
        ) -> TwitchUserData:
            return TwitchUserData(
                storeDateTime = datetime.now(timezone.utc),
                userId = userId,
                userLogin = 'stashiocat',
                userName = 'stashiocat',
            )

        async def requireByLoginOrName(
            self,
            userLoginOrName: str,
        ) -> TwitchUserData:
            raise NotImplementedError()

        async def requireIdByLoginOrName(
            self,
            userLoginOrName: str,
        ) -> str:
            raise NotImplementedError()

        async def set(
            self,
            userId: str,
            userLogin: str,
            userName: str,
        ):
            raise NotImplementedError()

        async def setAll(
            self,
            users: Collection[TwitchUserInterface],
        ):
            raise NotImplementedError()

    presenter: Final[CutenessPresenterInterface] = CutenessPresenter(
        twitchUserIdsRepository = FakeTwitchUserIdsRepository(),
    )

    @pytest.mark.asyncio
    async def test_printCuteness_withNoneCuteness(self):
        result = CutenessResult(
            cutenessDate = CutenessDate("2022-06"),
            cuteness = None,
            userId = 'abc',
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
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == 'stashiocat\'s Jun 2022 cuteness is 10 ✨'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, CutenessPresenterInterface)
        assert isinstance(self.presenter, CutenessPresenter)
