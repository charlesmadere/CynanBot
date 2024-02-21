import traceback
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBot.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
from CynanBot.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from CynanBot.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from CynanBot.users.pkmnCatchType import PkmnCatchType
from CynanBot.users.user import User


class CutenessRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

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


class PkmnBattleRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(funtoonRepository, FuntoonRepositoryInterface), f"malformed {funtoonRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

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


class PkmnCatchRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(funtoonRepository, FuntoonRepositoryInterface), f"malformed {funtoonRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()

        if not isinstance(twitchUser, User):
            # dumb hack, idk what to do about this for now. regardless this should never ever
            # happen under the current codebase
            self.__timber.log('PkmnCatchRedemption', f'Received a UserInterface instance that was not a User instance: \"{twitchUser}\"')
            return False
        elif not twitchUser.isPkmnEnabled() or not twitchUser.hasPkmnCatchBoosterPacks():
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
        assert isinstance(pkmnCatchBoosterPack, PkmnCatchBoosterPack), f"malformed {pkmnCatchBoosterPack=}"

        if pkmnCatchBoosterPack.getCatchType() is PkmnCatchType.NORMAL:
            return FuntoonPkmnCatchType.NORMAL
        elif pkmnCatchBoosterPack.getCatchType() is PkmnCatchType.GREAT:
            return FuntoonPkmnCatchType.GREAT
        elif pkmnCatchBoosterPack.getCatchType() is PkmnCatchType.ULTRA:
            return FuntoonPkmnCatchType.ULTRA
        else:
            raise ValueError(f'unknown PkmnCatchType: \"{pkmnCatchBoosterPack.getCatchType()}\"')


class PkmnEvolveRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(funtoonRepository, FuntoonRepositoryInterface), f"malformed {funtoonRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

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


class PkmnShinyRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        funtoonRepository: FuntoonRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(funtoonRepository, FuntoonRepositoryInterface), f"malformed {funtoonRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__funtoonRepository: FuntoonRepositoryInterface = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

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


class SuperTriviaGameRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameBuilder, TriviaGameBuilderInterface), f"malformed {triviaGameBuilder=}"
        assert isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"

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
            return False

        self.__triviaGameMachine.submitAction(startNewSuperTriviaGameAction)

        self.__timber.log('TriviaGameRedemption', f'Redeemed super trivia game for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchChannel.getTwitchChannelName()}')
        return True


class TriviaGameRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameBuilder, TriviaGameBuilderInterface), f"malformed {triviaGameBuilder=}"
        assert isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"

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
            return False

        self.__triviaGameMachine.submitAction(startNewTriviaGameAction)

        self.__timber.log('TriviaGameRedemption', f'Redeemed trivia game for {twitchChannelPointsMessage.getUserName()}:{twitchChannelPointsMessage.getUserId()} in {twitchChannel.getTwitchChannelName()}')
        return True
