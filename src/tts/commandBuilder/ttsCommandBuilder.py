from typing import Final

from .ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsCheerDonation import TtsCheerDonation
from ..models.ttsEvent import TtsEvent
from ..models.ttsSubscriptionDonation import TtsSubscriptionDonation
from ...chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ...misc import utils as utils


class TtsCommandBuilder(TtsCommandBuilderInterface):

    def __init__(
        self,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface,
    ):
        if not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')

        self.__chatterPreferredNameHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper

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
        preferredNameData = await self.__chatterPreferredNameHelper.get(
            chatterUserId = event.userId,
            twitchChannelId = event.twitchChannelId,
        )

        if preferredNameData is None:
            return event.userName
        else:
            return preferredNameData.preferredName

    async def __processCheerDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsCheerDonation,
    ) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(donation, TtsCheerDonation):
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
        elif not isinstance(donation, TtsSubscriptionDonation):
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
