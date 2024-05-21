import CynanBot.misc.utils as utils
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

    async def getCorrectAnswerBool(
        self,
        triviaQuestion: TrueFalseTriviaQuestion
    ) -> bool:
        if not isinstance(triviaQuestion, TrueFalseTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')

        return triviaQuestion.correctAnswer

    async def getCorrectAnswers(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if isinstance(triviaQuestion, MultipleChoiceTriviaQuestion):
            return await self.__getCorrectAnswersMultipleChoice(triviaQuestion, delimiter)
        elif isinstance(triviaQuestion, QuestionAnswerTriviaQuestion):
            return await self.__getCorrectAnswersQuestionAnswer(triviaQuestion, delimiter)
        elif isinstance(triviaQuestion, TrueFalseTriviaQuestion):
            return await self.__getCorrectAnswersTrueFalse(triviaQuestion)
        else:
            raise RuntimeError(f'Unknown AbsTriviaQuestion type: {triviaQuestion}')

    async def __getCorrectAnswersMultipleChoice(
        self,
        triviaQuestion: MultipleChoiceTriviaQuestion,
        delimiter: str
    ) -> str:
        correctAnswers: list[str] = list()

        for index, correctAnswer in triviaQuestion.indexesWithCorrectAnswers.items():
            correctAnswerOrdinal = chr(ord('A') + index)
            correctAnswers.append(f'[{correctAnswerOrdinal}] {correctAnswer}')

        if len(correctAnswers) == 1:
            return f'The correct answer is: {correctAnswers[0]}'

        correctAnswersString = delimiter.join(correctAnswers)
        return f'The correct answers are: {correctAnswersString}'

    async def __getCorrectAnswersQuestionAnswer(
        self,
        triviaQuestion: QuestionAnswerTriviaQuestion,
        delimiter: str
    ) -> str:
        correctAnswers = triviaQuestion.correctAnswers

        if len(correctAnswers) == 1:
            return f'The correct answer is: {correctAnswers[0]}'

        correctAnswersString = delimiter.join(correctAnswers)
        return f'The correct answers are: {correctAnswersString}'

    async def __getCorrectAnswersTrueFalse(
        self,
        triviaQuestion: TrueFalseTriviaQuestion
    ) -> str:
        correctAnswer = str(triviaQuestion.correctAnswer).lower()
        return f'The correct answer is: {correctAnswer}'

    async def getPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delimiter: str = ' '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if isinstance(triviaQuestion, MultipleChoiceTriviaQuestion):
            return await self.__getPromptMultipleChoice(triviaQuestion, delimiter)
        elif isinstance(triviaQuestion, QuestionAnswerTriviaQuestion):
            return await self.__getPromptQuestionAnswer(triviaQuestion)
        elif isinstance(triviaQuestion, TrueFalseTriviaQuestion):
            return await self.__getPromptTrueFalse(triviaQuestion)
        else:
            raise RuntimeError(f'Unknown AbsTriviaQuestion type: {triviaQuestion}')

    async def __getPromptMultipleChoice(
        self,
        triviaQuestion: MultipleChoiceTriviaQuestion,
        delimiter: str
    ) -> str:
        responses: list[str] = list()
        ordinalCharacter = 'A'

        for response in triviaQuestion.responses:
            responses.append(f'[{ordinalCharacter}] {response}')
            ordinalCharacter = chr(ord(ordinalCharacter) + 1)

        responsesString = delimiter.join(responses)
        return f'— {triviaQuestion.question} {responsesString}'.strip()

    async def __getPromptQuestionAnswer(
        self,
        triviaQuestion: QuestionAnswerTriviaQuestion
    ) -> str:
        categoryPrompt = ''

        if utils.isValidStr(triviaQuestion.category):
            categoryPrompt = f' category is {triviaQuestion.category} —'

        return f'—{categoryPrompt} {triviaQuestion.question}'.strip()

    async def __getPromptTrueFalse(
        self,
        triviaQuestion: TrueFalseTriviaQuestion
    ) -> str:
        return f'— True or false! {triviaQuestion.question}'.strip()

    async def getResponses(
        self,
        triviaQuestion: AbsTriviaQuestion
    ) -> list[str]:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')

        if isinstance(triviaQuestion, MultipleChoiceTriviaQuestion):
            return await self.__getResponsesMultipleChoice(triviaQuestion)
        elif isinstance(triviaQuestion, QuestionAnswerTriviaQuestion):
            return await self.__getResponsesQuestionAnswer(triviaQuestion)
        elif isinstance(triviaQuestion, TrueFalseTriviaQuestion):
            return await self.__getResponsesTrueFalse(triviaQuestion)
        else:
            raise RuntimeError(f'Unknown AbsTriviaQuestion type: {triviaQuestion}')

    async def __getResponsesMultipleChoice(
        self,
        triviaQuestion: MultipleChoiceTriviaQuestion
    ) -> list[str]:
        responses: list[str] = list()
        ordinalCharacter = 'A'

        for response in triviaQuestion.responses:
            responses.append(f'[{ordinalCharacter}] {response}')
            ordinalCharacter = chr(ord(ordinalCharacter) + 1)

        return responses

    async def __getResponsesQuestionAnswer(
        self,
        triviaQuestion: QuestionAnswerTriviaQuestion
    ) -> list[str]:
        return list()

    async def __getResponsesTrueFalse(
        self,
        triviaQuestion: TrueFalseTriviaQuestion
    ) -> list[str]:
        return [ str(True).lower(), str(False).lower() ]
