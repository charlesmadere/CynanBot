from typing import Collection, Final

import pygame
import pygame._sdl2.audio as PygameAudio

from .pygameAudioFrequency import PygameAudioFrequency
from .pygameInitializerInterface import PygameInitializerInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class PygameInitializer(PygameInitializerInterface):

    def __init__(
        self,
        timber: TimberInterface,
        channelCount: int = 128,
        audioFrequency: PygameAudioFrequency = PygameAudioFrequency.FORTY_EIGHT_KHZ,
        audioDeviceName: str | None = 'Motherboard Audio',
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(channelCount):
            raise TypeError(f'channelCount argument is malformed: \"{channelCount}\"')
        elif channelCount < 8 or channelCount > utils.getShortMaxSafeSize():
            raise ValueError(f'channelCount argument is out of bounds: {channelCount}')
        elif not isinstance(audioFrequency, PygameAudioFrequency):
            raise TypeError(f'audioFrequency argument is malformed: \"{audioFrequency}\"')
        elif audioDeviceName is not None and not isinstance(audioDeviceName, str):
            raise TypeError(f'audioDeviceName argument is malformed: \"{audioDeviceName}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__channelCount: Final[int] = channelCount
        self.__audioFrequency: Final[PygameAudioFrequency] = audioFrequency
        self.__audioDeviceName: Final[str | None] = audioDeviceName

        self.__isInitialized: bool = False

    def __initialize(self):
        pygame.mixer.pre_init(
            frequency = self.__audioFrequency.hzValue,
        )

        pygame.init()

        pygame.mixer.init(
            frequency = self.__audioFrequency.hzValue,
        )

        pygame.mixer.set_num_channels(self.__channelCount)

        audioDeviceName = self.__audioDeviceName
        if not utils.isValidStr(audioDeviceName):
            return

        allAudioDevices = PygameAudio.get_audio_device_names(iscapture = False)
        if not isinstance(allAudioDevices, Collection):
            self.__timber.log('PygameInitializer', f'Attempted set audio device, but none were returned by Pygame ({audioDeviceName=}) ({allAudioDevices=})')
            return

        audioDeviceIndex: int | None = None

        for index, currentAudioDeviceName in enumerate(allAudioDevices):
            if not utils.isValidStr(currentAudioDeviceName):
                continue
            elif currentAudioDeviceName == audioDeviceName:
                audioDeviceIndex = index
                break

        if not utils.isValidInt(audioDeviceIndex):
            self.__timber.log('PygameInitializer', f'Failed to find requested audio device ({audioDeviceIndex=}) ({audioDeviceName=}) ({allAudioDevices=})')
            return

        pygame.mixer.quit()

        pygame.mixer.init(
            devicename = audioDeviceName,
            frequency = self.__audioFrequency.hzValue,
        )

        self.__timber.log('PygameInitializer', f'Set requested audio device ({audioDeviceIndex=}) ({audioDeviceName=}) ({allAudioDevices=})')

    def start(self):
        if self.__isInitialized:
            self.__timber.log('PygameInitializer', 'Not initializing Pygame as it has already been initialized')
            return

        self.__isInitialized = True
        self.__timber.log('PygameInitializer', f'Pygame is initializing...')
        self.__initialize()
        self.__timber.log('PygameInitializer', f'Finished initializing Pygame ({self.__channelCount=}) ({self.__audioFrequency=}) ({self.__audioDeviceName=})')
