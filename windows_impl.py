import pyautogui
import logging

from keyboard_simulator import KeyboardSimulator

logger = logging.getLogger(__name__)

KEY_MAP = {
    'd': 'd',
    'f': 'f',
    'j': 'j',
    'k': 'k',
}


class WindowsKeyboardImpl(KeyboardSimulator):
    def __init__(self):
        pyautogui.FAILSAFE = False
        logger.info("Windows keyboard implementation initialized")

    def press(self, key: str):
        if not self.is_valid_key(key):
            raise ValueError(f"Invalid key: {key}")
        try:
            pyautogui.keyDown(KEY_MAP[key])
            logger.debug(f"Key {key} pressed")
        except Exception as e:
            logger.error(f"Failed to press key {key}: {e}")
            raise

    def release(self, key: str):
        if not self.is_valid_key(key):
            raise ValueError(f"Invalid key: {key}")
        try:
            pyautogui.keyUp(KEY_MAP[key])
            logger.debug(f"Key {key} released")
        except Exception as e:
            logger.error(f"Failed to release key {key}: {e}")
            raise
