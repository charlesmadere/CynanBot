from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.cheerActions.wizards.absWizard import AbsWizard
from CynanBot.cheerActions.wizards.soundAlertSteps import SoundAlertSteps


class SoundAlertWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps = SoundAlertSteps()
        self.__bits: int | None = None
        self.__tag: str | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.SOUND_ALERT

    def getSteps(self) -> SoundAlertSteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__tag=}'

    def requireBits(self) -> int:
        bits = self.__bits

        if bits is None:
            raise ValueError(f'bits value has not been set: ({self=})')

        return bits

    def requireTag(self) -> str:
        tag = self.__tag

        if tag is None:
            raise ValueError(f'tag value has not been set: ({self=})')

        return tag

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def setBits(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits = bits

    def setTag(self, tag: str):
        if not utils.isValidStr(tag):
            raise TypeError(f'tag argument is malformed: \"{tag}\"')

        self.__tag = tag

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'steps': self.__steps,
            'tag': self.__tag,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
