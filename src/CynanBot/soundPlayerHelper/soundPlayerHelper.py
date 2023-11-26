from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface


class SoundPlayerHelper(SoundPlayerHelperInterface):

    def __init__(
        self,
        systemCommandHelper: SystemCommandHelperInterface
    ):
        if not isinstance(systemCommandHelper, SystemCommandHelperInterface):
            raise ValueError(f'systemCommandHelper argument is malformed: \"{systemCommandHelper}\"')

        self.__systemCommandHelper: SystemCommandHelperInterface = systemCommandHelper

    async def play(self, soundAlert: SoundAlert):
        if not isinstance(soundAlert, SoundAlert):
            raise ValueError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        # TODO
        pass
