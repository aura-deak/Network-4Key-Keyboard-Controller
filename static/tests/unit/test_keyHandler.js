import { describe, it, expect } from 'vitest';
import { getKeyFromElement, VALID_KEYS } from './keyHandler.js';

describe('Key Handler', () => {
    describe('getKeyFromElement', () => {
        it('should return key from button with key-btn class', () => {
            const button = document.createElement('button');
            button.classList.add('key-btn');
            button.dataset.key = 'd';

            expect(getKeyFromElement(button)).toBe('d');
        });

        it('should return null for non-key-btn element', () => {
            const div = document.createElement('div');
            expect(getKeyFromElement(div)).toBeNull();
        });

        it('should return null for null element', () => {
            expect(getKeyFromElement(null)).toBeNull();
        });

        it('should return null for undefined element', () => {
            expect(getKeyFromElement(undefined)).toBeNull();
        });

        it('should return null for element without dataset.key', () => {
            const button = document.createElement('button');
            button.classList.add('key-btn');
            expect(getKeyFromElement(button)).toBeNull();
        });
    });

    describe('VALID_KEYS', () => {
        it('should contain d, f, j, k', () => {
            expect(VALID_KEYS).toContain('d');
            expect(VALID_KEYS).toContain('f');
            expect(VALID_KEYS).toContain('j');
            expect(VALID_KEYS).toContain('k');
        });

        it('should have exactly 4 keys', () => {
            expect(VALID_KEYS.length).toBe(4);
        });
    });
});
