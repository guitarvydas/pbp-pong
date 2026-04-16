Good news — there's an excellent video that's exactly what you're looking for, plus a few supporting resources.

---

## Video to Watch First

**Branch Education — "How do Graphics Cards Work?"** (28 min, YouTube) `https://youtu.be/h9Z4oGN89MU`

It uses detailed 3D animations to physically explore the architecture inside an actual GPU chip (the RTX 3090 / GA102), tracing how tens of trillions of calculations per second are organized. This is the clearest visual treatment of the hardware I know of.

**Follow-up: Kayvon Fatahalian — Stanford CS149 (Parallel Computing)** The lecture "From Shader Code to a Teraflop" is freely available; it's the academic counterpart to the Branch video, covering how shader cores hide memory latency. Search "CS149 Fatahalian GPU" or find it via Class Central.

---

## The Mental Model (Layers)

Here's the layered picture you're building toward, from hardware up to your GLSL:

### Layer 1 — The Physical Chip

A GPU is not one big processor — it's hundreds of small **Streaming Multiprocessors (SMs)**, each containing:

- many **ALUs** (arithmetic units, do the actual math)
- a small fast **shared memory / L1 cache** (on-chip SRAM, ~kilobytes, very fast)
- a **warp scheduler** (decides which threads run next)

Neighboring pixels are usually applying the same operations, so rather than granting shader cores true independence, they are grouped together so all of them execute threads from the same instruction stream. NVIDIA calls these groups **warps** (32 threads); AMD calls them **wavefronts** (64 threads).

### Layer 2 — The Memory Hierarchy

From fastest/smallest to slowest/largest:

|Memory|Where|Speed|Who uses it|
|---|---|---|---|
|Registers|Inside each core|~1 cycle|Your GLSL local variables|
|Shared memory / L1|Inside each SM|~5 cycles|Threads in same workgroup cooperating|
|L2 cache|Chip-wide|~30 cycles|Automatically managed|
|VRAM (GDDR/HBM)|On the card, off-chip|~200+ cycles|Textures, framebuffers, big buffers|
|System RAM|CPU side|even slower|Host JS data before upload|

If the GPU can recall data from caches rather than requesting it from VRAM, data is accessed and processed faster — each additional read or write through the memory hierarchy slows performance and uses more power.

### Layer 3 — Where Your Data Sits

In your Forth Haiku / WebGL context:

- **GLSL local variables** → registers (ephemeral, per-invocation, gone when fragment shader exits)
- **Textures** (`sampler2D`) → VRAM, read through the texture cache (hardware-sampled, filtered)
- **Framebuffers** (the canvas, render targets) → VRAM
- **Uniforms** (`uniform float time_val`) → small constant buffer, broadcast to all cores

This is why textures are the _only_ practical state store in GLSL — they're the one thing that persists in VRAM across shader invocations and can be re-read next frame.

### Layer 4 — The API Stack

```
Your GLSL / Forth Haiku code
        ↓
WebGL (JavaScript API)        ← you manage uploads, bindings, draw calls
        ↓
Browser's WebGL implementation
        ↓
OS GPU driver
        ↓
Physical GPU hardware
```

The GPU processes all data which is in its local memory, not central memory — therefore, data needed by the GPU must be loaded/copied to GPU memory first, and communication overhead between CPU and GPU should be reduced by keeping data on the GPU rather than communicating repeatedly.

---

## The Key Insight for Forth Haiku

Your fragment shader runs as **one invocation per pixel**, all in parallel, each one stateless. The only bridge to the previous frame is a **texture in VRAM** — which is why ping-pong framebuffers are the canonical pattern for anything stateful. The GPU hardware enforces this: a shader core has no way to write to the texture it's currently reading from in the same pass.