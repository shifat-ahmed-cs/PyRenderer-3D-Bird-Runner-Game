"""
Launcher script for the 3D Bird Runner Game (CSE 423 Computer Graphics).
Run with:
    python run_bird_game.py
"""
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.bird_runner_3d import launch_game

if __name__ == "__main__":
    print("=" * 65)
    print("      CSE 423: 3D BIRD RUNNER - 3-LANE PERSPECTIVE FLIGHT")
    print("=" * 65)
    print("Controls:")
    print("  - Steer Left   : Left Arrow / A Key")
    print("  - Steer Right  : Right Arrow / D Key")
    print("  - Restart      : R Key")
    print("  - Exit         : Q Key / Escape")
    print("\nFeatures:")
    print("  - 3-Lane Perspective Flight with vanishing horizon")
    print("  - Approaching 3D Monolith Obstacles")
    print("  - 3 Lives System (Hearts)")
    print("  - Golden Coins (+50 pts) & Invincibility Artifact Shields (+100 pts)")
    print("=" * 65)
    print("Launching interactive graphical game window...")
    launch_game()

