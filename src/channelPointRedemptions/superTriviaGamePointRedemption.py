from typing import Final

from .absChannelPointRedemption2 import AbsChannelPointRedemption2
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


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

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = channelPointsRedemption.twitchChannel,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        if action is None:
            return False

        self.__triviaGameMachine.submitAction(action)
        self.__timber.log('SuperTriviaGameRedemption', f'Redeemed ({channelPointsRedemption=}) ({action=})')
        return True
