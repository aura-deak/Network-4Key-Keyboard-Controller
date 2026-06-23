import pytest
from unittest.mock import patch


class TestPlatformFactory:
    @patch('platform_factory.sys.platform', 'linux')
    @patch('platform_factory.LinuxKeyboardImpl')
    def test_create_linux_simulator(self, mock_linux_impl):
        from platform_factory import create_keyboard_simulator
        mock_instance = mock_linux_impl.return_value
        result = create_keyboard_simulator()
        assert result == mock_instance
        mock_linux_impl.assert_called_once()

    @patch('platform_factory.sys.platform', 'win32')
    @patch('platform_factory.WindowsKeyboardImpl')
    def test_create_windows_simulator(self, mock_windows_impl):
        from platform_factory import create_keyboard_simulator
        mock_instance = mock_windows_impl.return_value
        result = create_keyboard_simulator()
        assert result == mock_instance
        mock_windows_impl.assert_called_once()

    @patch('platform_factory.sys.platform', 'darwin')
    def test_unsupported_platform_raises(self):
        from platform_factory import create_keyboard_simulator
        with pytest.raises(NotImplementedError, match="Platform darwin is not supported"):
            create_keyboard_simulator()

    @patch('platform_factory.sys.platform', 'linux')
    @patch('platform_factory.LinuxKeyboardImpl')
    def test_returns_keyboard_simulator_instance(self, mock_linux_impl):
        from platform_factory import create_keyboard_simulator
        from keyboard_simulator import KeyboardSimulator
        result = create_keyboard_simulator()
        assert isinstance(result, KeyboardSimulator)
