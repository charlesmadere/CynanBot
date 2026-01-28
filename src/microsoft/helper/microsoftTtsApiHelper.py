import traceback

from .microsoftTtsApiHelperInterface import MicrosoftTtsApiHelperInterface
from ..apiService.microsoftTtsApiServiceInterface import MicrosoftTtsApiServiceInterface
from ..models.microsoftTtsVoice import MicrosoftTtsVoice
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class MicrosoftTtsApiHelper(MicrosoftTtsApiHelperInterface):

    def __init__(
        self,
        microsoftTtsApiService: MicrosoftTtsApiServiceInterface,
        timber: TimberInterface
    ):
        if not isinstance(microsoftTtsApiService, MicrosoftTtsApiServiceInterface):
            raise TypeError(f'microsoftTtsApiService argument is malformed: \"{microsoftTtsApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__microsoftTtsApiService: MicrosoftTtsApiServiceInterface = microsoftTtsApiService
        self.__timber: TimberInterface = timber

    async def getSpeech(
        self,
        voice: MicrosoftTtsVoice,
        message: str | None
    ) -> bytes | None:
        if not isinstance(voice, MicrosoftTtsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        try:
            return await self.__microsoftTtsApiService.getSpeech(
                voice = voice,
                message = message
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftTtsApiHelper', f'Encountered network error when fetching speech ({voice=}) ({message=})', e, traceback.format_exc())
            return None
