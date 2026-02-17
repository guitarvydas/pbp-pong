// --- MAIN ---
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;

    // Court dimensions (in normalized coords)
    float courtMargin = 0.02;
    float centerLineWidth = 0.002;
    float paddleWidth = 0.015;
    float paddleHeight = 0.15;
    float ballRadius = 0.015;
    float lineThickness = 0.003;

    // Colors
    vec3 bgColor = vec3(0.05, 0.05, 0.1);
    vec3 lineColor = vec3(0.3, 0.3, 0.4);
    vec3 paddleColor = vec3(0.3, 0.78, 0.69);  // #4ec9b0
    vec3 ballColor = vec3(1.0, 1.0, 1.0);

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

    // --- Ball ---
    vec2 ballPos = u_ball_pos;
    float d = length(uv - ballPos);
    if (d < ballRadius) {
        col = ballColor;
    }

    fragColor = vec4(col, 1.0);
}
