from .ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsCheerDonation import TtsCheerDonation
from ..models.ttsDonationType import TtsDonationType
from ..models.ttsEvent import TtsEvent
from ..models.ttsSubscriptionDonation import TtsSubscriptionDonation
from ...misc import utils as utils


class TtsCommandBuilder(TtsCommandBuilderInterface):

    async def buildDonationPrefix(self, event: TtsEvent | None) -> str | None:
        if event is not None and not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if event is None:
            return None

        donationPrefix = await self.__processDonationPrefix(event)
        if not utils.isValidStr(donationPrefix):
            return None

        return donationPrefix

    async def __processCheerDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsCheerDonation,
    ) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(donation, TtsCheerDonation):
            raise TypeError(f'donation argument is malformed: \"{donation}\"')
        elif donation.donationType is not TtsDonationType.CHEER:
            raise TypeError(f'TtsDonationType is not {TtsDonationType.CHEER}: \"{donation.donationType}\" ({donation=})')

        return f'{event.userName} cheered {donation.bits}!'

    async def __processDonationPrefix(self, event: TtsEvent) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        donation = event.donation

        if donation is None:
            return None

        if isinstance(donation, TtsCheerDonation):
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
        elif donation.donationType is not TtsDonationType.SUBSCRIPTION:
            raise TypeError(f'TtsDonationType is not {TtsDonationType.SUBSCRIPTION}: \"{donation.donationType}\" ({donation=})')

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
                return f'{event.userName} gifted {numberOfGiftedSubs} {subsPlurality}!'
        else:
            return f'{event.userName} subscribed!'
