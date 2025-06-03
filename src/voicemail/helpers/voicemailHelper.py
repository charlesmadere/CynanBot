from datetime import datetime, timedelta
from typing import Final

from frozenlist import FrozenList

from .voicemailHelperInterface import VoicemailHelperInterface
from ..models.addVoicemailResult import AddVoicemailResult
from ..models.preparedVoicemailData import PreparedVoicemailData
from ..models.voicemailData import VoicemailData
from ..repositories.voicemailsRepositoryInterface import VoicemailsRepositoryInterface
from ..settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class VoicemailHelper(VoicemailHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        voicemailsRepository: VoicemailsRepositoryInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(voicemailsRepository, VoicemailsRepositoryInterface):
            raise TypeError(f'voicemailsRepository argument is malformed: \"{voicemailsRepository}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__voicemailsRepository: Final[VoicemailsRepositoryInterface] = voicemailsRepository
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    async def addVoicemail(
        self,
        message: str | None,
        originatingUserId: str,
        targetUserId: str,
        twitchChannelId: str
    ) -> AddVoicemailResult:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(originatingUserId):
            raise TypeError(f'originatingUserId argument is malformed: \"{originatingUserId}\"')
        elif not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cleanedMessage = utils.cleanStr(message)

        if not utils.isValidStr(cleanedMessage):
            return AddVoicemailResult.MESSAGE_MALFORMED
        elif targetUserId == originatingUserId:
            return AddVoicemailResult.TARGET_USER_IS_ORIGINATING_USER
        elif targetUserId == twitchChannelId:
            return AddVoicemailResult.TARGET_USER_IS_TWITCH_CHANNEL_USER

        allTargetUserVoicemails = await self.__voicemailsRepository.getAllForTargetUser(
            targetUserId = targetUserId,
            twitchChannelId = twitchChannelId
        )

        maximumPerTargetUser = await self.__voicemailSettingsRepository.getMaximumPerTargetUser()

        if len(allTargetUserVoicemails) >= maximumPerTargetUser:
            return AddVoicemailResult.MAXIMUM_FOR_TARGET_USER

        allOriginatingUserVoicemails = await self.__voicemailsRepository.getAllForOriginatingUser(
            originatingUserId = originatingUserId,
            twitchChannelId = twitchChannelId
        )

        maximumPerOriginatingUser = await self.__voicemailSettingsRepository.getMaximumPerOriginatingUser()

        if len(allOriginatingUserVoicemails) >= maximumPerOriginatingUser:
            await self.__deleteOverflowingVoicemails(
                overflowingVoicemails = allOriginatingUserVoicemails,
                maximumVoicemailCount =  maximumPerOriginatingUser,
                originatingUserId = originatingUserId,
                targetUserId = targetUserId,
                twitchChannelId = twitchChannelId
            )

        return await self.__voicemailsRepository.addVoicemail(
            message = cleanedMessage,
            originatingUserId = originatingUserId,
            targetUserId = targetUserId,
            twitchChannelId = twitchChannelId
        )

    async def __deleteOverflowingVoicemails(
        self,
        overflowingVoicemails: FrozenList[VoicemailData],
        maximumVoicemailCount: int,
        originatingUserId: str,
        targetUserId: str,
        twitchChannelId: str
    ):
        numberToDelete = len(overflowingVoicemails) - maximumVoicemailCount

        for index in range(numberToDelete):
            voicemailToDelete = overflowingVoicemails[index]

            await self.__voicemailsRepository.removeVoicemail(
                twitchChannelId = twitchChannelId,
                voicemailId = voicemailToDelete.voicemailId
            )

        self.__timber.log('VoicemailHelper', f'Deleted {numberToDelete} overflowing voicemail(s) ({originatingUserId=}) ({targetUserId=}) ({twitchChannelId=})')

    async def getAllForOriginatingUser(
        self,
        originatingUserId: str,
        twitchChannelId: str
    ) -> FrozenList[PreparedVoicemailData]:
        if not utils.isValidStr(originatingUserId):
            raise TypeError(f'originatingUserId argument is malformed: \"{originatingUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        allForOriginatingUser = await self.__voicemailsRepository.getAllForOriginatingUser(
            originatingUserId = originatingUserId,
            twitchChannelId = twitchChannelId
        )

        allPreparedVoicemails: FrozenList[PreparedVoicemailData] = FrozenList()

        for voicemail in allForOriginatingUser:
            preparedVoicemail = await self.__prepareVoicemailData(
                twitchChannelId = twitchChannelId,
                voicemail = voicemail
            )

            if preparedVoicemail is not None:
                allPreparedVoicemails.append(preparedVoicemail)

        allPreparedVoicemails.freeze()
        return allPreparedVoicemails

    async def getAllForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> FrozenList[PreparedVoicemailData]:
        if not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        allForTargetUser = await self.__voicemailsRepository.getAllForTargetUser(
            targetUserId = targetUserId,
            twitchChannelId = twitchChannelId
        )

        allPreparedVoicemails: FrozenList[PreparedVoicemailData] = FrozenList()

        for voicemail in allForTargetUser:
            preparedVoicemail = await self.__prepareVoicemailData(
                twitchChannelId = twitchChannelId,
                voicemail = voicemail
            )

            if preparedVoicemail is not None:
                allPreparedVoicemails.append(preparedVoicemail)

        allPreparedVoicemails.freeze()
        return allPreparedVoicemails

    async def popForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> PreparedVoicemailData | None:
        if not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        while True:
            voicemail = await self.__voicemailsRepository.getForTargetUser(
                targetUserId = targetUserId,
                twitchChannelId = twitchChannelId
            )

            if voicemail is None:
                return None

            preparedVoicemail = await self.__prepareVoicemailData(
                twitchChannelId = twitchChannelId,
                voicemail = voicemail
            )

            if preparedVoicemail is not None:
                await self.__voicemailsRepository.removeVoicemail(
                    twitchChannelId = twitchChannelId,
                    voicemailId = voicemail.voicemailId
                )

                return preparedVoicemail

    async def __prepareVoicemailData(
        self,
        twitchChannelId: str,
        voicemail: VoicemailData
    ) -> PreparedVoicemailData | None:
        now = datetime.now(self.__timeZoneRepository.getDefault())

        maximumVoicemailAgeDays = timedelta(
            days = await self.__voicemailSettingsRepository.getMaximumVoicemailAgeDays()
        )

        if now - maximumVoicemailAgeDays > voicemail.createdDateTime:
            self.__timber.log('VoicemailHelper', f'This voicemail is too old and will be discarded ({twitchChannelId=}) ({voicemail=}) ({maximumVoicemailAgeDays=})')

            await self.__voicemailsRepository.removeVoicemail(
                twitchChannelId = twitchChannelId,
                voicemailId = voicemail.voicemailId
            )

            return None

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId
        )

        originatingUserName = await self.__userIdsRepository.fetchUserName(
            userId = voicemail.originatingUserId,
            twitchAccessToken = twitchAccessToken
        )

        targetUserName = await self.__userIdsRepository.fetchUserName(
            userId = voicemail.targetUserId,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(originatingUserName) or not utils.isValidStr(targetUserName):
            self.__timber.log('VoicemailHelper', f'Failed to fetch originating user name and/or target user name for a voicemail, this voicemail will be discarded ({twitchChannelId=}) ({voicemail=}) ({maximumVoicemailAgeDays=}) ({originatingUserName=}) ({targetUserName=})')

            await self.__voicemailsRepository.removeVoicemail(
                twitchChannelId = twitchChannelId,
                voicemailId = voicemail.voicemailId
            )

            return None

        return PreparedVoicemailData(
            originatingUserName = originatingUserName,
            targetUserName = targetUserName,
            voicemail = voicemail
        )
