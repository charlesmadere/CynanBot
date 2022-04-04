import asyncio
import locale
from abc import ABC, abstractmethod

from twitchio.channel import Channel

import CynanBotCommon.utils as utils
import twitch.twitchUtils as twitchUtils
from cuteness.cutenessBoosterPack import CutenessBoosterPack
from cuteness.cutenessRepository import CutenessRepository
from cuteness.doubleCutenessHelper import DoubleCutenessHelper
from CynanBotCommon.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBotCommon.trivia.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from generalSettingsRepository import GeneralSettingsRepository
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType
from triviaUtils import TriviaUtils
from users.user import User


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
        doubleCutenessHelper: DoubleCutenessHelper,
        timber: Timber
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif doubleCutenessHelper is None:
            raise ValueError(f'doubleCutenessHelper argument is malformed: \"{doubleCutenessHelper}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__doubleCutenessHelper: DoubleCutenessHelper = doubleCutenessHelper
        self.__timber: Timber = timber

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
            await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            self.__timber.log('CutenessRedemption', f'Redeemed cuteness redemption of {incrementAmount} for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        except (OverflowError, ValueError) as e:
            self.__timber.log('CutenessRedemption', f'Error redeeming cuteness redemption of {incrementAmount} for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}: {e}')
            await twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

        return True


class PkmnBattleRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

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
        actionCompleted = False

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnBattle(
                userThatRedeemed = userNameThatRedeemed,
                userToBattle = opponentUserName,
                twitchChannel = twitchUser.getHandle()
            ):
                actionCompleted = True

        if not actionCompleted and self.__generalSettingsRepository.isFuntoonTwitchChatFallbackEnabled():
            await twitchUtils.safeSend(twitchChannel, f'!battle {userNameThatRedeemed} {opponentUserName}')
            actionCompleted = True

        self.__timber.log('PkmnBattleRedemption', f'Redeemed pkmn battle redemption for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        return actionCompleted


class PkmnCatchRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

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

        funtoonPkmnCatchType: FuntoonPkmnCatchType = None
        if pkmnCatchBoosterPack.hasCatchType():
            funtoonPkmnCatchType = self.__toFuntoonPkmnCatchType(pkmnCatchBoosterPack)

        self.__timber.log('PkmnCatchRedemption', f'Redeemed Pokemon Catch for {userNameThatRedeemed}:{userIdThatRedeemed} (catch type: {pkmnCatchBoosterPack.getCatchType()}) in {twitchUser.getHandle()}')

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnCatch(
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
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

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

        self.__timber.log('PkmnEvolveRedemption', f'Redeemed Pokemon Evolve for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnGiveEvolve(
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
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

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

        self.__timber.log('PkmnShinyRedemption', f'Redeemed Pokemon Shiny for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')

        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnGiveShiny(
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

    def __init__(
        self,
        timber: Timber
    ):
        if timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: Timber = timber

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

        self.__timber.log('PotdPointRedemption', f'Fetching Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}...')

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchUtils.safeSend(twitchChannel, f'@{userNameThatRedeemed} here\'s the POTD: {picOfTheDay}')
            self.__timber.log('PotdPointRedemption', f'Redeemed Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
            return True
        except FileNotFoundError as e:
            self.__timber.log('PotdPointRedemption', f'Tried to redeem Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}, but the POTD file is missing: {e}')
            await twitchUtils.safeSend(twitchChannel, f'⚠ Pic Of The Day file for {twitchUser.getHandle()} is missing')
        except ValueError as e:
            self.__timber.log('PotdPointRedemption', f'Tried to redeem Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}, but the POTD content is malformed: {e}')
            await twitchUtils.safeSend(twitchChannel, f'⚠ Pic Of The Day content for {twitchUser.getHandle()} is malformed')

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
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameRepository: TriviaGameRepository,
        triviaScoreRepository: TriviaScoreRepository,
        triviaUtils: TriviaUtils
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameRepository is None:
            raise ValueError(f'triviaGameRepository argument is malformed: \"{triviaGameRepository}\"')
        elif triviaScoreRepository is None:
            raise ValueError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif triviaUtils is None:
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameRepository: TriviaGameRepository = triviaGameRepository
        self.__triviaScoreRepository: TriviaScoreRepository = triviaScoreRepository
        self.__triviaUtils: TriviaUtils = triviaUtils

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
            triviaQuestion = await self.__triviaGameRepository.fetchTrivia(
                twitchChannel = twitchUser.getHandle(),
                isJokeTriviaRepositoryEnabled = twitchUser.isJokeTriviaRepositoryEnabled()
            )
        except (RuntimeError, ValueError) as e:
            self.__timber.log('TriviaGameRedemption', f'Error retrieving trivia in {twitchUser.getHandle()}: {e}')
            await twitchUtils.safeSend(twitchChannel, '⚠ Error retrieving trivia')
            return False

        self.__triviaGameRepository.startNewTriviaGame(
            twitchChannel = twitchUser.getHandle(),
            userId = userIdThatRedeemed,
            userName = userNameThatRedeemed
        )

        delaySeconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay()
        if twitchUser.hasWaitForTriviaAnswerDelay():
            delaySeconds = twitchUser.getWaitForTriviaAnswerDelay()
        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)

        points = self.__generalSettingsRepository.getTriviaGamePoints()
        if twitchUser.hasTriviaGamePoints():
            points = twitchUser.getTriviaGamePoints()
        pointsStr = locale.format_string("%d", points, grouping = True)

        pointsPlurality = 'points'
        if points == 1:
            pointsPlurality = 'point'

        await twitchUtils.safeSend(twitchChannel, f'🏫 @{userNameThatRedeemed} !answer in {delaySecondsStr}s for {pointsStr} {pointsPlurality}: {triviaQuestion.getPrompt()}')

        await twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = delaySeconds,
            message = f'😿 {userNameThatRedeemed}, you\'re out of time! {self.__triviaUtils.getAnswerReveal(triviaQuestion)}',
            heartbeat = lambda: not self.__triviaGameRepository.isAnswered(twitchUser.getHandle()),
            beforeSend = lambda: (await self.__triviaScoreRepository.incrementTotalLosses(twitchUser.getHandle(), userIdThatRedeemed) for _ in '_').__anext__()
        )

        self.__timber.log('TriviaGameRedemption', f'Redeemed trivia game for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        return True
