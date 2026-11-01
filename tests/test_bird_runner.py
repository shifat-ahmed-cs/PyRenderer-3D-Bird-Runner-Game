"""
Unit tests for the 3D Bird Runner Game (CSE 423 Computer Graphics).
Verifies game mechanics: 3-lane movement, perspective projection,
collision detection, lives management, coin collection, and artifact shields.
"""
import unittest
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.bird_runner_3d import BirdGame3D, GameObject


class TestBirdRunner3D(unittest.TestCase):
    def setUp(self):
        self.game = BirdGame3D()

    def test_initial_state(self):
        """Verify starting parameters."""
        self.assertEqual(self.game.lives, 3)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.coins, 0)
        self.assertEqual(self.game.current_lane, 0)
        self.assertFalse(self.game.has_shield)
        self.assertFalse(self.game.game_over)

    def test_lane_movement_boundaries(self):
        """Verify bird lane switching stays within [-1, 0, 1]."""
        self.game.move_left()
        self.assertEqual(self.game.target_lane, -1)
        self.game.move_left()  # Boundary check: cannot go beyond left (-1)
        self.assertEqual(self.game.target_lane, -1)

        self.game.move_right()
        self.assertEqual(self.game.target_lane, 0)
        self.game.move_right()
        self.assertEqual(self.game.target_lane, 1)
        self.game.move_right()  # Boundary check: cannot go beyond right (+1)
        self.assertEqual(self.game.target_lane, 1)

    def test_coin_collection(self):
        """Verify picking up coins increases coin count and score."""
        self.game.objects.append(GameObject(lane=0, z=0.5, obj_type='COIN'))
        self.game.update(0.05)
        self.assertEqual(self.game.coins, 1)
        self.assertGreaterEqual(self.game.score, 50)

    def test_artifact_shield_activation(self):
        """Verify collecting an invincibility artifact grants shield."""
        self.game.objects.append(GameObject(lane=0, z=0.5, obj_type='ARTIFACT'))
        self.game.update(0.05)
        self.assertTrue(self.game.has_shield)
        self.assertGreater(self.game.shield_timer, 0.0)
        self.assertGreaterEqual(self.game.score, 100)

    def test_obstacle_collision_decreases_life(self):
        """Verify hitting an obstacle without shield loses 1 life."""
        self.game.objects.append(GameObject(lane=0, z=0.5, obj_type='OBSTACLE'))
        self.game.update(0.05)
        self.assertEqual(self.game.lives, 2)
        self.assertFalse(self.game.game_over)

    def test_obstacle_collision_with_shield_preserves_life(self):
        """Verify shield prevents life loss when colliding with obstacle."""
        self.game.has_shield = True
        self.game.shield_timer = 5.0
        self.game.objects.append(GameObject(lane=0, z=0.5, obj_type='OBSTACLE'))
        self.game.update(0.05)
        self.assertEqual(self.game.lives, 3, "Shield must protect lives!")

    def test_game_over_on_zero_lives(self):
        """Verify 3 collisions trigger game over."""
        self.game.lives = 1
        self.game.objects.append(GameObject(lane=0, z=0.5, obj_type='OBSTACLE'))
        self.game.update(0.05)
        self.assertEqual(self.game.lives, 0)
        self.assertTrue(self.game.game_over)

    def test_perspective_projection_math(self):
        """Verify 3D coordinates map to valid 2D screen coordinates with depth scaling."""
        screen_x, screen_y, scale = self.game.project_3d_to_2d(0.0, 0.0, 10.0, width=600, height=500)
        self.assertIsInstance(screen_x, int)
        self.assertIsInstance(screen_y, int)
        self.assertGreater(scale, 0.0)
        self.assertLess(scale, 1.0)  # Object at distance 10 should be smaller than at distance 0


if __name__ == "__main__":
    unittest.main()

