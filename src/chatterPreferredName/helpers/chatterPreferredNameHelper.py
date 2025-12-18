from typing import Any, Final

from .chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from .chatterPreferredNameStringCleaner import ChatterPreferredNameStringCleaner
from ..exceptions import ChatterPreferredNameFeatureIsDisabledException, ChatterPreferredNameIsInvalidException
from ..models.chatterPreferredNameData import ChatterPreferredNameData
from ..repositories.chatterPreferredNameRepositoryInterface import ChatterPreferredNameRepositoryInterface
from ..settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ...misc import utils as utils


class ChatterPreferredNameHelper(ChatterPreferredNameHelperInterface):

    def __init__(
        self,
        chatterPreferredNameRepository: ChatterPreferredNameRepositoryInterface,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface,
        chatterPreferredNameStringCleaner: ChatterPreferredNameStringCleaner,
    ):
        if not isinstance(chatterPreferredNameRepository, ChatterPreferredNameRepositoryInterface):
            raise TypeError(f'chatterPreferredNameRepository argument is malformed: \"{chatterPreferredNameRepository}\"')
        elif not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif not isinstance(chatterPreferredNameStringCleaner, ChatterPreferredNameStringCleaner):
            raise TypeError(f'chatterPreferredNameStringCleaner argument is malformed: \"{chatterPreferredNameStringCleaner}\"')

        self.__chatterPreferredNameRepository: Final[ChatterPreferredNameRepositoryInterface] = chatterPreferredNameRepository
        self.__chatterPreferredNameSettings: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings
        self.__chatterPreferredNameStringCleaner: Final[ChatterPreferredNameStringCleaner] = chatterPreferredNameStringCleaner

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

    async def set(
        self,
        chatterUserId: str,
        preferredName: str | Any | None,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__chatterPreferredNameSettings.isEnabled():
            raise ChatterPreferredNameFeatureIsDisabledException()

        preferredName = await self.__chatterPreferredNameStringCleaner.clean(
            name = preferredName,
        )

        if not utils.isValidStr(preferredName):
            raise ChatterPreferredNameIsInvalidException(f'The given preferred name is invalid ({chatterUserId=}) ({preferredName=}) ({twitchChannelId=})')

        return await self.__chatterPreferredNameRepository.set(
            chatterUserId = chatterUserId,
            preferredName = preferredName,
            twitchChannelId = twitchChannelId,
        )
