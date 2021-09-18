import asyncio
import locale
from abc import ABC, abstractmethod

import CynanBotCommon.utils as utils
import twitchUtils
from CynanBotCommon.funtoonRepository import FuntoonRepository
from CynanBotCommon.triviaGameRepository import TriviaGameRepository
from generalSettingsRepository import GeneralSettingsRepository
from TwitchIO.twitchio.channel import Channel
from user import User


class AbsPointRedemption(ABC):

    @abstractmethod
    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        pass


class PkmnBattleRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userIdThatRedemeed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedemeed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        splits = utils.getCleanedSplits(redemptionMessage)
        if not utils.hasItems(splits):
            await twitchUtils.safeSend(twitchChannel, f'⚠ Sorry @{userNameThatRedeemed}, you must specify the exact user name of the person you want to fight')
            return False

        opponentUserName = utils.removePreceedingAt(splits[0])

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if self.__funtoonRepository.pkmnBattle(
                userThatRedeemed = userNameThatRedeemed,
                userToBattle = opponentUserName,
                twitchChannel = twitchUser.getHandle()
            ):
                return True

        if self.__generalSettingsRepository.isFuntoonTwitchChatFallbackEnabled():
            await twitchUtils.safeSend(twitchChannel, f'!battle {userNameThatRedeemed} {opponentUserName}')
            return True
        else:
            return False


class PkmnCatchRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userIdThatRedemeed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedemeed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if self.__funtoonRepository.pkmnCatch(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle()
            ):
                return True

        if self.__generalSettingsRepository.isFuntoonTwitchChatFallbackEnabled():
            await twitchUtils.safeSend(twitchChannel, f'!catch {userNameThatRedeemed}')
            return True
        else:
            return False


class PkmnEvolveRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userIdThatRedemeed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedemeed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if self.__funtoonRepository.pkmnGiveEvolve(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle()
            ):
                return True

        if self.__generalSettingsRepository.isFuntoonTwitchChatFallbackEnabled():
            await twitchUtils.safeSend(twitchChannel, f'!freeevolve {userNameThatRedeemed}')
            return True
        else:
            return False


class PkmnShinyRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userIdThatRedemeed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedemeed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if self.__funtoonRepository.pkmnGiveShiny(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle()
            ):
                return True

        if self.__generalSettingsRepository.isFuntoonTwitchChatFallbackEnabled():
            await twitchUtils.safeSend(twitchChannel, f'!freeshiny {userNameThatRedeemed}')
            return True
        else:
            return False


class PotdPointRedemption(AbsPointRedemption):

    def __init__(self):
        pass

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userIdThatRedemeed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedemeed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        print(f'Sending POTD to {userNameThatRedeemed} in {twitchUser.getHandle()}...')

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchUtils.safeSend(twitchChannel, f'@{userNameThatRedeemed} here\'s the POTD: {picOfTheDay}')
            return True
        except FileNotFoundError:
            await twitchUtils.safeSend(twitchChannel, f'⚠ {twitchUser.getHandle()}\'s POTD file is missing!')
        except ValueError:
            await twitchUtils.safeSend(twitchChannel, f'⚠ {twitchUser.getHandle()}\'s POTD content is malformed!')

        return False


class StubPointRedemption(AbsPointRedemption):

    def __init__(self):
        pass

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        return False


class TriviaGameRedemption(AbsPointRedemption):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        triviaGameRepository: TriviaGameRepository
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif triviaGameRepository is None:
            raise ValueError(f'triviaGameRepository argument is malformed: \"{triviaGameRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__triviaGameRepository: TriviaGameRepository = triviaGameRepository

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        userIdThatRedemeed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userIdThatRedemeed):
            raise ValueError(f'userIdThatRedemeed argument is malformed: \"{userIdThatRedemeed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        triviaQuestion = None
        try:
            triviaQuestion = self.__triviaGameRepository.fetchTrivia(
                twitchChannel = twitchUser.getHandle(),
                isLocalTriviaRepositoryEnabled = twitchUser.isLocalTriviaRepositoryEnabled()
            )
        except (RuntimeError, ValueError) as e:
            print(f'Error retrieving trivia in {twitchUser.getHandle()}: {e}')
            await twitchUtils.safeSend(twitchChannel, '⚠ Error retrieving trivia')
            return False

        self.__triviaGameRepository.startNewTriviaGame(
            twitchChannel = twitchUser.getHandle(),
            userId = userIdThatRedemeed,
            userName = userNameThatRedeemed
        )

        points = self.__generalSettingsRepository.getTriviaGamePoints()
        if twitchUser.hasTriviaGamePoints():
            points = twitchUser.getTriviaGamePoints()
        pointsStr = locale.format_string("%d", points, grouping = True)

        delaySeconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay()
        if twitchUser.hasWaitForTriviaAnswerDelay():
            delaySeconds = twitchUser.getWaitForTriviaAnswerDelay()
        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)

        await twitchUtils.safeSend(twitchChannel, f'🏫 {userNameThatRedeemed} you have {delaySecondsStr} seconds to answer the trivia game! Please answer using the !answer command. Get it right and you\'ll win {pointsStr} cuteness points! ✨')
        await twitchUtils.safeSend(twitchChannel, triviaQuestion.getPrompt())

        asyncio.create_task(twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = delaySeconds,
            message = f'😿 Sorry {userNameThatRedeemed}, you\'re out of time! The answer is: {triviaQuestion.getAnswerReveal()}',
            heartbeat = lambda: not self.__triviaGameRepository.isAnswered(twitchUser.getHandle())
        ))

        return True
