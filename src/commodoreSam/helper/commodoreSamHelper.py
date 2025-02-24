import traceback

from .commodoreSamHelperInterface import CommodoreSamHelperInterface
from ..apiService.commodoreSamApiService import CommodoreSamApiServiceInterface
from ..exceptions import CommodoreSamFailedToGenerateSpeechFileException
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class CommodoreSamHelper(CommodoreSamHelperInterface):

    def __init__(
        self,
        commodoreSamApiService: CommodoreSamApiServiceInterface,
        timber: TimberInterface
    ):
        if not isinstance(commodoreSamApiService, CommodoreSamApiServiceInterface):
            raise TypeError(f'commodoreSamApiService argument is malformed: \"{commodoreSamApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__commodoreSamApiService: CommodoreSamApiServiceInterface = commodoreSamApiService
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
            return await self.__commodoreSamApiService.generateSpeechFile(
                text = message
            )
        except CommodoreSamFailedToGenerateSpeechFileException as e:
            self.__timber.log('CommodoreSamHelper', f'Encountered error when generating speech ({message=}): {e}', e, traceback.format_exc())
            return None
