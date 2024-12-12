import abc
from typing import TypeVar, Generic

KeyT = TypeVar("KeyT")
ValueT = TypeVar("ValueT")


class MemoizedOperation(Generic[KeyT, ValueT]):
    def __init__(self):
        self.cache: dict[KeyT, ValueT] = {}

    def execute(self, key: KeyT) -> ValueT:
        if key not in self.cache:
            self.cache[key] = self.execute_uncached(key)

        return self.cache[key]

    @abc.abstractmethod
    def execute_uncached(self, key: KeyT) -> ValueT:
        raise NotImplementedError

