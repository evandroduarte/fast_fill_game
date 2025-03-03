from enum import Enum
from typing import Dict, List, Optional, Tuple, Set, Union
import time


class CellColor(str, Enum):
    RED = "red"
    BLUE = "blue"
    EMPTY = "empty"


class GameStatus(str, Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    FINISHED = "finished"


class Game:
    def __init__(self):
        self.grid: List[List[CellColor]] = [
            [CellColor.EMPTY for _ in range(4)] for _ in range(4)
        ]
        self.red_count: int = 0
        self.blue_count: int = 0
        self.start_time: Optional[float] = None
        self.status: GameStatus = GameStatus.WAITING
        self.winner: Optional[Union[CellColor, str]] = None
        self.players: Dict[str, CellColor] = {}
        self.current_time: float = 0

    def add_player(self, player_id: str) -> CellColor:
        """Add a new player to the game and return their color."""
        if len(self.players) >= 2:
            raise ValueError("Game is full")

        # Assign red to first player, blue to second
        color = CellColor.RED if CellColor.RED not in self.players.values() else CellColor.BLUE
        self.players[player_id] = color

        # Start the game when the second player joins
        if len(self.players) == 2:
            self.start_time = time.time()
            self.status = GameStatus.PLAYING

        return color

    def remove_player(self, player_id: str) -> None:
        """Remove a player from the game."""
        if player_id in self.players:
            del self.players[player_id]

        # Reset game state if all players left
        if len(self.players) == 0:
            self.reset()
        elif self.status == GameStatus.PLAYING:
            # If playing and a player left, end the game
            self.status = GameStatus.WAITING
            self.start_time = None

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.grid = [[CellColor.EMPTY for _ in range(4)] for _ in range(4)]
        self.red_count = 0
        self.blue_count = 0
        self.start_time = None
        self.status = GameStatus.WAITING
        self.winner = None
        self.current_time = 0

    def update_cell(self, row: int, col: int, color: CellColor) -> bool:
        """
        Update a cell with a player's color.
        Returns True if the update was successful, False otherwise.
        """
        if (self.status != GameStatus.PLAYING or
                row < 0 or row >= 4 or
                col < 0 or col >= 4 or
                self.grid[row][col] != CellColor.EMPTY):
            return False

        self.grid[row][col] = color

        if color == CellColor.RED:
            self.red_count += 1
        else:
            self.blue_count += 1

        # Check if grid is full
        total_cells = self.red_count + self.blue_count
        if total_cells == 16:  # 4x4 grid
            self.end_game()

        return True

    def end_game(self) -> None:
        """End the game and determine the winner."""
        self.status = GameStatus.FINISHED

        if self.red_count > self.blue_count:
            self.winner = CellColor.RED
        elif self.blue_count > self.red_count:
            self.winner = CellColor.BLUE
        else:
            self.winner = "tie"

    def update_time(self) -> None:
        """Update elapsed time if game is in progress."""
        if self.status == GameStatus.PLAYING and self.start_time is not None:
            self.current_time = int(time.time() - self.start_time)

    def get_state(self, player_id: Optional[str] = None) -> Dict:
        """Get the current game state."""
        self.update_time()

        state = {
            "grid": [[cell for cell in row] for row in self.grid],
            "redCount": self.red_count,
            "blueCount": self.blue_count,
            "timeElapsed": self.current_time,
            "gameStatus": self.status,
            "winner": self.winner,
            "playerColor": self.players.get(player_id) if player_id else None
        }

        return state
