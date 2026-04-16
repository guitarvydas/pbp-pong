A caveat first: Game of Life can't run in the _current_ `renderer_gpu_simple.html` because that viewer has no ping-pong infrastructure. The GLSL itself is simple — the complexity is in what the viewer needs to provide. So this is a good way to read the GLSL clearly, knowing we'll need a new viewer later.

---

## The Two Shaders

Game of Life needs exactly two shaders.

### Shader 1 — Initialization (run once)

Seeds the first texture with random noise:

```glsl
precision mediump float;

uniform vec2 u_resolution;

// A simple pseudo-random function
float rand(vec2 co) {
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution;
    float alive = step(0.5, rand(uv));   // ~50% cells start alive
    gl_FragColor = vec4(alive, alive, alive, 1.0);
}
```

### Shader 2 — Update (run every frame)

This is the one sent through the pipeline each generation:

```glsl
precision mediump float;

uniform sampler2D u_state;    // previous generation, in VRAM
uniform vec2 u_resolution;

void main() {
    vec2 uv    = gl_FragCoord.xy / u_resolution;
    vec2 px    = 1.0 / u_resolution;  // size of one texel in UV space

    // Sample all 8 neighbors
    float n  = texture2D(u_state, uv + vec2(  0.0,  px.y)).r;
    float s  = texture2D(u_state, uv + vec2(  0.0, -px.y)).r;
    float e  = texture2D(u_state, uv + vec2( px.x,   0.0)).r;
    float w  = texture2D(u_state, uv + vec2(-px.x,   0.0)).r;
    float ne = texture2D(u_state, uv + vec2( px.x,  px.y)).r;
    float nw = texture2D(u_state, uv + vec2(-px.x,  px.y)).r;
    float se = texture2D(u_state, uv + vec2( px.x, -px.y)).r;
    float sw = texture2D(u_state, uv + vec2(-px.x, -px.y)).r;

    float neighbors = n + s + e + w + ne + nw + se + sw;
    float alive     = texture2D(u_state, uv).r;

    // Conway's rules, written in plain float comparisons
    float next = 0.0;
    if (alive > 0.5) {
        if (neighbors > 1.5 && neighbors < 3.5) next = 1.0;  // survive
    } else {
        if (neighbors > 2.5 && neighbors < 3.5) next = 1.0;  // born
    }

    gl_FragColor = vec4(next, next, next, 1.0);
}
```

---

## Reading the Update Shader

A few things worth noticing as you read it:

**`px = 1.0 / u_resolution`** converts the resolution (say, 512×512) into the UV-space size of one texel (1/512 ≈ 0.00195). Adding `px.y` to a UV coordinate moves exactly one pixel north.

**`.r` on a texture sample** — the cell state is stored as a float in the red channel. `1.0` = alive, `0.0` = dead. The other three channels (g, b, a) are just along for the ride.

**Float comparisons instead of integers** — `neighbors > 1.5 && neighbors < 3.5` is the float way of saying `neighbors == 2 || neighbors == 3`. Because neighbor counts are sums of 0.0/1.0 floats, they land exactly on whole numbers, so this is safe.

**`gl_FragColor = vec4(next, next, next, 1.0)`** — writes the new state back to VRAM (into the _other_ framebuffer, the one not being read). All four channels get the same value so the display looks greyscale.

---

## What the Viewer Needs to Provide

```
Viewer sets up:
  texA, texB         — two same-size RGBA float textures in VRAM
  fboA, fboB         — two framebuffers, each attached to one texture

Init pass:
  render init shader → fboA

Each frame:
  read from texA, write to fboB   (update shader)
  draw texB to canvas              (display pass)
  swap A ↔ B

WebSocket receives new update GLSL → recompile shader, reset to init
```

The GLSL above is the entire logic. Everything else — allocation, ping-pong, the animation loop — lives in the viewer's JavaScript. That's the right separation: GLSL states the _rules_, JS manages the _memory_.