import re
import traceback
from typing import Final, Pattern

from ..exceptions import UnknownTimeoutTargetException, ImmuneTimeoutTargetException
from ..models.actions.absTimeoutAction import AbsTimeoutAction
from ..models.timeoutTarget import TimeoutTarget
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.exceptions import NoSuchUserException
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class DetermineTimeoutTargetUseCase:

    def __init__(
        self,
        timber: TimberInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__timeoutTargetRegEx: Final[Pattern] = re.compile(r'^\s*@?(\w+)\s*', re.IGNORECASE)

    async def __determineTargetUserName(
        self,
        timeoutAction: AbsTimeoutAction,
    ) -> str:
        messageContainingTarget: str | None = timeoutAction.getChatMessage()
        if not utils.isValidStr(messageContainingTarget):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=})')

        messageContainingTarget = await self.__twitchMessageStringUtils.removeCheerStrings(messageContainingTarget)
        if not utils.isValidStr(messageContainingTarget):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=})')

        targetMatch = self.__timeoutTargetRegEx.match(messageContainingTarget)
        if targetMatch is None:
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=}) ({targetMatch=})')

        targetUserName: str | None = targetMatch.group(1)
        if not utils.isValidStr(targetUserName) or not utils.strContainsAlphanumericCharacters(targetUserName):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=}) ({targetMatch=}) ({targetUserName=})')

        return targetUserName

    async def __fetchUserId(
        self,
        twitchChannelId: str,
        userName: str | None,
    ) -> str:
        if not utils.isValidStr(userName):
            raise UnknownTimeoutTargetException(f'Given invalid/unknown timeout target ({twitchChannelId=}) ({userName=})')

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        try:
            return await self.__userIdsRepository.requireUserId(
                userName = userName,
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

        timeoutTarget = TimeoutTarget(
            userId = targetUserId,
            userName = targetUserName,
        )

        if await self.__timeoutImmuneUserIdsRepository.isImmune(targetUserId):
            raise ImmuneTimeoutTargetException(
                timeoutTarget = timeoutTarget,
            )
        else:
            return timeoutTarget
