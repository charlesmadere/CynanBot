from frozenlist import FrozenList

from .halfLifeHelperInterface import HalfLifeHelperInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ..parser.halfLifeMessageVoiceParserInterface import HalfLifeMessageVoiceParserInterface
from ..service.halfLifeServiceInterface import HalfLifeServiceInterface
from ..settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils


class HalfLifeHelper(HalfLifeHelperInterface):

    def __init__(
        self,
        halfLifeService: HalfLifeServiceInterface,
        halfLifeMessageVoiceParser: HalfLifeMessageVoiceParserInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface
    ):
        if not isinstance(halfLifeService, HalfLifeServiceInterface):
            raise TypeError(f'halfLifeApiService argument is malformed: \"{halfLifeService}\"')
        elif not isinstance(halfLifeMessageVoiceParser, HalfLifeMessageVoiceParserInterface):
            raise TypeError(f'halfLifeMessageVoiceParser argument is malformed: \"{halfLifeMessageVoiceParser}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')

        self.__halfLifeService: HalfLifeServiceInterface = halfLifeService
        self.__halfLifeMessageVoiceParser: HalfLifeMessageVoiceParserInterface = halfLifeMessageVoiceParser
        self.__halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface = halfLifeSettingsRepository

    async def generateTts(
        self,
        voice: HalfLifeVoice,
        message: str | None
    ) -> FrozenList[str] | None:
        if not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        result = await self.__halfLifeMessageVoiceParser.determineVoiceFromMessage(message)

        if result is not None:
            message = result.message
            voice = result.voice

        directory = await self.__halfLifeSettingsRepository.getSoundsDirectory()

        return await self.__halfLifeService.getWavs(
            directory = directory,
            text = message,
            voice = voice
        )
