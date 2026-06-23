import pytest
from keyboard_simulator import KeyboardSimulator


class ConcreteKeyboardSimulator(KeyboardSimulator):
    def press(self, key: str):
        super().press(key)

    def release(self, key: str):
        super().release(key)


class TestKeyboardSimulator:
    simulator = ConcreteKeyboardSimulator()

    def test_is_valid_key_valid(self):
        for key in ['d', 'f', 'j', 'k']:
            assert self.simulator.is_valid_key(key) is True

    def test_is_valid_key_invalid(self):
        for key in ['a', 'b', 'x', 'z', '1', '0']:
            assert self.simulator.is_valid_key(key) is False

    def test_press_valid_key(self):
        self.simulator.press('d')
        self.simulator.press('f')
        self.simulator.press('j')
        self.simulator.press('k')

    def test_press_invalid_key_raises(self):
        with pytest.raises(ValueError, match="Invalid key"):
            self.simulator.press('x')

    def test_release_valid_key(self):
        self.simulator.release('d')
        self.simulator.release('f')
        self.simulator.release('j')
        self.simulator.release('k')

    def test_release_invalid_key_raises(self):
        with pytest.raises(ValueError, match="Invalid key"):
            self.simulator.release('x')

    def test_valid_keys_list(self):
        assert KeyboardSimulator.VALID_KEYS == ['d', 'f', 'j', 'k']
