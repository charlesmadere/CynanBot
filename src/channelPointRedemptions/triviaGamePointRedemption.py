from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class TriviaGamePointRedemption(AbsChannelPointRedemption):

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
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        startNewTriviaGameAction = await self.__triviaGameBuilder.createNewTriviaGame(
            twitchChannel = twitchChannelPointsMessage.twitchUser.handle,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            userId = twitchChannelPointsMessage.userId,
            userName = twitchChannelPointsMessage.userName,
        )

        if startNewTriviaGameAction is None:
            return False

        self.__triviaGameMachine.submitAction(startNewTriviaGameAction)
        self.__timber.log('TriviaGameRedemption', f'Redeemed trivia game for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchChannel.getTwitchChannelName()}')
        return True
