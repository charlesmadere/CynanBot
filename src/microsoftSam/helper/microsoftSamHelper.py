import traceback
from asyncio import AbstractEventLoop

from .microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ..apiService.microsoftSamApiServiceInterface import MicrosoftSamApiServiceInterface
from ..models.microsoftSamFileReference import MicrosoftSamFileReference
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ..parser.microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface
from ..settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class MicrosoftSamHelper(MicrosoftSamHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        apiService: MicrosoftSamApiServiceInterface,
        microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        if not isinstance(apiService, MicrosoftSamApiServiceInterface):
            raise TypeError(f'apiService argument is malformed: \"{apiService}\"')
        elif not isinstance(microsoftSamMessageVoiceParser, MicrosoftSamMessageVoiceParserInterface):
            raise TypeError(f'microsoftSamMessageVoiceParser argument is malformed: \"{microsoftSamMessageVoiceParser}\"')
        elif not isinstance(microsoftSamSettingsRepository, MicrosoftSamSettingsRepositoryInterface):
            raise TypeError(f'microsoftSamSettingsRepository argument is malformed: \"{microsoftSamSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__apiService: MicrosoftSamApiServiceInterface = apiService
        self.__microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface = microsoftSamMessageVoiceParser
        self.__microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = microsoftSamSettingsRepository
        self.__timber: TimberInterface = timber

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> MicrosoftSamFileReference | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        # TODO
        return None

    async def getSpeech(
        self,
        message: str | None
    ) -> bytes | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        result = await self.__microsoftSamMessageVoiceParser.determineVoiceFromMessage(message)
        voice: MicrosoftSamVoice

        if result is None:
            voice = await self.__microsoftSamSettingsRepository.getDefaultVoice()
        else:
            message = result.message
            voice = result.voice

        try:
            return await self.__apiService.getSpeech(
                voice = voice,
                text = message
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftSamHelper', f'Encountered network error when fetching speech ({message=}): {e}', e, traceback.format_exc())
            return None
