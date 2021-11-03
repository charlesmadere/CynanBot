import asyncio
import locale
from abc import ABC, abstractmethod

from twitchio.channel import Channel

import CynanBotCommon.utils as utils
import twitchUtils
from cuteness.cutenessBoosterPack import CutenessBoosterPack
from cuteness.cutenessRepository import CutenessRepository
from cuteness.doubleCutenessHelper import DoubleCutenessHelper
from CynanBotCommon.funtoonRepository import (FuntoonPkmnCatchType,
                                              FuntoonRepository)
from CynanBotCommon.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.triviaModels import AbsTriviaQuestion
from CynanBotCommon.triviaScoreRepository import TriviaScoreRepository
from generalSettingsRepository import GeneralSettingsRepository
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType
from user.user import User


class AbsPointRedemption(ABC):

    @abstractmethod
    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        pass


class CutenessRedemption(AbsPointRedemption):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        doubleCutenessHelper: DoubleCutenessHelper
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif doubleCutenessHelper is None:
            raise ValueError(f'doubleCutenessHelper argument is malformed: \"{doubleCutenessHelper}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__doubleCutenessHelper: DoubleCutenessHelper = doubleCutenessHelper

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isCutenessEnabled() or not twitchUser.hasCutenessBoosterPacks():
            return False

        cutenessBoosterPack: CutenessBoosterPack = None

        for cbp in twitchUser.getCutenessBoosterPacks():
            if rewardId == cbp.getRewardId():
                cutenessBoosterPack = cbp
                break

        if cutenessBoosterPack is None:
            return False

        incrementAmount = cutenessBoosterPack.getAmount()

        if self.__doubleCutenessHelper.isWithinDoubleCuteness(twitchUser.getHandle()):
            incrementAmount = cutenessBoosterPack.getAmount() * 2

        try:
            self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

        return True


class DoubleCutenessRedemption(AbsPointRedemption):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        doubleCutenessHelper: DoubleCutenessHelper
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif doubleCutenessHelper is None:
            raise ValueError(f'doubleCutenessHelper argument is malformed: \"{doubleCutenessHelper}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__doubleCutenessHelper: DoubleCutenessHelper = doubleCutenessHelper

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isCutenessEnabled() or not twitchUser.hasCutenessBoosterPacks():
            return False

        print(f'Enabling double cuteness points in {twitchUser.getHandle()} ({utils.getNowTimeText(includeSeconds = True)})')
        self.__doubleCutenessHelper.beginDoubleCuteness(twitchUser.getHandle())
        cutenessBoosterPacks = twitchUser.getCutenessBoosterPacks()

        # It's sort of not obvious what's going on here, but so what I'm trying to do is not
        # penalize the given user for redeeming double cuteness. Double cuteness should just cost
        # the user the same number of channel points that the baseline cuteness redemption is, and
        # so let's go ahead and multiply that by 2.
        incrementAmount = cutenessBoosterPacks[0].getAmount() * 2

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            await twitchUtils.safeSend(twitchChannel, f'✨ Double cuteness points enabled for the next {self.__cutenessRepository.getDoubleCutenessTimeSecondsStr()} seconds! Increase your cuteness now~ ✨ Also, cuteness for {userNameThatRedeemed} has increased to {result.getCutenessStr()} ✨')

            asyncio.create_task(twitchUtils.waitThenSend(
                messageable = twitchChannel,
                delaySeconds = self.__cutenessRepository.getDoubleCutenessTimeSeconds(),
                message = 'Double cuteness has ended! 😿'
            ))
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {userNameThatRedeemed}')


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
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isPkmnEnabled():
            return False

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
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isPkmnEnabled() or not twitchUser.hasPkmnCatchBoosterPacks():
            return False

        pkmnCatchBoosterPack: PkmnCatchBoosterPack = None

        for pkbp in twitchUser.getPkmnCatchBoosterPacks():
            if rewardId == pkbp.getRewardId():
                pkmnCatchBoosterPack = pkbp
                break

        if pkmnCatchBoosterPack is None:
            return False

        funtoonPkmnCatchType = self.__toFuntoonPkmnCatchType(pkmnCatchBoosterPack)

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if self.__funtoonRepository.pkmnCatch(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle(),
                funtoonPkmnCatchType = funtoonPkmnCatchType
            ):
                return True

        if self.__generalSettingsRepository.isFuntoonTwitchChatFallbackEnabled():
            await twitchUtils.safeSend(twitchChannel, f'!catch {userNameThatRedeemed}')
            return True
        else:
            return False

    def __toFuntoonPkmnCatchType(
        self,
        pkmnCatchBoosterPack: PkmnCatchBoosterPack
    ) -> FuntoonPkmnCatchType:
        if pkmnCatchBoosterPack is None:
            raise ValueError(f'pkmnCatchBoosterPack argument is malformed: \"{pkmnCatchBoosterPack}\"')

        if pkmnCatchBoosterPack.getCatchType() is PkmnCatchType.NORMAL:
            return FuntoonPkmnCatchType.NORMAL
        elif pkmnCatchBoosterPack.getCatchType() is PkmnCatchType.GREAT:
            return FuntoonPkmnCatchType.GREAT
        elif pkmnCatchBoosterPack.getCatchType() is PkmnCatchType.ULTRA:
            return FuntoonPkmnCatchType.ULTRA
        else:
            raise ValueError(f'unknown PkmnCatchType: \"{pkmnCatchBoosterPack.getCatchType()}\"')


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
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isPkmnEnabled():
            return False

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
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isPkmnEnabled():
            return False

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
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
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
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        return False


class TriviaGameRedemption(AbsPointRedemption):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        triviaGameRepository: TriviaGameRepository,
        triviaScoreRepository: TriviaScoreRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif triviaGameRepository is None:
            raise ValueError(f'triviaGameRepository argument is malformed: \"{triviaGameRepository}\"')
        elif triviaScoreRepository is None:
            raise ValueError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__triviaGameRepository: TriviaGameRepository = triviaGameRepository
        self.__triviaScoreRepository: TriviaScoreRepository = triviaScoreRepository

    async def handlePointRedemption(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not self.__generalSettingsRepository.isTriviaGameEnabled():
            return False
        elif not twitchUser.isTriviaGameEnabled():
            return False

        triviaQuestion: AbsTriviaQuestion = None
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
            userId = userIdThatRedeemed,
            userName = userNameThatRedeemed
        )

        cutenessResult = self.__cutenessRepository.fetchCuteness(
            fetchLocalLeaderboard = False,
            twitchChannel = twitchUser.getHandle(),
            userId = userIdThatRedeemed,
            userName = userNameThatRedeemed
        )

        triviaGameTutorialCutenessThreshold = self.__generalSettingsRepository.getTriviaGameTutorialCutenessThreshold()
        if twitchUser.hasTriviaGameTutorialCutenessThreshold():
            triviaGameTutorialCutenessThreshold = twitchUser.getTriviaGameTutorialCutenessThreshold()

        delaySeconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay()
        if twitchUser.hasWaitForTriviaAnswerDelay():
            delaySeconds = twitchUser.getWaitForTriviaAnswerDelay()
        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)

        points = self.__generalSettingsRepository.getTriviaGamePoints()
        if twitchUser.hasTriviaGamePoints():
            points = twitchUser.getTriviaGamePoints()
        pointsStr = locale.format_string("%d", points, grouping = True)

        if cutenessResult.hasCuteness() and cutenessResult.getCuteness() >= triviaGameTutorialCutenessThreshold:
            await twitchUtils.safeSend(twitchChannel, f'🏫 {userNameThatRedeemed} !answer in {delaySecondsStr}s for {pointsStr} points: {triviaQuestion.getPrompt()}')
        else:
            await twitchUtils.safeSend(twitchChannel, f'🏫 {userNameThatRedeemed} you have {delaySecondsStr} seconds to answer the trivia game! Please answer using the !answer command. Get it right and you\'ll win {pointsStr} cuteness points! ✨')
            await twitchUtils.safeSend(twitchChannel, triviaQuestion.getPrompt())

        asyncio.create_task(twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = delaySeconds,
            message = f'😿 Sorry {userNameThatRedeemed}, you\'re out of time! The answer is: {triviaQuestion.getAnswerReveal()}',
            heartbeat = lambda: not self.__triviaGameRepository.isAnswered(twitchUser.getHandle()),
            beforeSend = lambda: self.__triviaScoreRepository.incrementTotalLosses(twitchUser.getHandle(), userIdThatRedeemed)
        ))

        return True
