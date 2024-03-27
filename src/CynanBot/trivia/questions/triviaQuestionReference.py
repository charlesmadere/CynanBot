from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource


class TriviaQuestionReference():

    def __init__(
        self,
        emote: str,
        triviaId: str,
        twitchChannel: str,
        originalTriviaSource: TriviaSource | None,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ):
        if not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif originalTriviaSource is not None and not isinstance(originalTriviaSource, TriviaSource):
            raise TypeError(f'originalTriviaSource argument is malformed: \"{originalTriviaSource}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaQuestionType):
            raise TypeError(f'triviaType argument is malformed: \"{triviaType}\"')

        self.__emote: str = emote
        self.__triviaId: str = triviaId
        self.__twitchChannel: str = twitchChannel
        self.__originalTriviaSource: TriviaSource | None = originalTriviaSource
        self.__triviaSource: TriviaSource = triviaSource
        self.__triviaType: TriviaQuestionType = triviaType

    def getEmote(self) -> str:
        return self.__emote

    def getOriginalTriviaSource(self) -> TriviaSource | None:
        return self.__originalTriviaSource

    def getTriviaId(self) -> str:
        return self.__triviaId

    def getTriviaSource(self) -> TriviaSource:
        return self.__triviaSource

    def getTriviaType(self) -> TriviaQuestionType:
        return self.__triviaType

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'emote': self.__emote,
            'originalTriviaSource': self.__originalTriviaSource,
            'triviaId': self.__triviaId,
            'triviaSource': self.__triviaSource,
            'triviaType': self.__triviaType,
            'twitchChannel': self.__twitchChannel
        }
