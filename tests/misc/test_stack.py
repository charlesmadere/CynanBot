import pytest

from src.misc.stack import Stack


class TestStack():

    def test_clear(self):
        stack: Stack[bool] = Stack()
        stack.push(True)
        stack.clear()
        assert len(stack) == 0

    def test_clear_withEmptyStack(self):
        stack: Stack[bool] = Stack()
        stack.clear()
        assert len(stack) == 0

    def test_len_withEmptyStack(self):
        stack: Stack[int] = Stack()
        assert len(stack) == 0

    def test_push_and_pop(self):
        stack: Stack[str] = Stack()
        stack.push('a')
        assert len(stack) == 1
        assert stack.pop() == 'a'
        assert len(stack) == 0

        stack.push('b')
        assert len(stack) == 1
        assert stack.pop() == 'b'
        assert len(stack) == 0

    def test_push_and_top(self):
        stack: Stack[str] = Stack()
        stack.push('a')
        assert len(stack) == 1
        assert stack.top() == 'a'
        assert len(stack) == 1

        stack.push('b')
        assert len(stack) == 2
        assert stack.top() == 'b'
        assert len(stack) == 2

    def test_pop_withEmptyStack_raisesIndexError(self):
        stack: Stack[float] = Stack()
        value: float | None = None

        with pytest.raises(IndexError):
            value = stack.pop()

        assert value is None

    def test_top_withEmptyStack_raisesIndexError(self):
        stack: Stack[str] = Stack()
        value: str | None = None

        with pytest.raises(IndexError):
            value = stack.top()

        assert value is None
