from typing import Final

from .chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..models.chatterPreferredNameData import ChatterPreferredNameData
from ..repositories.chatterPreferredNameRepositoryInterface import ChatterPreferredNameRepositoryInterface
from ..settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ...misc import utils as utils


class ChatterPreferredNameHelper(ChatterPreferredNameHelperInterface):

    def __init__(
        self,
        chatterPreferredNameRepository: ChatterPreferredNameRepositoryInterface,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface,
    ):
        if not isinstance(chatterPreferredNameRepository, ChatterPreferredNameRepositoryInterface):
            raise TypeError(f'chatterPreferredNameRepository argument is malformed: \"{chatterPreferredNameRepository}\"')
        elif not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')

        self.__chatterPreferredNameRepository: Final[ChatterPreferredNameRepositoryInterface] = chatterPreferredNameRepository
        self.__chatterPreferredNameSettings: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings

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
