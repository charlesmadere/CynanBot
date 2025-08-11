from typing import Final

from .absTriviaEventHandler import AbsTriviaEventHandler
from ..events.absTriviaEvent import AbsTriviaEvent
from ..events.clearedSuperTriviaQueueTriviaEvent import ClearedSuperTriviaQueueTriviaEvent
from ..events.correctAnswerTriviaEvent import CorrectAnswerTriviaEvent
from ..events.correctSuperAnswerTriviaEvent import CorrectSuperAnswerTriviaEvent
from ..events.failedToFetchQuestionSuperTriviaEvent import FailedToFetchQuestionSuperTriviaEvent
from ..events.failedToFetchQuestionTriviaEvent import FailedToFetchQuestionTriviaEvent
from ..events.gameAlreadyInProgressTriviaEvent import GameAlreadyInProgressTriviaEvent
from ..events.gameNotReadyCheckAnswerTriviaEvent import GameNotReadyCheckAnswerTriviaEvent
from ..events.incorrectAnswerTriviaEvent import IncorrectAnswerTriviaEvent
from ..events.incorrectSuperAnswerTriviaEvent import IncorrectSuperAnswerTriviaEvent
from ..events.invalidAnswerInputTriviaEvent import InvalidAnswerInputTriviaEvent
from ..events.newQueuedSuperTriviaGameEvent import NewQueuedSuperTriviaGameEvent
from ..events.newSuperTriviaGameEvent import NewSuperTriviaGameEvent
from ..events.newTriviaGameEvent import NewTriviaGameEvent
from ..events.outOfTimeSuperTriviaEvent import OutOfTimeSuperTriviaEvent
from ..events.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from ..events.wrongUserCheckAnswerTriviaEvent import WrongUserCheckAnswerTriviaEvent
from ..triviaUtilsInterface import TriviaUtilsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class TriviaEventHandler(AbsTriviaEventHandler):

    def __init__(
        self,
        timber: TimberInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None
        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        if not isinstance(event, AbsTriviaEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('TriviaEventHandler', f'Received new trivia event ({event=})')

        twitchChannelProvider = self.__twitchChannelProvider
        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchChannelProvider is None or twitchConnectionReadinessProvider is None:
            self.__timber.log('TriviaEventHandler', f'Received new trivia event, but it won\'t be handled, as the twitchChannelProvider and/or twitchConnectionReadinessProvider instances have not been set ({event=}) ({twitchChannelProvider=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, ClearedSuperTriviaQueueTriviaEvent):
            await self.__handleClearedSuperTriviaQueueTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, CorrectAnswerTriviaEvent):
            await self.__handleCorrectAnswerTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, CorrectSuperAnswerTriviaEvent):
            await self.__handleCorrectSuperAnswerTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, FailedToFetchQuestionTriviaEvent):
            await self.__handleFailedToFetchQuestionTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, FailedToFetchQuestionSuperTriviaEvent):
            await self.__handleFailedToFetchQuestionSuperTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, GameAlreadyInProgressTriviaEvent):
            await self.__handleGameAlreadyInProgressTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, GameNotReadyCheckAnswerTriviaEvent):
            await self.__handleGameNotReadyCheckAnswerTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, IncorrectAnswerTriviaEvent):
            await self.__handleIncorrectAnswerTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, IncorrectSuperAnswerTriviaEvent):
            await self.__handleIncorrectSuperAnswerTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, InvalidAnswerInputTriviaEvent):
            await self.__handleInvalidAnswerInputTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, NewQueuedSuperTriviaGameEvent):
            await self.__handleNewQueuedSuperTriviaGameEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, NewTriviaGameEvent):
            await self.__handleNewTriviaGameEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, NewSuperTriviaGameEvent):
            await self.__handleNewSuperTriviaGameEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, OutOfTimeTriviaEvent):
            await self.__handleOutOfTimeTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, OutOfTimeSuperTriviaEvent):
            await self.__handleOutOfTimeSuperTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, WrongUserCheckAnswerTriviaEvent):
            await self.__handleWrongUserCheckAnswerTriviaEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        else:
            self.__timber.log('TriviaEventHandler', f'Received unhandled trivia event ({event=})')

    async def __handleClearedSuperTriviaQueueTriviaEvent(
        self,
        event: ClearedSuperTriviaQueueTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        message = await self.__triviaUtils.getClearedSuperTriviaQueueMessage(
            numberOfGamesRemoved = event.numberOfGamesRemoved
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleCorrectAnswerTriviaEvent(
        self,
        event: CorrectAnswerTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        message = await self.__triviaUtils.getCorrectAnswerReveal(
            question = event.triviaQuestion,
            newCuteness = event.cutenessResult,
            celebratoryEmote = event.celebratoryTwitchEmote,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleFailedToFetchQuestionTriviaEvent(
        self,
        event: FailedToFetchQuestionTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch trivia question')

    async def __handleFailedToFetchQuestionSuperTriviaEvent(
        self,
        event: FailedToFetchQuestionSuperTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch super trivia question')

    async def __handleGameAlreadyInProgressTriviaEvent(
        self,
        event: GameAlreadyInProgressTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleGameNotReadyCheckAnswerTriviaEvent(
        self,
        event: GameNotReadyCheckAnswerTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleOutOfTimeTriviaEvent(
        self,
        event: OutOfTimeTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            outOfTimeEmote = event.outOfTimeEmote,
            userNameThatRedeemed = event.userName,
            specialTriviaStatus = event.specialTriviaStatus
        ))

    async def __handleIncorrectAnswerTriviaEvent(
        self,
        event: IncorrectAnswerTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        message = await self.__triviaUtils.getIncorrectAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            wrongAnswerEmote = event.wrongAnswerEmote,
            specialTriviaStatus = event.specialTriviaStatus
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleIncorrectSuperAnswerTriviaEvent(
        self,
        event: IncorrectSuperAnswerTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleInvalidAnswerInputTriviaEvent(
        self,
        event: InvalidAnswerInputTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        message = await self.__triviaUtils.getInvalidAnswerInputPrompt(
            question = event.triviaQuestion,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            specialTriviaStatus = event.specialTriviaStatus
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleNewQueuedSuperTriviaGameEvent(
        self,
        event: NewQueuedSuperTriviaGameEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleNewTriviaGameEvent(
        self,
        event: NewTriviaGameEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getTriviaGameQuestionPrompt(
            triviaQuestion = event.triviaQuestion,
            delaySeconds = event.secondsToLive,
            points = event.pointsForWinning,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        ))

    async def __handleNewSuperTriviaGameEvent(
        self,
        event: NewSuperTriviaGameEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaGameQuestionPrompt(
            triviaQuestion = event.triviaQuestion,
            delaySeconds = event.secondsToLive,
            points = event.pointsForWinning,
            emote = event.emote,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        ))

    async def __handleCorrectSuperAnswerTriviaEvent(
        self,
        event: CorrectSuperAnswerTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        message = await self.__triviaUtils.getSuperTriviaCorrectAnswerReveal(
            question = event.triviaQuestion,
            newCuteness = event.cutenessResult,
            points = event.pointsForWinning,
            celebratoryEmote = event.celebratoryTwitchEmote,
            emote = event.emote,
            userName = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId
        )

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.toxicTriviaPunishmentResult,
            emote = event.emote,
            twitchUser = twitchUser
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.remainingQueueSize
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    async def __handleOutOfTimeSuperTriviaEvent(
        self,
        event: OutOfTimeSuperTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaOutOfTimeAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            outOfTimeEmote = event.outOfTimeEmote,
            specialTriviaStatus = event.specialTriviaStatus
        ))

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.toxicTriviaPunishmentResult,
            emote = event.emote,
            twitchUser = twitchUser
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.remainingQueueSize
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    async def __handleWrongUserCheckAnswerTriviaEvent(
        self,
        event: WrongUserCheckAnswerTriviaEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
