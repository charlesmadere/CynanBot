from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaQuestionPresenterInterface import \
    TriviaQuestionPresenterInterface


class TriviaQuestionPresenter(TriviaQuestionPresenterInterface):

    async def __presentMultipleChoice(self, triviaQuestion: MultipleChoiceTriviaQuestion) -> str:
        # TODO
        raise RuntimeError()

    async def __presentQuestionAnswer(self, triviaQuestion: QuestionAnswerTriviaQuestion) -> str:
        # TODO
        raise RuntimeError()

    async def __presentTrueFalse(self, triviaQuestion: TrueFalseTriviaQuestion) -> str:
        # TODO
        raise RuntimeError()

    async def toString(self, triviaQuestion: AbsTriviaQuestion) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')

        if isinstance(triviaQuestion, MultipleChoiceTriviaQuestion):
            return await self.__presentMultipleChoice(triviaQuestion)
        elif isinstance(triviaQuestion, QuestionAnswerTriviaQuestion):
            return await self.__presentQuestionAnswer(triviaQuestion)
        elif isinstance(triviaQuestion, TrueFalseTriviaQuestion):
            return await self.__presentTrueFalse(triviaQuestion)
        else:
            raise RuntimeError(f'Unknown trivia question type: {triviaQuestion}')
