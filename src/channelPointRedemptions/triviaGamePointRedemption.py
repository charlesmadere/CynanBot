from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.userInterface import UserInterface


class TriviaGamePointRedemption(AbsChannelPointRedemption2):

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

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        action = await self.__triviaGameBuilder.createNewTriviaGame(
            twitchChannel = pointsRedemption.twitchChannel,
            twitchChannelId = pointsRedemption.twitchChannelId,
            userId = pointsRedemption.redemptionUserId,
            userName = pointsRedemption.redemptionUserName,
        )

        if action is None:
            return PointsRedemptionResult.IGNORED

        self.__triviaGameMachine.submitAction(action)
        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({action=}) ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'TriviaGamePointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardId = twitchUser.triviaGameRewardId

        if utils.isValidStr(rewardId):
            return frozenset({ rewardId })
        else:
            return frozenset()
