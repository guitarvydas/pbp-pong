I want to write a Pong-like game that works on an MVC basis. The view is in the browser, the controller is in the browser, the model is on the command line that sends commands to the view via websockets and receives controller information via websockets.

---

when I run node pong-server.js it appears that the game freeruns (included below). Why?

---

the arrow keys and W,S don't seem to do anything

---

Refactor the code so that all motion logic is moved to the server. The client is just a Part.

The client's main input API contains inputs for:
- ball p(x,y)
- game over screen on/off (displays score and who won)
- left paddle (x,y)
- right paddle (x,y)
- update score

It has a secondary set of API inputs:
- gameWidth
- gameHeight
- paddle size (height, width)
- ball size

Ball speed issues are handled in the server.

The server has its own timer, the client is only a slave which is only a display and a keyboard interface.

The client output API is
- left paddle up/down step
- right paddle up/down step

The client keeps the (x,y) state of the movable objects, like ball, left paddle, right paddle.
The client displays the center line and the current score.
When the server sends an update to any position, the internal state of the client is updated, the movable objects are erased and re-drawn at the current state.

Have I missed discussing any requirements or issues?

