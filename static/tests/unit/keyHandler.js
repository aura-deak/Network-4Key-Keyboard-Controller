export function getKeyFromElement(element) {
    if (!element || !element.classList.contains('key-btn')) {
        return null;
    }
    return element.dataset.key || null;
}

export const VALID_KEYS = ['d', 'f', 'j', 'k'];