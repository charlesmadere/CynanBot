from typing import Final

from .chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..models.chatterPrefferedTts import ChatterPreferredTts
from ..repository.chatterPreferredTtsRepositoryInterface import ChatterPreferredTtsRepositoryInterface
from ..settings.chatterPreferredTtsSettingsRepositoryInterface import ChatterPreferredTtsSettingsRepositoryInterface
from ...misc import utils as utils


class ChatterPreferredTtsHelper(ChatterPreferredTtsHelperInterface):

    def __init__(
        self,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')

        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return None

        preferredTts = await self.__chatterPreferredTtsRepository.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        if preferredTts is None:
            return None
        elif not await self.__chatterPreferredTtsSettingsRepository.isTtsProviderEnabled(
            provider = preferredTts.properties.provider
        ):
            return None
        else:
            return preferredTts
