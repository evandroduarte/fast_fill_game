import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useCallback } from 'react';
import { GameGrid } from './GameGrid';
import { GameInfo } from './GameInfo';
import { useWebSocket } from '../hooks/useWebSocket';
export const GamePage = () => {
    const { gameState, sendAction, connected } = useWebSocket();
    const handleCellClick = useCallback((row, col) => {
        if (gameState.playerColor && gameState.gameStatus === 'playing') {
            sendAction({
                type: 'cell_click',
                row,
                col,
                color: gameState.playerColor
            });
        }
    }, [gameState.playerColor, gameState.gameStatus, sendAction]);
    if (!connected) {
        return _jsx("div", { className: "connecting", children: "Connecting to server..." });
    }
    return (_jsxs("div", { className: "game-page", children: [_jsx("h1", { children: "Fast Fill Game" }), _jsx(GameGrid, { grid: gameState.grid, onCellClick: handleCellClick, playerColor: gameState.playerColor, isGameActive: gameState.gameStatus === 'playing' }), _jsx(GameInfo, { redCount: gameState.redCount, blueCount: gameState.blueCount, timeElapsed: gameState.timeElapsed, playerColor: gameState.playerColor, gameStatus: gameState.gameStatus, winner: gameState.winner })] }));
};
