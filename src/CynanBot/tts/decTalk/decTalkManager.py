import CynanBot.misc.utils as utils
from CynanBot.systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.decTalk.decTalkCommandBuilder import DecTalkCommandBuilder
from CynanBot.tts.decTalk.decTalkFileManagerInterface import \
    DecTalkFileManagerInterface
from CynanBot.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface


class DecTalkManager(TtsManagerInterface):

    def __init__(
        self,
        decTalkCommandBuilder: DecTalkCommandBuilder,
        decTalkFileManager: DecTalkFileManagerInterface,
        systemCommandHelper: SystemCommandHelperInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(decTalkCommandBuilder, DecTalkCommandBuilder):
            raise TypeError(f'decTalkCommandBuilder argument is malformed: \"{decTalkCommandBuilder}\"')
        elif not isinstance(decTalkFileManager, DecTalkFileManagerInterface):
            raise TypeError(f'decTalkFileManager argument is malformed: \"{decTalkFileManager}\"')
        elif not isinstance(systemCommandHelper, SystemCommandHelperInterface):
            raise TypeError(f'systemCommandHelper argument is malformed: \"{systemCommandHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__decTalkFileManager: DecTalkFileManagerInterface = decTalkFileManager
        self.__systemCommandHelper: SystemCommandHelperInterface = systemCommandHelper
        self.__timber: TimberInterface = timber
        self.__decTalkCommandBuilder: TtsCommandBuilderInterface = decTalkCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

    async def processTtsEvent(self, event: TtsEvent):
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isTtsEnabled():
            return

        command = await self.__decTalkCommandBuilder.buildAndCleanEvent(event)

        if not utils.isValidStr(command):
            self.__timber.log('DecTalkManager', f'Failed to parse TTS message in \"{event.getTwitchChannel()}\" into a valid command: \"{event}\"')
            return

        fileName = await self.__decTalkFileManager.writeCommandToNewFile(command)

        if not utils.isValidStr(fileName):
            self.__timber.log('DecTalkManager', f'Failed to write TTS message in \"{event.getTwitchChannel()}\" to temporary file ({command=})')
            return

        self.__timber.log('DecTalkManager', f'Executing TTS message in \"{event.getTwitchChannel()}\"...')
        pathToDecTalk = utils.cleanPath(await self.__ttsSettingsRepository.requireDecTalkPath())

        await self.__systemCommandHelper.executeCommand(
            command = f'{pathToDecTalk} -pre \"[:phone on]\" < \"{fileName}\"',
            timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()
        )

        await self.__decTalkFileManager.deleteFile(fileName)
