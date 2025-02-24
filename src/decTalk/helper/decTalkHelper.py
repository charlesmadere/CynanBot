import traceback

from .decTalkHelperInterface import DecTalkHelperInterface
from ..apiService.decTalkApiServiceInterface import DecTalkApiServiceInterface
from ..exceptions import DecTalkFailedToGenerateSpeechFileException
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class DecTalkHelper(DecTalkHelperInterface):

    def __init__(
        self,
        apiService: DecTalkApiServiceInterface,
        timber: TimberInterface
    ):
        if not isinstance(apiService, DecTalkApiServiceInterface):
            raise TypeError(f'apiService argument is malformed: \"{apiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__apiService: DecTalkApiServiceInterface = apiService
        self.__timber: TimberInterface = timber

    async def getSpeech(
        self,
        message: str | None
    ) -> str | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        try:
            return await self.__apiService.generateSpeechFile(
                text = message
            )
        except DecTalkFailedToGenerateSpeechFileException as e:
            self.__timber.log('DecTalkHelper', f'Encountered error when generating speech ({message=}): {e}', e, traceback.format_exc())
            return None
