import random

from .toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class ToxicTriviaHelper:

    def __init__(
        self,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface,
        timber: TimberInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        if not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface):
            raise TypeError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')

        self.__toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = toxicTriviaOccurencesRepository
        self.__timber: TimberInterface = timber
        self.__triviaSettings: TriviaSettingsInterface = triviaSettings

    async def isToxicSuperTriviaQuestion(self, twitchChannelId: str) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__triviaSettings.areToxicTriviasEnabled():
            return False

        probability = await self.__triviaSettings.getToxicProbability()
        randomNumber = random.uniform(0, 1)

        if randomNumber > probability:
            return False

        self.__timber.log('ToxicTriviaHelper', f'A toxic super trivia question was encountered in {twitchChannelId}!')
        return True

    async def toxicTriviaWin(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        result = await self.__toxicTriviaOccurencesRepository.incrementToxicCount(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        self.__timber.log('ToxicTriviaHelper', f'In {twitchChannel}, {userName}:{result.userId} won a toxic trivia question!')
