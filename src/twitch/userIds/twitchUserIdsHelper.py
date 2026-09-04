import traceback
from datetime import timedelta
from typing import Collection, Final

from .exceptions import NoTwitchUserDataFoundException
from .twitchUserData import TwitchUserData
from .twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from .twitchUserIdsRepositoryInterface import TwitchUserIdsRepositoryInterface
from ..api.models.twitchFetchUserWithIdRequest import TwitchFetchUserWithIdRequest
from ..api.models.twitchFetchUserWithLoginRequest import TwitchFetchUserWithLoginRequest
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..localModels.twitchUserInterface import TwitchUserInterface
from ..localModels.twitchUserStub import TwitchUserStub
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TwitchUserIdsHelper(TwitchUserIdsHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchUserIdsRepository: TwitchUserIdsRepositoryInterface,
        userDataTimeToLive: timedelta = timedelta(days = 180),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchUserIdsRepository, TwitchUserIdsRepositoryInterface):
            raise TypeError(f'twitchUserIdsRepository argument is malformed: \"{twitchUserIdsRepository}\"')
        elif not isinstance(userDataTimeToLive, timedelta):
            raise TypeError(f'userDataTimeToLive argument is malformed: \"{userDataTimeToLive}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchUserIdsRepository: Final[TwitchUserIdsRepositoryInterface] = twitchUserIdsRepository
        self.__userDataTimeToLive: Final[timedelta] = userDataTimeToLive

    async def __fetchById(
        self,
        userId: str,
        twitchAccessToken: str | None,
    ) -> TwitchUserStub | None:
        if not utils.isValidStr(twitchAccessToken):
            return None

        request = TwitchFetchUserWithIdRequest(
            userId = userId,
        )

        try:
            response = await self.__twitchApiService.fetchUser(
                twitchAccessToken = twitchAccessToken,
                fetchUserRequest = request,
            )
        except Exception as e:
            self.__timber.log('TwitchUserIdsHelper', f'Failed to fetch Twitch user by ID ({userId=}) ({request=})', e, traceback.format_exc())
            return None

        for user in response.data:
            if user.userId == userId:
                return TwitchUserStub(
                    userId = user.userId,
                    userLogin = user.userLogin,
                    userName = user.displayName,
                )

        self.__timber.log('TwitchUserIdsHelper', f'No Twitch user found for ID ({userId=}) ({request=}) ({response=})')
        return None

    async def __fetchByLogin(
        self,
        userLogin: str,
        twitchAccessToken: str | None,
    ) -> TwitchUserStub | None:
        if not utils.isValidStr(twitchAccessToken):
            return None

        request = TwitchFetchUserWithLoginRequest(
            userLogin = userLogin,
        )

        try:
            response = await self.__twitchApiService.fetchUser(
                twitchAccessToken = twitchAccessToken,
                fetchUserRequest = request,
            )
        except Exception as e:
            self.__timber.log('TwitchUserIdsHelper', f'Failed to fetch Twitch user by login ({userLogin=}) ({request=})', e, traceback.format_exc())
            return None

        for user in response.data:
            if user.userLogin == userLogin:
                return TwitchUserStub(
                    userId = user.userId,
                    userLogin = user.userLogin,
                    userName = user.displayName,
                )

        self.__timber.log('TwitchUserIdsHelper', f'No Twitch user found for login ({userLogin=}) ({request=}) ({response=})')
        return None

    async def getById(
        self,
        userId: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData | None:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userData = await self.__twitchUserIdsRepository.getById(
            userId = userId,
        )

        if userData is not None and (not utils.isValidStr(twitchAccessToken) or await self.__isNotExpired(userData)):
            return userData

        userStub = await self.__fetchById(
            userId = userId,
            twitchAccessToken = twitchAccessToken,
        )

        if userStub is None:
            if userData is None:
                return None
            else:
                self.__timber.log('TwitchUserIdsHelper', f'Attempted but failed to fetch Twitch user by ID, so will purposely return old data ({userId=}) ({userData=}) ({userStub=})')
                return userData

        await self.set(
            userId = userStub.userId,
            userLogin = userStub.userLogin,
            userName = userStub.userName,
        )

        return await self.requireById(
            userId = userId,
        )

    async def getByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData | None:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userData = await self.__twitchUserIdsRepository.getByLoginOrName(
            userLoginOrName = userLoginOrName,
        )

        if userData is not None and (not utils.isValidStr(twitchAccessToken) or await self.__isNotExpired(userData)):
            return userData

        userStub = await self.__fetchByLogin(
            userLogin = userLoginOrName,
            twitchAccessToken = twitchAccessToken,
        )

        if userStub is None:
            if userData is None:
                return None
            else:
                self.__timber.log('TwitchUserIdsHelper', f'Attempted but failed to fetch Twitch user by login or name, so will purposely return old data ({userLoginOrName=}) ({userData=}) ({userStub=})')
                return userData

        await self.set(
            userId = userStub.userId,
            userLogin = userStub.userLogin,
            userName = userStub.userName,
        )

        return await self.requireById(
            userId = userStub.userId,
        )

    async def getIdByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> str | None:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userData = await self.getByLoginOrName(
            userLoginOrName = userLoginOrName,
            twitchAccessToken = twitchAccessToken,
        )

        if userData is None:
            return None

        return userData.userId

    async def __isNotExpired(self, userData: TwitchUserData) -> bool:
        now = self.__timeZoneRepository.getNow()
        return now <= (userData.storeDateTime + self.__userDataTimeToLive)

    async def requireById(
        self,
        userId: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userData = await self.getById(
            userId = userId,
            twitchAccessToken = twitchAccessToken,
        )

        if userData is None:
            hasTwitchAccessToken = utils.isValidStr(twitchAccessToken)
            raise NoTwitchUserDataFoundException(f'No Twitch user data found ({userId=}) ({hasTwitchAccessToken=})')

        return userData

    async def requireByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userData = await self.getByLoginOrName(
            userLoginOrName = userLoginOrName,
            twitchAccessToken = twitchAccessToken,
        )

        if userData is None:
            hasTwitchAccessToken = utils.isValidStr(twitchAccessToken)
            raise NoTwitchUserDataFoundException(f'No Twitch user data found ({userLoginOrName=}) ({hasTwitchAccessToken=})')

        return userData

    async def requireIdByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> str:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userData = await self.getByLoginOrName(
            userLoginOrName = userLoginOrName,
            twitchAccessToken = twitchAccessToken,
        )

        if userData is None:
            hasTwitchAccessToken = utils.isValidStr(twitchAccessToken)
            raise NoTwitchUserDataFoundException(f'No Twitch user data found ({userLoginOrName=}) ({hasTwitchAccessToken=})')

        return userData.userId

    async def set(
        self,
        userId: str,
        userLogin: str,
        userName: str,
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        await self.__twitchUserIdsRepository.set(
            userId = userId,
            userLogin = userLogin,
            userName = userName,
        )

    async def setAll(
        self,
        users: Collection[TwitchUserInterface],
    ):
        if not isinstance(users, Collection):
            raise TypeError(f'users argument is malformed: \"{users}\"')

        await self.__twitchUserIdsRepository.setAll(
            users = users,
        )
