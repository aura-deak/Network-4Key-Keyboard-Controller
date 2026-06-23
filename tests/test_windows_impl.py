import pytest
from unittest.mock import MagicMock, patch


class TestWindowsKeyboardImpl:
    @patch('windows_impl.pyautogui')
    def test_initialization(self, mock_pyautogui):
        from windows_impl import WindowsKeyboardImpl
        impl = WindowsKeyboardImpl()
        mock_pyautogui.FAILSAFE = False

    @patch('windows_impl.pyautogui')
    def test_press_valid_key(self, mock_pyautogui):
        from windows_impl import WindowsKeyboardImpl
        impl = WindowsKeyboardImpl()
        impl.press('d')

        mock_pyautogui.keyDown.assert_called_with('d')

    @patch('windows_impl.pyautogui')
    def test_release_valid_key(self, mock_pyautogui):
        from windows_impl import WindowsKeyboardImpl
        impl = WindowsKeyboardImpl()
        impl.release('d')

        mock_pyautogui.keyUp.assert_called_with('d')

    @patch('windows_impl.pyautogui')
    def test_press_invalid_key_raises(self, mock_pyautogui):
        from windows_impl import WindowsKeyboardImpl
        impl = WindowsKeyboardImpl()

        with pytest.raises(ValueError, match="Invalid key"):
            impl.press('x')

    @patch('windows_impl.pyautogui')
    def test_release_invalid_key_raises(self, mock_pyautogui):
        from windows_impl import WindowsKeyboardImpl
        impl = WindowsKeyboardImpl()

        with pytest.raises(ValueError, match="Invalid key"):
            impl.release('x')

    @patch('windows_impl.pyautogui')
    def test_all_valid_keys(self, mock_pyautogui):
        from windows_impl import WindowsKeyboardImpl
        impl = WindowsKeyboardImpl()

        for key in ['d', 'f', 'j', 'k']:
            impl.press(key)
            mock_pyautogui.keyDown.assert_called_with(key)
