import random

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.toxicTriviaOccurencesRepository import \
    ToxicTriviaOccurencesRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class ToxicTriviaHelper():

    def __init__(
        self,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepository,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        if not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepository):
            raise ValueError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise ValueError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository
        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

    async def isToxicSuperTriviaQuestion(self, twitchChannel: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        if not await self.__triviaSettingsRepository.areToxicTriviasEnabled():
            return False        

        probability = await self.__triviaSettingsRepository.getToxicProbability()
        randomNumber = random.uniform(0, 1)

        if randomNumber > probability:
            return False

        self.__timber.log('ToxicTriviaHelper', f'A toxic super trivia question was encountered in {twitchChannel}!')
        return True

    async def toxicTriviaWin(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        result = await self.__toxicTriviaOccurencesRepository.incrementToxicCount(
            twitchChannel = twitchChannel,
            userId = userId
        )

        self.__timber.log('ToxicTriviaHelper', f'In {twitchChannel}, {userName}:{result.getUserId()} won a toxic trivia question!')
