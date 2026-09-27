from datetime import datetime, timezone
from typing import Final, Collection

import pytest

from src.cuteness.cutenessDate import CutenessDate
from src.cuteness.cutenessPresenter import CutenessPresenter
from src.cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from src.cuteness.cutenessResult import CutenessResult
from src.twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from src.twitch.localModels.twitchUserInterface import TwitchUserInterface
from src.twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from src.twitch.userIds.exceptions import NoTwitchUserDataFoundException
from src.twitch.userIds.twitchUserData import TwitchUserData
from src.twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class TestCutenessPresenter:

    CYNANBOT_USER_ID: Final[str] = 'abc123'

    STASHIO_USER_ID: Final[str] = 'def456'

    CYNANBOT_USER: Final[TwitchUserData] = TwitchUserData(
        storeDateTime = datetime.now(timezone.utc),
        userId = CYNANBOT_USER_ID,
        userLogin = 'cynanbot',
        userName = 'CynanBot',
    )

    STASHIO_USER: Final[TwitchUserData] = TwitchUserData(
        storeDateTime = datetime.now(timezone.utc),
        userId = STASHIO_USER_ID,
        userLogin = 'stashiocat',
        userName = 'stashiocat',
    )

    class FakeTwitchHandleProvider(TwitchHandleProviderInterface):

        async def getTwitchHandle(self) -> str:
            return TestCutenessPresenter.CYNANBOT_USER.userLogin

    class FakeTwitchTokensRepository(TwitchTokensRepositoryInterface):

        async def addUser(
            self,
            code: str,
            twitchChannel: str,
            twitchChannelId: str,
        ):
            raise NotImplementedError()

        async def clearCaches(self):
            pass

        async def getAccessToken(
            self,
            twitchChannel: str,
        ) -> str | None:
            return None

        async def getAccessTokenById(
            self,
            twitchChannelId: str,
        ) -> str | None:
            return None

        async def removeUser(
            self,
            twitchChannel: str,
        ):
            raise NotImplementedError()

        async def removeUserById(
            self,
            twitchChannelId: str,
        ):
            raise NotImplementedError()

        async def requireAccessToken(
            self,
            twitchChannel: str,
        ) -> str:
            raise NotImplementedError()

        async def requireAccessTokenById(
            self,
            twitchChannelId: str,
        ) -> str:
            raise NotImplementedError()

        def start(self):
            raise NotImplementedError()

    class FakeTwitchUserIdsHelper(TwitchUserIdsHelperInterface):

        async def clearCaches(self):
            pass

        async def getById(
            self,
            userId: str,
            twitchAccessToken: str | None = None,
        ) -> TwitchUserData | None:
            raise NotImplementedError()

        async def getByLoginOrName(
            self,
            userLoginOrName: str,
            twitchAccessToken: str | None = None,
        ) -> TwitchUserData | None:
            raise NotImplementedError()

        async def getIdByLoginOrName(
            self,
            userLoginOrName: str,
            twitchAccessToken: str | None = None,
        ) -> str | None:
            raise NotImplementedError()

        async def requireById(
            self,
            userId: str,
            twitchAccessToken: str | None = None,
        ) -> TwitchUserData:
            if userId == TestCutenessPresenter.CYNANBOT_USER_ID:
                return TestCutenessPresenter.CYNANBOT_USER

            elif userId == TestCutenessPresenter.STASHIO_USER_ID:
                return TestCutenessPresenter.STASHIO_USER

            else:
                raise NoTwitchUserDataFoundException(f'No Twitch user data found for userId: \"{userId}\"')

        async def requireByLoginOrName(
            self,
            userLoginOrName: str,
            twitchAccessToken: str | None = None,
        ) -> TwitchUserData:
            raise NotImplementedError()

        async def requireIdByLoginOrName(
            self,
            userLoginOrName: str,
            twitchAccessToken: str | None = None,
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
        twitchHandleProvider = FakeTwitchHandleProvider(),
        twitchTokensRepository = FakeTwitchTokensRepository(),
        twitchUserIdsHelper = FakeTwitchUserIdsHelper(),
    )

    @pytest.mark.asyncio
    async def test_printCuteness_withNoneCuteness(self):
        result = CutenessResult(
            cutenessDate = CutenessDate("2022-06"),
            cuteness = None,
            userId = self.STASHIO_USER_ID,
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == '😿 stashiocat has no cuteness in Jun 2022'

    @pytest.mark.asyncio
    async def test_printCuteness_with0Cuteness(self):
        result = CutenessResult(
            cutenessDate = CutenessDate("2022-06"),
            cuteness = None,
            userId = self.STASHIO_USER_ID,
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == '😿 stashiocat has no cuteness in Jun 2022'

    @pytest.mark.asyncio
    async def test_printCuteness_with10Cuteness(self):
        result = CutenessResult(
            cutenessDate = CutenessDate("2022-06"),
            cuteness = 10,
            userId = self.STASHIO_USER_ID,
        )

        printOut = await self.presenter.printCuteness(result)
        assert isinstance(printOut, str)
        assert printOut == '✨ stashiocat\'s Jun 2022 cuteness is 10'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, CutenessPresenter)
        assert isinstance(self.presenter, CutenessPresenterInterface)
