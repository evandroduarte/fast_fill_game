from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict
import asyncio

from app.game import Game, CellColor, GameStatus

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = Game()

# Connected WebSocket clients
connected_clients: Dict[str, WebSocket] = {}

# Regular broadcast of game state (for timer updates)
async def broadcast_game_state():
    while True:
        if game.status == "playing" and connected_clients:
            # Create individual messages for each player
            for client_id, websocket in connected_clients.items():
                message = {
                    "type": "game_state",
                    "state": game.get_state(client_id)
                }
                await websocket.send_text(json.dumps(message))
        await asyncio.sleep(1)  # Update every second

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_game_state())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(id(websocket))

    try:
        # Add player to game
        player_color = game.add_player(client_id)
        connected_clients[client_id] = websocket

        # Inform player of assigned color & initial state
        await send_message(websocket, {"type": "player_assign", "color": player_color})
        await send_message(websocket, {"type": "game_state", "state": game.get_state(client_id)})

        # Broadcast updated game state to all players
        await broadcast_game_state()

        # Process incoming messages
        async for message in websocket.iter_text():
            await handle_message(client_id, message)

    except ValueError as e:
        # Game is full
        await send_message(websocket, {"type": "error", "message": str(e)})
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Remove player on disconnect/error
        connected_clients.pop(client_id, None)
        game.remove_player(client_id)
        await broadcast_game_state()

async def send_message(websocket: WebSocket, message: dict):
    """Helper function to send a JSON message."""
    await websocket.send_text(json.dumps(message))

async def broadcast_game_state():
    """Broadcast the current game state to all connected clients."""
    if connected_clients:
        tasks = [
            send_message(ws, {"type": "game_state", "state": game.get_state(cid)})
            for cid, ws in connected_clients.items()
        ]
        await asyncio.gather(*tasks)

async def handle_message(client_id: str, message: str):
    """Processes incoming messages from the client."""
    try:
        action = json.loads(message)

        if action["type"] == "cell_click":
            player_color = game.players.get(client_id)
            if player_color and player_color == action["color"] and game.status == "playing":
                if game.update_cell(action["row"], action["col"], CellColor(player_color)):
                    await broadcast_game_state()

        elif action["type"] == "play_again":
            game.reset()
            if len(connected_clients) == 2:
                game.status = GameStatus.PLAYING
            await broadcast_game_state()

    except Exception as e:
        print(f"Error processing message from {client_id}: {e}")

@app.get("/")
async def root():
    return {"message": "Fast Fill Game API is running"}
