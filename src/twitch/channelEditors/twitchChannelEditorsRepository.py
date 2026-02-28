import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final

from .twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..api.models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TwitchChannelEditorsRepository(TwitchChannelEditorsRepositoryInterface):

    @dataclass(frozen = True, slots = True)
    class ChannelEditorsData:
        fetchedAt: datetime
        editors: frozenset[str]
        twitchChannelId: str

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        cacheTimeToLive: timedelta = timedelta(days = 1),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(cacheTimeToLive, timedelta):
            raise TypeError(f'cacheTimeToLive argument is malformed: \"{cacheTimeToLive}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__cacheTimeToLive: Final[timedelta] = cacheTimeToLive

        self.__cache: Final[dict[str, TwitchChannelEditorsRepository.ChannelEditorsData | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchChannelEditorsRepository', 'Caches cleared')

    async def __fetchEditorsData(
        self,
        twitchChannelId: str,
    ) -> ChannelEditorsData:
        editorsData = self.__cache.get(twitchChannelId, None)
        now = datetime.now(self.__timeZoneRepository.getDefault())
        mustFetch: bool

        if editorsData is None:
            mustFetch = True
        else:
            mustFetch = editorsData.fetchedAt + self.__cacheTimeToLive <= now

        if not mustFetch and editorsData is not None:
            return editorsData

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        if utils.isValidStr(twitchAccessToken):
            try:
                channelEditorsResponse = await self.__twitchApiService.fetchChannelEditors(
                    broadcasterId = twitchChannelId,
                    twitchAccessToken = twitchAccessToken,
                )

                editorsData = await self.__mapEditorsResponseToEditorsData(
                    fetchedAt = now,
                    twitchChannelId = twitchChannelId,
                    channelEditorsResponse = channelEditorsResponse,
                )
            except Exception as e:
                self.__timber.log('TwitchChannelEditorsRepository', f'Failed to fetch channel editors ({twitchChannelId=}) ({editorsData=})', e, traceback.format_exc())
                editorsData = None

        if editorsData is None:
            editorsData = TwitchChannelEditorsRepository.ChannelEditorsData(
                fetchedAt = now,
                editors = frozenset(),
                twitchChannelId = twitchChannelId,
            )

        self.__cache[twitchChannelId] = editorsData
        return editorsData

    async def fetchEditorIds(
        self,
        twitchChannelId: str,
    ) -> frozenset[str]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        editorsData = await self.__fetchEditorsData(
            twitchChannelId = twitchChannelId,
        )

        return editorsData.editors

    async def isEditor(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        editorIds = await self.fetchEditorIds(
            twitchChannelId = twitchChannelId,
        )

        return chatterUserId in editorIds

    async def __mapEditorsResponseToEditorsData(
        self,
        fetchedAt: datetime,
        twitchChannelId: str,
        channelEditorsResponse: TwitchChannelEditorsResponse,
    ) -> ChannelEditorsData:
        editorUserIds: set[str] = set()

        for channelEditor in channelEditorsResponse.editors:
            editorUserIds.add(channelEditor.userId)

        return TwitchChannelEditorsRepository.ChannelEditorsData(
            fetchedAt = fetchedAt,
            editors = frozenset(editorUserIds),
            twitchChannelId = twitchChannelId,
        )
