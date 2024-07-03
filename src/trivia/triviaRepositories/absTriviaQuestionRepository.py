from ..triviaExceptions import (NoTriviaCorrectAnswersException,
                                     NoTriviaMultipleChoiceResponsesException)
from .triviaQuestionRepositoryInterface import \
    TriviaQuestionRepositoryInterface
from ..triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from ...misc import utils as utils


class AbsTriviaQuestionRepository(TriviaQuestionRepositoryInterface):

    def __init__(
        self,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        if not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self._triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

    async def _buildMultipleChoiceResponsesList(
        self,
        correctAnswers: list[str],
        multipleChoiceResponses: list[str]
    ) -> list[str]:
        if not utils.hasItems(correctAnswers):
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not utils.hasItems(multipleChoiceResponses):
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        filteredMultipleChoiceResponses: list[str] = utils.copyList(correctAnswers)
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
                if cleanedResponse.lower() == filteredResponse.lower():
                    add = False
                    break

            if add:
                filteredMultipleChoiceResponses.append(cleanedResponse)

                if len(filteredMultipleChoiceResponses) >= maxMultipleChoiceResponses:
                    break

        if not utils.hasItems(filteredMultipleChoiceResponses):
            return filteredMultipleChoiceResponses

        if utils.areAllStrsInts(filteredMultipleChoiceResponses):
            filteredMultipleChoiceResponses.sort(key = lambda response: int(response))
        else:
            filteredMultipleChoiceResponses.sort(key = lambda response: response.lower())

        return filteredMultipleChoiceResponses

    async def _verifyIsActuallyMultipleChoiceQuestion(
        self,
        correctAnswers: list[str],
        multipleChoiceResponses: list[str]
    ) -> bool:
        if not utils.hasItems(correctAnswers):
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not utils.hasItems(multipleChoiceResponses):
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        for correctAnswer in correctAnswers:
            if correctAnswer.lower() != str(True).lower() and correctAnswer.lower() != str(False).lower():
                return True

        if len(multipleChoiceResponses) != 2:
            return True

        containsTrue = False
        containsFalse = False

        for response in multipleChoiceResponses:
            if response.lower() == str(True).lower():
                containsTrue = True
            elif response.lower() == str(False).lower():
                containsFalse = True

        return not containsTrue or not containsFalse
