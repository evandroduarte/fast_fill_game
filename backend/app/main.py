from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict
import asyncio

from app.game import Game, CellColor

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
        # Add the player to the game
        try:
            player_color = game.add_player(client_id)
            connected_clients[client_id] = websocket

            # Inform player of their color
            await websocket.send_text(json.dumps({
                "type": "player_assign",
                "color": player_color
            }))

            # Send initial game state
            await websocket.send_text(json.dumps({
                "type": "game_state",
                "state": game.get_state(client_id)
            }))

            # Broadcast game state to all players
            for cid, ws in connected_clients.items():
                if cid != client_id:  # Don't send to self again
                    await ws.send_text(json.dumps({
                        "type": "game_state",
                        "state": game.get_state(cid)
                    }))

        except ValueError as e:
            # Game is full
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": str(e)
            }))
            await websocket.close()
            return

        # Handle incoming messages from this client
        while True:
            data = await websocket.receive_text()
            action = json.loads(data)

            if action["type"] == "cell_click":
                player_color = game.players.get(client_id)
                if (player_color and
                    player_color == action["color"] and
                    game.status == "playing"):

                    success = game.update_cell(
                        action["row"],
                        action["col"],
                        CellColor(player_color)
                    )

                    if success:
                        # Broadcast updated game state to all players
                        for cid, ws in connected_clients.items():
                            await ws.send_text(json.dumps({
                                "type": "game_state",
                                "state": game.get_state(cid)
                            }))

    except WebSocketDisconnect:
        # Clean up when client disconnects
        if client_id in connected_clients:
            del connected_clients[client_id]
        game.remove_player(client_id)

        # Inform remaining players about the state change
        for cid, ws in connected_clients.items():
            await ws.send_text(json.dumps({
                "type": "game_state",
                "state": game.get_state(cid)
            }))

    except Exception as e:
        print(f"Error: {e}")
        # Clean up in case of error
        if client_id in connected_clients:
            del connected_clients[client_id]
        game.remove_player(client_id)

@app.get("/")
async def root():
    return {"message": "Fast Fill Game API is running"}
