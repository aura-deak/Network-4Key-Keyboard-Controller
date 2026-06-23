import logging

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from platform_factory import create_keyboard_simulator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'keyboard-controller-secret'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')

keyboard_simulator = None


@socketio.on('connect')
def handle_connect():
    logger.info("Client connected")
    emit('response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected")


@socketio.on('key_press')
def handle_key_press(data):
    key = data.get('key')
    if not key:
        emit('response', {'error': 'Key is required'})
        return

    if not keyboard_simulator.is_valid_key(key):
        emit('response', {'error': f'Invalid key: {key}'})
        return

    try:
        keyboard_simulator.press(key)
        emit('response', {'success': True, 'key': key, 'action': 'press'})
        logger.info(f"Key {key} pressed")
    except Exception as e:
        emit('response', {'error': str(e)})
        logger.error(f"Error pressing key {key}: {e}")


@socketio.on('key_release')
def handle_key_release(data):
    key = data.get('key')
    if not key:
        emit('response', {'error': 'Key is required'})
        return

    if not keyboard_simulator.is_valid_key(key):
        emit('response', {'error': f'Invalid key: {key}'})
        return

    try:
        keyboard_simulator.release(key)
        emit('response', {'success': True, 'key': key, 'action': 'release'})
        logger.info(f"Key {key} released")
    except Exception as e:
        emit('response', {'error': str(e)})
        logger.error(f"Error releasing key {key}: {e}")


def initialize():
    global keyboard_simulator
    try:
        keyboard_simulator = create_keyboard_simulator()
        logger.info("Keyboard simulator initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize keyboard simulator: {e}")
        raise


if __name__ == '__main__':
    initialize()
    logger.info("Starting Flask-SocketIO server on port 5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
