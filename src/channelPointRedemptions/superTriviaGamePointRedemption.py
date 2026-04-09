from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.questions.triviaSource import TriviaSource
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class SuperTriviaGamePointRedemption(AbsChannelPointRedemption2):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface] = triviaGameMachine

    async def __determineRequiredTriviaSource(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> TriviaSource | None:
        superTriviaLotrGameRewardId = pointsRedemption.twitchUser.superTriviaLotrGameRewardId

        if not utils.isValidStr(superTriviaLotrGameRewardId):
            return None
        elif superTriviaLotrGameRewardId == pointsRedemption.rewardId:
            return TriviaSource.LORD_OF_THE_RINGS
        else:
            return None

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        requiredTriviaSource = await self.__determineRequiredTriviaSource(
            pointsRedemption = pointsRedemption,
        )

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = pointsRedemption.twitchChannel,
            twitchChannelId = pointsRedemption.twitchChannelId,
            requiredTriviaSource = requiredTriviaSource,
        )

        if action is None:
            return PointsRedemptionResult.IGNORED

        self.__triviaGameMachine.submitAction(action)
        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({action=}) ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'SuperTriviaGamePointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardIds: set[str] = set()

        superTriviaGameRewardId = twitchUser.superTriviaGameRewardId
        if utils.isValidStr(superTriviaGameRewardId):
            rewardIds.add(superTriviaGameRewardId)

        superTriviaLotrGameRewardId = twitchUser.superTriviaLotrGameRewardId
        if utils.isValidStr(superTriviaLotrGameRewardId):
            rewardIds.add(superTriviaLotrGameRewardId)

        return frozenset(rewardIds)
