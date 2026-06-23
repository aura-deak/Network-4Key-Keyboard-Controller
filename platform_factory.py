import sys
import logging

from keyboard_simulator import KeyboardSimulator

logger = logging.getLogger(__name__)


class MockKeyboardSimulator(KeyboardSimulator):
    def __init__(self):
        logger.info("Using mock keyboard simulator (no actual keyboard control)")

    def press(self, key: str):
        super().press(key)
        logger.info(f"Mock press: {key}")

    def release(self, key: str):
        super().release(key)
        logger.info(f"Mock release: {key}")


def create_keyboard_simulator() -> KeyboardSimulator:
    platform = sys.platform

    if platform.startswith('linux'):
        try:
            from linux_impl import LinuxKeyboardImpl
            logger.info("Creating Linux keyboard simulator")
            return LinuxKeyboardImpl()
        except ImportError:
            logger.warning("uinput module not found, using mock simulator")
            return MockKeyboardSimulator()
    elif platform == 'win32':
        try:
            from windows_impl import WindowsKeyboardImpl
            logger.info("Creating Windows keyboard simulator")
            return WindowsKeyboardImpl()
        except ImportError:
            logger.warning("pyautogui module not found, using mock simulator")
            return MockKeyboardSimulator()
    else:
        logger.warning(f"Platform {platform} not supported, using mock simulator")
        return MockKeyboardSimulator()
