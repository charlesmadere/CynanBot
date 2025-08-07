from src.aniv.mapper.anivJsonMapper import AnivJsonMapper
from src.aniv.mapper.anivJsonMapperInterface import AnivJsonMapperInterface
from src.aniv.models.whichAnivUser import WhichAnivUser


class TestAnivJsonMapper:

    mapper: AnivJsonMapperInterface = AnivJsonMapper()

    def test_parseWhichAnivUser_withAcacStrings(self):
        result = self.mapper.parseWhichAnivUser('acac')
        assert result is WhichAnivUser.ACAC

        result = self.mapper.parseWhichAnivUser('a_c_a_c')
        assert result is WhichAnivUser.ACAC

        result = self.mapper.parseWhichAnivUser('a-c-a-c')
        assert result is WhichAnivUser.ACAC

        result = self.mapper.parseWhichAnivUser('a c a c')
        assert result is WhichAnivUser.ACAC

    def test_parseWhichAnivUser_withAneevStrings(self):
        result = self.mapper.parseWhichAnivUser('aneev')
        assert result is WhichAnivUser.ANEEV

        result = self.mapper.parseWhichAnivUser('a_n_e_e_v')
        assert result is WhichAnivUser.ANEEV

        result = self.mapper.parseWhichAnivUser('a-n-e-e-v')
        assert result is WhichAnivUser.ANEEV

        result = self.mapper.parseWhichAnivUser('a n e e v')
        assert result is WhichAnivUser.ANEEV

    def test_parseWhichAnivUser_withAnivStrings(self):
        result = self.mapper.parseWhichAnivUser('aniv')
        assert result is WhichAnivUser.ANIV

        result = self.mapper.parseWhichAnivUser('a_n_i_v')
        assert result is WhichAnivUser.ANIV

        result = self.mapper.parseWhichAnivUser('a-n-i-v')
        assert result is WhichAnivUser.ANIV

        result = self.mapper.parseWhichAnivUser('a n i v')
        assert result is WhichAnivUser.ANIV

    def test_parseWhichAnivUser_withEmptyString(self):
        result = self.mapper.parseWhichAnivUser('')
        assert result is None

    def test_parseWhichAnivUser_withNone(self):
        result = self.mapper.parseWhichAnivUser(None)
        assert result is None

    def test_parseWhichAnivUser_withWhitespaceString(self):
        result = self.mapper.parseWhichAnivUser(' ')
        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, AnivJsonMapper)
        assert isinstance(self.mapper, AnivJsonMapperInterface)
