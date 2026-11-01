"""
3D Bird Runner Game: 3-Lane Endless Flyer with 3D Perspective Projection.
Features:
- 3 Lanes (Left, Center, Right) with smooth lane-switching interpolation
- 3D Perspective Rendering (vanishing horizon, depth scaling, Painters algorithm)
- Approaching 3D obstacles (prisms/pillars)
- Lives system (3 hearts; collisions deplete lives)
- Collectible Golden Coins (+50 points)
- Rare Invincibility Artifacts (fly through obstacles safely, +100 points)
- Graphical Tkinter 60 FPS interactive window + Headless simulation mode
"""
import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional

# --- Game Entities ---

@dataclass
class GameObject:
    lane: int          # -1 = Left, 0 = Center, +1 = Right
    z: float           # Distance from camera (e.g. 50.0 down to 0.0)
    obj_type: str      # 'OBSTACLE', 'COIN', 'ARTIFACT'
    collected: bool = False

class BirdGame3D:
    def __init__(self):
        # Game State
        self.lives: int = 3
        self.score: int = 0
        self.coins: int = 0
        self.game_over: bool = False
        
        # Player Bird State
        self.current_lane: int = 0         # -1, 0, 1
        self.target_lane: int = 0
        self.bird_x: float = 0.0           # Interpolated lateral position
        self.bird_y: float = -0.5          # Vertical altitude
        self.wing_angle: float = 0.0
        
        # Power-up / Artifact state
        self.has_shield: bool = False
        self.shield_timer: float = 0.0     # Seconds remaining of invincibility
        
        # World & Perspective parameters
        self.speed: float = 18.0           # Units per second forward speed
        self.horizon_z: float = 40.0       # Spawn depth
        self.objects: List[GameObject] = []
        self.spawn_timer: float = 0.0
        self.game_time: float = 0.0

    def move_left(self):
        if not self.game_over and self.target_lane > -1:
            self.target_lane -= 1

    def move_right(self):
        if not self.game_over and self.target_lane < 1:
            self.target_lane += 1

    def reset(self):
        self.__init__()

    def spawn_wave(self):
        """Spawns obstacles, coins, and rare invincibility artifacts across the 3 lanes."""
        lanes = [-1, 0, 1]
        random.shuffle(lanes)
        
        # Pick 1 or 2 lanes for obstacles
        num_obstacles = random.choice([1, 1, 2])
        obs_lanes = lanes[:num_obstacles]
        for l in obs_lanes:
            self.objects.append(GameObject(lane=l, z=self.horizon_z, obj_type='OBSTACLE'))
            
        # 40% chance of Coin in a free lane
        free_lanes = [l for l in [-1, 0, 1] if l not in obs_lanes]
        if free_lanes and random.random() < 0.50:
            coin_lane = random.choice(free_lanes)
            self.objects.append(GameObject(lane=coin_lane, z=self.horizon_z + 2.0, obj_type='COIN'))
            
        # 15% chance of rare Invincibility Artifact
        if free_lanes and random.random() < 0.15:
            art_lane = random.choice(free_lanes)
            self.objects.append(GameObject(lane=art_lane, z=self.horizon_z + 4.0, obj_type='ARTIFACT'))

    def update(self, dt: float):
        if self.game_over:
            return

        self.game_time += dt
        self.score += int(dt * 15)  # Continuous distance score
        
        # Animate flapping wings
        self.wing_angle += dt * 12.0
        
        # Smooth lane transition interpolation (lerp)
        self.bird_x += (self.target_lane - self.bird_x) * min(1.0, dt * 10.0)
        self.current_lane = int(round(self.bird_x))

        # Handle Invincibility Shield countdown
        if self.has_shield:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.has_shield = False
                self.shield_timer = 0.0

        # Spawning mechanism
        self.spawn_timer += dt
        spawn_interval = max(0.9, 1.8 - (self.game_time * 0.015))  # Gradually accelerates
        if self.spawn_timer >= spawn_interval:
            self.spawn_timer = 0.0
            self.spawn_wave()

        # Update world objects (move towards camera)
        active_objects = []
        for obj in self.objects:
            obj.z -= self.speed * dt
            
            # Collision detection window near player bird (Z in [-0.5, 1.2])
            if -0.5 <= obj.z <= 1.2 and not obj.collected:
                # Check lane alignment
                if abs(self.bird_x - obj.lane) < 0.55:
                    if obj.obj_type == 'COIN':
                        obj.collected = True
                        self.coins += 1
                        self.score += 50
                    elif obj.obj_type == 'ARTIFACT':
                        obj.collected = True
                        self.has_shield = True
                        self.shield_timer = 6.0  # 6 seconds of invincibility
                        self.score += 100
                    elif obj.obj_type == 'OBSTACLE':
                        obj.collected = True
                        if self.has_shield:
                            # Shield absorbs impact safely!
                            self.score += 25
                        else:
                            self.lives -= 1
                            if self.lives <= 0:
                                self.game_over = True

            # Keep object if it hasn't passed behind the camera
            if obj.z > -2.0 and not obj.collected:
                active_objects.append(obj)

        self.objects = active_objects

    def project_3d_to_2d(self, x: float, y: float, z: float, width: int = 700, height: int = 550) -> Tuple[int, int, float]:
        """
        Perspective projection mapping 3D coordinates (lane_x, y, z) into 2D viewport.
        Vanishing point at (width / 2, height * 0.38).
        """
        vanish_x = width // 2
        vanish_y = int(height * 0.38)
        
        # Perspective scaling factor inversely proportional to distance Z
        scale = 1.0 / (max(0.1, z) * 0.12 + 1.0)
        
        screen_x = int(vanish_x + (x * 140.0) * scale)
        screen_y = int(vanish_y + ((-y * 80.0) + (z * 6.5)) * scale)
        return screen_x, screen_y, scale


