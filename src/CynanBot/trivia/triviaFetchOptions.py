from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions


class TriviaFetchOptions():

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(questionAnswerTriviaConditions, QuestionAnswerTriviaConditions):
            raise TypeError(f'questionAnswerTriviaConditions argument is malformed: \"{questionAnswerTriviaConditions}\"')

        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = questionAnswerTriviaConditions

    def areQuestionAnswerTriviaQuestionsEnabled(self) -> bool:
        return self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.ALLOWED \
            or self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireQuestionAnswerTriviaQuestion(self) -> bool:
        return self.__questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def toDictionary(self) -> dict[str, Any]:
        return {
            'questionAnswerTriviaConditions': self.__questionAnswerTriviaConditions,
            'twitchChannel': self.__twitchChannel,
            'twitchChannelId': self.__twitchChannelId
        }
