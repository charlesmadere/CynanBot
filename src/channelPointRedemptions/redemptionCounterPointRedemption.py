import traceback
from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..redemptionCounter.exceptions import RedemptionCounterNoSuchUserException, RedemptionCounterIsDisabledException
from ..redemptionCounter.helpers.redemptionCounterHelperInterface import RedemptionCounterHelperInterface
from ..redemptionCounter.settings.redemptionCounterSettingsInterface import RedemptionCounterSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class RedemptionCounterPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        redemptionCounterHelper: RedemptionCounterHelperInterface,
        redemptionCounterSettings: RedemptionCounterSettingsInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(redemptionCounterHelper, RedemptionCounterHelperInterface):
            raise TypeError(f'redemptionCounterHelper argument is malformed: \"{redemptionCounterHelper}\"')
        elif not isinstance(redemptionCounterSettings, RedemptionCounterSettingsInterface):
            raise TypeError(f'redemptionCounterSettings argument is malformed: \"{redemptionCounterSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__redemptionCounterHelper: Final[RedemptionCounterHelperInterface] = redemptionCounterHelper
        self.__redemptionCounterSettings: Final[RedemptionCounterSettingsInterface] = redemptionCounterSettings
        self.__timber: Final[TimberInterface] = timber
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.areRedemptionCountersEnabled:
            return False

        boosterPacks = twitchUser.redemptionCounterBoosterPacks
        if boosterPacks is None or len(boosterPacks) == 0:
            return False

        boosterPack = boosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if boosterPack is None:
            return False

        try:
            result = await self.__redemptionCounterHelper.increment(
                incrementAmount = boosterPack.incrementAmount,
                chatterUserId = twitchChannelPointsMessage.userId,
                counterName = boosterPack.counterName,
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId
            )
        except RedemptionCounterIsDisabledException as e:
            self.__timber.log('RedemptionCounterPointRedemption', f'Redemption Counter feature is currently disabled ({twitchChannelPointsMessage=}): {e}', e, traceback.format_exc())
            return True
        except RedemptionCounterNoSuchUserException as e:
            self.__timber.log('RedemptionCounterPointRedemption', f'Unable to find the user of the given user ID ({twitchChannelPointsMessage=}): {e}', e, traceback.format_exc())
            return True

        prefixEmote = await self.__trollmojiHelper.getDinkDonkEmote()
        if not utils.isValidStr(prefixEmote):
            prefixEmote = 'ⓘ'

        suffixEmote = ''
        if utils.isValidStr(boosterPack.emote):
            suffixEmote = boosterPack.emote

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{prefixEmote} @{twitchChannelPointsMessage.userName} has a new {result.counterName} count of {result.countStr}! {suffixEmote}'
        )

        self.__timber.log('RedemptionCounterPointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
