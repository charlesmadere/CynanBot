import traceback
from typing import Final

from .microsoftSamApiHelperInterface import MicrosoftSamApiHelperInterface
from ..apiService.microsoftSamApiServiceInterface import MicrosoftSamApiServiceInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class MicrosoftSamApiHelper(MicrosoftSamApiHelperInterface):

    def __init__(
        self,
        microsoftSamApiService: MicrosoftSamApiServiceInterface,
        timber: TimberInterface,
    ):
        if not isinstance(microsoftSamApiService, MicrosoftSamApiServiceInterface):
            raise TypeError(f'microsoftSamApiService argument is malformed: \"{microsoftSamApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__microsoftSamApiService: Final[MicrosoftSamApiServiceInterface] = microsoftSamApiService
        self.__timber: Final[TimberInterface] = timber

    async def getSpeech(
        self,
        voice: MicrosoftSamVoice,
        message: str | None,
    ) -> bytes | None:
        if not isinstance(voice, MicrosoftSamVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        try:
            return await self.__microsoftSamApiService.getSpeech(
                voice = voice,
                text = message,
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftSamApiHelper', f'Encountered network error when fetching speech ({voice=}) ({message=})', e, traceback.format_exc())
            return None
