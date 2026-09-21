from typing import Final

import pygame

from .pygameInitializerInterface import PygameInitializerInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class PygameInitializer(PygameInitializerInterface):

    def __init__(
        self,
        timber: TimberInterface,
        channelCount: int = 128,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(channelCount):
            raise TypeError(f'channelCount argument is malformed: \"{channelCount}\"')
        elif channelCount < 8 or channelCount > utils.getShortMaxSafeSize():
            raise ValueError(f'channelCount argument is out of bounds: {channelCount}')

        self.__timber: Final[TimberInterface] = timber
        self.__channelCount: Final[int] = channelCount

        self.__isInitialized: bool = False

    def start(self):
        if self.__isInitialized:
            return

        self.__timber.log('PygameInitializer', f'Pygame is initializing...')
        pygame.mixer.init()
        pygame.mixer.set_num_channels(self.__channelCount)
        self.__timber.log('PygameInitializer', f'Finished initializing pygame')
