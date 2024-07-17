import traceback
from typing import Any

from .exceptions import NoFuntoonTokenException
from .funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from .funtoonPkmnCatchType import FuntoonPkmnCatchType
from .funtoonRepositoryInterface import FuntoonRepositoryInterface
from .funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class FuntoonRepository(FuntoonRepositoryInterface):

    def __init__(
        self,
        funtoonJsonMapper: FuntoonJsonMapperInterface,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        funtoonApiUrl: str = 'https://funtoon.party/api'
    ):
        if not isinstance(funtoonJsonMapper, FuntoonJsonMapperInterface):
            raise TypeError(f'funtoonJsonMapper argument is malformed: \"{funtoonJsonMapper}\"')
        if not isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface):
            raise TypeError(f'funtoonTokensRepository argument is malformed: \"{funtoonTokensRepository}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidUrl(funtoonApiUrl):
            raise TypeError(f'funtoonApiUrl argument is malformed: \"{funtoonApiUrl}\"')

        self.__funtoonJsonMapper: FuntoonJsonMapperInterface = funtoonJsonMapper
        self.__funtoonTokensRepository: FuntoonTokensRepositoryInterface = funtoonTokensRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__funtoonApiUrl: str = funtoonApiUrl

    async def banTriviaQuestion(self, triviaId: str) -> bool:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'{self.__funtoonApiUrl}/trivia/review/{triviaId}')
        except GenericNetworkException as e:
            self.__timber.log('FuntoonRepository', f'Encountered network error when banning a trivia question ({triviaId=}): {e}', e, traceback.format_exc())
            return False

        responseStatus: int | None = None

        if response is not None:
            responseStatus = response.statusCode
            await response.close()

        return utils.isValidInt(responseStatus) and responseStatus == 200

    async def __hitFuntoon(
        self,
        event: str,
        funtoonToken: str,
        twitchChannel: str,
        twitchChannelId: str,
        data: dict[str, Any] | str | None = None
    ) -> bool:
        if not utils.isValidStr(event):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not utils.isValidStr(funtoonToken):
            raise TypeError(f'funtoonToken argument is malformed: \"{funtoonToken}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        url = f'{self.__funtoonApiUrl}/events/custom'

        jsonPayload = {
            'channel': twitchChannel,
            'data': data,
            'event': event
        }

        self.__timber.log('FuntoonRepository', f'Hitting Funtoon API \"{url}\" ({event=}) ({twitchChannel=}) ({twitchChannelId=}) ({jsonPayload=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = url,
                headers = {
                    'Authorization': funtoonToken,
                    'Content-Type': 'application/json'
                },
                json = jsonPayload
            )
        except GenericNetworkException as e:
            self.__timber.log('FuntoonRepository', f'Encountered network error ({url=}) ({event=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return False

        responseStatusCode: int | None = None
        if response is not None:
            responseStatusCode = response.statusCode
            await response.close()

        if responseStatusCode == 200:
            self.__timber.log('FuntoonRepository', f'Successfully hit Funtoon API ({url=}) ({event=}) ({twitchChannel=}) ({twitchChannelId=})')
            return True
        else:
            self.__timber.log('FuntoonRepository', f'Error when hitting Funtoon API ({url=}) ({event=}) ({twitchChannel=}) ({twitchChannelId=}) ({jsonPayload=}) ({funtoonToken=}) ({response=}) ({responseStatusCode=})')
            return False

    async def pkmnBattle(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str,
        userToBattle: str
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userThatRedeemed):
            raise TypeError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')
        elif not utils.isValidStr(userToBattle):
            raise TypeError(f'userToBattle argument is malformed: \"{userToBattle}\"')

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(
                twitchChannelId = twitchChannelId
            )
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnBattle as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
            return False

        return await self.__hitFuntoon(
            event = 'battle',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            data = {
                'player': userThatRedeemed,
                'opponent': userToBattle
            }
        )

    async def pkmnCatch(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str,
        funtoonPkmnCatchType: FuntoonPkmnCatchType | None = None
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userThatRedeemed):
            raise TypeError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')
        elif funtoonPkmnCatchType is not None and not isinstance(funtoonPkmnCatchType, FuntoonPkmnCatchType):
            raise TypeError(f'funtoonPkmnCatchType argument is malformed: \"{funtoonPkmnCatchType}\"')

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(
                twitchChannelId = twitchChannelId
            )
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnCatch as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
            return False

        data: dict[str, Any] | str | None

        if funtoonPkmnCatchType is None:
            data = userThatRedeemed
        else:
            catchType = await self.__funtoonJsonMapper.serializePkmnCatchType(funtoonPkmnCatchType)

            data = {
                'who': userThatRedeemed,
                'catchType': catchType
            }

        return await self.__hitFuntoon(
            event = 'catch',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            data = data
        )

    async def pkmnGiveEvolve(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userThatRedeemed):
            raise TypeError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(
                twitchChannelId = twitchChannelId
            )
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnGiveEvolve as twitchChannel \"{twitchChannel}\" has no Funtoon token: {e}', e, traceback.format_exc())
            return False

        return await self.__hitFuntoon(
            event = 'giveFreeEvolve',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            data = userThatRedeemed
        )

    async def pkmnGiveShiny(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userThatRedeemed):
            raise TypeError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(
                twitchChannelId = twitchChannelId
            )
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnGiveShiny as twitchChannel \"{twitchChannel}\" has no Funtoon token: {e}', e, traceback.format_exc())
            return False

        return await self.__hitFuntoon(
            event = 'giveFreeShiny',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            data = userThatRedeemed
        )
