import pytest

from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement


class TestCheerActionStreamStatusRequirement():

    def test_fromStr_withAnyString(self):
        result = CheerActionStreamStatusRequirement.fromStr('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    def test_fromStr_withEmptyString(self):
        result = CheerActionStreamStatusRequirement.fromStr('')
        assert result is CheerActionStreamStatusRequirement.ANY

    def test_fromStr_withHelloWorldString(self):
        result: CheerActionStreamStatusRequirement | None = None

        with pytest.raises(ValueError):
            result = CheerActionStreamStatusRequirement.fromStr('Hello, World!')

        assert result is None

    def test_fromStr_withNone(self):
        result = CheerActionStreamStatusRequirement.fromStr(None)
        assert result is CheerActionStreamStatusRequirement.ANY

    def test_fromStr_withOfflineString(self):
        result = CheerActionStreamStatusRequirement.fromStr('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    def test_fromStr_withOnlineString(self):
        result = CheerActionStreamStatusRequirement.fromStr('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    def test_fromStr_withWhitespaceString(self):
        result = CheerActionStreamStatusRequirement.fromStr(' ')
        assert result is CheerActionStreamStatusRequirement.ANY

    def test_getDatabaseString_withAny(self):
        string = CheerActionStreamStatusRequirement.ANY.getDatabaseString()
        assert string == 'any'

    def test_getDatabaseString_withOfflineline(self):
        string = CheerActionStreamStatusRequirement.OFFLINE.getDatabaseString()
        assert string == 'offline'

    def test_getDatabaseString_withOnline(self):
        string = CheerActionStreamStatusRequirement.ONLINE.getDatabaseString()
        assert string == 'online'
