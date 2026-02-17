// --- COMMON ---

#define ZOOM 8.0
#define CYCLE 100.0
#define THRES 0.8
#define BRUSHSIZE 1.0
#define FRAMESTEP 2.0

const vec3 bgCol = vec3(0.058, 0.082, 0.066);
const vec3 col1  = vec3(0.152, 0.647, 0.427);
const vec3 col2  = vec3(0.215, 0.345, 0.627);
const vec3 col3  = vec3(0.588, 0.317, 0.211);
const vec3 col4  = vec3(0.772, 0.203, 0.254);

// --- BUFFER_A ---
// Game of Life simulation

int getNeighbours(ivec2 pos) {
    int num = 0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            if (x == 0 && y == 0) continue;
            num += texelFetch(iChannel1, pos + ivec2(x, y), 0).r > THRES ? 1 : 0;
        }
    }
    return num;
}

vec4 updateState(vec2 uv, vec2 fragCoord) {
    vec4 previousState = texelFetch(iChannel1, ivec2(fragCoord), 0);
    float isAlive = previousState.x;
    int numNeighbours = getNeighbours(ivec2(fragCoord));

    if (isAlive > 0.0 && (numNeighbours == 2 || numNeighbours == 3)) {
        isAlive = 1.0;
    } else if (isAlive <= 0.0 && numNeighbours == 3) {
        isAlive = 1.0;
    } else {
        isAlive = 0.0;
    }

    if (distance(fragCoord, iMouse.xy / ZOOM) < BRUSHSIZE) {
        isAlive = 1.0;
    }

    vec4 newState = previousState;
    newState.x = isAlive;

    if (isAlive > 0.0) {
        newState.y = mod(newState.y + isAlive, CYCLE);
    } else {
        const float decayAmount = 0.05;
        newState.y = clamp(newState.y - decayAmount, 0.0, CYCLE);
    }
    return newState;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec4 col = vec4(0);

    if (iFrame < 1) {
        col = texture(iChannel0, uv);
    } else if (iFrame % int(FRAMESTEP) != 0) {
        col = texture(iChannel1, uv);
    } else {
        col = updateState(uv, fragCoord);
    }
    fragColor = col;
}

// --- BUFFER_B ---
// Gradient map, scanlines, LED circles

vec3 getGradient(float value) {
    if (value < 0.25) {
        return mix(bgCol, col1, value * 4.0);
    } else if (value < 0.5) {
        return mix(col1, col2, (value - 0.25) * 4.0);
    } else if (value < 0.75) {
        return mix(col2, col3, (value - 0.50) * 4.0);
    } else {
        return mix(col3, col4, (value - 0.75) * 4.0);
    }
}

float scanlines(vec2 fragCoord) {
    float intensity = 1.0;
    float val = abs(sin(fragCoord.y * 0.1 + iTime * FRAMESTEP) * intensity);
    return max(0.4, val);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy / ZOOM;
    vec2 gridUV = fract(fragCoord / ZOOM) - 0.5;

    vec4 state = texture(iChannel0, uv);

    state.y *= scanlines(fragCoord);
    vec3 col = getGradient(state.y / 100.0);

    float dis = length(gridUV);
    col *= smoothstep(0.1, 0.0, dis - 0.4);

    if (state.x > 0.0) {
        fragColor = vec4(col, 1.0);
    } else {
        const float blackMix = 0.5;
        fragColor = vec4(mix(col, bgCol, blackMix), 1.0);
    }
}

// --- MAIN ---
// CRT bulge + vignette

vec2 applyBulge(vec2 uv) {
    vec2 centerDis = abs(0.5 - uv);
    centerDis *= centerDis;
    float warp = 0.75;
    uv.x -= 0.5;
    uv.x *= 1.0 + (centerDis.y * (0.3 * warp));
    uv.x += 0.5;
    uv.y -= 0.5;
    uv.y *= 1.0 + (centerDis.x * (0.4 * warp));
    uv.y += 0.5;
    return uv;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    uv = applyBulge(uv);

    vec3 col = texture(iChannel0, uv).rgb;

    if (uv.y > 1.0 || uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        col *= (1.0 - length(uv - 0.5)) + 0.25;
        fragColor = vec4(col, 1.0);
    }
}
