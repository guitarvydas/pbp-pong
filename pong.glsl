// --- MAIN ---

// ---- Basketball hoop (sideways — backboard at wall, rim+net toward center) ----
vec3 drawHoop(vec3 bg, vec2 uv, float cx, float cy, float pw, float ph, bool flipX) {
    vec3 col = bg;
    // dir: +1 = right side faces center (left paddle), -1 = left side faces center (right paddle)
    float dir = flipX ? -1.0 : 1.0;

    // Scale factors
    float scale = ph * 0.9;

    // Backboard: tall vertical rectangle flush against the wall side
    float bbX = cx - dir * scale * 0.35;  // backboard position (wall side)
    float bbW = scale * 0.06;             // thin (horizontal)
    float bbH = scale * 0.75;             // tall (vertical)
    if (abs(uv.x - bbX) < bbW * 0.5 && abs(uv.y - cy) < bbH * 0.5) {
        vec3 boardCol = vec3(0.88, 0.9, 0.93);
        // Board edge highlight
        float edgeDist = min(abs(abs(uv.x - bbX) - bbW * 0.5), abs(abs(uv.y - cy) - bbH * 0.5));
        if (edgeDist < 0.002) {
            boardCol = vec3(0.4, 0.4, 0.45);
        }
        // Red rectangle target
        float sqW = bbW * 0.8;
        float sqH = bbH * 0.35;
        float sqDX = abs(uv.x - bbX);
        float sqDY = abs(uv.y - (cy + bbH * 0.05));
        if (sqDX < sqW * 0.5 && sqDY < sqH * 0.5) {
            if (sqDX > sqW * 0.35 || sqDY > sqH * 0.35) {
                boardCol = vec3(0.85, 0.12, 0.08);
            }
        }
        col = boardCol;
    }

    // Support pole behind backboard
    float poleX = bbX - dir * scale * 0.04;
    if (abs(uv.x - poleX) < scale * 0.015 && abs(uv.y - cy) < bbH * 0.55) {
        col = vec3(0.35, 0.35, 0.4);
    }

    // Rim: horizontal oval extending from backboard toward center court
    float rimAttachX = bbX + dir * bbW * 0.5;
    float rimEndX = rimAttachX + dir * scale * 0.4;
    float rimMidX = (rimAttachX + rimEndX) * 0.5;
    float rimCY = cy - scale * 0.02;
    float rimHalfW = abs(rimEndX - rimAttachX) * 0.5;
    float rimHalfH = scale * 0.12;

    // Rim as ellipse outline
    float rimDX = (uv.x - rimMidX) / rimHalfW;
    float rimDY = (uv.y - rimCY) / rimHalfH;
    float rimDist = length(vec2(rimDX, rimDY));
    float rimThick = 0.15;
    if (abs(rimDist - 1.0) < rimThick) {
        // Orange painted metal with highlight
        float highlight = pow(max(0.0, 1.0 - abs(rimDY)), 3.0) * 0.2;
        col = vec3(0.9, 0.38, 0.05) + highlight;
    }

    // Rim bracket: two small arms connecting backboard to rim
    float bracketW = abs(rimMidX - rimAttachX) * 0.6;
    float bStartX = rimAttachX;
    float bEndX = rimAttachX + dir * bracketW;
    float bMinX = min(bStartX, bEndX);
    float bMaxX = max(bStartX, bEndX);
    // Upper bracket
    if (uv.x > bMinX && uv.x < bMaxX && abs(uv.y - (rimCY + rimHalfH * 0.5)) < 0.0025) {
        col = vec3(0.5, 0.5, 0.55);
    }
    // Lower bracket
    if (uv.x > bMinX && uv.x < bMaxX && abs(uv.y - (rimCY - rimHalfH * 0.5)) < 0.0025) {
        col = vec3(0.5, 0.5, 0.55);
    }

    // Net: hangs below the rim, narrows downward
    float netTop = rimCY - rimHalfH * 0.7;
    float netBottom = rimCY - scale * 0.55;
    float netMinX = min(rimAttachX, rimEndX) + abs(rimEndX - rimAttachX) * 0.05;
    float netMaxX = max(rimAttachX, rimEndX) - abs(rimEndX - rimAttachX) * 0.05;

    if (uv.y < netTop && uv.y > netBottom && uv.x > netMinX && uv.x < netMaxX) {
        float netLocalY = (netTop - uv.y) / (netTop - netBottom);  // 0 at top, 1 at bottom

        // Net narrows toward bottom and toward the open end
        float narrowX = 1.0 - netLocalY * 0.55;
        float netCX = (netMinX + netMaxX) * 0.5;
        float netW = (netMaxX - netMinX) * 0.5 * narrowX;

        if (abs(uv.x - netCX) < netW) {
            // Diamond mesh pattern
            float meshScaleX = 220.0;
            float meshScaleY = 180.0;
            float mx = sin(uv.x * meshScaleX + uv.y * meshScaleY * 0.5);
            float my = sin(uv.y * meshScaleY + uv.x * meshScaleX * 0.5);
            float mesh = max(abs(mx), abs(my));

            if (mesh > 0.82) {
                // White net cords with slight depth shading
                float depth = 0.8 + 0.2 * (1.0 - netLocalY);
                col = vec3(0.95, 0.95, 0.92) * depth;
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
