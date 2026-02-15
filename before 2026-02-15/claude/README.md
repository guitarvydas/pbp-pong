# Pong Game - Refactored Client-Server Architecture

## Architecture Overview

This is a refactored version where **all motion logic lives on the server**, and the **client is purely a display Part** (slave) with keyboard interface.

### Key Design Principles

1. **Server owns the timer** - Game loop runs at 60 FPS on server
2. **Server owns all motion logic** - Ball physics, paddle movement, collision detection, scoring
3. **Client is a "dumb terminal"** - Only displays what the server tells it and sends keyboard input
4. **Clear API boundaries** - Discrete update commands, not continuous state broadcast
5. **Client maintains local display state** - Updated only when server sends position updates

## API Specification

### Client Input API (Primary)

Messages sent FROM server TO client:

1. **ball_position** - Update ball position
   ```json
   { "type": "ball_position", "x": 400, "y": 300 }
   ```

2. **left_paddle_position** - Update left paddle position
   ```json
   { "type": "left_paddle_position", "x": 20, "y": 250 }
   ```

3. **right_paddle_position** - Update right paddle position
   ```json
   { "type": "right_paddle_position", "x": 770, "y": 250 }
   ```

4. **score_update** - Update score
   ```json
   { "type": "score_update", "left": 3, "right": 5 }
   ```

5. **game_over** - Toggle game over screen
   ```json
   { "type": "game_over", "gameOver": true, "winner": "left" }
   ```

### Client Input API (Secondary - Initialization)

Configuration sent once on connection:

```json
{
  "type": "init",
  "gameWidth": 800,
  "gameHeight": 600,
  "paddleWidth": 10,
  "paddleHeight": 100,
  "ballSize": 10
}
```

### Client Output API

Messages sent FROM client TO server:

1. **left_paddle_up** - Step left paddle up
2. **left_paddle_down** - Step left paddle down
3. **right_paddle_up** - Step right paddle up
4. **right_paddle_down** - Step right paddle down
5. **reset_game** - Reset game after game over

```json
{ "type": "paddle_command", "command": "left_paddle_up" }
{ "type": "reset_game" }
```

## Client Responsibilities

The client is a **display Part** that:

1. **Maintains local state** of movable objects (ball, paddles)
2. **Displays**:
   - Center line
   - Current score
   - Ball at current position
   - Paddles at current positions
   - Game over screen
3. **Keyboard interface**:
   - W/S for left paddle
   - Arrow Up/Down for right paddle
   - R to reset after game over
4. **Update cycle**: When server sends position update → erase old → redraw at new position

## Server Responsibilities

The server owns:

1. **Game timer** - 60 FPS game loop
2. **All motion logic**:
   - Ball velocity and position updates
   - Paddle position updates (based on client commands)
   - Collision detection (walls, paddles)
   - Scoring logic
   - Win condition checking
3. **Ball speed handling** - All physics calculations
4. **Authoritative state** - Server is the single source of truth

## Setup and Running

### Prerequisites

```bash
npm install ws
```

### Start Server

```bash
node pong-server-refactored.js
```

You should see:
```
Pong game server running on ws://localhost:8080
Server controls all motion logic
Clients are display-only interfaces
```

### Open Client

Open `pong-client-refactored.html` in a web browser.

Multiple clients can connect simultaneously - they all see the same game state.

## Key Differences from Original

| Aspect | Original | Refactored |
|--------|----------|------------|
| **Motion Logic** | Mixed (some on client) | 100% on server |
| **Timer** | Server + client rendering | Server only |
| **Client Role** | View + partial control | Pure display Part |
| **State Updates** | Full state broadcast | Discrete position updates |
| **Client State** | Receives full state | Maintains local state, updates on command |
| **API** | Generic state sync | Clear input/output API |

## Protocol Flow

### Game Start

1. Client connects to server
2. Server sends `init` message with game dimensions
3. Server sends initial positions for ball and paddles
4. Server sends initial score (0-0)
5. Server starts game loop (if first client)

### Normal Gameplay

1. User presses key (e.g., 'W')
2. Client sends `paddle_command: left_paddle_up`
3. Server updates left paddle position
4. Server sends `left_paddle_position` to all clients
5. Each client erases old paddle, draws at new position

Every frame (60 FPS):
1. Server updates ball position based on velocity
2. Server sends `ball_position` to all clients
3. Clients erase old ball, draw at new position

### Scoring

1. Server detects ball out of bounds
2. Server increments score
3. Server sends `score_update` to clients
4. Clients update score display
5. Server checks win condition
6. If won: Server sends `game_over` message
7. Clients display game over screen

### Game Reset

1. User presses 'R' when game is over
2. Client sends `reset_game` command
3. Server resets all state
4. Server sends updated positions and score to all clients
5. Server sends `game_over: false` to hide overlay
6. Game continues

## Design Decisions Addressed

### ✅ All motion logic on server
Ball physics, collision detection, and paddle movement calculations all happen server-side.

### ✅ Client is just a Part
Client has no game logic - it's purely a rendering surface and keyboard interface.

### ✅ Clear API boundaries
- Primary API: position updates and game state
- Secondary API: initialization/configuration
- Output API: discrete paddle step commands

### ✅ Server owns timer
Game loop runs at 60 FPS on server. Client has no timer.

### ✅ Client maintains state
Client keeps (x,y) of ball and paddles, updates only when server commands.

### ✅ Ball speed handled by server
All velocity calculations, speed adjustments, and physics are server-side.

### ✅ Erase and redraw pattern
When server sends position update, client erases old object and redraws at new position.

## Potential Enhancements

Based on your requirements, you might want to consider:

1. **Network resilience**:
   - Message sequence numbers to detect drops
   - Periodic full state sync to recover from drift
   - Client-side prediction with server reconciliation

2. **Game modes**:
   - Single player vs AI (server controls one paddle)
   - Tournament mode (best of N games)
   - Different difficulty levels

3. **Visual effects**:
   - Server could send collision event messages
   - Client could add particle effects, sounds, etc.

4. **Scalability**:
   - Multiple game rooms
   - Spectator mode (receive updates but can't control)
   - Replay recording/playback

## Testing the Architecture

To verify the client is truly a "dumb display":

1. Open browser dev console while playing
2. Modify `clientState.ball.x = 100` in console
3. Ball position should snap back on next server update
4. This proves client state is subordinate to server

## Conclusion

This architecture ensures:
- ✅ Single source of truth (server)
- ✅ Client can't cheat (no local physics)
- ✅ Deterministic gameplay (server-authoritative)
- ✅ Clean separation of concerns
- ✅ Easy to add spectator mode
- ✅ Network latency isolated to input lag (not physics drift)

The client is now truly just a Part - a display and keyboard interface with no game logic.
