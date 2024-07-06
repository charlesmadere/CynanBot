from .absCheerAction import AbsCheerAction
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from ..misc import utils as utils


class SoundAlertCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        directory: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            isEnable = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__directory: str = directory

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.SOUND_ALERT

    @property
    def directory(self) -> str:
        return self.__directory
