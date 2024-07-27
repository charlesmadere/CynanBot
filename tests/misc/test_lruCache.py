import pytest

from src.misc.lruCache import LruCache


class TestLruCache:

    def test_constructWithNegativeOneCapacity(self):
        with pytest.raises(ValueError):
            LruCache(-1)

    def test_constructWithOneCapacity(self):
        with pytest.raises(ValueError):
            LruCache(1)

    def test_constructWithThreeCapacity(self):
        lruCache = LruCache(3)

        assert isinstance(lruCache, LruCache)

    def test_constructWithTwoCapacity(self):
        lruCache = LruCache(2)

        assert isinstance(lruCache, LruCache)

    def test_constructWithZeroCapacity(self):
        with pytest.raises(ValueError):
            LruCache(0)

    def test_containsWhenEmptyIsFalse(self):
        lruCache = LruCache(3)
        assert lruCache.contains('hello') is False
        assert lruCache.contains('world') is False

    def test_contains(self):
        lruCache = LruCache(3)
        assert lruCache.contains('charmander') is False
        assert lruCache.contains('squirtle') is False
        assert lruCache.contains('bulbasaur') is False
        assert lruCache.contains('pikachu') is False
        assert lruCache.contains('mew') is False

        lruCache.put('charmander')
        assert lruCache.contains('charmander') is True
        assert lruCache.contains('squirtle') is False
        assert lruCache.contains('bulbasaur') is False
        assert lruCache.contains('pikachu') is False
        assert lruCache.contains('mew') is False

        lruCache.put('squirtle')
        assert lruCache.contains('charmander') is True
        assert lruCache.contains('squirtle') is True
        assert lruCache.contains('bulbasaur') is False
        assert lruCache.contains('pikachu') is False
        assert lruCache.contains('mew') is False

        lruCache.put('bulbasaur')
        assert lruCache.contains('charmander') is True
        assert lruCache.contains('squirtle') is True
        assert lruCache.contains('bulbasaur') is True
        assert lruCache.contains('pikachu') is False
        assert lruCache.contains('mew') is False

        lruCache.put('pikachu')
        assert lruCache.contains('charmander') is False
        assert lruCache.contains('squirtle') is True
        assert lruCache.contains('bulbasaur') is True
        assert lruCache.contains('pikachu') is True
        assert lruCache.contains('mew') is False

        lruCache.put('mew')
        assert lruCache.contains('charmander') is False
        assert lruCache.contains('squirtle') is False
        assert lruCache.contains('bulbasaur') is True
        assert lruCache.contains('pikachu') is True
        assert lruCache.contains('mew') is True

        lruCache.put('charmander')
        assert lruCache.contains('charmander') is True
        assert lruCache.contains('squirtle') is False
        assert lruCache.contains('bulbasaur') is False
        assert lruCache.contains('pikachu') is True
        assert lruCache.contains('mew') is True