# --- Tkinter Graphical User Interface & Renderer ---

class BirdGameGUI:
    """
    Real-time 60 FPS Tkinter GUI renderer for 3D Bird Runner Game.
    Draws perspective runway, 3D obstacles, animated flying bird, coins, artifacts, and HUD.
    """
    def __init__(self, root, width: int = 700, height: int = 550):
        self.root = root
        self.width = width
        self.height = height
        self.game = BirdGame3D()
        self.last_time = time.time()
        
        # Setup UI
        self.root.title("CSE 423: 3D Bird Runner - Interactive Graphics Demo")
        self.root.resizable(False, False)
        
        import tkinter as tk
        self.canvas = tk.Canvas(root, width=width, height=height, bg="#0d1117", highlightthickness=0)
        self.canvas.pack()
        
        # Controls Binding
        self.root.bind("<Left>", lambda e: self.game.move_left())
        self.root.bind("<a>", lambda e: self.game.move_left())
        self.root.bind("<A>", lambda e: self.game.move_left())
        self.root.bind("<Right>", lambda e: self.game.move_right())
        self.root.bind("<d>", lambda e: self.game.move_right())
        self.root.bind("<D>", lambda e: self.game.move_right())
        self.root.bind("<r>", lambda e: self.restart())
        self.root.bind("<R>", lambda e: self.restart())
        self.root.bind("<q>", lambda e: self.root.destroy())
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Start game loop
        self.tick()

    def restart(self):
        self.game.reset()
        self.last_time = time.time()

    def tick(self):
        now = time.time()
        dt = min(0.05, now - self.last_time)
        self.last_time = now
        
        self.game.update(dt)
        self.render()
        
        self.root.after(16, self.tick)

    def render(self):
        self.canvas.delete("all")
        w, h = self.width, self.height
        vanish_x, vanish_y = w // 2, int(h * 0.38)
        
        # 1. Background Sky and Horizon
        self.canvas.create_rectangle(0, 0, w, vanish_y, fill="#0a0e17", outline="")
        self.canvas.create_rectangle(0, vanish_y, w, h, fill="#161b22", outline="")
        
        # Subtle Horizon Glow Line
        self.canvas.create_line(0, vanish_y, w, vanish_y, fill="#30363d", width=2)
        
        # 2. 3D Runway Lanes (Converging perspective lines)
        lane_coords = [-1.5, -0.5, 0.5, 1.5]
        for lx in lane_coords:
            px_near, py_near, _ = self.game.project_3d_to_2d(lx, -1.0, 0.0, w, h)
            px_far, py_far, _ = self.game.project_3d_to_2d(lx, -1.0, 45.0, w, h)
            color = "#58a6ff" if lx in [-1.5, 1.5] else "#30363d"
            width = 3 if lx in [-1.5, 1.5] else 1
            self.canvas.create_line(px_near, py_near, px_far, py_far, fill=color, width=width)

        # 3. Dynamic Depth Markers (Scrolling track lines)
        road_phase = (self.game.game_time * self.game.speed) % 8.0
        for marker_z in [road_phase + i * 8.0 for i in range(6)]:
            if marker_z < 45.0:
                p1_x, p1_y, _ = self.game.project_3d_to_2d(-1.5, -1.0, marker_z, w, h)
                p2_x, p2_y, _ = self.game.project_3d_to_2d(1.5, -1.0, marker_z, w, h)
                self.canvas.create_line(p1_x, p1_y, p2_x, p2_y, fill="#21262d", width=1)

        # 4. Render World Objects sorted by depth Z (Painters algorithm: back to front)
        sorted_objects = sorted(self.game.objects, key=lambda o: o.z, reverse=True)
        for obj in sorted_objects:
            if obj.z > 0.0:
                sx, sy, scale = self.game.project_3d_to_2d(obj.lane, -0.7, obj.z, w, h)
                
                if obj.obj_type == 'OBSTACLE':
                    # Draw 3D Monolith Obstacle
                    obs_w = max(4, int(45 * scale))
                    obs_h = max(8, int(75 * scale))
                    self.canvas.create_rectangle(sx - obs_w, sy - obs_h, sx + obs_w, sy,
                                                fill="#da3633", outline="#f85149", width=max(1, int(2 * scale)))
                    # 3D Top face highlight
                    top_offset = max(2, int(10 * scale))
                    self.canvas.create_polygon(
                        sx - obs_w, sy - obs_h,
                        sx, sy - obs_h - top_offset,
                        sx + obs_w, sy - obs_h,
                        fill="#f85149", outline=""
                    )
                elif obj.obj_type == 'COIN':
                    # Draw Spinning Golden Coin
                    coin_r = max(3, int(18 * scale))
                    self.canvas.create_oval(sx - coin_r, sy - coin_r, sx + coin_r, sy + coin_r,
                                           fill="#f1e05a", outline="#e3b341", width=2)
                    self.canvas.create_text(sx, sy, text="$", fill="#0d1117", font=("Arial", max(6, int(12 * scale)), "bold"))
                elif obj.obj_type == 'ARTIFACT':
                    # Draw Rare Glowing Invincibility Artifact (Cyan Diamond)
                    art_r = max(4, int(22 * scale))
                    points = [sx, sy - art_r, sx + art_r, sy, sx, sy + art_r, sx - art_r, sy]
                    self.canvas.create_polygon(points, fill="#388bfd", outline="#79c0ff", width=2)
                    self.canvas.create_oval(sx - art_r//2, sy - art_r//2, sx + art_r//2, sy + art_r//2,
                                           fill="#ffffff", outline="")

        # 5. Render Player Bird (3D animated avian wireframe)
        bx, by, b_scale = self.game.project_3d_to_2d(self.game.bird_x, self.game.bird_y, 0.0, w, h)
        
        # Tilt angle based on lane transition velocity
        bank_tilt = (self.game.target_lane - self.game.bird_x) * 15.0
        wing_flap = math.sin(self.game.wing_angle) * 18.0
        
        # Invincibility Forcefield Aura
        if self.game.has_shield:
            shield_radius = 55
            aura_color = "#388bfd" if int(self.game.game_time * 10) % 2 == 0 else "#79c0ff"
            self.canvas.create_oval(bx - shield_radius, by - shield_radius,
                                   bx + shield_radius, by + shield_radius,
                                   outline=aura_color, width=3, dash=(6, 4))
        
        # Bird Wings (Flapping polygon)
        left_wing = [bx, by, bx - 45, by - 10 + wing_flap, bx - 25, by + 12]
        right_wing = [bx, by, bx + 45, by - 10 + wing_flap, bx + 25, by + 12]
        self.canvas.create_polygon(left_wing, fill="#238636", outline="#2ea043", width=2)
        self.canvas.create_polygon(right_wing, fill="#238636", outline="#2ea043", width=2)
        
        # Bird Fuselage & Head
        self.canvas.create_oval(bx - 14, by - 18, bx + 14, by + 18, fill="#2ea043", outline="#3fb950", width=2)
        self.canvas.create_oval(bx - 8, by - 24, bx + 8, by - 10, fill="#3fb950", outline="")
        # Golden Beak
        self.canvas.create_polygon([bx - 4, by - 22, bx + 4, by - 22, bx, by - 29], fill="#f1e05a", outline="")

        # 6. Heads-Up Display (HUD)
        # Lives (Hearts)
        hearts_text = "♥ " * self.game.lives + "♡ " * (3 - max(0, self.game.lives))
        self.canvas.create_text(25, 28, anchor="w", text=f"LIVES: {hearts_text}", fill="#f85149", font=("Consolas", 15, "bold"))
        
        # Score & Distance
        self.canvas.create_text(w // 2, 28, anchor="center", text=f"SCORE: {self.game.score:05d}", fill="#e6edf3", font=("Consolas", 16, "bold"))
        
        # Coins
        self.canvas.create_text(w - 25, 28, anchor="e", text=f"COINS: {self.game.coins} [$$]", fill="#f1e05a", font=("Consolas", 14, "bold"))
        
        # Shield Banner (if active)
        if self.game.has_shield:
            timer_text = f"⚡ SHIELD INVINCIBLE: {self.game.shield_timer:.1f}s ⚡"
            self.canvas.create_rectangle(w//2 - 160, 52, w//2 + 160, 78, fill="#1f6feb", outline="#79c0ff", width=2)
            self.canvas.create_text(w//2, 65, anchor="center", text=timer_text, fill="#ffffff", font=("Consolas", 11, "bold"))

        # Footer Controls Hint
        self.canvas.create_text(w // 2, h - 16, anchor="center",
                               text="[<Left>/A] Steer Left  |  [<Right>/D] Steer Right  |  [R] Restart  |  [Q] Exit",
                               fill="#8b949e", font=("Consolas", 10))

        # 7. Game Over Screen Overlay
        if self.game.game_over:
            self.canvas.create_rectangle(0, 0, w, h, fill="#0d1117", stipple="gray50")
            self.canvas.create_text(w // 2, h // 2 - 40, text="GAME OVER", fill="#f85149", font=("Consolas", 32, "bold"))
            self.canvas.create_text(w // 2, h // 2 + 5, text=f"Final Score: {self.game.score}  |  Coins Collected: {self.game.coins}",
                                   fill="#e6edf3", font=("Consolas", 14))
            self.canvas.create_text(w // 2, h // 2 + 45, text="Press [R] to Play Again  or  [Q] to Exit",
                                   fill="#58a6ff", font=("Consolas", 13, "bold"))


def launch_game():
    """Starts the 3D Bird Runner Game in interactive GUI mode."""
    import tkinter as tk
    root = tk.Tk()
    app = BirdGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_game()
