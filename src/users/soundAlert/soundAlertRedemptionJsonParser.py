from typing import Any

from frozendict import frozendict

from .soundAlertRedemption import SoundAlertRedemption
from .soundAlertRedemptionJsonParserInterface import SoundAlertRedemptionJsonParserInterface
from ...misc import utils as utils
from ...soundPlayerManager.jsonMapper.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface


class SoundAlertRedemptionJsonParser(SoundAlertRedemptionJsonParserInterface):

    def __init__(
        self,
        soundAlertJsonMapper: SoundAlertJsonMapperInterface
    ):
        if not isinstance(soundAlertJsonMapper, SoundAlertJsonMapperInterface):
            raise TypeError(f'soundAlertJsonMapper argument is malformed: \"{soundAlertJsonMapper}\"')

        self.__soundAlertJsonMapper: SoundAlertJsonMapperInterface = soundAlertJsonMapper

    def parseRedemption(
        self,
        jsonContents: dict[str, Any]
    ) -> SoundAlertRedemption:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        isImmediate = utils.getBoolFromDict(jsonContents, 'isImmediate', False)

        soundAlertString = utils.getStrFromDict(jsonContents, 'soundAlert', '')
        soundAlert = self.__soundAlertJsonMapper.requireSoundAlert(soundAlertString)

        directoryPath: str | None = None
        if 'directoryPath' in jsonContents and utils.isValidStr(jsonContents.get('directoryPath')):
            directoryPath = utils.getStrFromDict(jsonContents, 'directoryPath')

        rewardId = utils.getStrFromDict(jsonContents, 'rewardId')

        return SoundAlertRedemption(
            isImmediate = isImmediate,
            soundAlert = soundAlert,
            directoryPath = directoryPath,
            rewardId = rewardId
        )

    def parseRedemptions(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, SoundAlertRedemption] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        redemptions: dict[str, SoundAlertRedemption] = dict()

        for redemptionJson in jsonContents:
            soundRedemption = self.parseRedemption(redemptionJson)
            redemptions[soundRedemption.rewardId] = soundRedemption

        return frozendict(redemptions)
