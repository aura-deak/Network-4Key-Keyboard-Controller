import uinput
import logging

from keyboard_simulator import KeyboardSimulator

logger = logging.getLogger(__name__)

KEY_MAP = {
    'd': uinput.KEY_D,
    'f': uinput.KEY_F,
    'j': uinput.KEY_J,
    'k': uinput.KEY_K,
}


class LinuxKeyboardImpl(KeyboardSimulator):
    def __init__(self):
        self._device = None
        self._initialize_device()

    def _initialize_device(self):
        try:
            self._device = uinput.Device(KEY_MAP.values())
            logger.info("Linux keyboard device initialized")
        except Exception as e:
            logger.error(f"Failed to initialize uinput device: {e}")
            raise

    def press(self, key: str):
        if not self.is_valid_key(key):
            raise ValueError(f"Invalid key: {key}")
        try:
            self._device.emit(KEY_MAP[key], 1)
            logger.debug(f"Key {key} pressed")
        except Exception as e:
            logger.error(f"Failed to press key {key}: {e}")
            raise

    def release(self, key: str):
        if not self.is_valid_key(key):
            raise ValueError(f"Invalid key: {key}")
        try:
            self._device.emit(KEY_MAP[key], 0)
            logger.debug(f"Key {key} released")
        except Exception as e:
            logger.error(f"Failed to release key {key}: {e}")
            raise
