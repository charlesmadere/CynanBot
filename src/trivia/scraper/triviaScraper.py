from typing import Final

from .triviaScraperInterface import TriviaScraperInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaRepositories.glacialTriviaQuestionRepositoryInterface import GlacialTriviaQuestionRepositoryInterface
from ...timber.timberInterface import TimberInterface


class TriviaScraper(TriviaScraperInterface):

    def __init__(
        self,
        glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface,
        timber: TimberInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        if not isinstance(glacialTriviaQuestionRepository, GlacialTriviaQuestionRepositoryInterface):
            raise TypeError(f'glacialTriviaQuestionRepository argument is malformed: \"{glacialTriviaQuestionRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')

        self.__glacialTriviaQuestionRepository: Final[GlacialTriviaQuestionRepositoryInterface] = glacialTriviaQuestionRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaSettings: Final[TriviaSettingsInterface] = triviaSettings

    async def store(self, question: AbsTriviaQuestion):
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not await self.__triviaSettings.isScraperEnabled():
            return
        elif question.triviaSource is TriviaSource.GLACIAL:
            return

        if await self.__glacialTriviaQuestionRepository.store(question):
            self.__timber.log('TriviaScraper', f'Stored a trivia question from {question.triviaSource} into glacial storage')
