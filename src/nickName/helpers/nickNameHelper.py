from typing import Final

from .nickNameHelperInterface import NickNameHelperInterface
from ..models.nickNameData import NickNameData
from ..repositories.nickNameRepositoryInterface import NickNameRepositoryInterface
from ..settings.nickNameSettingsInterface import NickNameSettingsInterface
from ...misc import utils as utils


class NickNameHelper(NickNameHelperInterface):

    def __init__(
        self,
        nickNameRepository: NickNameRepositoryInterface,
        nickNameSettings: NickNameSettingsInterface,
    ):
        if not isinstance(nickNameRepository, NickNameRepositoryInterface):
            raise TypeError(f'nickNameRepository argument is malformed: \"{nickNameRepository}\"')
        elif not isinstance(nickNameSettings, NickNameSettingsInterface):
            raise TypeError(f'nickNameSettings argument is malformed: \"{nickNameSettings}\"')

        self.__nickNameRepository: Final[NickNameRepositoryInterface] = nickNameRepository
        self.__nickNameSettings: Final[NickNameSettingsInterface] = nickNameSettings

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> NickNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__nickNameSettings.isEnabled():
            return None

        return await self.__nickNameRepository.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )
