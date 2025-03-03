import React, { useCallback } from 'react';
import { GameGrid } from './GameGrid';
import { GameInfo } from './GameInfo';
import { useWebSocket } from '../hooks/useWebSocket';

export const GamePage: React.FC = () => {
  const { gameState, sendAction, connected } = useWebSocket();

  const handleCellClick = useCallback((row: number, col: number) => {
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
    return <div className="connecting">Connecting to server...</div>;
  }

  return (
    <div className="game-page">
      <h1>Fast Fill Game</h1>
      <GameGrid
        grid={gameState.grid}
        onCellClick={handleCellClick}
        playerColor={gameState.playerColor}
        isGameActive={gameState.gameStatus === 'playing'}
      />
      <GameInfo
        redCount={gameState.redCount}
        blueCount={gameState.blueCount}
        timeElapsed={gameState.timeElapsed}
        playerColor={gameState.playerColor}
        gameStatus={gameState.gameStatus}
        winner={gameState.winner}
      />
    </div>
  );
};
