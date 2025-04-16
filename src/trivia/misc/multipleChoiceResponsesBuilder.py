from typing import Collection

from .multipleChoiceResponsesBuilderInterface import MultipleChoiceResponsesBuilderInterface
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaExceptions import NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException
from ...misc import utils as utils


class MultipleChoiceResponsesBuilder(MultipleChoiceResponsesBuilderInterface):

    def __init__(
        self,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        forcedLastMultipleChoiceResponses: frozenset[str] = frozenset({
            'all of the above',
            'all of these',
            'none of the above',
            'none of these'
        })
    ):
        if not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(forcedLastMultipleChoiceResponses, frozenset):
            raise TypeError(f'forcedLastMultipleChoiceResponses argument is malformed: \"{forcedLastMultipleChoiceResponses}\"')

        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__forcedLastMultipleChoiceResponses: frozenset[str] = forcedLastMultipleChoiceResponses

    async def build(
        self,
        correctAnswers: Collection[str],
        multipleChoiceResponses: Collection[str]
    ) -> list[str]:
        if not isinstance(correctAnswers, Collection) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(multipleChoiceResponses, Collection) or len(multipleChoiceResponses) == 0:
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        filteredMultipleChoiceResponses: list[str] = list()
        filteredMultipleChoiceResponses.extend(correctAnswers)
        maxMultipleChoiceResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()

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
            filteredMultipleChoiceResponses.sort(key = lambda response: self.__sortResponse(response))

        return filteredMultipleChoiceResponses

    def __sortResponse(self, response: str) -> str:
        if response.casefold() in self.__forcedLastMultipleChoiceResponses:
            # force these answers to the end of the list
            return 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'.casefold()
        else:
            return response.casefold()
