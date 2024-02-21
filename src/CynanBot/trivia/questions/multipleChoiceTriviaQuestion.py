from typing import List, Optional

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
        correctAnswers: List[str],
        multipleChoiceResponses: List[str],
        category: Optional[str],
        categoryId: Optional[str],
        question: str,
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        triviaSource: TriviaSource
    ):
        super().__init__(
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            triviaSource = triviaSource,
            triviaType = TriviaQuestionType.MULTIPLE_CHOICE,
        )

        if not utils.areValidStrs(correctAnswers):
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        if not utils.hasItems(multipleChoiceResponses):
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        self.__correctAnswers: List[str] = correctAnswers
        self.__multipleChoiceResponses: List[str] = multipleChoiceResponses

    def getAnswerOrdinals(self) -> List[int]:
        answerOrdinals: List[int] = list()

        for index in range(0, len(self.__multipleChoiceResponses)):
            answerOrdinals.append(index)

        return answerOrdinals

    def getCorrectAnswers(self) -> List[str]:
        answerStrings: List[str] = list()

        for index, correctAnswerChar in enumerate(self.getCorrectAnswerChars()):
            answerStrings.append(f'[{correctAnswerChar}] {self.__correctAnswers[index]}')

        return answerStrings

    def getCorrectAnswerChars(self) -> List[str]:
        correctAnswerOrdinals = self.getCorrectAnswerOrdinals()
        correctAnswerChars: List[str] = list()

        for ordinal in correctAnswerOrdinals:
            correctAnswerChars.append(chr(ord('A') + ordinal))

        if not utils.hasItems(correctAnswerChars):
            raise RuntimeError(f'Couldn\'t find any correct answer chars within \"{self.__correctAnswers}\"')
        if len(correctAnswerChars) != len(self.__correctAnswers):
            raise RuntimeError(f'The length of correctAnswerChars \"{correctAnswerChars}\" ({len(correctAnswerChars)}) is not equal to \"{self.__correctAnswers}\" ({len(self.__correctAnswers)})')

        correctAnswerChars.sort()
        return correctAnswerChars

    def getCorrectAnswerOrdinals(self) -> List[int]:
        ordinals: List[int] = list()

        for index, multipleChoiceResponse in enumerate(self.__multipleChoiceResponses):
            for correctAnswer in self.__correctAnswers:
                if multipleChoiceResponse == correctAnswer:
                    ordinals.append(index)
                    break

        if not utils.hasItems(ordinals):
            raise RuntimeError(f'Couldn\'t find any correct answer ordinals within \"{self.__correctAnswers}\"!')
        if len(ordinals) != len(self.__correctAnswers):
            raise RuntimeError(f'The length of ordinals \"{ordinals}\" ({len(ordinals)}) is not equal to \"{self.__correctAnswers}\" ({len(self.__correctAnswers)})')

        ordinals.sort()
        return ordinals

    def getPrompt(self, delimiter: str = ' ') -> str:
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        responsesList: List[str] = list()
        entryChar = 'A'

        for response in self.__multipleChoiceResponses:
            responsesList.append(f'[{entryChar}] {response}')
            entryChar = chr(ord(entryChar) + 1)

        responsesStr = delimiter.join(responsesList)
        return f'{self.getQuestion()} {responsesStr}'

    def getResponses(self) -> List[str]:
        return utils.copyList(self.__multipleChoiceResponses)
