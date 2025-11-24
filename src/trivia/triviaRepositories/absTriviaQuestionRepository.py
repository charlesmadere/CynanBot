from abc import ABC
from typing import Final

from .triviaQuestionRepositoryInterface import TriviaQuestionRepositoryInterface
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaExceptions import NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException
from ...misc import utils as utils


class AbsTriviaQuestionRepository(TriviaQuestionRepositoryInterface, ABC):

    def __init__(
        self,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
    ):
        if not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self._triviaSettingsRepository: Final[TriviaSettingsRepositoryInterface] = triviaSettingsRepository

    async def _buildMultipleChoiceResponsesList(
        self,
        correctAnswers: list[str],
        multipleChoiceResponses: list[str],
    ) -> list[str]:
        if not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(multipleChoiceResponses, list) or len(multipleChoiceResponses) == 0:
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        filteredMultipleChoiceResponses: list[str] = list(correctAnswers)
        maxMultipleChoiceResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()

        # Annoyingly, I've encountered a few situations where we can have a question with more
        # than one of the same multiple choice answers. The below logic takes some steps to make
        # sure this doesn't happen, while also ensuring that we don't have too many multiple
        # choice responses.

        for response in multipleChoiceResponses:
            cleanedResponse = utils.cleanStr(response, htmlUnescape = True)

            if not utils.isValidStr(cleanedResponse):
                continue

            add = True

            for filteredResponse in filteredMultipleChoiceResponses:
                if cleanedResponse.casefold() == filteredResponse.casefold():
                    add = False
                    break

            if add:
                filteredMultipleChoiceResponses.append(cleanedResponse)

                if len(filteredMultipleChoiceResponses) >= maxMultipleChoiceResponses:
                    break

        if len(filteredMultipleChoiceResponses) == 0:
            return filteredMultipleChoiceResponses

        if utils.areAllStrsInts(filteredMultipleChoiceResponses):
            filteredMultipleChoiceResponses.sort(key = lambda response: int(response))
        else:
            filteredMultipleChoiceResponses.sort(key = lambda response: response.casefold())

        return filteredMultipleChoiceResponses

    async def _verifyIsActuallyMultipleChoiceQuestion(
        self,
        correctAnswers: list[str],
        multipleChoiceResponses: list[str],
    ) -> bool:
        if not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(multipleChoiceResponses, list) or len(multipleChoiceResponses) == 0:
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        for correctAnswer in correctAnswers:
            if correctAnswer.casefold() != str(True).casefold() and correctAnswer.casefold() != str(False).casefold():
                return True

        if len(multipleChoiceResponses) != 2:
            return True

        containsTrue = False
        containsFalse = False

        for response in multipleChoiceResponses:
            if response.casefold() == str(True).casefold():
                containsTrue = True
            elif response.casefold() == str(False).casefold():
                containsFalse = True
            else:
                break

        return not containsTrue or not containsFalse
