import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.users.pkmn.pkmnCatchType import PkmnCatchType
from src.users.pkmn.pkmnCatchTypeJsonMapper import PkmnCatchTypeJsonMapper
from src.users.pkmn.pkmnCatchTypeJsonMapperInterface import PkmnCatchTypeJsonMapperInterface


class TestPkmnCatchTypeJsonMapper:

    timber: TimberInterface = TimberStub()

    jsonMapper: PkmnCatchTypeJsonMapperInterface = PkmnCatchTypeJsonMapper(
        timber = timber
    )

    def test_parse_withEmptyString(self):
        result = self.jsonMapper.parse('')
        assert result is None

    def test_parse_withGreat(self):
        result = self.jsonMapper.parse('great')
        assert result is PkmnCatchType.GREAT

    def test_parse_withNone(self):
        result = self.jsonMapper.parse(None)
        assert result is None

    def test_parse_withNormal(self):
        result = self.jsonMapper.parse('normal')
        assert result is PkmnCatchType.NORMAL

    def test_parse_withUltra(self):
        result = self.jsonMapper.parse('ultra')
        assert result is PkmnCatchType.ULTRA

    def test_parse_withWhitespaceString(self):
        result = self.jsonMapper.parse(' ')
        assert result is None

    def test_require_withEmptyString(self):
        result: PkmnCatchType | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.require('')

        assert result is None

    def test_require_withGreat(self):
        result = self.jsonMapper.require('great')
        assert result is PkmnCatchType.GREAT

    def test_require_withNone(self):
        result: PkmnCatchType | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.require(None)

        assert result is None

    def test_require_withNormal(self):
        result = self.jsonMapper.require('normal')
        assert result is PkmnCatchType.NORMAL

    def test_require_withUltra(self):
        result = self.jsonMapper.require('ultra')
        assert result is PkmnCatchType.ULTRA

    def test_require_withWhitespaceString(self):
        result: PkmnCatchType | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.require(' ')

        assert result is None
