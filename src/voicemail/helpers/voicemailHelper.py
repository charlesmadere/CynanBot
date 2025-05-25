from typing import Final

from frozenlist import FrozenList

from .voicemailHelperInterface import VoicemailHelperInterface
from ..models.addVoicemailResult import AddVoicemailResult
from ..models.voicemailData import VoicemailData
from ..repositories.voicemailsRepositoryInterface import VoicemailsRepositoryInterface
from ..settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface
from ...chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider


class VoicemailHelper(VoicemailHelperInterface):

    def __init__(
        self,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        timber: TimberInterface,
        voicemailsRepository: VoicemailsRepositoryInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(voicemailsRepository, VoicemailsRepositoryInterface):
            raise TypeError(f'voicemailsRepository argument is malformed: \"{voicemailsRepository}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__timber: Final[TimberInterface] = timber
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

        chatterPreferredTts = await self.__chatterPreferredTtsRepository.get(
            chatterUserId = originatingUserId,
            twitchChannelId = twitchChannelId
        )

        ttsProvider: TtsProvider | None = None

        if chatterPreferredTts is not None:
            ttsProvider = chatterPreferredTts.preferredTts.preferredTtsProvider

        return await self.__voicemailsRepository.addVoicemail(
            message = cleanedMessage,
            originatingUserId = originatingUserId,
            targetUserId = targetUserId,
            ttsProvider = ttsProvider,
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
    ) -> FrozenList[VoicemailData]:
        if not utils.isValidStr(originatingUserId):
            raise TypeError(f'originatingUserId argument is malformed: \"{originatingUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return await self.__voicemailsRepository.getAllForOriginatingUser(
            originatingUserId = originatingUserId,
            twitchChannelId = twitchChannelId
        )

    async def getAllForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> FrozenList[VoicemailData]:
        if not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return await self.__voicemailsRepository.getAllForTargetUser(
            targetUserId = targetUserId,
            twitchChannelId = twitchChannelId
        )

    async def getAndRemoveForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> VoicemailData | None:
        if not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        voicemail = await self.__voicemailsRepository.getForTargetUser(
            targetUserId = targetUserId,
            twitchChannelId = twitchChannelId
        )

        if voicemail is None:
            return None

        await self.__voicemailsRepository.removeVoicemail(
            twitchChannelId = twitchChannelId,
            voicemailId = voicemail.voicemailId
        )

        return voicemail
