import traceback
from abc import ABC, abstractmethod
from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from CynanBotCommon.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.trivia.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBotCommon.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from generalSettingsRepository import GeneralSettingsRepository
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType
from twitch.twitchChannel import TwitchChannel
from twitch.twitchChannelPointsMessage import TwitchChannelPointsMessage
from twitch.twitchUtils import TwitchUtils


class AbsPointRedemption(ABC):

    @abstractmethod
    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        pass


class CutenessRedemption(AbsPointRedemption):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(cutenessRepository, CutenessRepository):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not twitchUser.isCutenessEnabled() or not twitchUser.hasCutenessBoosterPacks():
            return False

        cutenessBoosterPack: Optional[CutenessBoosterPack] = None

        for cbp in twitchUser.getCutenessBoosterPacks():
            if twitchChannelPointsMessage.getRewardId() == cbp.getRewardId():
                cutenessBoosterPack = cbp
                break

        if cutenessBoosterPack is None:
            return False

        incrementAmount = cutenessBoosterPack.getAmount()

        try:
            await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = twitchChannelPointsMessage.getUserId(),
                userName = twitchChannelPointsMessage.getUserName()
            )

            self.__timber.log('CutenessRedemption', f'Redeemed cuteness of {incrementAmount} for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
        except (OverflowError, ValueError) as e:
            self.__timber.log('CutenessRedemption', f'Error redeeming cuteness of {incrementAmount} for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {twitchChannelPointsMessage.getUserName()}')

        return True


class PkmnBattleRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepositoryInterface):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not twitchUser.isPkmnEnabled():
            return False

        splits = utils.getCleanedSplits(twitchChannelPointsMessage.getRedemptionMessage())

        if not utils.hasItems(splits):
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Sorry @{twitchChannelPointsMessage.getUserName()}, you must specify the exact user name of the person you want to fight')
            return False

        opponentUserName = utils.removePreceedingAt(splits[0])
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonRepository.pkmnBattle(
            twitchChannel = twitchUser.getHandle(),
            userThatRedeemed = twitchChannelPointsMessage.getUserName(),
            userToBattle = opponentUserName
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!battle {twitchChannelPointsMessage.getUserName()} {opponentUserName}')
            actionCompleted = True

        self.__timber.log('PkmnBattleRedemption', f'Redeemed pkmn battle for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
        return actionCompleted


class PkmnCatchRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepositoryInterface):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not twitchUser.isPkmnEnabled() or not twitchUser.hasPkmnCatchBoosterPacks():
            return False

        pkmnCatchBoosterPack: Optional[PkmnCatchBoosterPack] = None
        for pkbp in twitchUser.getPkmnCatchBoosterPacks():
            if twitchChannelPointsMessage.getRewardId() == pkbp.getRewardId():
                pkmnCatchBoosterPack = pkbp
                break

        if pkmnCatchBoosterPack is None:
            return False

        funtoonPkmnCatchType: Optional[FuntoonPkmnCatchType] = None
        if pkmnCatchBoosterPack.hasCatchType():
            funtoonPkmnCatchType = self.__toFuntoonPkmnCatchType(pkmnCatchBoosterPack)

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonRepository.pkmnCatch(
            twitchChannel = twitchUser.getHandle(),
            userThatRedeemed = twitchChannelPointsMessage.getUserName(),
            funtoonPkmnCatchType = funtoonPkmnCatchType
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!catch {twitchChannelPointsMessage.getUserName()}')
            actionCompleted = True

        self.__timber.log('PkmnCatchRedemption', f'Redeemed pkmn catch for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} (catch type: {pkmnCatchBoosterPack.getCatchType()}) in {twitchUser.getHandle()}')
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
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepositoryInterface):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not twitchUser.isPkmnEnabled():
            return False

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonRepository.pkmnGiveEvolve(
            twitchChannel = twitchUser.getHandle(),
            userThatRedeemed = twitchChannelPointsMessage.getUserName()
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!freeevolve {twitchChannelPointsMessage.getUserName()}')
            actionCompleted = True

        self.__timber.log('PkmnEvolveRedemption', f'Redeemed pkmn evolve for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
        return actionCompleted


class PkmnShinyRedemption(AbsPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(funtoonRepository, FuntoonRepositoryInterface):
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not twitchUser.isPkmnEnabled():
            return False

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        actionCompleted = False

        if generalSettings.isFuntoonApiEnabled() and await self.__funtoonRepository.pkmnGiveShiny(
            twitchChannel = twitchUser.getHandle(),
            userThatRedeemed = twitchChannelPointsMessage.getUserName()
        ):
            actionCompleted = True

        if not actionCompleted and generalSettings.isFuntoonTwitchChatFallbackEnabled():
            await self.__twitchUtils.safeSend(twitchChannel, f'!freeshiny {twitchChannelPointsMessage.getUserName()}')
            actionCompleted = True

        self.__timber.log('PkmnShinyRedemption', f'Redeemed pkmn shiny for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
        return actionCompleted


class PotdPointRedemption(AbsPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtils
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()
        self.__timber.log('PotdPointRedemption', f'Fetching Pic Of The Day for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}...')

        try:
            picOfTheDay = await twitchUser.fetchPicOfTheDay()
            await self.__twitchUtils.safeSend(twitchChannel, f'@{twitchChannelPointsMessage.getUserName()} here\'s the POTD: {picOfTheDay}')
            self.__timber.log('PotdPointRedemption', f'Redeemed Pic Of The Day for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}')
            return True
        except FileNotFoundError as e:
            self.__timber.log('PotdPointRedemption', f'Tried to redeem Pic Of The Day for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}, but the POTD file is missing: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Pic Of The Day file for {twitchUser.getHandle()} is missing')
        except ValueError as e:
            self.__timber.log('PotdPointRedemption', f'Tried to redeem Pic Of The Day for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchUser.getHandle()}, but the POTD content is malformed: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Pic Of The Day content for {twitchUser.getHandle()} is malformed')

        return False


class StubPointRedemption(AbsPointRedemption):

    def __init__(self):
        pass

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        return False


class SuperTriviaGameRedemption(AbsPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise ValueError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')

        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        startNewSuperTriviaGameAction = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = twitchChannel.getTwitchChannelName()
        )

        if startNewSuperTriviaGameAction is None:
            return

        self.__triviaGameMachine.submitAction(startNewSuperTriviaGameAction)

        self.__timber.log('TriviaGameRedemption', f'Redeemed super trivia game for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchChannel.getTwitchChannelName()}')
        return True


class TriviaGameRedemption(AbsPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise ValueError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')

        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        startNewTriviaGameAction = await self.__triviaGameBuilder.createNewTriviaGame(
            twitchChannel = twitchChannel.getTwitchChannelName(),
            userId = twitchChannelPointsMessage.getUserId(),
            userName = twitchChannelPointsMessage.getUserName()
        )

        if startNewTriviaGameAction is None:
            return

        self.__triviaGameMachine.submitAction(startNewTriviaGameAction)

        self.__timber.log('TriviaGameRedemption', f'Redeemed trivia game for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchChannel.getTwitchChannelName()}')
        return True
