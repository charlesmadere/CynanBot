from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.scraper.triviaScraperInterface import \
    TriviaScraperInterface
from CynanBot.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaScraper(TriviaScraperInterface):

    def __init__(
        self,
        glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        if not isinstance(glacialTriviaQuestionRepository, GlacialTriviaQuestionRepositoryInterface):
            raise TypeError(f'glacialTriviaQuestionRepository argument is malformed: \"{glacialTriviaQuestionRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface = glacialTriviaQuestionRepository
        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

    async def store(self, question: AbsTriviaQuestion):
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not await self.__triviaSettingsRepository.isScraperEnabled():
            return

        if await self.__glacialTriviaQuestionRepository.store(question):
            self.__timber.log('TriviaScraper', f'Stored a trivia question from {question.triviaSource} into glacial storage')
