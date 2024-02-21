from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions


class TriviaFetchOptions():

    def __init__(
        self,
        twitchChannel: str,
        questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        assert isinstance(questionAnswerTriviaConditions, QuestionAnswerTriviaConditions), f"malformed {questionAnswerTriviaConditions=}"

        self.__twitchChannel: str = twitchChannel
        self.__questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = questionAnswerTriviaConditions

    def areQuestionAnswerTriviaQuestionsEnabled(self) -> bool:
        return self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.ALLOWED \
            or self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireQuestionAnswerTriviaQuestion(self) -> bool:
        return self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'questionAnswerTriviaConditions': self.__questionAnswerTriviaConditions,
            'twitchChannel': self.__twitchChannel
        }
