Both, at different levels. There are actually two different things called "uniforms" worth distinguishing.

---

## Plain Uniforms (what haiku.js uses)

```glsl
uniform float time_val;
uniform vec2 u_resolution;
uniform sampler2D u_state;
```

These are individual declared variables. The **hardware has a fixed maximum** — a limited number of "uniform slots" per shader stage. The GPU driver exposes this limit and you can query it:

```javascript
gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS)    // typically 128-256
gl.getParameter(gl.MAX_FRAGMENT_UNIFORM_VECTORS)  // typically 128-256
```

Each `vec4` (or `float`, `mat4`, etc.) consumes some number of these slots. The **software declares which ones it uses** in the GLSL source — the compiler then allocates them into the constant buffer automatically. You don't manually specify sizes or offsets. The driver handles packing.

So: hardware fixes the _ceiling_, software declares _what goes in it_, driver handles _layout_.

---

## Uniform Buffer Objects (UBOs) — WebGL 2 only

This is the more explicit version, not used in haiku.js:

```glsl
uniform CameraData {
    mat4 projection;
    mat4 view;
    vec3 position;
};
```

Here the **software explicitly declares the block structure and its size**. You allocate a buffer of a specific byte size in VRAM and bind it. This gives you more control and better performance when sharing uniforms across multiple shaders. The hardware still has a maximum UBO size (queryable as `gl.MAX_UNIFORM_BLOCK_SIZE`, typically 16KB–64KB).

---

## The Sampler Is Different

`sampler2D` is a special case — it doesn't actually store texture data in the uniform buffer at all. It consumes a **texture unit slot** (a separate hardware resource), and the uniform just holds an integer index pointing to that slot. The texture data itself lives elsewhere in VRAM entirely.

```
Uniform buffer  →  holds: float, vec2, mat4, etc.   (small constant data)
Texture units   →  hold: sampler handles             (indexes into VRAM textures)
VRAM            →  holds: the actual texture pixels  (large data)
```

---

## The Practical Limit That Matters for Forth Haiku

For simple generative shaders the uniform limit is never a concern — you're typically using just 2-3 uniforms (`time`, `resolution`, maybe `u_state`). The constraint that actually bites is the **texture unit count** (`gl.MAX_TEXTURE_IMAGE_UNITS`, typically 16), which limits how many textures you can read in a single shader pass. For ping-pong Game of Life you only need one, so you're well within budget.