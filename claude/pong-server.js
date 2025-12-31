const WebSocket = require('ws');

const PORT = 8080;
const wss = new WebSocket.Server({ port: PORT });

// Game constants
const GAME_WIDTH = 800;
const GAME_HEIGHT = 600;
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;
const BALL_SIZE = 10;
const PADDLE_STEP = 8;
const BALL_SPEED_X = 5;
const BALL_SPEED_Y = 5;
const WINNING_SCORE = 11;

// Game state (SERVER OWNS ALL STATE)
let gameState = {
  ball: {
    x: GAME_WIDTH / 2,
    y: GAME_HEIGHT / 2,
    dx: BALL_SPEED_X,
    dy: BALL_SPEED_Y
  },
  leftPaddle: {
    x: 20,
    y: GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2
  },
  rightPaddle: {
    x: GAME_WIDTH - 20 - PADDLE_WIDTH,
    y: GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2
  },
  score: {
    left: 0,
    right: 0
  },
  gameOver: false,
  winner: null
};

// Track connected clients
let clients = new Set();
let gameLoopInterval = null;

// Send initialization data to client (secondary API)
function sendInitData(ws) {
  ws.send(JSON.stringify({
    type: 'init',
    gameWidth: GAME_WIDTH,
    gameHeight: GAME_HEIGHT,
    paddleWidth: PADDLE_WIDTH,
    paddleHeight: PADDLE_HEIGHT,
    ballSize: BALL_SIZE
  }));
}

// Send ball position update (primary API)
function sendBallPosition(x, y) {
  const message = JSON.stringify({
    type: 'ball_position',
    x: x,
    y: y
  });
  broadcast(message);
}

// Send left paddle position update (primary API)
function sendLeftPaddlePosition(x, y) {
  const message = JSON.stringify({
    type: 'left_paddle_position',
    x: x,
    y: y
  });
  broadcast(message);
}

// Send right paddle position update (primary API)
function sendRightPaddlePosition(x, y) {
  const message = JSON.stringify({
    type: 'right_paddle_position',
    x: x,
    y: y
  });
  broadcast(message);
}

// Send score update (primary API)
function sendScoreUpdate(leftScore, rightScore) {
  const message = JSON.stringify({
    type: 'score_update',
    left: leftScore,
    right: rightScore
  });
  broadcast(message);
}

// Send game over screen state (primary API)
function sendGameOver(isGameOver, winner) {
  const message = JSON.stringify({
    type: 'game_over',
    gameOver: isGameOver,
    winner: winner
  });
  broadcast(message);
}

