import pytest
from unittest.mock import MagicMock, patch


class TestLinuxKeyboardImpl:
    @patch('linux_impl.uinput.Device')
    def test_initialization(self, mock_device_class):
        from linux_impl import LinuxKeyboardImpl
        impl = LinuxKeyboardImpl()
        mock_device_class.assert_called_once()

    @patch('linux_impl.uinput.Device')
    def test_press_valid_key(self, mock_device_class):
        from linux_impl import LinuxKeyboardImpl
        mock_device = MagicMock()
        mock_device_class.return_value = mock_device

        impl = LinuxKeyboardImpl()
        impl.press('d')

        mock_device.emit.assert_called()
        call_args = mock_device.emit.call_args
        from linux_impl import KEY_MAP
        assert call_args[0][0] == KEY_MAP['d']
        assert call_args[0][1] == 1

    @patch('linux_impl.uinput.Device')
    def test_release_valid_key(self, mock_device_class):
        from linux_impl import LinuxKeyboardImpl
        mock_device = MagicMock()
        mock_device_class.return_value = mock_device

        impl = LinuxKeyboardImpl()
        impl.release('d')

        mock_device.emit.assert_called()
        call_args = mock_device.emit.call_args
        from linux_impl import KEY_MAP
        assert call_args[0][0] == KEY_MAP['d']
        assert call_args[0][1] == 0

    @patch('linux_impl.uinput.Device')
    def test_press_invalid_key_raises(self, mock_device_class):
        from linux_impl import LinuxKeyboardImpl
        impl = LinuxKeyboardImpl()

        with pytest.raises(ValueError, match="Invalid key"):
            impl.press('x')

    @patch('linux_impl.uinput.Device')
    def test_release_invalid_key_raises(self, mock_device_class):
        from linux_impl import LinuxKeyboardImpl
        impl = LinuxKeyboardImpl()

        with pytest.raises(ValueError, match="Invalid key"):
            impl.release('x')

    @patch('linux_impl.uinput.Device')
    def test_key_map_contains_all_valid_keys(self, mock_device_class):
        from linux_impl import LinuxKeyboardImpl, KEY_MAP
        impl = LinuxKeyboardImpl()

        for key in ['d', 'f', 'j', 'k']:
            assert key in KEY_MAP
            impl.press(key)

    @patch('linux_impl.uinput.Device')
    def test_init_failure(self, mock_device_class):
        from linux_impl import LinuxKeyboardImpl
        mock_device_class.side_effect = Exception("Device error")

        with pytest.raises(Exception):
            LinuxKeyboardImpl()
