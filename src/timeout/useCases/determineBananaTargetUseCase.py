import random
import re
import traceback
from typing import Final, Pattern

from ..exceptions import UnknownTimeoutTargetException
from ..models.actions.bananaTimeoutAction import BananaTimeoutAction
from ..models.bananaTimeoutTarget import BananaTimeoutTarget
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ..timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.exceptions import NoSuchUserException
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class DetermineBananaTargetUseCase:

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHistoryRepository, TimeoutActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutActionHistoryRepository argument is malformed: \"{timeoutActionHistoryRepository}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionHistoryRepository: Final[TimeoutActionHistoryRepositoryInterface] = timeoutActionHistoryRepository
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__timeoutTargetRegEx: Final[Pattern] = re.compile(r'^\s*@?(\w+)\s*', re.IGNORECASE)

    async def __determineTargetUserName(
        self,
        timeoutAction: BananaTimeoutAction,
    ) -> str:
        messageContainingTarget: str | None = timeoutAction.chatMessage

        if not utils.isValidStr(messageContainingTarget) and timeoutAction.pointRedemption is not None:
            messageContainingTarget = timeoutAction.pointRedemption.message

        if not utils.isValidStr(messageContainingTarget):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=})')

        messageContainingTarget = await self.__twitchMessageStringUtils.removeCheerStrings(messageContainingTarget)

        if not utils.isValidStr(messageContainingTarget):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=})')

        targetMatch = self.__timeoutTargetRegEx.match(messageContainingTarget)

        if targetMatch is None:
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=}) ({targetMatch=})')

        targetUserName: str | None = targetMatch.group(1)

        if not utils.isValidStr(targetUserName):
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
            self.__timber.log('DetermineBananaTargetUseCase', f'Failed to fetch user ID to use as a timeout target ({twitchChannelId=}) ({userName=}): {e}', e, traceback.format_exc())
            raise UnknownTimeoutTargetException(f'Failed to fetch user ID to use as a timeout target ({twitchChannelId=}) ({userName=})')

    async def __generateDiceRoll(self) -> TimeoutDiceRoll:
        dieSize = await self.__timeoutActionSettings.getDieSize()
        roll = random.randint(1, dieSize)

        return TimeoutDiceRoll(
            dieSize = dieSize,
            roll = roll,
        )

    async def invoke(
        self,
        timeoutAction: BananaTimeoutAction,
    ) -> BananaTimeoutTarget:
        if not isinstance(timeoutAction, BananaTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        targetUserName = await self.__determineTargetUserName(
            timeoutAction = timeoutAction,
        )

        targetUserId = await self.__fetchUserId(
            twitchChannelId = timeoutAction.twitchChannelId,
            userName = targetUserName,
        )

        timeoutTarget = BananaTimeoutTarget(
            targetUserId = targetUserId,
            targetUserName = targetUserName,
        )

        if not timeoutAction.isRandomChanceEnabled:
            await self.__activeChattersRepository.remove(
                chatterUserId = timeoutTarget.targetUserId,
                twitchChannelId = timeoutAction.twitchChannelId,
            )

            return timeoutTarget

        # TODO
        diceRoll = await self.__generateDiceRoll()

        # TODO
        raise RuntimeError()
