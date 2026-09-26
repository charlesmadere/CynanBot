import re
from dataclasses import dataclass
from typing import Final, Pattern

from ..exceptions import CassetteTapeMessageHasNoTargetException, CassetteTapeFeatureIsDisabledException, \
    CassetteTapeTargetIsNotFollowingException, VoicemailMessageIsEmptyException, VoicemailTargetInboxIsFullException, \
    VoicemailTargetIsOriginatingUserException, VoicemailTargetIsStreamerException
from ..models.chatterItemType import ChatterItemType
from ..models.useChatterItemAction import UseChatterItemAction
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..useCases.cassetteTapeItemUseCaseInterface import CassetteTapeItemUseCaseInterface
from ...misc import utils as utils
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface
from ...twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from ...users.exceptions import NoSuchUserException
from ...voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ...voicemail.models.addVoicemailResult import AddVoicemailResult
from ...voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class CassetteTapeItemUseCase(CassetteTapeItemUseCaseInterface):

    @dataclass(frozen = True, slots = True)
    class ParsedVoicemailRequest:
        cleanedMessage: str
        targetUserData: TwitchUserInterface

    def __init__(
        self,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface,
    ):
        if not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

        self.__targetUserNameRegEx: Final[Pattern] = re.compile(r'^\s*@?(\w+)\s*', re.IGNORECASE)

    async def invoke(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> CassetteTapeItemUseCaseInterface.Result:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__isCassetteTapeFeatureEnabled():
            raise CassetteTapeFeatureIsDisabledException()

        parsedVoicemailRequest = await self.__parseVoicemailRequest(
            twitchAccessToken = twitchAccessToken,
            action = action,
        )

        if await self.__voicemailSettingsRepository.targetUserMustBeFollowing():
            isFollowing = await self.__twitchFollowingStatusRepository.isFollowing(
                twitchAccessToken = twitchAccessToken,
                twitchChannelId = action.twitchChannelId,
                userId = parsedVoicemailRequest.targetUserData.getUserId(),
            )

            if not isFollowing:
                raise CassetteTapeTargetIsNotFollowingException(
                    targetUserData = parsedVoicemailRequest.targetUserData,
                    originatingAction = action,
                )

        addVoicemailResult = await self.__voicemailHelper.addVoicemail(
            message = parsedVoicemailRequest.cleanedMessage,
            originatingUserId = action.chatterUserId,
            targetUserId = parsedVoicemailRequest.targetUserData.getUserId(),
            twitchChannelId = action.twitchChannelId,
        )

        match addVoicemailResult:
            case AddVoicemailResult.FEATURE_DISABLED:
                raise CassetteTapeFeatureIsDisabledException()

            case AddVoicemailResult.MAXIMUM_FOR_TARGET_USER:
                raise VoicemailTargetInboxIsFullException(
                    targetUserData = parsedVoicemailRequest.targetUserData,
                )

            case AddVoicemailResult.MESSAGE_MALFORMED:
                raise VoicemailMessageIsEmptyException(
                    message = parsedVoicemailRequest.cleanedMessage,
                    originatingAction = action,
                )

            case AddVoicemailResult.OK:
                return CassetteTapeItemUseCaseInterface.Result(
                    addVoicemailResult = addVoicemailResult,
                    targetUserData = parsedVoicemailRequest.targetUserData,
                )

            case AddVoicemailResult.TARGET_USER_IS_ORIGINATING_USER:
                raise VoicemailTargetIsOriginatingUserException()

            case AddVoicemailResult.TARGET_USER_IS_TWITCH_CHANNEL_USER:
                raise VoicemailTargetIsStreamerException()

    async def __isCassetteTapeFeatureEnabled(self) -> bool:
        if ChatterItemType.CASSETTE_TAPE not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return False
        elif not await self.__voicemailSettingsRepository.isEnabled():
            return False
        else:
            return True

    async def __parseVoicemailRequest(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> ParsedVoicemailRequest:
        cleanedMessage = utils.cleanStr(action.chatMessage)

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
            targetUserData = await self.__twitchUserIdsHelper.requireByLoginOrName(
                userLoginOrName = targetUserName,
                twitchAccessToken = twitchAccessToken,
            )
        except NoSuchUserException:
            raise CassetteTapeMessageHasNoTargetException(
                cleanedMessage = cleanedMessage,
                originatingAction = action,
            )

        return CassetteTapeItemUseCase.ParsedVoicemailRequest(
            cleanedMessage = cleanedMessage,
            targetUserData = targetUserData,
        )
