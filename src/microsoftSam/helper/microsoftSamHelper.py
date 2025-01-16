import traceback

from .microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ..apiService.microsoftSamApiServiceInterface import MicrosoftSamApiServiceInterface
from ..microsoftSamVoiceMapperInterface import MicrosoftSamVoiceMapperInterface
from ..parser.microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface
from ..settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class MicrosoftSamHelper(MicrosoftSamHelperInterface):

    def __init__(
        self,
        apiService: MicrosoftSamApiServiceInterface,
        microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        microsoftSamVoiceMapper: MicrosoftSamVoiceMapperInterface,
        timber: TimberInterface
    ):
        if not isinstance(apiService, MicrosoftSamApiServiceInterface):
            raise TypeError(f'apiService argument is malformed: \"{apiService}\"')
        elif not isinstance(microsoftSamMessageVoiceParser, MicrosoftSamMessageVoiceParserInterface):
            raise TypeError(f'microsoftSamMessageVoiceParser argument is malformed: \"{microsoftSamMessageVoiceParser}\"')
        elif not isinstance(microsoftSamSettingsRepository, MicrosoftSamSettingsRepositoryInterface):
            raise TypeError(f'microsoftSamSettingsRepository argument is malformed: \"{microsoftSamSettingsRepository}\"')
        elif not isinstance(microsoftSamVoiceMapper, MicrosoftSamVoiceMapperInterface):
            raise TypeError(f'microsoftSamVoiceMapper argument is malformed: \"{microsoftSamVoiceMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__apiService: MicrosoftSamApiServiceInterface = apiService
        self.__microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface = microsoftSamMessageVoiceParser
        self.__microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = microsoftSamSettingsRepository
        self.__microsoftSamVoiceMapper: MicrosoftSamVoiceMapperInterface = microsoftSamVoiceMapper
        self.__timber: TimberInterface = timber

    async def getSpeech(
        self,
        message: str | None
    ) -> bytes | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        result = await self.__microsoftSamMessageVoiceParser.determineVoiceFromMessage(message)
        voice = await self.__microsoftSamSettingsRepository.getDefaultVoice()

        if result is not None:
            message = result.message
            voice = result.voice

        data = self.__microsoftSamVoiceMapper.data(voice)

        try:
            return await self.__apiService.getSpeech(
                text = message,
                voice = data.voice,
                pitch = data.pitch,
                speed = data.speed
            )
        except GenericNetworkException as e:
            self.__timber.log('MicrosoftSamHelper', f'Encountered network error when fetching speech ({message=}): {e}', e, traceback.format_exc())
            return None
