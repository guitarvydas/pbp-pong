# Pong Game - MVC Architecture with WebSockets

A classic Pong game demonstrating MVC (Model-View-Controller) architecture where:
- **Model**: Node.js server (command line) - handles game logic
- **View**: Browser (HTML Canvas) - renders the game
- **Controller**: Browser (keyboard input) - captures player input

Communication between Model and View/Controller happens via WebSockets.

## Architecture

```
┌─────────────────────────────────────┐
│         Browser (Client)            │
│                                     │
│  ┌─────────┐      ┌──────────────┐ │
│  │  VIEW   │      │ CONTROLLER   │ │
│  │ Canvas  │      │  Keyboard    │ │
│  │Rendering│      │    Input     │ │
│  └────┬────┘      └──────┬───────┘ │
│       │                  │         │
│       └──────────┬───────┘         │
│                  │                 │
└──────────────────┼─────────────────┘
                   │ WebSocket
                   │
┌──────────────────┼─────────────────┐
│                  │                 │
│            ┌─────▼─────┐           │
│            │   MODEL   │           │
│            │Game Logic │           │
│            │  Server   │           │
│            └───────────┘           │
│                                    │
│    Node.js Server (Command Line)   │
└────────────────────────────────────┘
```

## Prerequisites

- Node.js (v12 or higher)
- npm (comes with Node.js)
- A modern web browser

## Setup

1. Install the WebSocket dependency:
```bash
npm install ws
```

## Running the Game

1. **Start the Model (Server)**:
```bash
node pong-server.js
```

You should see:
```
Pong game server running on ws://localhost:8080
Controls:
  Left paddle: W (up), S (down)
  Right paddle: Arrow Up, Arrow Down
```

The server will also display score updates in the terminal as the game progresses.

2. **Open the View/Controller (Browser)**:
   - Open `pong-client.html` in your web browser
   - You can open it directly (file://) or serve it with a simple HTTP server

3. **Play the Game**:
   - Left paddle: W (up), S (down)
   - Right paddle: Arrow Up, Arrow Down

## How It Works

### Model (pong-server.js)
- Maintains the authoritative game state (ball position, paddle positions, scores)
- Runs game loop at 60 FPS
- Handles physics (collisions, ball movement)
- Receives controller input from browser via WebSocket
- Broadcasts state updates to all connected clients

### View (pong-client.html - rendering)
- Receives game state updates from server via WebSocket
- Renders the current state on HTML Canvas
- Updates score display

### Controller (pong-client.html - input)
- Captures keyboard events
- Maintains local control state
- Sends control updates to server via WebSocket

## Features

- Real MVC separation with WebSocket communication
- Smooth 60 FPS gameplay
- Collision detection with dynamic ball angles
- Score tracking
- Auto-reconnect on disconnect
- Support for multiple simultaneous viewers

## Customization

You can modify game parameters in `pong-server.js`:
- `GAME_WIDTH`, `GAME_HEIGHT`: Canvas dimensions
- `PADDLE_SPEED`: How fast paddles move
- `BALL_SPEED`: Initial ball speed
- `PADDLE_HEIGHT`: Size of paddles

## Troubleshooting

- **Can't connect**: Make sure the server is running on port 8080
- **Port in use**: Change the PORT constant in pong-server.js
- **Laggy gameplay**: The model runs on your local machine, so lag should be minimal. Check your CPU usage.
