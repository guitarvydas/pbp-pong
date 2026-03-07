// --- MAIN ---
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;

    // Court dimensions (in normalized coords)
    float courtMargin = 0.02;
    float centerLineWidth = 0.002;
    float paddleWidth = 0.015;
    float paddleHeight = 0.15;
    float ballRadius = 0.05;
    float lineThickness = 0.003;

    // Colors
    vec3 bgColor = vec3(0.05, 0.05, 0.1);
    vec3 lineColor = vec3(0.3, 0.3, 0.4);
    vec3 paddleColor = vec3(0.3, 0.78, 0.69);  // #4ec9b0

    vec3 col = bgColor;

    // --- Court border ---
    if (uv.x < courtMargin + lineThickness && uv.x > courtMargin) col = lineColor;
    if (uv.x > 1.0 - courtMargin - lineThickness && uv.x < 1.0 - courtMargin) col = lineColor;
    if (uv.y < courtMargin + lineThickness && uv.y > courtMargin) col = lineColor;
    if (uv.y > 1.0 - courtMargin - lineThickness && uv.y < 1.0 - courtMargin) col = lineColor;

    // --- Center dashed line ---
    float centerX = abs(uv.x - 0.5);
    float dashPhase = mod(uv.y * 30.0, 2.0);
    if (centerX < centerLineWidth && dashPhase < 1.0) {
        col = lineColor;
    }

    // --- Left paddle ---
    float lpx = courtMargin + 0.03;  // fixed X near left wall
    float lpy = u_paddle_left_y;     // controlled by uniform
    if (uv.x > lpx - paddleWidth * 0.5 && uv.x < lpx + paddleWidth * 0.5 &&
        uv.y > lpy - paddleHeight * 0.5 && uv.y < lpy + paddleHeight * 0.5) {
        col = paddleColor;
    }

    // --- Right paddle ---
    float rpx = 1.0 - courtMargin - 0.03;  // fixed X near right wall
    float rpy = u_paddle_right_y;           // controlled by uniform
    if (uv.x > rpx - paddleWidth * 0.5 && uv.x < rpx + paddleWidth * 0.5 &&
        uv.y > rpy - paddleHeight * 0.5 && uv.y < rpy + paddleHeight * 0.5) {
        col = paddleColor;
    }

    // --- Ball (3D tennis ball) ---
    vec2 ballPos = u_ball_pos;
    float d = length(uv - ballPos);
    if (d < ballRadius) {
        // Sphere shading
        float nd = d / ballRadius;  // 0 at center, 1 at edge
        float z = sqrt(1.0 - nd * nd);  // sphere surface normal z

        vec3 normal = vec3((uv - ballPos) / ballRadius, z);

        // Light at the player's eye: centered on screen, far in front
        // The light direction changes per-fragment relative to the ball's
        // world position, so the specular glint shifts as the ball moves.
        vec3 eyePos = vec3(0.5, 0.5, 3.0);
        vec3 fragPos3D = vec3(ballPos, 0.0) + vec3((uv - ballPos), z * ballRadius);
        vec3 lightDir = normalize(eyePos - fragPos3D);
        vec3 viewDir = normalize(eyePos - fragPos3D);
        float diffuse = max(dot(normal, lightDir), 0.0);
        vec3 halfVec = normalize(lightDir + viewDir);
        float specular = pow(max(dot(normal, halfVec), 0.0), 48.0);

        // Tennis ball felt colors
        vec3 ballBase = vec3(0.8, 0.82, 0.1);    // tennis yellow-green
        vec3 ballShadow = vec3(0.45, 0.48, 0.05); // darker felt

        // Felt fuzz noise (procedural)
        float fuzz = sin(uv.x * 800.0) * sin(uv.y * 800.0) * 0.03;

        // Tennis ball seam curve
        // Map point onto sphere surface for seam calculation
        float theta = atan(normal.y, normal.x);
        float phi = asin(clamp(normal.z, -1.0, 1.0));
        float seam = abs(sin(2.0 * theta) * cos(phi) + cos(2.0 * theta) * sin(phi));
        float seamLine = smoothstep(0.03, 0.0, abs(seam - 0.5) - 0.47);

        vec3 feltColor = mix(ballBase, ballShadow, 0.3 - 0.3 * diffuse) + fuzz;

        // White seam with slight indent shadow
        vec3 seamColor = vec3(0.95, 0.95, 0.9);
        feltColor = mix(feltColor, seamColor, seamLine * 0.7);

        // Ambient + diffuse + specular
        vec3 ballCol = feltColor * (0.35 + 0.65 * diffuse) + vec3(1.0) * specular * 0.4;

        // Soft edge falloff
        float edgeFade = smoothstep(1.0, 0.85, nd);
        col = mix(col, ballCol, edgeFade);
    }

    fragColor = vec4(col, 1.0);
}
