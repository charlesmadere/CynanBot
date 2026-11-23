from asyncio import AbstractEventLoop
from typing import Final

from .pygameMediaPlayerManager import PygameMediaPlayerManager
from ..provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..settings.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...pygame.pygameInitializerInterface import PygameInitializerInterface
from ...timber.timberInterface import TimberInterface


class PygameSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        pygameInitializer: PygameInitializerInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(pygameInitializer, PygameInitializerInterface):
            raise TypeError(f'pygameInitializer argument is malformed: \"{pygameInitializer}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__pygameInitializer: Final[PygameInitializerInterface] = pygameInitializer
        self.__soundPlayerSettingsRepository: Final[SoundPlayerSettingsRepositoryInterface] = soundPlayerSettingsRepository
        self.__timber: Final[TimberInterface] = timber

        self.__soundPlayerManager: PygameMediaPlayerManager | None = None

    def constructNewInstance(self) -> PygameMediaPlayerManager:
        return PygameMediaPlayerManager(
            eventLoop = self.__eventLoop,
            pygameInitializer = self.__pygameInitializer,
            soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
            timber = self.__timber,
        )

    def getSharedInstance(self) -> PygameMediaPlayerManager:
        soundPlayerManager = self.__soundPlayerManager

        if soundPlayerManager is None:
            soundPlayerManager = self.constructNewInstance()
            self.__soundPlayerManager = soundPlayerManager

        return soundPlayerManager
