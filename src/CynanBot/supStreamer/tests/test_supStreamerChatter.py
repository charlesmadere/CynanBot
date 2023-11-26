from supStreamer.supStreamerChatter import SupStreamerChatter


class TestSupStreamerChatter():

    def test_equals_withDifferentUserIds(self):
        first = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'abc123'
        )

        second = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'def456'
        )

        assert first != second

    def test_equals_withSameUserIds(self):
        first = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'abc123'
        )

        second = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'abc123'
        )

        assert first == second

    def test_hash_withDifferentUserIds(self):
        first = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'xyz789'
        )

        second = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'abc123'
        )

        assert hash(first) != hash(second)

    def test_hash_withSameUserIds(self):
        first = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'abc123'
        )

        second = SupStreamerChatter(
            mostRecentSup = None,
            userId = 'abc123'
        )

        assert hash(first) == hash(second)
