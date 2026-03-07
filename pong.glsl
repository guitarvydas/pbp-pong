// --- MAIN ---

// Light source position — closer Z = more pronounced glint shift
const vec3 LIGHT_POS = vec3(0.5, 0.5, 0.8);

// ---- Basketball net receptacle (3D cylindrical net basket) ----
vec3 drawHoop(vec3 bg, vec2 uv, float cx, float cy, float pw, float ph, bool flipX) {
    vec3 col = bg;
    float dir = flipX ? -1.0 : 1.0;

    float scale = ph;

    // Basket lies on its side: open end toward center court
    float openX = cx + dir * scale * 0.35;
    float closedX = cx - dir * scale * 0.15;
    float bodyMinX = min(openX, closedX);
    float bodyMaxX = max(openX, closedX);
    float bodyLen = bodyMaxX - bodyMinX;

    if (uv.x >= bodyMinX - scale * 0.03 && uv.x <= bodyMaxX + scale * 0.03) {
        // t: 0 at closed end, 1 at open end
        float t = (flipX)
            ? (bodyMaxX - uv.x) / bodyLen
            : (uv.x - bodyMinX) / bodyLen;

        // Tapered radius: wider at open end
        float openR = scale * 0.42;
        float closedR = scale * 0.22;
        float radius = mix(closedR, openR, clamp(t, 0.0, 1.0));

        float dy = uv.y - cy;
        float absDy = abs(dy);

        // Light source at player's eye
        vec3 eyePos = LIGHT_POS;

        // --- Rim rings ---
        float rimWidth = scale * 0.02;

        // Open end rim
        float openDist = abs(uv.x - openX);
        if (openDist < rimWidth && absDy < openR) {
            // Cylindrical normal for rim ring
            float normY = dy / openR;
            float normZ = sqrt(max(0.0, 1.0 - normY * normY));
            vec3 rimNorm = normalize(vec3(dir * 0.1, normY, normZ));
            vec3 rimPos3D = vec3(uv, 0.0);
            vec3 rimLightDir = normalize(eyePos - rimPos3D);
            float rimDiff = max(dot(rimNorm, rimLightDir), 0.0);
            float rimSpec = pow(max(dot(reflect(-rimLightDir, rimNorm), normalize(eyePos - rimPos3D)), 0.0), 40.0);
            vec3 rimBase = vec3(0.9, 0.4, 0.05);
            col = rimBase * (0.3 + 0.7 * rimDiff) + vec3(1.0, 0.8, 0.5) * rimSpec * 0.5;
            return col;
        }

        // Closed end rim
        float closedDist = abs(uv.x - closedX);
        if (closedDist < rimWidth * 0.7 && absDy < closedR) {
            float normY = dy / closedR;
            float normZ = sqrt(max(0.0, 1.0 - normY * normY));
            vec3 rimNorm = normalize(vec3(-dir * 0.1, normY, normZ));
            vec3 rimPos3D = vec3(uv, 0.0);
            vec3 rimLightDir = normalize(eyePos - rimPos3D);
            float rimDiff = max(dot(rimNorm, rimLightDir), 0.0);
            col = vec3(0.5, 0.5, 0.55) * (0.3 + 0.7 * rimDiff);
            return col;
        }

        if (uv.x >= bodyMinX && uv.x <= bodyMaxX && absDy < radius) {
            // --- 3D cylinder mapping ---
            // Treat the basket as a horizontal cylinder
            // For each pixel, compute where it sits on the cylinder surface
            float normDy = dy / radius;  // -1 to 1

            // Angle around the cylinder (0 = front face, PI/2 = top/bottom edges)
            float theta = asin(clamp(normDy, -1.0, 1.0));

            // Z depth of this point on the cylinder surface
            float cylZ = cos(theta);  // 1.0 at front, 0.0 at edges

            // Surface normal on cylinder
            vec3 cylNormal = normalize(vec3(0.0, normDy, cylZ));

            // 3D position for lighting
            vec3 fragPos3D = vec3(uv.x, uv.y, cylZ * radius * 0.5);
            vec3 lightDir = normalize(eyePos - fragPos3D);
            vec3 viewDir = normalize(eyePos - fragPos3D);

            float diffuse = max(dot(cylNormal, lightDir), 0.0);
            vec3 halfVec = normalize(lightDir + viewDir);
            float specular = pow(max(dot(cylNormal, halfVec), 0.0), 30.0);

            // --- Top/bottom edge wires (structural rings) ---
            float edgeDist = abs(absDy - radius);
            if (edgeDist < scale * 0.008) {
                vec3 wireBase = vec3(0.85, 0.37, 0.05);
                col = wireBase * (0.3 + 0.7 * diffuse) + vec3(1.0, 0.8, 0.5) * specular * 0.3;
                return col;
            }

            // --- Structural rings along the body ---
            float ringSpacing = bodyLen * 0.25;
            float localX = uv.x - bodyMinX;
            float ringDist = mod(localX + ringSpacing * 0.5, ringSpacing);
            ringDist = abs(ringDist - ringSpacing * 0.5);
            if (ringDist < scale * 0.005) {
                vec3 ringBase = vec3(0.6, 0.6, 0.65);
                col = ringBase * (0.3 + 0.7 * diffuse) + vec3(1.0) * specular * 0.2;
                return col;
            }

            // --- Net mesh ---
            // Map mesh coords onto the cylinder surface so diamonds
            // compress at the edges (foreshortening)
            float meshU = uv.x * 180.0;
            float meshV = theta * 90.0;  // angular coord gives 3D wrapping

            float d1 = sin(meshU + meshV);
            float d2 = sin(meshU - meshV);

            // Cord visibility threshold: tighter weave toward closed end
            float cordThresh = mix(0.72, 0.62, t);

            bool isCord = abs(d1) > cordThresh || abs(d2) > cordThresh;

            if (isCord) {
                // Cord normal: perturb cylinder normal with cord direction
                float cordAngle = (abs(d1) > abs(d2)) ? (meshU + meshV) : (meshU - meshV);
                float cordNx = cos(cordAngle * 0.02) * 0.3;
                float cordNy = sin(cordAngle * 0.02) * 0.3;
                vec3 cordNormal = normalize(cylNormal + vec3(cordNx, cordNy, 0.0));

                float cordDiff = max(dot(cordNormal, lightDir), 0.0);
                float cordSpec = pow(max(dot(reflect(-lightDir, cordNormal), viewDir), 0.0), 20.0);

                // White nylon with shading
                vec3 cordBase = vec3(0.93, 0.93, 0.89);

                // Darken cords on the back side of the cylinder
                float depthDarken = 0.5 + 0.5 * cylZ;

                col = cordBase * depthDarken * (0.25 + 0.75 * cordDiff)
                    + vec3(1.0) * cordSpec * 0.2;
            }
            // else: hole in net, background shows through
        }
    }

    return col;
}

