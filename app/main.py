from typing import Any, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8

    def resize(self) -> None:
        old_hash_table = self.hash_table
        current_len = len(self.hash_table)
        self.length = 0
        self.hash_table = ([None] * current_len) * 2
        for node in old_hash_table:
            if node is None or node == "Deleted":
                continue
            else:
                key, hash_value, value = node
                self.__setitem__(key, value)

    def __setitem__(self, key: Any, value: Any) -> None:
        capacity = len(self.hash_table)
        if self.length + 1 >= capacity * 2 // 3:
            self.resize()
            capacity = len(self.hash_table)
        capacity_try = capacity
        hash_value = hash(key)
        index = hash_value % capacity
        node = (key, hash_value, value)
        while capacity_try != 0:
            if self.hash_table[index] is None:
                self.hash_table[index] = node
                self.length += 1
                break
            elif self.hash_table[index][0] == node[0]:
                self.hash_table[index] = node
                break
            else:
                index = (index + 1) % capacity
                capacity_try -= 1

    def __getitem__(self, key: Any) -> Any:
        capacity = len(self.hash_table)
        capacity_try = capacity
        hash_value = hash(key)
        index = hash_value % capacity
        while capacity_try != 0:
            if self.hash_table[index] is None:
                raise KeyError(key)
            elif self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            else:
                index = (index + 1) % capacity
                capacity_try -= 1
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def __delitem__(self, key: Any) -> None:
        capacity = len(self.hash_table)
        capacity_try = capacity
        hash_value = hash(key)
        index = hash_value % capacity
        while capacity_try != 0:
            if self.hash_table[index] is None:
                raise KeyError(key)
            elif self.hash_table[index][0] == key:
                self.hash_table[index] = "Deleted"
                self.length -= 1
                break
            else:
                index = (index + 1) % capacity
                capacity_try -= 1
        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        capacity = len(self.hash_table)
        capacity_try = capacity
        hash_value = hash(key)
        index = hash_value % capacity
        while capacity_try != 0:
            if self.hash_table[index] is None:
                return default
            elif self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            else:
                index = (index + 1) % capacity
                capacity_try -= 1
        return default

    def pop(self, key: Any, default: Any = None) -> Any:
        capacity = len(self.hash_table)
        capacity_try = capacity
        hash_value = hash(key)
        index = hash_value % capacity
        while capacity_try != 0:
            if self.hash_table[index] is None:
                raise KeyError(key)
            elif self.hash_table[index][0] == key:
                result = self.hash_table[index][2]
                self.__delitem__(key)
                return result
            else:
                index = (index + 1) % capacity
                capacity_try -= 1
        return default

    def update(self, other: Any = None, **kwargs) -> None:
        if other is not None:
            if hasattr(other, "items"):
                for key, value in other.items():
                    self.__setitem__(key, value)
            else:
                for key, value in other:
                    self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __iter__(self) -> Iterator[Any]:
        for cell in self.hash_table:
            if cell is None or cell == "Deleted":
                continue
            yield cell[0]
