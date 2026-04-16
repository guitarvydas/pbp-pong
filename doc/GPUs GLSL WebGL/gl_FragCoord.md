It's a **built-in variable** that the GPU hardware populates automatically — you never declare it or assign it. It arrives "pre-filled" at the start of every fragment shader invocation.

---

## Where it comes from in the pipeline

There are two stages before the fragment shader runs:

**1. Vertex shader** — processes geometry (positions of triangle corners). For a full-screen shader like haiku.js uses, this is just two triangles covering the whole canvas, with corners at the screen edges.

**2. Rasterizer** — this is **fixed-function hardware** (not programmable, not a shader). It takes the triangle geometry output by the vertex shader and:

- determines which pixels fall inside the triangle
- spawns one fragment shader invocation per covered pixel
- **computes the screen-space coordinate of each pixel's center**
- stuffs that coordinate into `gl_FragCoord` before handing off to the fragment shader

So `gl_FragCoord` is produced by the rasterizer hardware and injected into each invocation automatically. You have no control over it — it simply tells each shader core "you are responsible for this pixel."

---

## What's in it exactly

`gl_FragCoord` is a `vec4`:

```glsl
gl_FragCoord.x   // pixel column, in pixels, from left edge
gl_FragCoord.y   // pixel row, in pixels, from bottom edge (not top!)
gl_FragCoord.z   // depth value (0.0–1.0), used for 3D z-buffering
gl_FragCoord.w   // 1/w from clip space, rarely used in 2D work
```

For a 512×512 canvas, `gl_FragCoord.xy` ranges from `(0.5, 0.5)` at the bottom-left pixel to `(511.5, 511.5)` at the top-right. The 0.5 offset is because coordinates refer to **pixel centers**, not pixel corners — a hardware convention.

---

## Why divide by `u_resolution`

```glsl
vec2 uv = gl_FragCoord.xy / u_resolution;
```

This converts from **pixel space** (0–511) to **UV space** (0.0–1.0). UV space is what `texture2D()` expects — it's resolution-independent so the same shader works on any canvas size. It's also where (0,0) is bottom-left and (1,1) is top-right, which maps cleanly to texture coordinates.

---

## The hardware picture end to end

```
Vertex shader          Rasterizer             Fragment shader
(programmable)         (fixed hardware)       (programmable)

triangle corners   →   which pixels?      →   gl_FragCoord = (x, y, z, w)
                        spawn one                             ↓
                        invocation                    your GLSL runs
                        per pixel
```

The rasterizer is the thing that turns geometry into the **embarrassingly parallel** problem — one independent invocation per pixel — that makes GPUs so effective. `gl_FragCoord` is its one message to each invocation: "here is your pixel."