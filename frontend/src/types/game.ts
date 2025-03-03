export type CellColor = 'red' | 'blue' | 'empty';
export type PlayerColor = 'red' | 'blue';

export interface GameState {
  grid: CellColor[][];
  redCount: number;
  blueCount: number;
  timeElapsed: number;
  gameStatus: 'waiting' | 'playing' | 'finished';
  winner: PlayerColor | 'tie' | null;
  playerColor: PlayerColor | null;
}

export interface GameAction {
  type: 'cell_click';
  row: number;
  col: number;
  color: PlayerColor;
}
