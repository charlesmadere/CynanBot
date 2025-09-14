from typing import Final

from ..models.useChatterItemAction import UseChatterItemAction
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ...voicemail.models.addVoicemailResult import AddVoicemailResult
from ...voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class CassetteTapeItemUseCase:

    def __init__(
        self,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface,
    ):
        if not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    async def invoke(self, action: UseChatterItemAction) -> AddVoicemailResult:
        if not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        return AddVoicemailResult.FEATURE_DISABLED
