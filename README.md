# PyRenderer & 3D Bird Runner: Software Graphics Engine & Game

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI: Passing](https://img.shields.io/badge/build-passing-brightgreen.svg)](.github/workflows/ci.yml)
[![Domain: Computer Graphics](https://img.shields.io/badge/domain-Computer%20Graphics-blue.svg)]()
[![Academic: BRACU CSE423](https://img.shields.io/badge/course-CSE%20423-orange.svg)]()

## 📌 Course Context: CSE 423 (Computer Graphics)
*Department of Computer Science and Engineering, BRAC University*  
**Core Principles:** 2D Rasterization (Bresenham's Line, Midpoint Circle), Cohen-Sutherland Viewport Line Clipping, 3D Viewing Pipeline & Perspective Projection, Phong Illumination & Shading Models, and Real-Time Interactive 3D Game Architecture.

---

## 🏗️ Dual-Tier Architecture: Engine + Application

This project provides both the **foundational mathematical engine** (what university professors and graphics researchers evaluate) and a **fully playable interactive 3D application** (what industry recruiters and game studios evaluate).

```
===================================================================================
                   CSE 423 COMPUTER GRAPHICS ARCHITECTURE
===================================================================================
 [Tier 1: Foundational Engine]             [Tier 2: Interactive Application]
  - Bresenham Line Rasterizer               - 3D Bird Runner Game (Tkinter 60 FPS)
  - Midpoint Circle Generator               - 3-Lane Lateral Switching
  - Cohen-Sutherland Line Clipper           - Perspective Horizon & Depth Scaling
  - 3D Rotation Matrices & Transforms       - Approaching 3D Monolith Obstacles
  - Perspective Division & Camera Model     - 3-Heart Health / Lives System
  - Phong Lighting & Specular Shading       - Collectible Coins & Shield Artifacts
===================================================================================
```

---

## 🎮 Tier 2: 3D Bird Runner Game Mechanics

The interactive game demonstrates real-time application of projective geometry and computer graphics principles:

1. **3-Lane Flying Track:** Left (`-1`), Center (`0`), and Right (`+1`) lanes with smooth non-linear interpolation (`lerp`) and banking angle tilt during lateral motion.
2. **Perspective Projection & Vanishing Point:** Track edges, dividers, approaching obstacles, coins, and artifacts map from 3D world coordinates $(x, y, z)$ into 2D viewport coordinates using perspective scaling $S = \frac{1}{z \cdot c + 1}$.
3. **Painters Algorithm (Depth Sorting):** All world entities are sorted by distance $Z$ descending so distant horizon elements are rendered first, followed by foreground obstacles, player bird, and screen HUD overlays.
4. **Collision & Health System:** 
   - 3 Hearts / Lives. Colliding with a red monolith obstacle consumes 1 life.
   - When all 3 lives are lost, the game over state triggers.
5. **Score Boosters & Mystical Artifacts:**
   - **Golden Coins (+50 pts):** Increase score and coin tally.
   - **Invincibility Artifact (+100 pts):** Envelops the bird in an iridescent cyan forcefield for 6 seconds, granting total immunity to pass straight through obstacles!

---

## 🎯 Tier 1: Graphics Mathematics & Pipeline Foundations

### 1. Bresenham's Line Algorithm
- Employs pure integer decision variables avoiding floating-point division:
  $$d_{new} = d_{old} + 2\Delta y - 2\Delta x$$
  Generalizes across all octants with step variables $s_x, s_y \in \{-1, +1\}$.

### 2. Midpoint Circle Algorithm
- Generates 8-way symmetric circle points using incremental quadratic stepping:
  $$d = 1 - r, \quad d_{next} = d + 2x + 1 \quad (\text{or } d + 2(x - y) + 1)$$

### 3. Cohen-Sutherland Line Clipping Algorithm
- Implements 4-bit region outcodes ($\text{TOP}=1000_2, \text{BOTTOM}=0100_2, \text{RIGHT}=0010_2, \text{LEFT}=0001_2$).
- Rapid bitwise $\text{OR}$ (trivial accept) and bitwise $\text{AND}$ (trivial reject), calculating exact parametric boundary intersections.

### 4. 3D Geometric Transforms & Perspective Projection
- Rotation matrices around axes ($R_x(\theta), R_y(\theta), R_z(\theta)$).
- Perspective projection mapping 3D coordinates $(x, y, z)$ to screen space:
  $$x_s = \frac{x}{z + d} \cdot S + c_x, \quad y_s = -\frac{y}{z + d} \cdot S + c_y$$

### 5. Phong Illumination Model
$$I = I_a k_a + I_d k_d (\mathbf{N} \cdot \mathbf{L}) + I_s k_s (\mathbf{R} \cdot \mathbf{V})^n$$
- Calculates ambient background light, Lambertian diffuse reflection, and specular reflection highlights using the reflection vector $\mathbf{R} = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}$.

---

## 🚀 Quickstart & Testing

### 1. Play the 3D Bird Runner Game (Interactive GUI)
```bash
# Launch via main wrapper
python main.py --game

# Or launch directly via examples
python examples/run_bird_game.py
```
**Controls:**
- `Left Arrow` / `A`: Switch Lane Left
- `Right Arrow` / `D`: Switch Lane Right
- `R`: Restart Game
- `Q` / `Esc`: Exit

### 2. Run the Mathematical Engine Demonstration
```bash
python main.py
```

### 3. Run Automated Unit Tests
```bash
python tests/test_graphics.py
python tests/test_bird_runner.py
```

---

## 💼 Academic & Industrial Relevance
- **US Graduate Admissions:** Demonstrates foundational mastery of projective geometry, hardware rasterization primitives, and physical light simulation from scratch without relying on third-party black boxes.
- **Game Engine & Rendering Roles:** Proves complete end-to-end capability: from writing foundational vector math algorithms to architecting real-time interactive 60 FPS gameplay loops with collision physics and HUD feedback.
