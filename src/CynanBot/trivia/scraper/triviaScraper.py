from CynanBot.trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.scraper.triviaScraperInterface import TriviaScraperInterface


class TriviaScraper(TriviaScraperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

    async def store(self, question: AbsTriviaQuestion):
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not await self.__triviaSettingsRepository.isScraperEnabled():
            return

        # TODO
        pass
