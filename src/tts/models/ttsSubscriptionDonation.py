import locale
from dataclasses import dataclass

from .ttsDonation import TtsDonation
from ...twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True, slots = True)
class TtsSubscriptionDonation(TtsDonation):
    isAnonymous: bool
    cumulativeMonths: int | None
    durationMonths: int | None
    numberOfGiftedSubs: int | None
    tier: TwitchSubscriberTier

    @property
    def numberOfGiftedSubsStr(self) -> str:
        numberOfGiftedSubs = self.requireNumberOfGiftedSubs()
        return locale.format_string("%d", numberOfGiftedSubs, grouping = True)

    def requireNumberOfGiftedSubs(self) -> int:
        numberOfGiftedSubs = self.numberOfGiftedSubs

        if numberOfGiftedSubs is None:
            raise RuntimeError(f'TtsSubscriptionDonation has no numberOfGiftedSubs value: ({self}) ({numberOfGiftedSubs=})')

        return numberOfGiftedSubs
