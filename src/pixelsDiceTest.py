import asyncio
from asyncio import AbstractEventLoop

from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.pixelsDice.machine.pixelsDiceMachine import PixelsDiceMachine
from src.pixelsDice.mappers.pixelsDiceStateMapper import PixelsDiceStateMapper
from src.pixelsDice.mappers.pixelsDiceStateMapperInterface import PixelsDiceStateMapperInterface
from src.pixelsDice.pixelsDiceSettings import PixelsDiceSettings
from src.pixelsDice.pixelsDiceSettingsInterface import PixelsDiceSettingsInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop,
)

timber: TimberInterface = TimberStub()

pixelsDiceStateMapper: PixelsDiceStateMapperInterface = PixelsDiceStateMapper()

pixelsDiceSettings: PixelsDiceSettingsInterface = PixelsDiceSettings(
    settingsJsonReader = JsonStaticReader(
        jsonContents = {
            'diceName': 'Dice Boi',
        },
    ),
)

pixelsDiceMachine = PixelsDiceMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    pixelsDiceStateMapper = pixelsDiceStateMapper,
    pixelsDiceSettings = pixelsDiceSettings,
    timber = timber,
)

async def main():
    pass

    try:
        await pixelsDiceMachine.test()
        await asyncio.sleep(30)
    except Exception as e:
        print(f'exception: {e}')

    pass

asyncio.run(main())
