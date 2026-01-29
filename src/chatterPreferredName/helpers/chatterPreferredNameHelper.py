from typing import Any, Final

from .chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from .chatterPreferredNameStringCleanerInterface import ChatterPreferredNameStringCleanerInterface
from ..exceptions import ChatterPreferredNameFeatureIsDisabledException, ChatterPreferredNameIsInvalidException
from ..models.chatterPreferredNameData import ChatterPreferredNameData
from ..repositories.chatterPreferredNameRepositoryInterface import ChatterPreferredNameRepositoryInterface
from ..settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...twitch.api.models.twitchFetchUserWithIdRequest import TwitchFetchUserWithIdRequest
from ...twitch.api.models.twitchUser import TwitchUser
from ...twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from ...twitch.exceptions import TwitchStatusCodeException
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface


class ChatterPreferredNameHelper(ChatterPreferredNameHelperInterface):

    def __init__(
        self,
        chatterPreferredNameRepository: ChatterPreferredNameRepositoryInterface,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface,
        chatterPreferredNameStringCleaner: ChatterPreferredNameStringCleanerInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
    ):
        if not isinstance(chatterPreferredNameRepository, ChatterPreferredNameRepositoryInterface):
            raise TypeError(f'chatterPreferredNameRepository argument is malformed: \"{chatterPreferredNameRepository}\"')
        elif not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif not isinstance(chatterPreferredNameStringCleaner, ChatterPreferredNameStringCleanerInterface):
            raise TypeError(f'chatterPreferredNameStringCleaner argument is malformed: \"{chatterPreferredNameStringCleaner}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')

        self.__chatterPreferredNameRepository: Final[ChatterPreferredNameRepositoryInterface] = chatterPreferredNameRepository
        self.__chatterPreferredNameSettings: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings
        self.__chatterPreferredNameStringCleaner: Final[ChatterPreferredNameStringCleanerInterface] = chatterPreferredNameStringCleaner
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterPreferredNameSettings.isEnabled():
            return None

        return await self.__chatterPreferredNameRepository.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

    async def set(
        self,
        chatterUserId: str,
        preferredName: str | Any | None,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterPreferredNameSettings.isEnabled():
            raise ChatterPreferredNameFeatureIsDisabledException()

        preferredName = await self.__chatterPreferredNameStringCleaner.clean(
            preferredName = preferredName,
        )

        if not utils.isValidStr(preferredName):
            raise ChatterPreferredNameIsInvalidException(f'The given preferred name is invalid ({chatterUserId=}) ({preferredName=}) ({twitchChannelId=})')

        await self.__verifyPreferredNameIsNotStreamerName(
            chatterUserId = chatterUserId,
            preferredName = preferredName,
            twitchChannelId = twitchChannelId,
        )

        return await self.__chatterPreferredNameRepository.set(
            chatterUserId = chatterUserId,
            preferredName = preferredName,
            twitchChannelId = twitchChannelId,
        )

    async def __verifyPreferredNameIsNotStreamerName(
        self,
        chatterUserId: str,
        preferredName: str,
        twitchChannelId: str,
    ):
        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(twitchAccessToken):
            return

        try:
            response = await self.__twitchApiService.fetchUser(
                twitchAccessToken = twitchAccessToken,
                fetchUserRequest = TwitchFetchUserWithIdRequest(
                    userId = twitchChannelId,
                ),
            )
        except (GenericNetworkException, TwitchStatusCodeException):
            # let's just ignore this exception for now
            return

        twitchUser: TwitchUser | None = None

        for user in response.data:
            if user.userId == twitchChannelId:
                twitchUser = user
                break

        if twitchUser is None:
            return

        if preferredName.casefold() == twitchUser.displayName.casefold():
            raise ChatterPreferredNameIsInvalidException(f'The given preferred name is invalid because it matches the streamer\'s displayName ({chatterUserId=}) ({preferredName=}) ({twitchChannelId=}) ({twitchUser=})')
        elif preferredName.casefold() == twitchUser.userLogin.casefold():
            raise ChatterPreferredNameIsInvalidException(f'The given preferred name is invalid because it matches the streamer\'s userLogin ({chatterUserId=}) ({preferredName=}) ({twitchChannelId=}) ({twitchUser=})')
