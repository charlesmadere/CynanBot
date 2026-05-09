import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.pixelsDice.listeners.pixelsDiceEventListener import PixelsDiceEventListener
from src.pixelsDice.machine.pixelsDiceMachine import PixelsDiceMachine
from src.pixelsDice.machine.pixelsDiceMachineInterface import PixelsDiceMachineInterface
from src.pixelsDice.mappers.pixelsDiceStateMapper import PixelsDiceStateMapper
from src.pixelsDice.mappers.pixelsDiceStateMapperInterface import PixelsDiceStateMapperInterface
from src.pixelsDice.models.events.absPixelsDiceEvent import AbsPixelsDiceEvent
from src.pixelsDice.settings.pixelsDiceSettings import PixelsDiceSettings
from src.pixelsDice.settings.pixelsDiceSettingsInterface import PixelsDiceSettingsInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub

eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = BackgroundTaskHelper(
    eventLoop = eventLoop,
)

timber: Final[TimberInterface] = TimberStub()

pixelsDiceStateMapper: Final[PixelsDiceStateMapperInterface] = PixelsDiceStateMapper()

pixelsDiceSettings: Final[PixelsDiceSettingsInterface] = PixelsDiceSettings(
    settingsJsonReader = JsonStaticReader(
        jsonContents = {
            'diceName': 'Dice Boi',
        },
    ),
)

class PixelsDiceEventHandler(PixelsDiceEventListener):

    async def onNewPixelsDiceEvent(self, event: AbsPixelsDiceEvent):
        print(event)

pixelsDiceEventListener: Final[PixelsDiceEventListener] = PixelsDiceEventHandler()

pixelsDiceMachine: Final[PixelsDiceMachineInterface] = PixelsDiceMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    pixelsDiceEventListener = pixelsDiceEventListener,
    pixelsDiceSettings = pixelsDiceSettings,
    pixelsDiceStateMapper = pixelsDiceStateMapper,
    timber = timber,
)

async def main():
    pass

    try:
        pixelsDiceMachine.start()
        await asyncio.sleep(30)
    except Exception as e:
        print(f'exception: {e}')

    pass

asyncio.run(main())
