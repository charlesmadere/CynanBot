import re
import traceback
from typing import Final, Pattern

from .determineTimeoutTargetUseCaseInterface import DetermineTimeoutTargetUseCaseInterface
from ..exceptions import ImmuneTimeoutTargetException, NoGivenTimeoutTargetException, UnknownTimeoutTargetException
from ..models.actions.absTimeoutAction import AbsTimeoutAction
from ..models.timeoutTarget import TimeoutTarget
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.userIds.twitchUserData import TwitchUserData
from ...twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from ...users.exceptions import NoSuchUserException


class DetermineTimeoutTargetUseCase(DetermineTimeoutTargetUseCaseInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

        self.__timeoutTargetRegEx: Final[Pattern] = re.compile(r'^\s*@?(\w+)\s*', re.IGNORECASE)

    async def __determineTargetUserName(
        self,
        timeoutAction: AbsTimeoutAction,
    ) -> str:
        messageContainingTarget: str | None = timeoutAction.getChatMessage()
        if not utils.isValidStr(messageContainingTarget):
            raise NoGivenTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=})')

        targetMatch = self.__timeoutTargetRegEx.match(messageContainingTarget)
        if targetMatch is None:
            raise NoGivenTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=}) ({targetMatch=})')

        targetUserName: str | None = targetMatch.group(1)
        if not utils.isValidStr(targetUserName) or not utils.strContainsAlphanumericCharacters(targetUserName):
            raise NoGivenTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=}) ({targetMatch=}) ({targetUserName=})')

        return targetUserName

    async def __fetchUserData(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> TwitchUserData:
        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        try:
            return await self.__twitchUserIdsHelper.requireById(
                userId = userId,
                twitchAccessToken = twitchAccessToken,
            )
        except NoSuchUserException as e:
            self.__timber.log('DetermineTimeoutTargetUseCase', f'Failed to fetch user data to use as a timeout target ({twitchChannelId=}) ({userId=})', e, traceback.format_exc())
            raise UnknownTimeoutTargetException(f'Failed to fetch user data to use as a timeout target ({twitchChannelId=}) ({userId=})')

    async def __fetchUserId(
        self,
        twitchChannelId: str,
        userName: str,
    ) -> str:
        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        try:
            return await self.__twitchUserIdsHelper.requireIdByLoginOrName(
                userLoginOrName = userName,
                twitchAccessToken = twitchAccessToken,
            )
        except NoSuchUserException as e:
            self.__timber.log('DetermineTimeoutTargetUseCase', f'Failed to fetch user ID to use as a timeout target ({twitchChannelId=}) ({userName=})', e, traceback.format_exc())
            raise UnknownTimeoutTargetException(f'Failed to fetch user ID to use as a timeout target ({twitchChannelId=}) ({userName=})')

    async def invoke(
        self,
        timeoutAction: AbsTimeoutAction,
    ) -> TimeoutTarget:
        if not isinstance(timeoutAction, AbsTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        targetUserName = await self.__determineTargetUserName(
            timeoutAction = timeoutAction,
        )

        targetUserId = await self.__fetchUserId(
            twitchChannelId = timeoutAction.getTwitchChannelId(),
            userName = targetUserName,
        )

        if targetUserId == timeoutAction.getTwitchChannelId():
            targetUserId = timeoutAction.getInstigatorUserId()

        targetUserData = await self.__fetchUserData(
            twitchChannelId = timeoutAction.getTwitchChannelId(),
            userId = targetUserId,
        )

        timeoutTarget = TimeoutTarget(
            userId = targetUserData.userId,
            userLogin = targetUserData.userLogin,
            userName = targetUserData.userName,
        )

        if await self.__timeoutImmuneUserIdsRepository.isImmune(targetUserId):
            raise ImmuneTimeoutTargetException(
                timeoutTarget = timeoutTarget,
            )
        else:
            return timeoutTarget
