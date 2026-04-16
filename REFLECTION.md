In classic Pong, the ball is essentially a 2D vector (position + velocity) that reflects based on what it hits:

**Paddle**
The ball reverses its horizontal direction (dx = -dx). In the original arcade version, the angle of reflection also varies depending on *where* on the paddle the ball strikes — hitting near the edges sends it off at a steeper angle, while hitting the centre returns it more flatly. This gives the player some control over trajectory.

**Roof and Floor**
The ball reverses its vertical direction (dy = -dy) — a simple mirror reflection off the horizontal boundary.

**Walls (left and right sides)**
These are *scoring* boundaries, not reflective surfaces. If the ball reaches the left wall, the right player scores a point (and vice versa), and the ball is reset to the centre for the next serve.

**Summary table:**

| Surface | Effect |
|---|---|
| Paddle | Reverse horizontal (dx), optionally adjust angle by hit position |
| Roof / Floor | Reverse vertical (dy) |
| Left / Right wall | Score a point, reset ball |

The core mechanic is deliberately simple — just sign-flipping a velocity component — but the paddle angle variation is what gives Pong its skill ceiling and strategic depth.
