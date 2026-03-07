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

    // --- Ball (3D basketball) ---
    vec2 ballPos = u_ball_pos;
    float d = length(uv - ballPos);
    if (d < ballRadius) {
        // Sphere shading
        float nd = d / ballRadius;  // 0 at center, 1 at edge
        float z = sqrt(1.0 - nd * nd);  // sphere surface normal z

        vec3 normal = vec3((uv - ballPos) / ballRadius, z);

        // Light at the player's eye
        vec3 eyePos = vec3(0.5, 0.5, 3.0);
        vec3 fragPos3D = vec3(ballPos, 0.0) + vec3((uv - ballPos), z * ballRadius);
        vec3 lightDir = normalize(eyePos - fragPos3D);
        vec3 viewDir = normalize(eyePos - fragPos3D);
        float diffuse = max(dot(normal, lightDir), 0.0);
        vec3 halfVec = normalize(lightDir + viewDir);
        float specular = pow(max(dot(normal, halfVec), 0.0), 24.0);

        // Basketball leather colors
        vec3 orangeBase = vec3(0.76, 0.35, 0.07);   // classic basketball orange
        vec3 orangeDark = vec3(0.45, 0.18, 0.03);   // shadow tone

        // Pebble grain texture (leather bumps)
        float grain1 = sin(uv.x * 1200.0 + uv.y * 400.0) * sin(uv.y * 1100.0 + uv.x * 300.0);
        float grain2 = sin(uv.x * 700.0 - uv.y * 900.0) * sin(uv.y * 800.0 - uv.x * 600.0);
        float grain = (grain1 + grain2) * 0.02;

        // Spherical coordinates for seam pattern
        float theta = atan(normal.y, normal.x);  // longitude
        float phi = asin(clamp(normal.z, -1.0, 1.0));  // latitude

        // Basketball seam pattern: 1 equator + 2 meridians at 90 degrees
        float seamWidth = 0.06;

        // Horizontal seam (equator)
        float equator = smoothstep(seamWidth, seamWidth * 0.3, abs(phi));

        // Two vertical seams (perpendicular great circles)
        float meridian1 = smoothstep(seamWidth, seamWidth * 0.3, abs(sin(theta)));
        float meridian2 = smoothstep(seamWidth, seamWidth * 0.3, abs(cos(theta)));

        // Curved side seams: two arcs connecting the poles through the panels
        float arc1 = sin(theta * 2.0) * 0.5;
        float curvedSeam1 = smoothstep(seamWidth, seamWidth * 0.3,
            abs(phi - arc1 * 0.8));
        float arc2 = cos(theta * 2.0) * 0.5;
        float curvedSeam2 = smoothstep(seamWidth, seamWidth * 0.3,
            abs(phi - arc2 * 0.8));

        float seams = max(max(equator, max(meridian1, meridian2)),
                         max(curvedSeam1, curvedSeam2));

        // Seam channel is dark and slightly indented
        vec3 seamColor = vec3(0.05, 0.02, 0.0);

        // Build leather color with lighting
        vec3 leather = mix(orangeBase, orangeDark, 0.3 - 0.3 * diffuse) + grain;

        // Mix in seams
        vec3 ballCol = mix(leather, seamColor, seams * 0.85);

        // Ambient + diffuse + specular (leather has a softer sheen than felt)
        ballCol = ballCol * (0.3 + 0.7 * diffuse) + vec3(1.0, 0.9, 0.8) * specular * 0.3;

        // Soft edge falloff
        float edgeFade = smoothstep(1.0, 0.85, nd);
        col = mix(col, ballCol, edgeFade);
    }

    fragColor = vec4(col, 1.0);
}
