export class TouchTracker {
    constructor() {
        this.activeTouches = new Map();
    }

    getKeyFromElement(element) {
        if (!element || !element.classList.contains('key-btn')) {
            return null;
        }
        return element.dataset.key;
    }

    getElementFromPoint(x, y) {
        return document.elementFromPoint(x, y);
    }

    updateTouch(touch) {
        const element = this.getElementFromPoint(touch.clientX, touch.clientY);
        const key = this.getKeyFromElement(element);

        if (key) {
            const prevKey = this.activeTouches.get(touch.identifier);
            if (prevKey && prevKey !== key) {
                this.sendRelease(prevKey);
            }
            this.sendPress(key);
            this.activeTouches.set(touch.identifier, key);
            return { action: 'press', key, prevKey };
        } else {
            const prevKey = this.activeTouches.get(touch.identifier);
            if (prevKey) {
                this.sendRelease(prevKey);
                this.activeTouches.delete(touch.identifier);
                return { action: 'release', key: prevKey };
            }
        }
        return null;
    }

    removeTouch(touch) {
        const key = this.activeTouches.get(touch.identifier);
        if (key) {
            this.sendRelease(key);
            this.activeTouches.delete(touch.identifier);
            return { action: 'release', key };
        }
        return null;
    }

    sendPress(key) {}
    sendRelease(key) {}
}
