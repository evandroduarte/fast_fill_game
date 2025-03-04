# Fast Fill Game

A simple 2-player real-time game where players compete to fill a grid with their color. The player with the most squares at the end wins.

## Game

[Fill Game Website](http://fill-game-lb-1845414604.us-east-2.elb.amazonaws.com/)

## Project Structure

The project consists of two main components:

1. **Frontend**: React application built with Vite and TypeScript
2. **Backend**: Python FastAPI application with WebSocket support

## Running the Backend

### Prerequisites
- Docker
- Docker Compose

### Installation

```bash
cd backend

docker-compose up --build
```

The backend server will start on `http://localhost:8000`.

## Running the Frontend

### Prerequisites
- Docker
- Docker Compose

### Installation

```bash
cd frontend

docker-compose up --build
```

The frontend development server will start, typically on `http://localhost:8080`.

## How to Play

1. Open two browser windows/tabs and navigate to the frontend URL in both
2. The first player to join will be assigned the red color
3. The second player will be assigned the blue color
4. The game starts automatically when both players have joined
5. Click on empty squares to fill them with your color
6. The game ends when the grid is full
7. The player with the most squares wins

## Technologies Used

- **Frontend**: React, TypeScript, Vite, WebSocket API
- **Backend**: Python, FastAPI, WebSockets, asyncio

## AI Tools Used

- GitHub Copilot for code completion and suggestions
- Claude.ai for architecture planning and debugging assistance
