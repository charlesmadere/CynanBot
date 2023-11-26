import CynanBot.misc.utils as utils
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions


class TriviaFetchOptions():

    def __init__(
        self,
        twitchChannel: str,
        isJokeTriviaRepositoryEnabled: bool = False,
        questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
    ):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidBool(isJokeTriviaRepositoryEnabled):
            raise ValueError(f'isJokeTriviaRepositoryEnabled argument is malformed: \"{isJokeTriviaRepositoryEnabled}\"')
        elif not isinstance(questionAnswerTriviaConditions, QuestionAnswerTriviaConditions):
            raise ValueError(f'questionAnswerTriviaConditions argument is malformed: \"{questionAnswerTriviaConditions}\"')

        self.__twitchChannel: str = twitchChannel
        self.__isJokeTriviaRepositoryEnabled: bool = isJokeTriviaRepositoryEnabled
        self.__questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = questionAnswerTriviaConditions

    def areQuestionAnswerTriviaQuestionsEnabled(self) -> bool:
        return self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.ALLOWED \
            or self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def isJokeTriviaRepositoryEnabled(self) -> bool:
        return self.__isJokeTriviaRepositoryEnabled

    def requireQuestionAnswerTriviaQuestion(self) -> bool:
        return self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def __str__(self) -> str:
        return f'twitchChannel=\"{self.__twitchChannel}\", isJokeTriviaRepositoryEnabled=\"{self.__isJokeTriviaRepositoryEnabled}\", questionAnswerTriviaConditions=\"{self.__questionAnswerTriviaConditions}\"'
