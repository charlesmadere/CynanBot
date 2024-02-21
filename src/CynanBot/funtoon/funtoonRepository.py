import traceback
from typing import Any, Optional

import CynanBot.misc.utils as utils
from CynanBot.funtoon.exceptions import NoFuntoonTokenException
from CynanBot.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from CynanBot.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBot.funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class FuntoonRepository(FuntoonRepositoryInterface):

    def __init__(
        self,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        funtoonApiUrl: str = 'https://funtoon.party/api'
    ):
        assert isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface), f"malformed {funtoonTokensRepository=}"
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        if not utils.isValidUrl(funtoonApiUrl):
            raise ValueError(f'funtoonApiUrl argument is malformed: \"{funtoonApiUrl}\"')

        self.__funtoonTokensRepository: FuntoonTokensRepositoryInterface = funtoonTokensRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__funtoonApiUrl: str = funtoonApiUrl

    async def banTriviaQuestion(self, triviaId: str) -> bool:
        if not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'{self.__funtoonApiUrl}/trivia/review/{triviaId}')
        except GenericNetworkException as e:
            self.__timber.log('FuntoonRepository', f'Encountered network error when banning a trivia question (triviaId={triviaId}): {e}', e, traceback.format_exc())
            return False

        responseStatus: Optional[int] = None

        if response is not None:
            responseStatus = response.getStatusCode()
            await response.close()

        return utils.isValidInt(responseStatus) and responseStatus == 200

    async def __hitFuntoon(
        self,
        event: str,
        funtoonToken: str,
        twitchChannel: str,
        data: Optional[Any] = None
    ) -> bool:
        if not utils.isValidStr(event):
            raise ValueError(f'event argument is malformed: \"{event}\"')
        if not utils.isValidStr(funtoonToken):
            raise ValueError(f'funtoonToken argument is malformed: \"{funtoonToken}\"')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        url = f'{self.__funtoonApiUrl}/events/custom'

        jsonPayload = {
            'channel': twitchChannel,
            'data': data,
            'event': event
        }

        self.__timber.log('FuntoonRepository', f'Hitting Funtoon API \"{url}\" for \"{twitchChannel}\" for event \"{event}\", JSON payload: {jsonPayload}')
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
            self.__timber.log('FuntoonRepository', f'Encountered network error for \"{twitchChannel}\" for event \"{event}\": {e}', e, traceback.format_exc())
            return False

        responseStatus: Optional[int] = None
        if response is not None:
            responseStatus = response.getStatusCode()
            await response.close()

        if responseStatus == 200:
            self.__timber.log('FuntoonRepository', f'Successfully hit Funtoon API \"{url}\" for \"{twitchChannel}\" for event \"{event}\"')
            return True
        else:
            self.__timber.log('FuntoonRepository', f'Error when hitting Funtoon API \"{url}\" for \"{twitchChannel}\" for event \"{event}\" with token \"{funtoonToken}\", JSON payload: {jsonPayload}, response: \"{response}\"')
            return False

    async def pkmnBattle(
        self,
        twitchChannel: str,
        userThatRedeemed: str,
        userToBattle: str
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userThatRedeemed):
            raise ValueError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')
        if not utils.isValidStr(userToBattle):
            raise ValueError(f'userToBattle argument is malformed: \"{userToBattle}\"')

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(twitchChannel)
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnBattle as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
            return False

        return await self.__hitFuntoon(
            event = 'battle',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            data = {
                'player': userThatRedeemed,
                'opponent': userToBattle
            }
        )

    async def pkmnCatch(
        self,
        twitchChannel: str,
        userThatRedeemed: str,
        funtoonPkmnCatchType: Optional[FuntoonPkmnCatchType] = None
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userThatRedeemed):
            raise ValueError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')
        assert funtoonPkmnCatchType is None or isinstance(funtoonPkmnCatchType, FuntoonPkmnCatchType), f"malformed {funtoonPkmnCatchType=}"

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(twitchChannel)
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnCatch as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
            return False

        data = None
        if funtoonPkmnCatchType is None:
            data = userThatRedeemed
        else:
            data = {
                'who': userThatRedeemed,
                'catchType': funtoonPkmnCatchType.toStr()
            }

        return await self.__hitFuntoon(
            event = 'catch',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            data = data
        )

    async def pkmnGiveEvolve(
        self,
        twitchChannel: str,
        userThatRedeemed: str
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userThatRedeemed):
            raise ValueError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(twitchChannel)
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnGiveEvolve as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
            return False

        return await self.__hitFuntoon(
            event = 'giveFreeEvolve',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            data = userThatRedeemed
        )

    async def pkmnGiveShiny(
        self,
        twitchChannel: str,
        userThatRedeemed: str
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userThatRedeemed):
            raise ValueError(f'userThatRedeemed argument is malformed: \"{userThatRedeemed}\"')

        try:
            funtoonToken = await self.__funtoonTokensRepository.requireToken(twitchChannel)
        except NoFuntoonTokenException as e:
            self.__timber.log('FuntoonRepository', f'Can\'t perform pkmnGiveShiny as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
            return False

        return await self.__hitFuntoon(
            event = 'giveFreeShiny',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            data = userThatRedeemed
        )
