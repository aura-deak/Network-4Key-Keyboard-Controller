const socket = io();
const statusEl = document.getElementById('status');
const buttons = document.querySelectorAll('.key-btn');
const KEY_TO_BUTTON = {
    'd': document.querySelector('[data-key="d"]'),
    'f': document.querySelector('[data-key="f"]'),
    'j': document.querySelector('[data-key="j"]'),
    'k': document.querySelector('[data-key="k"]')
};
const BUTTON_TO_KEY = {};
for (const [key, btn] of Object.entries(KEY_TO_BUTTON)) {
    BUTTON_TO_KEY[btn.dataset.key] = key;
}
const activeTouches = new Map();

function getKeyFromElement(element) {
    if (!element || !element.classList.contains('key-btn')) {
        return null;
    }
    return element.dataset.key;
}

function updateButtonState(key, isPressed) {
    const btn = KEY_TO_BUTTON[key];
    if (!btn) return;
    if (isPressed) {
        btn.classList.add('pressed');
    } else {
        btn.classList.remove('pressed');
    }
}

function sendKeyPress(key) {
    socket.emit('key_press', { key });
    updateButtonState(key, true);
}

function sendKeyRelease(key) {
    socket.emit('key_release', { key });
    updateButtonState(key, false);
}

function handleTouch(touch) {
    const element = document.elementFromPoint(touch.clientX, touch.clientY);
    const key = getKeyFromElement(element);

    if (key) {
        const prevKey = activeTouches.get(touch.identifier);
        if (prevKey && prevKey !== key) {
            sendKeyRelease(prevKey);
        }
        sendKeyPress(key);
        activeTouches.set(touch.identifier, key);
    } else {
        const prevKey = activeTouches.get(touch.identifier);
        if (prevKey) {
            sendKeyRelease(prevKey);
            activeTouches.delete(touch.identifier);
        }
    }
}

document.addEventListener('touchstart', (e) => {
    e.preventDefault();
    for (const touch of e.changedTouches) {
        handleTouch(touch);
    }
}, { passive: false });

document.addEventListener('touchmove', (e) => {
    e.preventDefault();
    for (const touch of e.changedTouches) {
        handleTouch(touch);
    }
}, { passive: false });

document.addEventListener('touchend', (e) => {
    e.preventDefault();
    for (const touch of e.changedTouches) {
        const key = activeTouches.get(touch.identifier);
        if (key) {
            sendKeyRelease(key);
            activeTouches.delete(touch.identifier);
        }
    }
}, { passive: false });

document.addEventListener('touchcancel', (e) => {
    e.preventDefault();
    for (const touch of e.changedTouches) {
        const key = activeTouches.get(touch.identifier);
        if (key) {
            sendKeyRelease(key);
            activeTouches.delete(touch.identifier);
        }
    }
}, { passive: false });

socket.on('connect', () => {
    statusEl.textContent = 'Connected';
});

socket.on('disconnect', () => {
    statusEl.textContent = 'Disconnected';
    activeTouches.clear();
    buttons.forEach(btn => btn.classList.remove('pressed'));
});

socket.on('response', (data) => {
    if (data.error) {
        console.error('Error:', data.error);
    }
});