// Broadcast message to all connected clients
function broadcast(message) {
  clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// Game loop - SERVER OWNS THE TIMER
function gameLoop() {
  if (gameState.gameOver) {
    return; // Don't update if game is over
  }

  // Update ball position based on velocity
  gameState.ball.x += gameState.ball.dx;
  gameState.ball.y += gameState.ball.dy;

  // Ball collision with top and bottom walls
  if (gameState.ball.y <= 0 || gameState.ball.y >= GAME_HEIGHT - BALL_SIZE) {
    gameState.ball.dy *= -1;
  }

  // Ball collision with left paddle
  if (gameState.ball.x <= gameState.leftPaddle.x + PADDLE_WIDTH &&
      gameState.ball.x >= gameState.leftPaddle.x &&
      gameState.ball.y + BALL_SIZE >= gameState.leftPaddle.y &&
      gameState.ball.y <= gameState.leftPaddle.y + PADDLE_HEIGHT) {
    gameState.ball.dx = Math.abs(gameState.ball.dx);
    // Add variation based on where ball hits paddle
    const hitPos = (gameState.ball.y - gameState.leftPaddle.y) / PADDLE_HEIGHT;
    gameState.ball.dy = (hitPos - 0.5) * BALL_SPEED_Y * 2;
  }

  // Ball collision with right paddle
  if (gameState.ball.x + BALL_SIZE >= gameState.rightPaddle.x &&
      gameState.ball.x <= gameState.rightPaddle.x + PADDLE_WIDTH &&
      gameState.ball.y + BALL_SIZE >= gameState.rightPaddle.y &&
      gameState.ball.y <= gameState.rightPaddle.y + PADDLE_HEIGHT) {
    gameState.ball.dx = -Math.abs(gameState.ball.dx);
    // Add variation based on where ball hits paddle
    const hitPos = (gameState.ball.y - gameState.rightPaddle.y) / PADDLE_HEIGHT;
    gameState.ball.dy = (hitPos - 0.5) * BALL_SPEED_Y * 2;
  }

  // Scoring - ball goes out of bounds
  if (gameState.ball.x < 0) {
    gameState.score.right++;
    console.log(`Score: Left ${gameState.score.left} - Right ${gameState.score.right}`);
    sendScoreUpdate(gameState.score.left, gameState.score.right);
    
    // Check for win condition
    if (gameState.score.right >= WINNING_SCORE) {
      gameState.gameOver = true;
      gameState.winner = 'right';
      sendGameOver(true, 'right');
      console.log('Game Over! Right player wins!');
    } else {
      resetBall();
    }
  } else if (gameState.ball.x > GAME_WIDTH) {
    gameState.score.left++;
    console.log(`Score: Left ${gameState.score.left} - Right ${gameState.score.right}`);
    sendScoreUpdate(gameState.score.left, gameState.score.right);
    
    // Check for win condition
    if (gameState.score.left >= WINNING_SCORE) {
      gameState.gameOver = true;
      gameState.winner = 'left';
      sendGameOver(true, 'left');
      console.log('Game Over! Left player wins!');
    } else {
      resetBall();
    }
  }

  // Send updated ball position to clients
  sendBallPosition(gameState.ball.x, gameState.ball.y);
}

function resetBall() {
  gameState.ball.x = GAME_WIDTH / 2;
  gameState.ball.y = GAME_HEIGHT / 2;
  gameState.ball.dx = BALL_SPEED_X * (Math.random() > 0.5 ? 1 : -1);
  gameState.ball.dy = BALL_SPEED_Y * (Math.random() > 0.5 ? 1 : -1);
  
  // Send new ball position
  sendBallPosition(gameState.ball.x, gameState.ball.y);
}

function resetGame() {
  gameState.score.left = 0;
  gameState.score.right = 0;
  gameState.gameOver = false;
  gameState.winner = null;
  
  // Reset positions
  gameState.leftPaddle.y = GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2;
  gameState.rightPaddle.y = GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2;
  
  // Send updates to clients
  sendScoreUpdate(0, 0);
  sendGameOver(false, null);
  sendLeftPaddlePosition(gameState.leftPaddle.x, gameState.leftPaddle.y);
  sendRightPaddlePosition(gameState.rightPaddle.x, gameState.rightPaddle.y);
  
  resetBall();
  console.log('Game reset');
}

// Handle paddle movement commands from client
function handlePaddleCommand(command) {
  if (gameState.gameOver) {
    return; // Ignore paddle commands if game is over
  }

  switch(command) {
    case 'left_paddle_up':
      if (gameState.leftPaddle.y > 0) {
        gameState.leftPaddle.y -= PADDLE_STEP;
        if (gameState.leftPaddle.y < 0) gameState.leftPaddle.y = 0;
        sendLeftPaddlePosition(gameState.leftPaddle.x, gameState.leftPaddle.y);
      }
      break;
      
    case 'left_paddle_down':
      if (gameState.leftPaddle.y < GAME_HEIGHT - PADDLE_HEIGHT) {
        gameState.leftPaddle.y += PADDLE_STEP;
        if (gameState.leftPaddle.y > GAME_HEIGHT - PADDLE_HEIGHT) {
          gameState.leftPaddle.y = GAME_HEIGHT - PADDLE_HEIGHT;
        }
        sendLeftPaddlePosition(gameState.leftPaddle.x, gameState.leftPaddle.y);
      }
      break;
      
    case 'right_paddle_up':
      if (gameState.rightPaddle.y > 0) {
        gameState.rightPaddle.y -= PADDLE_STEP;
        if (gameState.rightPaddle.y < 0) gameState.rightPaddle.y = 0;
        sendRightPaddlePosition(gameState.rightPaddle.x, gameState.rightPaddle.y);
      }
      break;
      
    case 'right_paddle_down':
      if (gameState.rightPaddle.y < GAME_HEIGHT - PADDLE_HEIGHT) {
        gameState.rightPaddle.y += PADDLE_STEP;
        if (gameState.rightPaddle.y > GAME_HEIGHT - PADDLE_HEIGHT) {
          gameState.rightPaddle.y = GAME_HEIGHT - PADDLE_HEIGHT;
        }
        sendRightPaddlePosition(gameState.rightPaddle.x, gameState.rightPaddle.y);
      }
      break;
  }
}

// Start game loop when first client connects
function startGameLoop() {
  if (!gameLoopInterval) {
    gameLoopInterval = setInterval(gameLoop, 1000 / 60); // 60 FPS
    console.log('Game loop started');
  }
}

// Stop game loop when last client disconnects
function stopGameLoop() {
  if (gameLoopInterval && clients.size === 0) {
    clearInterval(gameLoopInterval);
    gameLoopInterval = null;
    console.log('Game loop stopped');
  }
}

// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log('Client connected');
  clients.add(ws);
  
  // Send initialization data (secondary API)
  sendInitData(ws);
  
  // Send current game state
  ws.send(JSON.stringify({
    type: 'ball_position',
    x: gameState.ball.x,
    y: gameState.ball.y
  }));
  ws.send(JSON.stringify({
    type: 'left_paddle_position',
    x: gameState.leftPaddle.x,
    y: gameState.leftPaddle.y
  }));
  ws.send(JSON.stringify({
    type: 'right_paddle_position',
    x: gameState.rightPaddle.x,
    y: gameState.rightPaddle.y
  }));
  ws.send(JSON.stringify({
    type: 'score_update',
    left: gameState.score.left,
    right: gameState.score.right
  }));
  ws.send(JSON.stringify({
    type: 'game_over',
    gameOver: gameState.gameOver,
    winner: gameState.winner
  }));
  
  // Start game loop if this is first client
  startGameLoop();

  // Handle incoming messages from client (output API)
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      
      if (data.type === 'paddle_command') {
        handlePaddleCommand(data.command);
      } else if (data.type === 'reset_game') {
        resetGame();
      }
    } catch (e) {
      console.error('Error parsing message:', e);
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
    clients.delete(ws);
    stopGameLoop();
  });
});

console.log(`Pong game server running on ws://localhost:${PORT}`);
console.log('Server controls all motion logic');
console.log('Clients are display-only interfaces');
