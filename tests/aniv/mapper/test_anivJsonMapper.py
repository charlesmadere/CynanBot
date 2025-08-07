from src.aniv.mapper.anivJsonMapper import AnivJsonMapper
from src.aniv.mapper.anivJsonMapperInterface import AnivJsonMapperInterface
from src.aniv.models.whichAnivUser import WhichAnivUser


class TestAnivJsonMapper:

    mapper: AnivJsonMapperInterface = AnivJsonMapper()

    def test_parseWhichAnivUser_withAnivStrings(self):
        result = self.mapper.parseWhichAnivUser('aniv')
        assert result is WhichAnivUser.ANIV

    def test_parseWhichAnivUser_withNone(self):
        result = self.mapper.parseWhichAnivUser(None)
        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, AnivJsonMapper)
        assert isinstance(self.mapper, AnivJsonMapperInterface)
