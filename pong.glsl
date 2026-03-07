// --- MAIN ---

// ---- Basketball hoop (backboard + rim + net) ----
vec3 drawHoop(vec3 bg, vec2 uv, float cx, float cy, float pw, float ph, bool flipX) {
    vec3 col = bg;
    float dir = flipX ? -1.0 : 1.0;

    // Backboard: white rectangle behind the rim
    float bbW = pw * 1.8;
    float bbH = ph * 0.55;
    float bbX = cx - dir * pw * 0.3;
    if (abs(uv.x - bbX) < bbW * 0.5 && abs(uv.y - (cy + ph * 0.15)) < bbH * 0.5) {
        // White backboard with slight transparency feel
        vec3 boardCol = vec3(0.9, 0.92, 0.95);
        // Red square target on backboard
        float sqH = bbH * 0.45;
        float sqW = bbW * 0.4;
        if (abs(uv.x - bbX) < sqW * 0.5 && abs(uv.y - (cy + ph * 0.15)) < sqH * 0.5) {
            // Red outline only
            float inner = step(sqW * 0.35, abs(uv.x - bbX)) + step(sqH * 0.35, abs(uv.y - (cy + ph * 0.15)));
            if (inner < 1.0) {
                boardCol = vec3(0.85, 0.88, 0.92);
            } else {
                boardCol = vec3(0.85, 0.15, 0.1);
            }
        }
        col = boardCol;
    }

    // Rim: orange ring extending from backboard
    float rimCX = cx + dir * pw * 0.6;
    float rimCY = cy - ph * 0.05;
    float rimRadius = pw * 1.2;
    float rimThick = 0.004;
    float dRim = abs(length(vec2(uv.x - rimCX, (uv.y - rimCY) * 1.8)) - rimRadius);
    if (dRim < rimThick) {
        col = vec3(0.85, 0.35, 0.05); // orange rim
    }

    // Rim connector bracket
    float bracketY = rimCY;
    float bracketX1 = cx;
    float bracketX2 = rimCX - dir * rimRadius * 0.5;
    float bMinX = min(bracketX1, bracketX2);
    float bMaxX = max(bracketX1, bracketX2);
    if (uv.x > bMinX && uv.x < bMaxX && abs(uv.y - bracketY) < 0.003) {
        col = vec3(0.5, 0.5, 0.55); // metal bracket
    }

    // Net: hanging strings below rim
    float netTop = rimCY - 0.005;
    float netBottom = rimCY - ph * 0.45;
    float netLeft = rimCX - rimRadius * 0.85;
    float netRight = rimCX + rimRadius * 0.85;
    if (uv.y < netTop && uv.y > netBottom && uv.x > netLeft && uv.x < netRight) {
        float netLocalY = (netTop - uv.y) / (netTop - netBottom);
        // Net narrows toward bottom
        float narrowing = 1.0 - netLocalY * 0.5;
        float netMidX = rimCX;
        if (abs(uv.x - netMidX) < rimRadius * 0.85 * narrowing) {
            // Vertical strings
            float vString = sin((uv.x - netLeft) * 350.0);
            // Horizontal strings (wider spacing toward bottom)
            float hSpacing = 80.0 - netLocalY * 30.0;
            float hString = sin(uv.y * hSpacing);
            if (vString > 0.85 || hString > 0.9) {
                col = vec3(0.95, 0.95, 0.95); // white net
            }
        }
    }

    return col;
}

// ---- Baseball bat ----
vec3 drawBat(vec3 bg, vec2 uv, float cx, float cy, float pw, float ph, bool flipX) {
    vec3 col = bg;
    float dir = flipX ? -1.0 : 1.0;

    // Bat is vertical, centered at (cx, cy)
    float batLength = ph * 1.1;
    float localY = (uv.y - (cy - batLength * 0.35)) / batLength;

    if (localY >= 0.0 && localY <= 1.0) {
        // Bat profile: thin handle at bottom, widens to barrel at top
        float handleWidth = pw * 0.3;
        float barrelWidth = pw * 2.2;
        float knobWidth = pw * 0.8;

        float width;
        if (localY < 0.05) {
            // Knob at very bottom
            width = mix(knobWidth, handleWidth * 0.7, localY / 0.05);
        } else if (localY < 0.35) {
            // Handle: thin grip
            width = handleWidth;
        } else if (localY < 0.55) {
            // Taper: handle to barrel
            float t = (localY - 0.35) / 0.2;
            width = mix(handleWidth, barrelWidth, t * t);
        } else if (localY < 0.92) {
            // Barrel: fat part
            width = barrelWidth;
        } else {
            // Cap: rounds off
            float t = (localY - 0.92) / 0.08;
            width = barrelWidth * (1.0 - t * t);
        }

        float dx = abs(uv.x - cx);
        if (dx < width * 0.5) {
            // Wood grain color
            float grain = sin(uv.y * 600.0 + sin(uv.x * 200.0) * 2.0) * 0.03;
            float grain2 = sin(uv.y * 150.0 + uv.x * 80.0) * 0.02;

            vec3 woodLight = vec3(0.72, 0.52, 0.28);  // ash wood
            vec3 woodDark = vec3(0.55, 0.38, 0.18);

            // Cylindrical shading: darker at edges
            float shade = 1.0 - (dx / (width * 0.5)) * (dx / (width * 0.5));
            vec3 woodCol = mix(woodDark, woodLight, shade) + grain + grain2;

            // Handle wrap (grip tape) region
            if (localY > 0.08 && localY < 0.33) {
                float tape = sin(uv.y * 400.0 - uv.x * 100.0 * dir);
                vec3 tapeCol = tape > 0.0 ? vec3(0.15, 0.15, 0.15) : vec3(0.25, 0.25, 0.25);
                woodCol = mix(tapeCol, woodCol, 0.1);
                woodCol *= (0.7 + 0.3 * shade); // keep cylindrical shading
            }

            // Brand logo region on barrel
            if (localY > 0.65 && localY < 0.75 && dx < width * 0.3) {
                // Subtle oval logo stamp
                float logoD = length(vec2((uv.x - cx) / (width * 0.3), (localY - 0.7) / 0.04));
                if (logoD < 1.0) {
                    woodCol = mix(woodCol, vec3(0.4, 0.25, 0.1), 0.3);
                }
            }

            // Specular highlight down the length
            float spec = pow(max(0.0, 1.0 - abs(uv.x - cx + dir * width * 0.15) / (width * 0.2)), 4.0);
            woodCol += vec3(0.15, 0.12, 0.08) * spec;

            col = woodCol;
        }
    }

    return col;
}

// ---- Paddle dispatcher ----
// style: 0.0 = basketball hoop, 1.0 = baseball bat
vec3 drawPaddle(vec3 bg, vec2 uv, float cx, float cy, float pw, float ph, float style, bool flipX) {
    if (style < 0.5) {
        return drawHoop(bg, uv, cx, cy, pw, ph, flipX);
    } else {
        return drawBat(bg, uv, cx, cy, pw, ph, flipX);
    }
}

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
    float lpx = courtMargin + 0.03;
    float lpy = u_paddle_left_y;
    col = drawPaddle(col, uv, lpx, lpy, paddleWidth, paddleHeight, u_paddle_left_style, false);

    // --- Right paddle ---
    float rpx = 1.0 - courtMargin - 0.03;
    float rpy = u_paddle_right_y;
    col = drawPaddle(col, uv, rpx, rpy, paddleWidth, paddleHeight, u_paddle_right_style, true);

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
