import React from 'react';
import { CellColor, PlayerColor } from '../types/game';

interface GameGridProps {
  grid: CellColor[][];
  onCellClick: (row: number, col: number) => void;
  playerColor: PlayerColor | null;
  isGameActive: boolean;
}

export const GameGrid: React.FC<GameGridProps> = ({
  grid,
  onCellClick,
  playerColor,
  isGameActive
}) => {
  return (
    <div className="game-grid">
      {grid.map((row, rowIndex) => (
        <div key={rowIndex} className="grid-row">
          {row.map((cell, colIndex) => (
            <div
              key={`${rowIndex}-${colIndex}`}
              className={`grid-cell ${cell !== 'empty' ? cell : ''}`}
              onClick={() => {
                if (isGameActive && cell === 'empty' && playerColor) {
                  onCellClick(rowIndex, colIndex);
                }
              }}
            />
          ))}
        </div>
      ))}
    </div>
  );
};
