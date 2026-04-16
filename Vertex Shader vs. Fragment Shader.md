Because the two shaders solve fundamentally different problems — one operates on **geometry**, the other on **pixels** — and keeping them separate maps efficiently onto the hardware.

---

## The historical reason: what GPUs were built to do

The original job of a GPU was rendering **3D scenes** — objects made of triangles floating in 3D space, projected onto a 2D screen, with textures and lighting applied. That naturally breaks into two distinct problems:

**Problem 1: Where do things land on screen?** A triangle in 3D space has corners (vertices). You need to transform each corner through model → world → camera → screen space. This involves matrix multiplications — one per vertex. Scenes have thousands of triangles but relatively few vertices compared to pixels.

**Problem 2: What color is each pixel?** Once you know which pixels a triangle covers, you need to compute a color for each one — sampling textures, computing lighting, applying effects. Scenes have millions of pixels per frame.

These two problems have very different **data ratios**, so the GPU handles them in sequence.

---

## The pipeline as a funnel

```
3D vertices (thousands)
      ↓
 Vertex shader         ← runs once per vertex
      ↓
 Rasterizer            ← expands vertices into pixels (fixed hardware)
      ↓
 Fragment shader       ← runs once per pixel (millions)
      ↓
 Framebuffer
```

The rasterizer is the expansion stage — it takes a small number of transformed vertices and generates a much larger number of pixel-sized fragments. This funnel shape is why the two shaders exist as separate stages.

---

## What each shader actually does

**Vertex shader** — answers "where?"

```glsl
// Minimal vertex shader
attribute vec2 a_position;   // corner of a triangle, in your coordinate system

void main() {
    gl_Position = vec4(a_position, 0.0, 1.0);  // output: where on screen
}
```

It transforms coordinates. For a full-screen haiku.js quad, this is almost trivial — just pass the corners through. In a 3D game it involves multiplying by model, view, and projection matrices.

**Fragment shader** — answers "what color?"

```glsl
void main() {
    // gl_FragCoord already tells us which pixel we are
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);  // output: color of this pixel
}
```

---

## Why Forth Haiku barely notices the vertex shader

For generative 2D shaders, the vertex shader is just boilerplate — two triangles covering the whole screen, no transformation needed. All the interesting work is in the fragment shader. The vertex shader is effectively saying "draw a canvas," and the fragment shader is saying "here is what every pixel of that canvas looks like."

This is why haiku.js can get away with a fixed, trivial vertex shader and let the Forth programmer focus entirely on the fragment side. The vertex/fragment split was designed for 3D, but 2D generative shader work exploits the fragment stage while treating the vertex stage as invisible plumbing.

---

## The deeper hardware reason

Keeping them separate lets the GPU apply different optimizations to each stage:

- Vertex work is **sequential per vertex**, small data set, can be pipelined aggressively
- Fragment work is **embarrassingly parallel** across millions of independent pixels, needs massive core count
- The rasterizer between them is fixed-function silicon — extremely fast precisely because it's _not_ programmable

A single unified "do everything" shader would be harder to optimize at the hardware level. The staged pipeline lets the GPU allocate the right kind of resources to each problem.