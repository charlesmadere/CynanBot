from typing import Final

from .ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsCheerDonation import TtsCheerDonation
from ..models.ttsDonationType import TtsDonationType
from ..models.ttsEvent import TtsEvent
from ..models.ttsSubscriptionDonation import TtsSubscriptionDonation
from ...misc import utils as utils
from ...nickName.helpers.nickNameHelperInterface import NickNameHelperInterface


class TtsCommandBuilder(TtsCommandBuilderInterface):

    def __init__(
        self,
        nickNameHelper: NickNameHelperInterface,
    ):
        if not isinstance(nickNameHelper, NickNameHelperInterface):
            raise TypeError(f'nickNameHelper argument is malformed: \"{nickNameHelper}\"')

        self.__nickNameHelper: Final[NickNameHelperInterface] = nickNameHelper

    async def buildDonationPrefix(self, event: TtsEvent | None) -> str | None:
        if event is None:
            return None
        elif not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        donationPrefix = await self.__processDonationPrefix(
            event = event,
        )

        if not utils.isValidStr(donationPrefix):
            return None

        return donationPrefix

    async def __fetchEventUserName(
        self,
        event: TtsEvent,
    ) -> str:
        nickNameData = await self.__nickNameHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if nickNameData is not None and utils.isValidStr(nickNameData.nickName):
            return nickNameData.nickName
        else:
            return event.userName

    async def __processCheerDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsCheerDonation,
    ) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(donation, TtsCheerDonation) or donation.donationType is not TtsDonationType.CHEER:
            raise TypeError(f'donation argument is malformed: \"{donation}\"')

        eventUserName = await self.__fetchEventUserName(
            event = event,
        )

        return f'{eventUserName} cheered {donation.bits}!'

    async def __processDonationPrefix(self, event: TtsEvent) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        donation = event.donation

        if donation is None:
            return None

        elif isinstance(donation, TtsCheerDonation):
            return await self.__processCheerDonationPrefix(
                event = event,
                donation = donation,
            )

        elif isinstance(donation, TtsSubscriptionDonation):
            return await self.__processSubscriptionDonationPrefix(
                event = event,
                donation = donation,
            )

        else:
            raise RuntimeError(f'donation type is unknown: \"{type(donation)=}\"')

    async def __processSubscriptionDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsSubscriptionDonation,
    ) -> str:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(donation, TtsSubscriptionDonation) or donation.donationType is not TtsDonationType.SUBSCRIPTION:
            raise TypeError(f'donation argument is malformed: \"{donation}\"')

        eventUserName = await self.__fetchEventUserName(
            event = event,
        )

        numberOfGiftedSubs = donation.numberOfGiftedSubs

        if numberOfGiftedSubs is not None and numberOfGiftedSubs >= 1:
            subsPlurality: str

            if numberOfGiftedSubs == 1:
                subsPlurality = 'sub'
            else:
                subsPlurality = 'subs'

            if donation.isAnonymous:
                return f'anonymous gifted {numberOfGiftedSubs} {subsPlurality}!'
            else:
                return f'{eventUserName} gifted {numberOfGiftedSubs} {subsPlurality}!'
        else:
            return f'{eventUserName} subscribed!'
