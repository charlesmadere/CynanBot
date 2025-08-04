import pytest

from src.aniv.models.whichAnivUser import WhichAnivUser
from src.users.aniv.anivUserSettingsJsonParser import AnivUserSettingsJsonParser
from src.users.aniv.anivUserSettingsJsonParserInterface import AnivUserSettingsJsonParserInterface


class TestAnivUserSettingsJsonParser:

    parser: AnivUserSettingsJsonParserInterface = AnivUserSettingsJsonParser()

    def test_parseWhichAnivUser_withAcac(self):
        result = self.parser.parseWhichAnivUser('acac')
        assert result is WhichAnivUser.ACAC

    def test_parseWhichAnivUser_withAneev(self):
        result = self.parser.parseWhichAnivUser('aneev')
        assert result is WhichAnivUser.ANEEV

    def test_parseWhichAnivUser_withAniv(self):
        result = self.parser.parseWhichAnivUser('aniv')
        assert result is WhichAnivUser.ANIV

    def test_parseWhichAnivUser_withEmptyString(self):
        result = self.parser.parseWhichAnivUser('')
        assert result is None

    def test_parseWhichAnivUser_withNone(self):
        result = self.parser.parseWhichAnivUser(None)
        assert result is None

    def test_parseWhichAnivUser_withWhitespaceString(self):
        result = self.parser.parseWhichAnivUser(' ')
        assert result is None

    def test_requireWhichAnivUser_withAcac(self):
        result = self.parser.requireWhichAnivUser('acac')
        assert result is WhichAnivUser.ACAC

    def test_requireWhichAnivUser_withAneev(self):
        result = self.parser.requireWhichAnivUser('aneev')
        assert result is WhichAnivUser.ANEEV

    def test_requireWhichAnivUser_withAniv(self):
        result = self.parser.requireWhichAnivUser('aniv')
        assert result is WhichAnivUser.ANIV

    def test_requireWhichAnivUser_withEmptyString(self):
        result: WhichAnivUser | None = None

        with pytest.raises(ValueError):
            result = self.parser.requireWhichAnivUser('')

        assert result is None

    def test_requireWhichAnivUser_withNone(self):
        result: WhichAnivUser | None = None

        with pytest.raises(ValueError):
            result = self.parser.requireWhichAnivUser(None)

        assert result is None

    def test_requireWhichAnivUser_withWhitespaceString(self):
        result: WhichAnivUser | None = None

        with pytest.raises(ValueError):
            result = self.parser.requireWhichAnivUser(' ')

        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, AnivUserSettingsJsonParser)
        assert isinstance(self.parser, AnivUserSettingsJsonParserInterface)
