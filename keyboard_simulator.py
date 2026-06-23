from abc import ABC, abstractmethod


class KeyboardSimulator(ABC):
    VALID_KEYS = ['d', 'f', 'j', 'k']

    @abstractmethod
    def press(self, key: str) -> None:
        if not self.is_valid_key(key):
            raise ValueError(f"Invalid key: {key}")

    @abstractmethod
    def release(self, key: str) -> None:
        if not self.is_valid_key(key):
            raise ValueError(f"Invalid key: {key}")

    def is_valid_key(self, key: str) -> bool:
        return key in self.VALID_KEYS
