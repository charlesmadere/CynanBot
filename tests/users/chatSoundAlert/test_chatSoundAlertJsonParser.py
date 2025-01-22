from frozenlist import FrozenList

from src.soundPlayerManager.soundAlert import SoundAlert
from src.soundPlayerManager.jsonMapper.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.jsonMapper.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from src.users.chatSoundAlert.chatSoundAlertJsonParser import ChatSoundAlertJsonParser
from src.users.chatSoundAlert.chatSoundAlertJsonParserInterface import ChatSoundAlertJsonParserInterface
from src.users.chatSoundAlert.chatSoundAlertQualifier import ChatSoundAlertQualifer
from src.users.chatSoundAlert.chatSoundAlertType import ChatSoundAlertType
from src.users.chatSoundAlert.directoryPathChatSoundAlert import DirectoryPathChatSoundAlert
from src.users.chatSoundAlert.filePathChatSoundAlert import FilePathChatSoundAlert
from src.users.chatSoundAlert.soundAlertChatSoundAlert import SoundAlertChatSoundAlert


class TestChatSoundAlertJsonParser:

    soundAlertJsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper()

    jsonParser: ChatSoundAlertJsonParserInterface = ChatSoundAlertJsonParser(
        soundAlertJsonMapper = soundAlertJsonMapper
    )

    def test_parseAlertQualifier_withContainsString(self):
        result = self.jsonParser.parseAlertQualifier('contains')
        assert result is ChatSoundAlertQualifer.CONTAINS

    def test_parseAlertQualifier_withExactString(self):
        result = self.jsonParser.parseAlertQualifier('exact')
        assert result is ChatSoundAlertQualifer.EXACT

    def test_parseAlertType_withDirectoryPathString(self):
        result = self.jsonParser.parseAlertType('directory_path')
        assert result is ChatSoundAlertType.DIRECTORY_PATH

    def test_parseAlertType_withFilePathString(self):
        result = self.jsonParser.parseAlertType('file_path')
        assert result is ChatSoundAlertType.FILE_PATH

    def test_parseAlertType_withSoundAlertString(self):
        result = self.jsonParser.parseAlertType('sound_alert')
        assert result is ChatSoundAlertType.SOUND_ALERT

    def test_parseChatSoundAlert_withDirectoryPathChatSoundAlert(self):
        chatSoundAlert = DirectoryPathChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.CONTAINS,
            cooldownSeconds = None,
            volume = None,
            directoryPath = 'directoryPath',
            message = 'hello'
        )

        result = self.jsonParser.parseChatSoundAlert({
            'alertType': chatSoundAlert.alertType.name.lower(),
            'cooldownSeconds': chatSoundAlert.cooldownSeconds,
            'directoryPath': chatSoundAlert.directoryPath,
            'message': chatSoundAlert.message,
            'qualifier': chatSoundAlert.qualifier.name.lower(),
            'volume': chatSoundAlert.volume
        })

        assert isinstance(result, DirectoryPathChatSoundAlert)
        assert result.alertType is chatSoundAlert.alertType
        assert result.cooldownSeconds == chatSoundAlert.cooldownSeconds
        assert result.directoryPath == chatSoundAlert.directoryPath
        assert result.message == chatSoundAlert.message
        assert result.qualifier is chatSoundAlert.qualifier

    def test_parseChatSoundAlert_withFilePathChatSoundAlert(self):
        chatSoundAlert = FilePathChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.EXACT,
            cooldownSeconds = None,
            volume = None,
            filePath = 'filePath',
            message = 'hello'
        )

        result = self.jsonParser.parseChatSoundAlert({
            'alertType': chatSoundAlert.alertType.name.lower(),
            'cooldownSeconds': chatSoundAlert.cooldownSeconds,
            'filePath': chatSoundAlert.filePath,
            'message': chatSoundAlert.message,
            'qualifier': chatSoundAlert.qualifier.name.lower(),
            'volume': chatSoundAlert.volume
        })

        assert isinstance(result, FilePathChatSoundAlert)
        assert result.alertType is chatSoundAlert.alertType
        assert result.cooldownSeconds == chatSoundAlert.cooldownSeconds
        assert result.filePath == chatSoundAlert.filePath
        assert result.message == chatSoundAlert.message
        assert result.qualifier is chatSoundAlert.qualifier
        assert result.volume == chatSoundAlert.volume

    def test_parseChatSoundAlert_withSoundAlertChatSoundAlert(self):
        chatSoundAlert = SoundAlertChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.CONTAINS,
            cooldownSeconds = None,
            volume = None,
            soundAlert = SoundAlert.GRENADE_1,
            message = 'hello'
        )

        result = self.jsonParser.parseChatSoundAlert({
            'alertType': chatSoundAlert.alertType.name.lower(),
            'cooldownSeconds': chatSoundAlert.cooldownSeconds,
            'message': chatSoundAlert.message,
            'qualifier': chatSoundAlert.qualifier.name.lower(),
            'soundAlert': self.soundAlertJsonMapper.serializeSoundAlert(chatSoundAlert.soundAlert),
            'volume': chatSoundAlert.volume,
        })

        assert isinstance(result, SoundAlertChatSoundAlert)
        assert result.alertType is chatSoundAlert.alertType
        assert result.cooldownSeconds == chatSoundAlert.cooldownSeconds
        assert result.message == chatSoundAlert.message
        assert result.qualifier is chatSoundAlert.qualifier
        assert result.soundAlert == chatSoundAlert.soundAlert

    def test_parseChatSoundAlerts(self):
        contains = FilePathChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.CONTAINS,
            cooldownSeconds = None,
            volume = 100,
            filePath = 'world.mp3',
            message = 'world'
        )

        exact = FilePathChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.EXACT,
            cooldownSeconds = None,
            volume = None,
            filePath = 'hello.mp3',
            message = 'hello'
        )

        # This method is intended to output the results list in a particular order (alerts with
        # the EXACT qualifier should be sorted to the front).
        results = self.jsonParser.parseChatSoundAlerts([
            {
                'alertType': contains.alertType.name.lower(),
                'qualifier': contains.qualifier.name.lower(),
                'filePath': contains.filePath,
                'message': contains.message,
                'volume': contains.volume
            },
            {
                'alertType': exact.alertType.name.lower(),
                'qualifier': exact.qualifier.name.lower(),
                'filePath': exact.filePath,
                'message': exact.message,
                'volume': exact.volume
            }
        ])

        assert isinstance(results, FrozenList)
        assert results.frozen
        assert len(results) == 2

        element = results[0]
        assert isinstance(element, FilePathChatSoundAlert)
        assert element.alertType is exact.alertType
        assert element.cooldownSeconds == exact.cooldownSeconds
        assert element.filePath == exact.filePath
        assert element.message == exact.message
        assert element.qualifier is exact.qualifier
        assert element.volume == exact.volume

        element = results[1]
        assert isinstance(element, FilePathChatSoundAlert)
        assert element.alertType is contains.alertType
        assert element.cooldownSeconds == exact.cooldownSeconds
        assert element.filePath == contains.filePath
        assert element.message == contains.message
        assert element.qualifier is contains.qualifier
        assert element.volume == contains.volume

    def test_sanity(self):
        assert self.jsonParser is not None
        assert isinstance(self.jsonParser, ChatSoundAlertJsonParser)
        assert isinstance(self.jsonParser, ChatSoundAlertJsonParserInterface)
