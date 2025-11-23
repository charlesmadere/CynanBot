import pytest

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

    def test_parseWhichAnivUser_withAlbeeevStrings(self):
        result = self.mapper.parseWhichAnivUser('albeeev')
        assert result is WhichAnivUser.ALBEEEV

        result = self.mapper.parseWhichAnivUser('a_l_b_e_e_e_v')
        assert result is WhichAnivUser.ALBEEEV

        result = self.mapper.parseWhichAnivUser('a-l-b-e-e-e-v')
        assert result is WhichAnivUser.ALBEEEV

        result = self.mapper.parseWhichAnivUser('a l b e e e v')
        assert result is WhichAnivUser.ALBEEEV

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

    def test_requireWhichAnivUser_withAcacStrings(self):
        result = self.mapper.requireWhichAnivUser('acac')
        assert result is WhichAnivUser.ACAC

        result = self.mapper.requireWhichAnivUser('a_c_a_c')
        assert result is WhichAnivUser.ACAC

        result = self.mapper.requireWhichAnivUser('a-c-a-c')
        assert result is WhichAnivUser.ACAC

        result = self.mapper.requireWhichAnivUser('a c a c')
        assert result is WhichAnivUser.ACAC

    def test_requireWhichAnivUser_withAlbeeevStrings(self):
        result = self.mapper.requireWhichAnivUser('albeeev')
        assert result is WhichAnivUser.ALBEEEV

        result = self.mapper.requireWhichAnivUser('a_l_b_e_e_e_v')
        assert result is WhichAnivUser.ALBEEEV

        result = self.mapper.requireWhichAnivUser('a-l-b-e-e-e-v')
        assert result is WhichAnivUser.ALBEEEV

        result = self.mapper.requireWhichAnivUser('a l b e e e v')
        assert result is WhichAnivUser.ALBEEEV

    def test_requireWhichAnivUser_withAneevStrings(self):
        result = self.mapper.requireWhichAnivUser('aneev')
        assert result is WhichAnivUser.ANEEV

        result = self.mapper.requireWhichAnivUser('a_n_e_e_v')
        assert result is WhichAnivUser.ANEEV

        result = self.mapper.requireWhichAnivUser('a-n-e-e-v')
        assert result is WhichAnivUser.ANEEV

        result = self.mapper.requireWhichAnivUser('a n e e v')
        assert result is WhichAnivUser.ANEEV

    def test_requireWhichAnivUser_withAnivStrings(self):
        result = self.mapper.requireWhichAnivUser('aniv')
        assert result is WhichAnivUser.ANIV

        result = self.mapper.requireWhichAnivUser('a_n_i_v')
        assert result is WhichAnivUser.ANIV

        result = self.mapper.requireWhichAnivUser('a-n-i-v')
        assert result is WhichAnivUser.ANIV

        result = self.mapper.requireWhichAnivUser('a n i v')
        assert result is WhichAnivUser.ANIV

    def test_requireWhichAnivUser_withEmptyString(self):
        result: WhichAnivUser | None = None

        with pytest.raises(ValueError):
            result = self.mapper.requireWhichAnivUser('')

        assert result is None

    def test_requireWhichAnivUser_withNoneString(self):
        result: WhichAnivUser | None = None

        with pytest.raises(ValueError):
            result = self.mapper.requireWhichAnivUser(None)

        assert result is None

    def test_requireWhichAnivUser_withWhitespaceString(self):
        result: WhichAnivUser | None = None

        with pytest.raises(ValueError):
            result = self.mapper.requireWhichAnivUser(' ')

        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, AnivJsonMapper)
        assert isinstance(self.mapper, AnivJsonMapperInterface)
