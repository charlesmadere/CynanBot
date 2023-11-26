import CynanBot.misc.utils as utils
from CynanBot.trivia.triviaSource import TriviaSource
from CynanBot.trivia.triviaType import TriviaType


class TriviaQuestionReference():

    def __init__(
        self,
        emote: str,
        triviaId: str,
        twitchChannel: str,
        triviaSource: TriviaSource,
        triviaType: TriviaType
    ):
        if not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise ValueError(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaType):
            raise ValueError(f'triviaType argument is malformed: \"{triviaType}\"')

        self.__emote: str = emote
        self.__triviaId: str = triviaId
        self.__twitchChannel: str = twitchChannel
        self.__triviaSource: TriviaSource = triviaSource
        self.__triviaType: TriviaType = triviaType

    def getEmote(self) -> str:
        return self.__emote

    def getTriviaId(self) -> str:
        return self.__triviaId

    def getTriviaSource(self) -> TriviaSource:
        return self.__triviaSource

    def getTriviaType(self) -> TriviaType:
        return self.__triviaType

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