// ---- Baseball bat (3D, concave on court-facing edge) ----
vec3 drawBat(vec3 bg, vec2 uv, float cx, float cy, float pw, float ph, bool flipX) {
    vec3 col = bg;
    float dir = flipX ? -1.0 : 1.0;

    // Bat is vertical, centered at (cx, cy)
    float batLength = ph * 1.1;
    float localY = (uv.y - (cy - batLength * 0.35)) / batLength;

    if (localY >= 0.0 && localY <= 1.0) {
        // Bat profile widths
        float handleWidth = pw * 0.3;
        float barrelWidth = pw * 2.2;
        float knobWidth = pw * 0.8;

        float width;
        if (localY < 0.05) {
            width = mix(knobWidth, handleWidth * 0.7, localY / 0.05);
        } else if (localY < 0.35) {
            width = handleWidth;
        } else if (localY < 0.55) {
            float t = (localY - 0.35) / 0.2;
            width = mix(handleWidth, barrelWidth, t * t);
        } else {
            // Barrel with gentle taper toward tip
            float t = (localY - 0.55) / 0.45;
            float taper = 1.0 - t * t * t * 0.3;  // subtle narrowing
            width = barrelWidth * taper;
        }

        // Concave scoop on the court-facing edge (barrel region)
        float concaveDepth = 0.0;
        if (localY > 0.4) {
            float barrelT = (localY - 0.4) / 0.6;
            concaveDepth = sin(barrelT * 3.14159) * barrelWidth * 0.35;
        }

        float dx = uv.x - cx;
        bool courtSide = (dx * dir) > 0.0;

        // Court-facing edge is scooped inward; back edge stays convex
        float halfW_court = width * 0.5 - concaveDepth;
        float halfW_back = width * 0.5;
        float edgeLimit = courtSide ? halfW_court : halfW_back;

        if (abs(dx) < edgeLimit) {
            // Normalized position across the bat for this side
            float sideDx = courtSide ? (dx * dir) : (-dx * dir);
            float sideMax = courtSide ? halfW_court : halfW_back;
            float sideNorm = sideDx / max(sideMax, 0.001);  // 0 at center, 1 at edge

            // 3D surface: convex back, concave court-facing scoop
            float cylZ;
            vec3 normal;

            if (courtSide && concaveDepth > 0.001) {
                // Concave: Z dips inward, normal points back toward court
                cylZ = 0.3 + 0.7 * (1.0 - sideNorm * sideNorm);
                normal = normalize(vec3(-dir * sideNorm * 0.8, 0.0, cylZ));
            } else {
                // Convex: standard cylinder
                float normDx = dx / (halfW_back);
                cylZ = sqrt(max(0.0, 1.0 - normDx * normDx));
                normal = normalize(vec3(normDx, 0.0, cylZ));
            }

            // Lighting
            vec3 fragPos3D = vec3(uv.x, uv.y, cylZ * width * 0.25);
            vec3 eyePos = LIGHT_POS;
            vec3 lightDir = normalize(eyePos - fragPos3D);
            vec3 viewDir = normalize(eyePos - fragPos3D);
            float diffuse = max(dot(normal, lightDir), 0.0);
            vec3 halfVec = normalize(lightDir + viewDir);
            float specular = pow(max(dot(normal, halfVec), 0.0), 50.0);

            // Wood grain
            float grain = sin(uv.y * 600.0 + sin(uv.x * 200.0) * 2.0) * 0.03;
            float grain2 = sin(uv.y * 150.0 + uv.x * 80.0) * 0.02;
            vec3 woodLight = vec3(0.72, 0.52, 0.28);
            vec3 woodDark = vec3(0.55, 0.38, 0.18);
            vec3 woodCol = mix(woodDark, woodLight, 0.5 + 0.5 * cylZ) + grain + grain2;

            // Grip tape on handle
            if (localY > 0.08 && localY < 0.33) {
                float tape = sin(uv.y * 400.0 - uv.x * 100.0 * dir);
                vec3 tapeCol = tape > 0.0 ? vec3(0.15, 0.15, 0.15) : vec3(0.25, 0.25, 0.25);
                woodCol = mix(tapeCol, woodCol, 0.1);
                specular *= 0.3;
            }

            // Brand logo on barrel back
            if (localY > 0.65 && localY < 0.75 && !courtSide && abs(dx) < width * 0.3) {
                float logoD = length(vec2((uv.x - cx) / (width * 0.3), (localY - 0.7) / 0.04));
                if (logoD < 1.0) {
                    woodCol = mix(woodCol, vec3(0.4, 0.25, 0.1), 0.3);
                }
            }

            // Apply lighting
            vec3 litCol = woodCol * (0.2 + 0.8 * diffuse);
            litCol += vec3(1.0, 0.9, 0.7) * specular * 0.6;
            litCol *= (0.6 + 0.4 * cylZ);

            col = litCol;
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
    float ballRadius = 0.015;
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

    // --- Ball (3D tennis ball) — drawn first so paddles render on top ---
    vec2 ballPos = u_ball_pos;
    float d = length(uv - ballPos);
    if (d < ballRadius) {
        // Sphere shading
        float nd = d / ballRadius;  // 0 at center, 1 at edge
        float z = sqrt(1.0 - nd * nd);  // sphere surface normal z

        vec3 normal = vec3((uv - ballPos) / ballRadius, z);

        // Light at the player's eye
        vec3 eyePos = LIGHT_POS;
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

    // --- Left paddle ---
    float lpx = courtMargin + 0.03;
    float lpy = u_paddle_left_y;
    col = drawPaddle(col, uv, lpx, lpy, paddleWidth, paddleHeight, u_paddle_left_style, false);

    // --- Right paddle ---
    float rpx = 1.0 - courtMargin - 0.03;
    float rpy = u_paddle_right_y;
    col = drawPaddle(col, uv, rpx, rpy, paddleWidth, paddleHeight, u_paddle_right_style, true);

    fragColor = vec4(col, 1.0);
}
