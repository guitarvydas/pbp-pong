const WebSocket = require('ws');

const PORT = 8080;
const wss = new WebSocket.Server({ port: PORT });

// Game constants
const GAME_WIDTH = 800;
const GAME_HEIGHT = 600;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;
const BALL_SIZE = 10;
const PADDLE_SPEED = 8;
const BALL_SPEED = 5;

// Game state (MODEL)
let gameState = {
  ball: {
    x: GAME_WIDTH / 2,
    y: GAME_HEIGHT / 2,
    dx: BALL_SPEED * (Math.random() > 0.5 ? 1 : -1),
    dy: BALL_SPEED * (Math.random() > 0.5 ? 1 : -1)
  },
  leftPaddle: {
    x: 20,
    y: GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2,
    height: PADDLE_HEIGHT
  },
  rightPaddle: {
    x: GAME_WIDTH - 20 - PADDLE_WIDTH,
    y: GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2,
    height: PADDLE_HEIGHT
  },
  score: {
    left: 0,
    right: 0
  }
};

// Controller state (from browser)
let controls = {
  leftUp: false,
  leftDown: false,
  rightUp: false,
  rightDown: false
};

// Broadcast state to all connected clients
function broadcastState() {
  const stateMessage = JSON.stringify({
    type: 'state',
    data: {
      ball: gameState.ball,
      leftPaddle: gameState.leftPaddle,
      rightPaddle: gameState.rightPaddle,
      score: gameState.score,
      gameWidth: GAME_WIDTH,
      gameHeight: GAME_HEIGHT,
      paddleWidth: PADDLE_WIDTH,
      ballSize: BALL_SIZE
    }
  });

  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(stateMessage);
    }
  });
}

// Game loop - updates model based on physics and controls
function gameLoop() {
  // Update paddle positions based on controls
  if (controls.leftUp && gameState.leftPaddle.y > 0) {
    gameState.leftPaddle.y -= PADDLE_SPEED;
  }
  if (controls.leftDown && gameState.leftPaddle.y < GAME_HEIGHT - PADDLE_HEIGHT) {
    gameState.leftPaddle.y += PADDLE_SPEED;
  }
  if (controls.rightUp && gameState.rightPaddle.y > 0) {
    gameState.rightPaddle.y -= PADDLE_SPEED;
  }
  if (controls.rightDown && gameState.rightPaddle.y < GAME_HEIGHT - PADDLE_HEIGHT) {
    gameState.rightPaddle.y += PADDLE_SPEED;
  }

  // Update ball position
  gameState.ball.x += gameState.ball.dx;
  gameState.ball.y += gameState.ball.dy;

  // Ball collision with top and bottom walls
  if (gameState.ball.y <= 0 || gameState.ball.y >= GAME_HEIGHT - BALL_SIZE) {
    gameState.ball.dy *= -1;
  }

  // Ball collision with paddles
  // Left paddle
  if (gameState.ball.x <= gameState.leftPaddle.x + PADDLE_WIDTH &&
      gameState.ball.x >= gameState.leftPaddle.x &&
      gameState.ball.y + BALL_SIZE >= gameState.leftPaddle.y &&
      gameState.ball.y <= gameState.leftPaddle.y + PADDLE_HEIGHT) {
    gameState.ball.dx = Math.abs(gameState.ball.dx);
    // Add some variation based on where it hits the paddle
    const hitPos = (gameState.ball.y - gameState.leftPaddle.y) / PADDLE_HEIGHT;
    gameState.ball.dy = (hitPos - 0.5) * BALL_SPEED * 2;
  }

  // Right paddle
  if (gameState.ball.x + BALL_SIZE >= gameState.rightPaddle.x &&
      gameState.ball.x <= gameState.rightPaddle.x + PADDLE_WIDTH &&
      gameState.ball.y + BALL_SIZE >= gameState.rightPaddle.y &&
      gameState.ball.y <= gameState.rightPaddle.y + PADDLE_HEIGHT) {
    gameState.ball.dx = -Math.abs(gameState.ball.dx);
    // Add some variation based on where it hits the paddle
    const hitPos = (gameState.ball.y - gameState.rightPaddle.y) / PADDLE_HEIGHT;
    gameState.ball.dy = (hitPos - 0.5) * BALL_SPEED * 2;
  }

  // Scoring - ball goes out of bounds
  if (gameState.ball.x < 0) {
    gameState.score.right++;
    resetBall();
    console.log(`Score: Left ${gameState.score.left} - Right ${gameState.score.right}`);
  } else if (gameState.ball.x > GAME_WIDTH) {
    gameState.score.left++;
    resetBall();
    console.log(`Score: Left ${gameState.score.left} - Right ${gameState.score.right}`);
  }

  // Broadcast updated state
  broadcastState();
}

function resetBall() {
  gameState.ball.x = GAME_WIDTH / 2;
  gameState.ball.y = GAME_HEIGHT / 2;
  gameState.ball.dx = BALL_SPEED * (Math.random() > 0.5 ? 1 : -1);
  gameState.ball.dy = BALL_SPEED * (Math.random() > 0.5 ? 1 : -1);
}

// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log('Client connected');

  // Send initial state
  ws.send(JSON.stringify({
    type: 'state',
    data: {
      ball: gameState.ball,
      leftPaddle: gameState.leftPaddle,
      rightPaddle: gameState.rightPaddle,
      score: gameState.score,
      gameWidth: GAME_WIDTH,
      gameHeight: GAME_HEIGHT,
      paddleWidth: PADDLE_WIDTH,
      ballSize: BALL_SIZE
    }
  }));

  // Handle incoming messages (controller input)
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      if (data.type === 'controls') {
        controls = { ...controls, ...data.data };
      }
    } catch (e) {
      console.error('Error parsing message:', e);
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Start game loop (60 FPS)
setInterval(gameLoop, 1000 / 60);

console.log(`Pong game server running on ws://localhost:${PORT}`);
console.log('Controls:');
console.log('  Left paddle: W (up), S (down)');
console.log('  Right paddle: Arrow Up, Arrow Down');
