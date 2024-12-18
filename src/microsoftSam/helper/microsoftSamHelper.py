import traceback

from .microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ..apiService.microsoftSamApiServiceInterface import MicrosoftSamApiServiceInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class MicrosoftSamHelper(MicrosoftSamHelperInterface):

    def __init__(
        self,
        apiService: MicrosoftSamApiServiceInterface,
        timber: TimberInterface
    ):
        if not isinstance(apiService, MicrosoftSamApiServiceInterface):
            raise TypeError(f'apiService argument is malformed: \"{apiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__apiService: MicrosoftSamApiServiceInterface = apiService
        self.__timber: TimberInterface = timber

    async def getSpeech(
        self,
        message: str | None
    ) -> bytes | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        try:
            return await self.__apiService.getSpeech(
                text = message
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftSamHelper', f'Encountered network error when fetching speech ({message=}): {e}', e, traceback.format_exc())
            return None
