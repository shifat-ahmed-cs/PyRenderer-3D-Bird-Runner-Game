"""
Entry point for CSE423_Computer_Graphics (PyRenderer & 3D Bird Runner).
Run with:
    python main.py           # Runs the 2D/3D graphics pipeline demonstration
    python main.py --game    # Launches the interactive 3D Bird Runner game
"""
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    if "--game" in sys.argv:
        from src.bird_runner_3d import launch_game
        launch_game()
    else:
        from examples.demo import main as run_demo
        run_demo()
        print("\n[TIP] To launch the playable 3D Bird Runner Game (3 lanes, obstacles, coins, shield artifacts):")
        print("      python main.py --game")
        print("      or:")
        print("      python examples/run_bird_game.py")
