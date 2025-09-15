import re
from dataclasses import dataclass
from typing import Final, Pattern

from ..exceptions import CassetteTapeMessageHasNoTargetException, CassetteTapeFeatureIsDisabledException, \
    CassetteTapeTargetIsNotFollowingException, UserTwitchAccessTokenIsMissing, VoicemailMessageIsEmptyException, \
    VoicemailTargetInboxIsFullException, VoicemailTargetIsOriginatingUserException, VoicemailTargetIsStreamerException
from ..models.cassetteTapeUseCaseResult import CassetteTapeUseCaseResult
from ..models.useChatterItemAction import UseChatterItemAction
from ...misc import utils as utils
from ...twitch.exceptions import TwitchAccessTokenMissingException
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.exceptions import NoSuchUserException
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ...voicemail.models.addVoicemailResult import AddVoicemailResult
from ...voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class CassetteTapeItemUseCase:

    @dataclass(frozen = True)
    class ParsedVoicemailRequest:
        cleanedMessage: str
        targetUserId: str
        targetUserName: str

    def __init__(
        self,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface,
    ):
        if not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

        self.__targetUserNameRegEx: Final[Pattern] = re.compile(r'^\s*@?(\w+)\s*', re.IGNORECASE)

    async def invoke(self, action: UseChatterItemAction) -> CassetteTapeUseCaseResult:
        if not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__voicemailSettingsRepository.isEnabled():
            raise CassetteTapeFeatureIsDisabledException()

        try:
            userTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
                twitchChannelId = action.twitchChannelId,
            )
        except TwitchAccessTokenMissingException:
            raise UserTwitchAccessTokenIsMissing(f'No Twitch access token is available for the given Twitch channel ({action=})')

        parsedVoicemailRequest = await self.__parseVoicemailRequest(
            userTwitchAccessToken = userTwitchAccessToken,
            action = action,
        )

        if await self.__voicemailSettingsRepository.targetUserMustBeFollowing():
            isFollowing = await self.__twitchFollowingStatusRepository.isFollowing(
                twitchAccessToken = userTwitchAccessToken,
                twitchChannelId = action.twitchChannelId,
                userId = parsedVoicemailRequest.targetUserId,
            )

            if not isFollowing:
                raise CassetteTapeTargetIsNotFollowingException(
                    targetUserId = parsedVoicemailRequest.targetUserId,
                    targetUserName = parsedVoicemailRequest.targetUserName,
                    originatingAction = action,
                )

        addVoicemailResult = await self.__voicemailHelper.addVoicemail(
            message = parsedVoicemailRequest.cleanedMessage,
            originatingUserId = action.chatterUserId,
            targetUserId = parsedVoicemailRequest.targetUserId,
            twitchChannelId = action.twitchChannelId,
        )

        match addVoicemailResult:
            case AddVoicemailResult.FEATURE_DISABLED:
                raise CassetteTapeFeatureIsDisabledException()

            case AddVoicemailResult.MAXIMUM_FOR_TARGET_USER:
                raise VoicemailTargetInboxIsFullException(
                    targetUserId = parsedVoicemailRequest.targetUserId,
                    targetUserName = parsedVoicemailRequest.targetUserName,
                )

            case AddVoicemailResult.MESSAGE_MALFORMED:
                raise VoicemailMessageIsEmptyException(
                    message = parsedVoicemailRequest.cleanedMessage,
                    originatingAction = action,
                )

            case AddVoicemailResult.OK:
                return CassetteTapeUseCaseResult(
                    addVoicemailResult = addVoicemailResult,
                    targetUserId = parsedVoicemailRequest.targetUserId,
                    targetUserName = parsedVoicemailRequest.targetUserName,
                )

            case AddVoicemailResult.TARGET_USER_IS_ORIGINATING_USER:
                raise VoicemailTargetIsOriginatingUserException()

            case AddVoicemailResult.TARGET_USER_IS_TWITCH_CHANNEL_USER:
                raise VoicemailTargetIsStreamerException()

    async def __parseVoicemailRequest(
        self,
        userTwitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> ParsedVoicemailRequest:
        if not utils.isValidStr(action.chatMessage):
            raise VoicemailMessageIsEmptyException(
                message = action.chatMessage,
                originatingAction = action,
            )

        cleanedMessage = await self.__twitchMessageStringUtils.removeCheerStrings(
            message = action.chatMessage,
        )

        if not utils.isValidStr(cleanedMessage):
            raise VoicemailMessageIsEmptyException(
                message = cleanedMessage,
                originatingAction = action,
            )

        userNameMatch = self.__targetUserNameRegEx.match(cleanedMessage)

        if userNameMatch is None or not utils.isValidStr(userNameMatch.group(1)):
            raise CassetteTapeMessageHasNoTargetException(
                cleanedMessage = cleanedMessage,
                originatingAction = action,
            )

        targetUserName = userNameMatch.group(1)
        cleanedMessage = utils.cleanStr(cleanedMessage[userNameMatch.end(1):])

        if not utils.isValidStr(cleanedMessage):
            raise VoicemailMessageIsEmptyException(
                message = cleanedMessage,
                originatingAction = action,
            )

        try:
            targetUserId = await self.__userIdsRepository.requireUserId(
                userName = targetUserName,
                twitchAccessToken = userTwitchAccessToken,
            )
        except NoSuchUserException:
            raise CassetteTapeMessageHasNoTargetException(
                cleanedMessage = cleanedMessage,
                originatingAction = action,
            )

        return CassetteTapeItemUseCase.ParsedVoicemailRequest(
            cleanedMessage = cleanedMessage,
            targetUserId = targetUserId,
            targetUserName = targetUserName,
        )
