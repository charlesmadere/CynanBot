from typing import Any

from frozendict import frozendict

from .ttsChatterBoosterPack import TtsChatterBoosterPack
from .ttsChatterBoosterPackParserInterface import TtsChatterBoosterPackParserInterface
from ..accessLevel.accessLevel import AccessLevel
from ..accessLevel.accessLevelParserInterface import AccessLevelJsonParserInterface
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...halfLife.parser.halfLifeJsonParserInterface import HalfLifeJsonParserInterface
from ...microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ...microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ...misc import utils as utils
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ...tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ...tts.ttsProvider import TtsProvider


class TtsChatterBoosterPackParser(TtsChatterBoosterPackParserInterface):

    def __init__(
        self,
        halfLifeJsonParser: HalfLifeJsonParserInterface,
        microsoftSamJsonParser: MicrosoftSamJsonParserInterface,
        streamElementsJsonParser: StreamElementsJsonParserInterface,
        accessLevelJsonParser: AccessLevelJsonParserInterface,
        ttsJsonMapper: TtsJsonMapperInterface
    ):
        if not isinstance(halfLifeJsonParser, HalfLifeJsonParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeJsonParser}\"')
        elif not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')
        elif not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')

        self.__halfLifeJsonParser: HalfLifeJsonParserInterface = halfLifeJsonParser
        self.__microsoftSamJsonParser: MicrosoftSamJsonParserInterface = microsoftSamJsonParser
        self.__streamElementsJsonParser: StreamElementsJsonParserInterface = streamElementsJsonParser
        self.__ttsChatterAccessLevelParser: AccessLevelJsonParserInterface = accessLevelJsonParser
        self.__ttsJsonMapper: TtsJsonMapperInterface = ttsJsonMapper

    def parseBoosterPack(
        self,
        defaultTtsProvider: TtsProvider,
        jsonContents: dict[str, Any]
    ) -> TtsChatterBoosterPack:

        userName = utils.getStrFromDict(jsonContents, 'userName')
        voiceStr = utils.getStrFromDict(jsonContents, 'voice', '')

        accessLevelStr = utils.getStrFromDict(jsonContents, 'access', '')
        accessLevel = self.__ttsChatterAccessLevelParser.parseAccessLevel(AccessLevel.SUBSCRIBER, accessLevelStr)

        ttsProviderStr = utils.getStrFromDict(jsonContents, 'ttsProvider')
        ttsProvider = self.__ttsJsonMapper.parseProvider(ttsProviderStr)
        if ttsProvider is None:
            ttsProvider = defaultTtsProvider

        voice: MicrosoftSamVoice | StreamElementsVoice | HalfLifeVoice | str | None

        match ttsProvider:
            case TtsProvider.DEC_TALK:
                voice = ''
            case TtsProvider.GOOGLE:
                voice = ''
            case TtsProvider.HALF_LIFE:
                voice = self.__halfLifeJsonParser.parseVoice(voiceStr)
            case TtsProvider.MICROSOFT_SAM:
                voice = self.__microsoftSamJsonParser.parseVoice(voiceStr)
            case TtsProvider.SINGING_DEC_TALK:
                voice = ''
            case TtsProvider.STREAM_ELEMENTS:
                voice = self.__streamElementsJsonParser.parseVoice(voiceStr)
            case TtsProvider.TTS_MONSTER:
                voice = voiceStr

        return TtsChatterBoosterPack(
            accessLevel = accessLevel,
            ttsProvider = ttsProvider,
            userName = userName,
            voice = voice
        )

    def parseBoosterPacks(
        self,
        defaultTtsProvider,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TtsChatterBoosterPack] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None
        boosterPacks: dict[str, TtsChatterBoosterPack] = dict()

        for boosterPackJson in jsonContents:
            boosterPack = self.parseBoosterPack(defaultTtsProvider, boosterPackJson)
            boosterPacks[boosterPack.userName.lower()] = boosterPack

        return frozendict(boosterPacks)
