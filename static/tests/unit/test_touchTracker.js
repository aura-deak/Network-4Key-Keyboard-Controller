import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TouchTracker } from './touchTracker.js';

describe('TouchTracker', () => {
    let tracker;
    let mockButton;

    beforeEach(() => {
        tracker = new TouchTracker();

        mockButton = document.createElement('button');
        mockButton.classList.add('key-btn');
        mockButton.dataset.key = 'd';
    });

    describe('getKeyFromElement', () => {
        it('should return key from key-btn element', () => {
            const key = tracker.getKeyFromElement(mockButton);
            expect(key).toBe('d');
        });

        it('should return null for non-key-btn element', () => {
            const div = document.createElement('div');
            expect(tracker.getKeyFromElement(div)).toBeNull();
        });

        it('should return null for null', () => {
            expect(tracker.getKeyFromElement(null)).toBeNull();
        });
    });

    describe('updateTouch', () => {
        it('should return press action when touch is on button', () => {
            const mockTouch = {
                identifier: 1,
                clientX: 100,
                clientY: 100
            };

            document.elementFromPoint = vi.fn().mockReturnValue(mockButton);

            const result = tracker.updateTouch(mockTouch);

            expect(result).toEqual({ action: 'press', key: 'd', prevKey: undefined });
            expect(tracker.activeTouches.get(1)).toBe('d');
        });

        it('should send release when touch moves to different button', () => {
            const mockButtonF = document.createElement('button');
            mockButtonF.classList.add('key-btn');
            mockButtonF.dataset.key = 'f';

            const mockTouch = { identifier: 1, clientX: 100, clientY: 100 };

            document.elementFromPoint = vi.fn()
                .mockReturnValueOnce(mockButton)
                .mockReturnValueOnce(mockButtonF);

            tracker.sendPress = vi.fn();
            tracker.sendRelease = vi.fn();

            tracker.updateTouch(mockTouch);
            const result = tracker.updateTouch(mockTouch);

            expect(tracker.sendRelease).toHaveBeenCalledWith('d');
            expect(result).toEqual({ action: 'press', key: 'f', prevKey: 'd' });
        });

        it('should send release when touch moves off button', () => {
            const mockTouch = { identifier: 1, clientX: 100, clientY: 100 };

            document.elementFromPoint = vi.fn()
                .mockReturnValueOnce(mockButton)
                .mockReturnValueOnce(null);

            tracker.sendPress = vi.fn();
            tracker.sendRelease = vi.fn();

            tracker.updateTouch(mockTouch);
            const result = tracker.updateTouch(mockTouch);

            expect(tracker.sendRelease).toHaveBeenCalledWith('d');
            expect(result).toEqual({ action: 'release', key: 'd' });
            expect(tracker.activeTouches.has(1)).toBe(false);
        });
    });

    describe('removeTouch', () => {
        it('should send release when removing active touch', () => {
            const mockTouch = { identifier: 1, clientX: 100, clientY: 100 };

            document.elementFromPoint = vi.fn().mockReturnValue(mockButton);
            tracker.sendPress = vi.fn();
            tracker.sendRelease = vi.fn();

            tracker.updateTouch(mockTouch);
            const result = tracker.removeTouch(mockTouch);

            expect(tracker.sendRelease).toHaveBeenCalledWith('d');
            expect(result).toEqual({ action: 'release', key: 'd' });
        });

        it('should return null for inactive touch', () => {
            const mockTouch = { identifier: 999, clientX: 100, clientY: 100 };
            const result = tracker.removeTouch(mockTouch);
            expect(result).toBeNull();
        });
    });

    describe('multi-touch', () => {
        it('should track multiple touches independently', () => {
            const mockTouch1 = { identifier: 1, clientX: 100, clientY: 100 };
            const mockTouch2 = { identifier: 2, clientX: 200, clientY: 100 };

            document.elementFromPoint = vi.fn().mockReturnValue(mockButton);
            tracker.sendPress = vi.fn();
            tracker.sendRelease = vi.fn();

            tracker.updateTouch(mockTouch1);
            tracker.updateTouch(mockTouch2);

            expect(tracker.activeTouches.get(1)).toBe('d');
            expect(tracker.activeTouches.get(2)).toBe('d');
        });
    });
});
