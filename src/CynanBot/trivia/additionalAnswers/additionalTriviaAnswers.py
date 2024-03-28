import CynanBot.misc.utils as utils
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswer import \
    AdditionalTriviaAnswer
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource


class AdditionalTriviaAnswers():

    def __init__(
        self,
        additionalAnswers: list[AdditionalTriviaAnswer],
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ):
        if not isinstance(additionalAnswers, list):
            raise TypeError(f'additionalAnswers argument is malformed: \"{additionalAnswers}\"')
        elif len(additionalAnswers) == 0:
            raise ValueError(f'additionAnswers argument is empty: \"{additionalAnswers}\"')
        elif not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaQuestionType):
            raise TypeError(f'triviaType argument is malformed: \"{triviaType}\"')

        self.__additionalAnswers: list[AdditionalTriviaAnswer] = additionalAnswers
        self.__triviaId: str = triviaId
        self.__triviaSource: TriviaSource = triviaSource
        self.__triviaType: TriviaQuestionType = triviaType

    def getAdditionalAnswers(self) -> list[AdditionalTriviaAnswer]:
        return self.__additionalAnswers

    def getAdditionalAnswersStrs(self) -> list[str]:
        additionalAnswersStrs: list[str] = list()

        for additionalAnswer in self.__additionalAnswers:
            additionalAnswersStrs.append(additionalAnswer.getAdditionalAnswer())

        return additionalAnswersStrs

    def getTriviaId(self) -> str:
        return self.__triviaId

    def getTriviaSource(self) -> TriviaSource:
        return self.__triviaSource

    def getTriviaType(self) -> TriviaQuestionType:
        return self.__triviaType
