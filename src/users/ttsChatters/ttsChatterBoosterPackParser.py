from typing import Any
from frozendict import frozendict

from ...misc import utils as utils
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ...tts.ttsJsonMapperInterface import TtsJsonMapperInterface
from ...tts.ttsProvider import TtsProvider

from .ttsChatterBoosterPack import TtsChatterBoosterPack
from .ttsChatterBoosterPackParserInterface import TtsChatterBoosterPackParserInterface


class TtsChatterBoosterPackParser(TtsChatterBoosterPackParserInterface):

    def __init__(
            self, 
            ttsJsonMapper: TtsJsonMapperInterface,
            streamElementsJsonParser: StreamElementsJsonParserInterface
        ):
        if not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        if not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')

        self.__ttsJsonMapper: TtsJsonMapperInterface = ttsJsonMapper
        self.__streamElementsJsonParser: StreamElementsJsonParserInterface = streamElementsJsonParser

    def parseBoosterPack(
        self,
        defaultTtsProvider: TtsProvider,
        jsonContents: dict[str, Any]
    ) -> TtsChatterBoosterPack :

        userName = utils.getStrFromDict(jsonContents, 'userName')
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        voiceStr = utils.getStrFromDict(jsonContents, 'voice')

        if not utils.isValidStr(voiceStr):
            raise TypeError(f'voice argument is malformed: \"{voiceStr}\"')

        ttsProviderStr = utils.getStrFromDict(jsonContents, 'ttsProvider')
        ttsProvider = self.__ttsJsonMapper.parseProvider(ttsProviderStr)
        if ttsProvider is None:
            ttsProvider = defaultTtsProvider
            
        voice: StreamElementsVoice | str | None
        
        match ttsProvider:
            case TtsProvider.STREAM_ELEMENTS:
                voice = self.__streamElementsJsonParser.parseVoice(voiceStr)
            case TtsProvider.TTS_MONSTER:
                voice = voiceStr
            case TtsProvider.DEC_TALK:
                voice = voiceStr
            case TtsProvider.GOOGLE:
                voice = ''

        return TtsChatterBoosterPack(
            userName = userName,
            voice = voice,
            ttsProvider = ttsProvider
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
