import pytest
from unittest.mock import MagicMock, patch
import sys


class TestApp:
    @pytest.fixture
    def mock_keyboard_simulator(self):
        with patch('app.keyboard_simulator') as mock:
            mock.is_valid_key.return_value = True
            yield mock

    @patch('app.emit')
    @patch('app.keyboard_simulator', None)
    def test_handle_connect(self, mock_emit):
        from app import handle_connect
        handle_connect()
        mock_emit.assert_called_with('response', {'status': 'connected'})

    @patch('app.emit')
    def test_handle_disconnect(self, mock_emit):
        from app import handle_disconnect
        handle_disconnect()

    @patch('app.emit')
    @patch('app.keyboard_simulator')
    def test_handle_key_press_valid_key(self, mock_simulator, mock_emit):
        from app import handle_key_press
        mock_simulator.is_valid_key.return_value = True

        handle_key_press({'key': 'd'})

        mock_simulator.press.assert_called_with('d')
        mock_emit.assert_called_with('response', {'success': True, 'key': 'd', 'action': 'press'})

    @patch('app.emit')
    @patch('app.keyboard_simulator')
    def test_handle_key_press_missing_key(self, mock_simulator, mock_emit):
        from app import handle_key_press

        handle_key_press({})

        mock_emit.assert_called_with('response', {'error': 'Key is required'})

    @patch('app.emit')
    @patch('app.keyboard_simulator')
    def test_handle_key_press_invalid_key(self, mock_simulator, mock_emit):
        from app import handle_key_press
        mock_simulator.is_valid_key.return_value = False

        handle_key_press({'key': 'x'})

        mock_emit.assert_called_with('response', {'error': 'Invalid key: x'})

    @patch('app.emit')
    @patch('app.keyboard_simulator')
    def test_handle_key_release_valid_key(self, mock_simulator, mock_emit):
        from app import handle_key_release
        mock_simulator.is_valid_key.return_value = True

        handle_key_release({'key': 'd'})

        mock_simulator.release.assert_called_with('d')
        mock_emit.assert_called_with('response', {'success': True, 'key': 'd', 'action': 'release'})

    @patch('app.emit')
    @patch('app.keyboard_simulator')
    def test_handle_key_release_invalid_key(self, mock_simulator, mock_emit):
        from app import handle_key_release
        mock_simulator.is_valid_key.return_value = False

        handle_key_release({'key': 'x'})

        mock_emit.assert_called_with('response', {'error': 'Invalid key: x'})

    @patch('app.emit')
    @patch('app.keyboard_simulator')
    def test_handle_key_press_exception(self, mock_simulator, mock_emit):
        from app import handle_key_press
        mock_simulator.is_valid_key.return_value = True
        mock_simulator.press.side_effect = Exception("Test error")

        handle_key_press({'key': 'd'})

        mock_emit.assert_called()
        call_args = mock_emit.call_args
        assert 'error' in call_args[0][1]
