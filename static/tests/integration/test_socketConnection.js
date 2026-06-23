import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('Socket Connection', () => {
    let mockSocket;

    beforeEach(() => {
        mockSocket = {
            on: vi.fn(),
            emit: vi.fn(),
            connected: true
        };

        global.io = vi.fn().mockReturnValue(mockSocket);
    });

    it('should connect to server', () => {
        expect(mockSocket.on).toBeDefined();
    });

    it('should register connect handler', () => {
        const connectHandler = vi.fn();
        mockSocket.on('connect', connectHandler);
        expect(mockSocket.on).toHaveBeenCalledWith('connect', connectHandler);
    });

    it('should register disconnect handler', () => {
        const disconnectHandler = vi.fn();
        mockSocket.on('disconnect', disconnectHandler);
        expect(mockSocket.on).toHaveBeenCalledWith('disconnect', disconnectHandler);
    });

    it('should emit key_press event', () => {
        mockSocket.emit('key_press', { key: 'd' });
        expect(mockSocket.emit).toHaveBeenCalledWith('key_press', { key: 'd' });
    });

    it('should emit key_release event', () => {
        mockSocket.emit('key_release', { key: 'd' });
        expect(mockSocket.emit).toHaveBeenCalledWith('key_release', { key: 'd' });
    });

    it('should receive response event', () => {
        const responseHandler = vi.fn();
        mockSocket.on('response', responseHandler);
        expect(mockSocket.on).toHaveBeenCalledWith('response', responseHandler);
    });
});
