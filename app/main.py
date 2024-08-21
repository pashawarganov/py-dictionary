from __future__ import annotations
from dataclasses import dataclass
from typing import Hashable, Any, Iterable

INITIAL_CAPACITY = 8
RESIZE_THRESHOLD = 2 / 3
CAPACITY_MULTIPLIER = 2


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.size = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    @property
    def current_max_size(self) -> int:
        return round(self.capacity * RESIZE_THRESHOLD)

    def resize(self) -> None:
        old_hash_table = self.hash_table

        self.__init__(self.capacity * CAPACITY_MULTIPLIER)

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            if self.size + 1 >= self.current_max_size:
                self.resize()
                return self.__setitem__(key, value)
            self.size += 1

        self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find key: {key}")

        return self.hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find key: {key}")

        self.hash_table[index] = None
        self.size -= 1

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return str(self.hash_table)

    def clear(self) -> None:
        self.__init__()

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
        except KeyError as e:
            if default:
                return default
            raise e
        self.__delitem__(key)
        return value

    def update(self, other: Dictionary | Iterable = None, **kwargs) -> None:
        if not other:
            for key, value in kwargs.items():
                self.__setitem__(key, value)
        elif isinstance(other, Dictionary):
            for node in other.hash_table:
                if node is not None:
                    self.__setitem__(node.key, node.value)
        elif isinstance(other, dict):
            for key, value in other.items():
                self.__setitem__(key, value)
        elif isinstance(other, Iterable):
            for el in other:
                try:
                    if len(el) == 2:
                        self.__setitem__(el[0], el[1])
                    else:
                        raise TypeError
                except TypeError:
                    raise ValueError("Cannot add this object to a Dictionary")
