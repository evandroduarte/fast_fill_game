import { useState, useEffect, useCallback } from 'react';
import { GameState, GameAction, PlayerColor } from '../types/game';

const WS_URL = 'ws://localhost:8000/ws';

export function useWebSocket() {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [gameState, setGameState] = useState<GameState>({
    grid: Array(4).fill(null).map(() => Array(4).fill('empty')),
    redCount: 0,
    blueCount: 0,
    timeElapsed: 0,
    gameStatus: 'waiting',
    winner: null,
    playerColor: null,
  });

  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log('Connected to server');
      setConnected(true);
      setSocket(ws);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('Received:', data);

      if (data.type === 'game_state') {
        setGameState(data.state);
      } else if (data.type === 'player_assign') {
        setGameState(prev => ({
          ...prev,
          playerColor: data.color as PlayerColor
        }));
      }
    };

    ws.onclose = () => {
      console.log('Disconnected from server');
      setConnected(false);
      setSocket(null);
    };

    return () => {
      ws.close();
    };
  }, []);

  const sendAction = useCallback((action: GameAction) => {
    if (socket && connected) {
      socket.send(JSON.stringify(action));
    }
  }, [socket, connected]);

  return { gameState, sendAction, connected };
}
