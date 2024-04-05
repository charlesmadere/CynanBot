from abc import ABC, abstractmethod

from CynanBot.cuteness.cutenessResult import CutenessResult
from CynanBot.trivia.banned.bannedTriviaGameController import \
    BannedTriviaGameController
from CynanBot.trivia.gameController.triviaGameController import \
    TriviaGameController
from CynanBot.trivia.gameController.triviaGameGlobalController import \
    TriviaGameGlobalController
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.score.triviaScoreResult import TriviaScoreResult
from CynanBot.trivia.specialStatus.shinyTriviaResult import ShinyTriviaResult
from CynanBot.trivia.specialStatus.specialTriviaStatus import \
    SpecialTriviaStatus
from CynanBot.trivia.specialStatus.toxicTriviaPunishmentResult import \
    ToxicTriviaPunishmentResult
from CynanBot.trivia.specialStatus.toxicTriviaResult import ToxicTriviaResult
from CynanBot.users.userInterface import UserInterface


class TriviaUtilsInterface(ABC):

    @abstractmethod
    async def getClearedSuperTriviaQueueMessage(self, numberOfGamesRemoved: int) -> str:
        pass

    @abstractmethod
    async def getCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        emote: str,
        userNameThatRedeemed: str,
        twitchUser: UserInterface,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        pass

    @abstractmethod
    async def getIncorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        pass

    @abstractmethod
    async def getInvalidAnswerInputPrompt(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: SpecialTriviaStatus | None = None
    ) -> str:
        pass

    @abstractmethod
    async def getOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        pass

    @abstractmethod
    async def getSuperTriviaCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        points: int,
        emote: str,
        userName: str,
        twitchUser: UserInterface,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        pass

    @abstractmethod
    async def getSuperTriviaLaunchpadPrompt(self, remainingQueueSize: int) -> str | None:
        pass

    @abstractmethod
    async def getSuperTriviaOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        pass

    @abstractmethod
    async def getSuperTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        emote: str,
        twitchUser: UserInterface,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = ' '
    ) -> str:
        pass

    @abstractmethod
    async def getToxicTriviaPunishmentMessage(
        self,
        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult | None,
        emote: str,
        twitchUser: UserInterface,
        bucketDelimiter: str = '; ',
        delimiter: str = ', '
    ) -> str | None:
        pass

    @abstractmethod
    async def getTriviaGameBannedControllers(
        self,
        bannedControllers: list[BannedTriviaGameController] | None,
        delimiter: str = ', '
    ) -> str:
        pass

    @abstractmethod
    async def getTriviaGameControllers(
        self,
        gameControllers: list[TriviaGameController] | None,
        delimiter: str = ', '
    ) -> str:
        pass

    @abstractmethod
    async def getTriviaGameGlobalControllers(
        self,
        gameControllers: list[TriviaGameGlobalController] | None,
        delimiter: str = ', '
    ) -> str:
        pass

    @abstractmethod
    async def getTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        emote: str,
        userNameThatRedeemed: str,
        twitchUser: UserInterface,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = ' '
    ) -> str:
        pass

    @abstractmethod
    async def getTriviaScoreMessage(
        self,
        shinyResult: ShinyTriviaResult,
        userName: str,
        toxicResult: ToxicTriviaResult,
        triviaResult: TriviaScoreResult
    ) -> str:
        pass

    @abstractmethod
    async def isPrivilegedTriviaUser(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> bool:
        pass
