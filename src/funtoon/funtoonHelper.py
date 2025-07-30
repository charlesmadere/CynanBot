import traceback
from typing import Any

from .apiService.funtoonApiServiceInterface import FuntoonApiServiceInterface
from .exceptions import NoFuntoonTokenException
from .funtoonHelperInterface import FuntoonHelperInterface
from .funtoonPkmnCatchType import FuntoonPkmnCatchType
from .jsonMapper.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from .tokens.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..timber.timberInterface import TimberInterface


class FuntoonHelper(FuntoonHelperInterface):

    def __init__(
        self,
        funtoonApiService: FuntoonApiServiceInterface,
        funtoonJsonMapper: FuntoonJsonMapperInterface,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(funtoonApiService, FuntoonApiServiceInterface):
            raise TypeError(f'funtoonApiService argument is malformed: \"{funtoonApiService}\"')
        elif not isinstance(funtoonJsonMapper, FuntoonJsonMapperInterface):
            raise TypeError(f'funtoonJsonMapper argument is malformed: \"{funtoonJsonMapper}\"')
        elif not isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface):
            raise TypeError(f'funtoonTokensRepository argument is malformed: \"{funtoonTokensRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__funtoonApiService: FuntoonApiServiceInterface = funtoonApiService
        self.__funtoonJsonMapper: FuntoonJsonMapperInterface = funtoonJsonMapper
        self.__funtoonTokensRepository: FuntoonTokensRepositoryInterface = funtoonTokensRepository
        self.__timber: TimberInterface = timber

    async def banTriviaQuestion(self, triviaId: str) -> bool:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')

        successfullyBanned = False

        try:
            successfullyBanned = await self.__funtoonApiService.banTriviaQuestion(triviaId = triviaId)
        except GenericNetworkException as e:
            self.__timber.log('FuntoonHelper', f'Encountered network error when banning trivia question ({triviaId=}): {e}', e, traceback.format_exc())

        return successfullyBanned

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
            self.__timber.log('FuntoonHelper', f'Can\'t perform pkmnBattle as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
            return False

        return await self.__funtoonApiService.customEvent(
            data = {
                'player': userThatRedeemed,
                'opponent': userToBattle
            },
            event = 'battle',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
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
            self.__timber.log('FuntoonHelper', f'Can\'t perform pkmnCatch as twitchChannel \"{twitchChannel}\" has no Funtoon token', e, traceback.format_exc())
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

        return await self.__funtoonApiService.customEvent(
            data = data,
            event = 'catch',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
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
            self.__timber.log('FuntoonHelper', f'Can\'t perform pkmnGiveEvolve as twitchChannel \"{twitchChannel}\" has no Funtoon token: {e}', e, traceback.format_exc())
            return False

        return await self.__funtoonApiService.customEvent(
            data = userThatRedeemed,
            event = 'giveFreeEvolve',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
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
            self.__timber.log('FuntoonHelper', f'Can\'t perform pkmnGiveShiny as twitchChannel \"{twitchChannel}\" has no Funtoon token: {e}', e, traceback.format_exc())
            return False

        return await self.__funtoonApiService.customEvent(
            data = userThatRedeemed,
            event = 'giveFreeShiny',
            funtoonToken = funtoonToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )
