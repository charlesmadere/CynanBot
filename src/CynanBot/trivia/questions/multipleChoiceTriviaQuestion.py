import CynanBot.misc.utils as utils
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (
    NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException)


class MultipleChoiceTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: list[str],
        multipleChoiceResponses: list[str],
        category: str | None,
        categoryId: str | None,
        question: str,
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        originalTriviaSource: TriviaSource | None,
        triviaSource: TriviaSource
    ):
        super().__init__(
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            originalTriviaSource = originalTriviaSource,
            triviaSource = triviaSource,
            triviaType = TriviaQuestionType.MULTIPLE_CHOICE,
        )

        if not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not utils.hasItems(multipleChoiceResponses) or len(multipleChoiceResponses) == 0:
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        self.__correctAnswers: list[str] = correctAnswers
        self.__multipleChoiceResponses: list[str] = multipleChoiceResponses

    def getAnswerOrdinals(self) -> list[int]:
        answerOrdinals: list[int] = list()

        for index in range(0, len(self.__multipleChoiceResponses)):
            answerOrdinals.append(index)

        return answerOrdinals

    def getCorrectAnswers(self) -> list[str]:
        return self.getDecoratedCorrectAnswers()

    def getCorrectAnswerChars(self) -> list[str]:
        correctAnswerOrdinals = self.getCorrectAnswerOrdinals()
        correctAnswerChars: list[str] = list()

        for ordinal in correctAnswerOrdinals:
            correctAnswerChars.append(chr(ord('A') + ordinal))

        if not utils.hasItems(correctAnswerChars):
            raise RuntimeError(f'Couldn\'t find any correct answer chars within \"{self.__correctAnswers}\"')
        elif len(correctAnswerChars) != len(self.__correctAnswers):
            raise RuntimeError(f'The length of correctAnswerChars \"{correctAnswerChars}\" ({len(correctAnswerChars)}) is not equal to \"{self.__correctAnswers}\" ({len(self.__correctAnswers)})')

        correctAnswerChars.sort()
        return correctAnswerChars

    def getCorrectAnswerOrdinals(self) -> list[int]:
        ordinals: list[int] = list()

        for index, multipleChoiceResponse in enumerate(self.__multipleChoiceResponses):
            for correctAnswer in self.__correctAnswers:
                if multipleChoiceResponse == correctAnswer:
                    ordinals.append(index)
                    break

        if not utils.hasItems(ordinals):
            raise RuntimeError(f'Couldn\'t find any correct answer ordinals within \"{self.__correctAnswers}\"!')
        elif len(ordinals) != len(self.__correctAnswers):
            raise RuntimeError(f'The length of ordinals \"{ordinals}\" ({len(ordinals)}) is not equal to \"{self.__correctAnswers}\" ({len(self.__correctAnswers)})')

        ordinals.sort()
        return ordinals

    def getDecoratedCorrectAnswers(self) -> list[str]:
        answerStrings: list[str] = list()

        for index, correctAnswerChar in enumerate(self.getCorrectAnswerChars()):
            answerStrings.append(f'[{correctAnswerChar}] {self.__correctAnswers[index]}')

        return answerStrings

    def getPrompt(self, delimiter: str = ' ') -> str:
        if not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        responsesList: list[str] = list()
        entryChar = 'A'

        for response in self.__multipleChoiceResponses:
            responsesList.append(f'[{entryChar}] {response}')
            entryChar = chr(ord(entryChar) + 1)

        responsesStr = delimiter.join(responsesList)
        return f'{self.getQuestion()} {responsesStr}'

    def getResponses(self) -> list[str]:
        return utils.copyList(self.__multipleChoiceResponses)

    def getUndecoratedCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__correctAnswers)
