from typing import Final

from .tm36SpecialEffectUseCaseInterface import Tm36SpecialEffectUseCaseInterface
from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ..models.useChatterItemAction import UseChatterItemAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...misc.randomUtilsInterface import RandomUtilsInterface
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface


class Tm36SpecialEffectUseCase(Tm36SpecialEffectUseCaseInterface):

    def __init__(
        self,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        randomUtils: RandomUtilsInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        dudSpecialEffectChance: float = 0.12,
    ):
        if not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not utils.isValidNum(dudSpecialEffectChance):
            raise TypeError(f'dudSpecialEffectChance argument is malformed: \"{dudSpecialEffectChance}\"')

        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils
        self.__timber: Final[TimberInterface] = timber
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__dudSpecialEffectChance: Final[float] = dudSpecialEffectChance

    async def invoke(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> Tm36SpecialEffectUseCaseInterface.AbsSpecialEffect:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(action, UseChatterItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        itemDetails = await self.__chatterInventorySettings.getTm36ItemDetails()

        if not itemDetails.dudSpecialEffectEnabled:
            return Tm36SpecialEffectUseCaseInterface.NoSpecialEffect()

        randomNumber = self.__randomUtils.float()

        if randomNumber > self.__dudSpecialEffectChance:
            return Tm36SpecialEffectUseCaseInterface.NoSpecialEffect()

        updatedInventory: ChatterInventoryData | None = None

        if not action.ignoreInventory:
            updatedInventory = await self.__chatterInventoryRepository.update(
                itemType = ChatterItemType.TM_36,
                changeAmount = -1,
                chatterUserId = action.chatterUserId,
                twitchChannelId = action.twitchChannelId,
            )

        self.__timber.log('Tm36SpecialEffectUseCase', f'Rolled a dud ({updatedInventory=}) ({randomNumber=}) ({action=}) ({self.__dudSpecialEffectChance=})')

        return Tm36SpecialEffectUseCaseInterface.DudSpecialEffect(
            updatedInventory = updatedInventory,
            gottemEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup(),
        )
