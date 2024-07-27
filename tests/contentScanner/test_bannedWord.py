from src.contentScanner.bannedWord import BannedWord
from src.contentScanner.bannedWordType import BannedWordType


class TestBannedWord:

    def test_equals_withDifferentWords(self):
        one = BannedWord('cat')
        two = BannedWord('dog')
        assert one != two

    def test_equals_withSameWords(self):
        one = BannedWord('hello')
        two = BannedWord('hello')
        assert one == two

    def test_hash_withDifferentWords(self):
        one = BannedWord('cat')
        two = BannedWord('dog')
        assert hash(one) != hash(two)

    def test_hash_withSameWords(self):
        one = BannedWord('hello')
        two = BannedWord('hello')
        assert hash(one) == hash(two)

    def test_getType(self):
        word = BannedWord('hello')
        assert word.wordType is BannedWordType.EXACT_WORD
