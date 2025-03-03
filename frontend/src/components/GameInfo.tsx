import React from 'react';
import { PlayerColor } from '../types/game';

interface GameInfoProps {
  redCount: number;
  blueCount: number;
  timeElapsed: number;
  playerColor: PlayerColor | null;
  gameStatus: 'waiting' | 'playing' | 'finished';
  winner: PlayerColor | 'tie' | null;
}

export const GameInfo: React.FC<GameInfoProps> = ({
  redCount,
  blueCount,
  timeElapsed,
  playerColor,
  gameStatus,
  winner
}) => {
  const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  const getStatusMessage = () => {
    if (gameStatus === 'waiting') {
      return 'Waiting for another player to join...';
    } else if (gameStatus === 'finished') {
      if (winner === 'tie') {
        return 'Game over! It\'s a tie!';
      } else {
        return `Game over! ${winner === playerColor ? 'You won!' : 'You lost!'}`;
      }
    } else {
      return 'Game in progress...';
    }
  };

  return (
    <div className="game-info">
      <div className="time-elapsed">
        Time: {formatTime(timeElapsed)}
      </div>
      <div className="square-counter">
        <span className={`red-count ${playerColor === 'red' ? 'my-color' : ''}`}>
          Red: {redCount}
        </span>
        <span className={`blue-count ${playerColor === 'blue' ? 'my-color' : ''}`}>
          Blue: {blueCount}
        </span>
      </div>
      <div className="status-message">
        {getStatusMessage()}
      </div>
      {playerColor && (
        <div className="player-info">
          You are playing as <span className={playerColor}>{playerColor}</span>
        </div>
      )}
    </div>
  );
};
