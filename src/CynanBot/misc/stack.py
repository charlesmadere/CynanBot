from __future__ import annotations

from typing import Generic, List, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):

    def __init__(self):
        self.__backingList: List[T] = list()

    def clear(self):
        self.__backingList.clear()

    def __len__(self) -> int:
        return len(self.__backingList)

    def pop(self) -> T:
        return self.__backingList.pop()

    def push(self, item: T):
        self.__backingList.append(item)

    def __repr__(self) -> str:
        return str(self.__backingList)

    def top(self) -> T:
        length = len(self)

        if length == 0:
            raise IndexError(f'`top()` can\'t be called on an empty stack')
        else:
            return self.__backingList[length - 1]
