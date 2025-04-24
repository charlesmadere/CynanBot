from frozenlist import FrozenList

from .halfLifeTtsHelperInterface import HalfLifeTtsHelperInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ..parser.halfLifeMessageVoiceParserInterface import HalfLifeMessageVoiceParserInterface
from ..service.halfLifeTtsServiceInterface import HalfLifeTtsServiceInterface
from ..settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils


class HalfLifeTtsHelper(HalfLifeTtsHelperInterface):

    def __init__(
        self,
        halfLifeTtsService: HalfLifeTtsServiceInterface,
        halfLifeMessageVoiceParser: HalfLifeMessageVoiceParserInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface
    ):
        if not isinstance(halfLifeTtsService, HalfLifeTtsServiceInterface):
            raise TypeError(f'halfLifeTtsService argument is malformed: \"{halfLifeTtsService}\"')
        elif not isinstance(halfLifeMessageVoiceParser, HalfLifeMessageVoiceParserInterface):
            raise TypeError(f'halfLifeMessageVoiceParser argument is malformed: \"{halfLifeMessageVoiceParser}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')

        self.__halfLifeTtsService: HalfLifeTtsServiceInterface = halfLifeTtsService
        self.__halfLifeMessageVoiceParser: HalfLifeMessageVoiceParserInterface = halfLifeMessageVoiceParser
        self.__halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface = halfLifeSettingsRepository

    async def generateTts(
        self,
        voice: HalfLifeVoice | None,
        message: str | None
    ) -> FrozenList[str] | None:
        if voice is not None and not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        if voice is None:
            voice = await self.__halfLifeSettingsRepository.getDefaultVoice()

        messageVoiceResult = await self.__halfLifeMessageVoiceParser.determineVoiceFromMessage(message)

        if messageVoiceResult is not None:
            voice = messageVoiceResult.voice
            message = messageVoiceResult.message

        soundsDirectory = await self.__halfLifeSettingsRepository.requireSoundsDirectory()

        return await self.__halfLifeTtsService.getWavs(
            voice = voice,
            directory = soundsDirectory,
            text = message
        )
