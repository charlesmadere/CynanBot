from frozenlist import FrozenList

from src.soundPlayerManager.soundAlert import SoundAlert
from src.soundPlayerManager.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
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
            directoryPath = 'directoryPath',
            message = 'hello',
            volume = None
        )

        result = self.jsonParser.parseChatSoundAlert({
            'alertType': chatSoundAlert.alertType.name.lower(),
            'qualifier': chatSoundAlert.qualifier.name.lower(),
            'directoryPath': chatSoundAlert.directoryPath,
            'message': chatSoundAlert.message
        })

        assert isinstance(result, DirectoryPathChatSoundAlert)
        assert result.alertType is chatSoundAlert.alertType
        assert result.directoryPath == chatSoundAlert.directoryPath
        assert result.message == chatSoundAlert.message
        assert result.qualifier is chatSoundAlert.qualifier

    def test_parseChatSoundAlert_withFilePathChatSoundAlert(self):
        chatSoundAlert = FilePathChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.EXACT,
            filePath = 'filePath',
            message = 'hello',
            volume = None
        )

        result = self.jsonParser.parseChatSoundAlert({
            'alertType': chatSoundAlert.alertType.name.lower(),
            'qualifier': chatSoundAlert.qualifier.name.lower(),
            'filePath': chatSoundAlert.filePath,
            'message': chatSoundAlert.message,
            'volume': chatSoundAlert.volume
        })

        assert isinstance(result, FilePathChatSoundAlert)
        assert result.alertType is chatSoundAlert.alertType
        assert result.filePath == chatSoundAlert.filePath
        assert result.message == chatSoundAlert.message
        assert result.volume == chatSoundAlert.volume
        assert result.qualifier is chatSoundAlert.qualifier

    def test_parseChatSoundAlert_withSoundAlertChatSoundAlert(self):
        chatSoundAlert = SoundAlertChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.CONTAINS,
            soundAlert = SoundAlert.TNT_1,
            message = 'hello',
            volume = None
        )

        result = self.jsonParser.parseChatSoundAlert({
            'alertType': chatSoundAlert.alertType.name.lower(),
            'qualifier': chatSoundAlert.qualifier.name.lower(),
            'message': chatSoundAlert.message,
            'soundAlert': self.soundAlertJsonMapper.serializeSoundAlert(chatSoundAlert.soundAlert)
        })

        assert isinstance(result, SoundAlertChatSoundAlert)
        assert result.alertType is chatSoundAlert.alertType
        assert result.message == chatSoundAlert.message
        assert result.qualifier is chatSoundAlert.qualifier
        assert result.soundAlert == chatSoundAlert.soundAlert

    def test_parseChatSoundAlerts(self):
        contains = FilePathChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.CONTAINS,
            filePath = 'world.mp3',
            message = 'world',
            volume = 100
        )

        exact = FilePathChatSoundAlert(
            qualifier = ChatSoundAlertQualifer.EXACT,
            filePath = 'hello.mp3',
            message = 'hello',
            volume = None
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
        assert element.qualifier is exact.qualifier
        assert element.filePath == exact.filePath
        assert element.message == exact.message
        assert element.volume == exact.volume

        element = results[1]
        assert isinstance(element, FilePathChatSoundAlert)
        assert element.alertType is contains.alertType
        assert element.qualifier is contains.qualifier
        assert element.filePath == contains.filePath
        assert element.message == contains.message
        assert element.volume == contains.volume

    def test_sanity(self):
        assert self.jsonParser is not None
        assert isinstance(self.jsonParser, ChatSoundAlertJsonParser)
        assert isinstance(self.jsonParser, ChatSoundAlertJsonParserInterface)
