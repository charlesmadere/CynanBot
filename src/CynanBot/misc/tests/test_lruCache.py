from CynanBot.misc.lruCache import LruCache


class TestLruCache():

    def test_constructWithNegativeOneCapacity(self):
        lruCache: LruCache = None
        exception: Exception = None

        try:
            lruCache = LruCache(-1)
        except Exception as e:
            exception = e

        assert lruCache is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_constructWithOneCapacity(self):
        lruCache: LruCache = None
        exception: Exception = None

        try:
            lruCache = LruCache(1)
        except Exception as e:
            exception = e

        assert lruCache is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_constructWithThreeCapacity(self):
        lruCache: LruCache = None
        exception: Exception = None

        try:
            lruCache = LruCache(3)
        except Exception as e:
            exception = e

        assert lruCache is not None
        assert exception is None

    def test_constructWithTwoCapacity(self):
        lruCache: LruCache = None
        exception: Exception = None

        try:
            lruCache = LruCache(2)
        except Exception as e:
            exception = e

        assert lruCache is not None
        assert exception is None

    def test_constructWithZeroCapacity(self):
        lruCache: LruCache = None
        exception: Exception = None

        try:
            lruCache = LruCache(0)
        except Exception as e:
            exception = e

        assert lruCache is None
        assert exception is not None
        assert isinstance(exception, ValueError)

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
