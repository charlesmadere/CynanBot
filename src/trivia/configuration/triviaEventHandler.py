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
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class TriviaEventHandler(AbsTriviaEventHandler):

    def __init__(
        self,
        timber: TimberInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        if not isinstance(event, AbsTriviaEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('TriviaEventHandler', f'Received new trivia event ({event=})')

        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchConnectionReadinessProvider is None:
            self.__timber.log('TriviaEventHandler', f'Received new trivia event, but it won\'t be handled, as the twitchConnectionReadinessProvider instance has not been set ({event=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, ClearedSuperTriviaQueueTriviaEvent):
            await self.__handleClearedSuperTriviaQueueTriviaEvent(
                event = event,
            )

        elif isinstance(event, CorrectAnswerTriviaEvent):
            await self.__handleCorrectAnswerTriviaEvent(
                event = event,
            )

        elif isinstance(event, CorrectSuperAnswerTriviaEvent):
            await self.__handleCorrectSuperAnswerTriviaEvent(
                event = event,
            )

        elif isinstance(event, FailedToFetchQuestionTriviaEvent):
            await self.__handleFailedToFetchQuestionTriviaEvent(
                event = event,
            )

        elif isinstance(event, FailedToFetchQuestionSuperTriviaEvent):
            await self.__handleFailedToFetchQuestionSuperTriviaEvent(
                event = event,
            )

        elif isinstance(event, GameAlreadyInProgressTriviaEvent):
            await self.__handleGameAlreadyInProgressTriviaEvent(
                event = event,
            )

        elif isinstance(event, GameNotReadyCheckAnswerTriviaEvent):
            await self.__handleGameNotReadyCheckAnswerTriviaEvent(
                event = event,
            )

        elif isinstance(event, IncorrectAnswerTriviaEvent):
            await self.__handleIncorrectAnswerTriviaEvent(
                event = event,
            )

        elif isinstance(event, IncorrectSuperAnswerTriviaEvent):
            await self.__handleIncorrectSuperAnswerTriviaEvent(
                event = event,
            )

        elif isinstance(event, InvalidAnswerInputTriviaEvent):
            await self.__handleInvalidAnswerInputTriviaEvent(
                event = event,
            )

        elif isinstance(event, NewQueuedSuperTriviaGameEvent):
            await self.__handleNewQueuedSuperTriviaGameEvent(
                event = event,
            )

        elif isinstance(event, NewTriviaGameEvent):
            await self.__handleNewTriviaGameEvent(
                event = event,
            )

        elif isinstance(event, NewSuperTriviaGameEvent):
            await self.__handleNewSuperTriviaGameEvent(
                event = event,
            )

        elif isinstance(event, OutOfTimeTriviaEvent):
            await self.__handleOutOfTimeTriviaEvent(
                event = event,
            )

        elif isinstance(event, OutOfTimeSuperTriviaEvent):
            await self.__handleOutOfTimeSuperTriviaEvent(
                event = event,
            )

        elif isinstance(event, WrongUserCheckAnswerTriviaEvent):
            await self.__handleWrongUserCheckAnswerTriviaEvent(
                event = event,
            )

        else:
            self.__timber.log('TriviaEventHandler', f'Received unhandled trivia event ({event=})')

    async def __handleClearedSuperTriviaQueueTriviaEvent(
        self,
        event: ClearedSuperTriviaQueueTriviaEvent,
    ):
        text = await self.__triviaUtils.getClearedSuperTriviaQueueMessage(
            numberOfGamesRemoved = event.numberOfGamesRemoved,
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId
        )

    async def __handleCorrectAnswerTriviaEvent(
        self,
        event: CorrectAnswerTriviaEvent,
    ):
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        text = await self.__triviaUtils.getCorrectAnswerReveal(
            question = event.triviaQuestion,
            newCuteness = event.cutenessResult,
            celebratoryEmote = event.celebratoryTwitchEmote,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleFailedToFetchQuestionTriviaEvent(
        self,
        event: FailedToFetchQuestionTriviaEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Unable to fetch trivia question',
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleFailedToFetchQuestionSuperTriviaEvent(
        self,
        event: FailedToFetchQuestionSuperTriviaEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Unable to fetch super trivia question',
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleGameAlreadyInProgressTriviaEvent(
        self,
        event: GameAlreadyInProgressTriviaEvent,
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleGameNotReadyCheckAnswerTriviaEvent(
        self,
        event: GameNotReadyCheckAnswerTriviaEvent,
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleOutOfTimeTriviaEvent(
        self,
        event: OutOfTimeTriviaEvent,
    ):
        text = await self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            outOfTimeEmote = event.outOfTimeEmote,
            userNameThatRedeemed = event.userName,
            specialTriviaStatus = event.specialTriviaStatus
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleIncorrectAnswerTriviaEvent(
        self,
        event: IncorrectAnswerTriviaEvent,
    ):
        text = await self.__triviaUtils.getIncorrectAnswerReveal(
            question = event.triviaQuestion,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            wrongAnswerEmote = event.wrongAnswerEmote,
            specialTriviaStatus = event.specialTriviaStatus,
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleIncorrectSuperAnswerTriviaEvent(
        self,
        event: IncorrectSuperAnswerTriviaEvent,
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleInvalidAnswerInputTriviaEvent(
        self,
        event: InvalidAnswerInputTriviaEvent,
    ):
        text = await self.__triviaUtils.getInvalidAnswerInputPrompt(
            question = event.triviaQuestion,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            specialTriviaStatus = event.specialTriviaStatus,
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNewQueuedSuperTriviaGameEvent(
        self,
        event: NewQueuedSuperTriviaGameEvent,
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    async def __handleNewTriviaGameEvent(
        self,
        event: NewTriviaGameEvent,
    ):
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        text = await self.__triviaUtils.getTriviaGameQuestionPrompt(
            triviaQuestion = event.triviaQuestion,
            delaySeconds = event.secondsToLive,
            points = event.pointsForWinning,
            emote = event.emote,
            userNameThatRedeemed = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus,
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleNewSuperTriviaGameEvent(
        self,
        event: NewSuperTriviaGameEvent,
    ):
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        text = await self.__triviaUtils.getSuperTriviaGameQuestionPrompt(
            triviaQuestion = event.triviaQuestion,
            delaySeconds = event.secondsToLive,
            points = event.pointsForWinning,
            emote = event.emote,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus,
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleCorrectSuperAnswerTriviaEvent(
        self,
        event: CorrectSuperAnswerTriviaEvent,
    ):
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        text = await self.__triviaUtils.getSuperTriviaCorrectAnswerReveal(
            question = event.triviaQuestion,
            newCuteness = event.cutenessResult,
            points = event.pointsForWinning,
            celebratoryEmote = event.celebratoryTwitchEmote,
            emote = event.emote,
            userName = event.userName,
            twitchUser = twitchUser,
            specialTriviaStatus = event.specialTriviaStatus,
        )

        self.__twitchChatMessenger.send(
            text = text,
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.toxicTriviaPunishmentResult,
            emote = event.emote,
            twitchUser = twitchUser,
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            self.__twitchChatMessenger.send(
                text = toxicTriviaPunishmentPrompt,
                twitchChannelId = event.twitchChannelId,
                replyMessageId = event.twitchChatMessageId,
            )

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.remainingQueueSize,
        )

        if utils.isValidStr(launchpadPrompt):
            self.__twitchChatMessenger.send(
                text = launchpadPrompt,
                twitchChannelId = event.twitchChannelId,
            )

    async def __handleOutOfTimeSuperTriviaEvent(
        self,
        event: OutOfTimeSuperTriviaEvent,
    ):
        twitchUser = await self.__usersRepository.getUserAsync(event.twitchChannel)

        self.__twitchChatMessenger.send(
            text = await self.__triviaUtils.getSuperTriviaOutOfTimeAnswerReveal(
                question = event.triviaQuestion,
                emote = event.emote,
                outOfTimeEmote = event.outOfTimeEmote,
                specialTriviaStatus = event.specialTriviaStatus,
            ),
            twitchChannelId = event.twitchChannelId,
        )

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.toxicTriviaPunishmentResult,
            emote = event.emote,
            twitchUser = twitchUser,
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            self.__twitchChatMessenger.send(
                text = toxicTriviaPunishmentPrompt,
                twitchChannelId = event.twitchChannelId,
            )

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.remainingQueueSize,
        )

        if utils.isValidStr(launchpadPrompt):
            self.__twitchChatMessenger.send(
                text = launchpadPrompt,
                twitchChannelId = event.twitchChannelId,
            )

    async def __handleWrongUserCheckAnswerTriviaEvent(
        self,
        event: WrongUserCheckAnswerTriviaEvent,
    ):
        # this is intentionally empty and currently has no intended use case
        pass

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
