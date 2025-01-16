from typing import Any

from frozendict import frozendict

from ..soundAlertRedemption import SoundAlertRedemption
from ..soundAlertRedemptionJsonParserInterface import SoundAlertRedemptionJsonParserInterface


class StubSoundAlertRedemptionJsonParser(SoundAlertRedemptionJsonParserInterface):

    def parseRedemption(
        self,
        jsonContents: dict[str, Any]
    ) -> SoundAlertRedemption:
        # this method is intentionally empty
        raise RuntimeError('Not implemented')

    def parseRedemptions(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, SoundAlertRedemption] | None:
        # this method is intentionally empty
        return None
