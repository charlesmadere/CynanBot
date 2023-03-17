from abc import ABC, abstractmethod
from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBotCommon.trivia.startNewTriviaGameAction import \
    StartNewTriviaGameAction
from CynanBotCommon.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from generalSettingsRepository import GeneralSettingsRepository
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType
from twitch.twitchChannel import TwitchChannel
from twitch.twitchUtils import TwitchUtils
from users.user import User


class AbsPointRedemption(ABC):

    @abstractmethod
    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
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
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(cutenessRepository, CutenessRepository):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if not isinstance(twitchChannel, TwitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(twitchUser, User):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isCutenessEnabled() or not twitchUser.hasCutenessBoosterPacks():
            return False

        cutenessBoosterPack: Optional[CutenessBoosterPack] = None

        for cbp in twitchUser.getCutenessBoosterPacks():
            if rewardId == cbp.getRewardId():
                cutenessBoosterPack = cbp
                break

        if cutenessBoosterPack is None:
            return False

        incrementAmount = cutenessBoosterPack.getAmount()

        try:
            await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            self.__timber.log('CutenessRedemption', f'Redeemed cuteness of {incrementAmount} for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        except (OverflowError, ValueError) as e:
            self.__timber.log('CutenessRedemption', f'Error redeeming cuteness of {incrementAmount} for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}: {e}', e)
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

        return True


class PkmnBattleRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepository):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if not isinstance(twitchChannel, TwitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(twitchUser, User):
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
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Sorry @{userNameThatRedeemed}, you must specify the exact user name of the person you want to fight')
            return False

        opponentUserName = utils.removePreceedingAt(splits[0])
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnBattle(
                userThatRedeemed = userNameThatRedeemed,
                userToBattle = opponentUserName,
                twitchChannel = twitchUser.getHandle()
            ):
                actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!battle {userNameThatRedeemed} {opponentUserName}')
            actionCompleted = True

        self.__timber.log('PkmnBattleRedemption', f'Redeemed pkmn battle for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        return actionCompleted


class PkmnCatchRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepository):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if not isinstance(twitchChannel, TwitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(twitchUser, User):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isPkmnEnabled() or not twitchUser.hasPkmnCatchBoosterPacks():
            return False

        pkmnCatchBoosterPack: Optional[PkmnCatchBoosterPack] = None
        for pkbp in twitchUser.getPkmnCatchBoosterPacks():
            if rewardId == pkbp.getRewardId():
                pkmnCatchBoosterPack = pkbp
                break

        if pkmnCatchBoosterPack is None:
            return False

        funtoonPkmnCatchType: Optional[FuntoonPkmnCatchType] = None
        if pkmnCatchBoosterPack.hasCatchType():
            funtoonPkmnCatchType = self.__toFuntoonPkmnCatchType(pkmnCatchBoosterPack)

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnCatch(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle(),
                funtoonPkmnCatchType = funtoonPkmnCatchType
            ):
                actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!catch {userNameThatRedeemed}')
            actionCompleted = True

        self.__timber.log('PkmnCatchRedemption', f'Redeemed pkmn catch for {userNameThatRedeemed}:{userIdThatRedeemed} (catch type: {pkmnCatchBoosterPack.getCatchType()}) in {twitchUser.getHandle()}')
        return actionCompleted

    def __toFuntoonPkmnCatchType(
        self,
        pkmnCatchBoosterPack: PkmnCatchBoosterPack
    ) -> FuntoonPkmnCatchType:
        if not isinstance(pkmnCatchBoosterPack, PkmnCatchBoosterPack):
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
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepository):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if not isinstance(twitchChannel, TwitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(twitchUser, User):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isPkmnEnabled():
            return False

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnGiveEvolve(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle()
            ):
                actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!freeevolve {userNameThatRedeemed}')
            actionCompleted = True

        self.__timber.log('PkmnEvolveRedemption', f'Redeemed pkmn evolve for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        return actionCompleted


class PkmnShinyRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepository):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepository = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if not isinstance(twitchChannel, TwitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(twitchUser, User):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        if not twitchUser.isPkmnEnabled():
            return False

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled():
            if await self.__funtoonRepository.pkmnGiveShiny(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle()
            ):
                actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!freeshiny {userNameThatRedeemed}')
            actionCompleted = True

        self.__timber.log('PkmnShinyRedemption', f'Redeemed pkmn shiny for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        return actionCompleted


class PotdPointRedemption(AbsPointRedemption):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if not isinstance(twitchChannel, TwitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(twitchUser, User):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        self.__timber.log('PotdPointRedemption', f'Fetching Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}...')

        try:
            picOfTheDay = await twitchUser.fetchPicOfTheDay()
            await self.__twitchUtils.safeSend(twitchChannel, f'@{userNameThatRedeemed} here\'s the POTD: {picOfTheDay}')
            self.__timber.log('PotdPointRedemption', f'Redeemed Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
            return True
        except FileNotFoundError as e:
            self.__timber.log('PotdPointRedemption', f'Tried to redeem Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}, but the POTD file is missing: {e}')
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Pic Of The Day file for {twitchUser.getHandle()} is missing')
        except ValueError as e:
            self.__timber.log('PotdPointRedemption', f'Tried to redeem Pic Of The Day for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}, but the POTD content is malformed: {e}')
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Pic Of The Day content for {twitchUser.getHandle()} is malformed')

        return False


class StubPointRedemption(AbsPointRedemption):

    def __init__(self):
        pass

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
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
        triviaGameMachine: TriviaGameMachine,
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachine):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchUser: User,
        redemptionMessage: str,
        rewardId: str,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str
    ) -> bool:
        if not isinstance(twitchChannel, TwitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(twitchUser, User):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled():
            return False
        elif not twitchUser.isTriviaGameEnabled():
            return False

        points = generalSettings.getTriviaGamePoints()
        if twitchUser.hasTriviaGamePoints():
            points = twitchUser.getTriviaGamePoints()

        secondsToLive = generalSettings.getWaitForTriviaAnswerDelay()
        if twitchUser.hasWaitForTriviaAnswerDelay():
            secondsToLive = twitchUser.getWaitForTriviaAnswerDelay()

        shinyMultiplier = generalSettings.getTriviaGameShinyMultiplier()
        if twitchUser.hasTriviaGameShinyMultiplier():
            shinyMultiplier = twitchUser.getTriviaGameShinyMultiplier()

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = twitchUser.getHandle(),
            isJokeTriviaRepositoryEnabled = twitchUser.isJokeTriviaRepositoryEnabled(),
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        self.__triviaGameMachine.submitAction(StartNewTriviaGameAction(
            isShinyTriviaEnabled = twitchUser.isShinyTriviaEnabled(),
            pointsForWinning = points,
            secondsToLive = secondsToLive,
            shinyMultiplier = shinyMultiplier,
            twitchChannel = twitchUser.getHandle(),
            userId = userIdThatRedeemed,
            userName = userNameThatRedeemed,
            triviaFetchOptions = triviaFetchOptions
        ))

        self.__timber.log('TriviaGameRedemption', f'Redeemed trivia game for {userNameThatRedeemed}:{userIdThatRedeemed} in {twitchUser.getHandle()}')
        return True
