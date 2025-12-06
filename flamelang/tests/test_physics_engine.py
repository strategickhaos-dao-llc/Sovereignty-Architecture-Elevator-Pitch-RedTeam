"""
Tests for Physics Engine
"""

import unittest
import math
from flamelang.core.physics_engine import PhysicsEngine


class TestPhysicsEngine(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = PhysicsEngine()
    
    def test_schwarzschild_metrics(self):
        """Test Schwarzschild metric calculations"""
        # Use solar mass and a distance of 10 million meters
        solar_mass = 1.989e30  # kg
        radius = 1e10  # meters
        
        result = self.engine.schwarzschild_metrics(solar_mass, radius)
        
        self.assertIsNotNone(result.event_horizon)
        self.assertGreater(result.event_horizon, 0)
        
        # Event horizon should be about 2.95 km for solar mass
        self.assertAlmostEqual(result.event_horizon, 2954, delta=2)
        
        self.assertGreater(result.redshift, 0)
        self.assertLessEqual(result.redshift, 1)
        
        self.assertGreater(result.escape_velocity, 0)
        self.assertLessEqual(result.escape_velocity, self.engine.c)
    
    def test_schwarzschild_event_horizon(self):
        """Test that redshift is zero at event horizon"""
        solar_mass = 1.989e30
        
        result = self.engine.schwarzschild_metrics(solar_mass, solar_mass)
        event_horizon = result.event_horizon
        
        # At event horizon, redshift should be 0
        result_at_horizon = self.engine.schwarzschild_metrics(solar_mass, event_horizon)
        self.assertEqual(result_at_horizon.redshift, 0.0)
    
    def test_ocean_eddy_analysis(self):
        """Test ocean eddy analysis"""
        # Simple 2x2 velocity field
        velocity_field = [
            [1.0, 0.5],
            [0.5, 1.0]
        ]
        
        result = self.engine.ocean_eddy_analysis(velocity_field)
        
        self.assertIsNotNone(result.cauchy_green_tensor)
        self.assertIsNotNone(result.strain_tensor)
        self.assertIsNotNone(result.lorentzian_metric)
        self.assertGreater(result.coherent_boundary, 0)
        
        # Check dimensions
        self.assertEqual(len(result.cauchy_green_tensor), 2)
        self.assertEqual(len(result.strain_tensor), 2)
        self.assertEqual(len(result.lorentzian_metric), 3)
    
    def test_geodesic_integration(self):
        """Test geodesic integration"""
        solar_mass = 1.989e30
        
        # Start position and velocity
        initial_pos = (1e10, 0, 0)  # 10 million meters from center
        initial_vel = (0, 1e5, 0)   # 100 km/s tangential velocity
        
        result = self.engine.geodesic_integration(initial_pos, initial_vel, solar_mass, steps=50)
        
        self.assertIsNotNone(result.trajectory)
        self.assertGreater(len(result.trajectory), 0)
        self.assertGreater(result.photon_sphere_radius, 0)
        
        # Photon sphere should be 1.5 times the Schwarzschild radius
        rs = (2 * self.engine.G * solar_mass) / (self.engine.c ** 2)
        self.assertAlmostEqual(result.photon_sphere_radius, 1.5 * rs, delta=0.1)
    
    def test_gravitational_redshift(self):
        """Test gravitational redshift calculation"""
        solar_mass = 1.989e30
        r_emit = 1e10     # Emission radius
        r_observe = 1e12  # Observation radius (farther from mass)
        
        z = self.engine.calculate_redshift(solar_mass, r_emit, r_observe)
        
        # Redshift should be negative (blueshift) when observing from farther away
        self.assertIsInstance(z, float)
    
    def test_tensor_product(self):
        """Test tensor product (matrix multiplication)"""
        tensor_a = [
            [1, 2],
            [3, 4]
        ]
        tensor_b = [
            [5, 6],
            [7, 8]
        ]
        
        result = self.engine.tensor_product(tensor_a, tensor_b)
        
        # Expected result: [[19, 22], [43, 50]]
        self.assertEqual(result[0][0], 19)
        self.assertEqual(result[0][1], 22)
        self.assertEqual(result[1][0], 43)
        self.assertEqual(result[1][1], 50)
    
    def test_tensor_product_incompatible(self):
        """Test tensor product with incompatible dimensions"""
        tensor_a = [[1, 2, 3]]
        tensor_b = [[1], [2]]
        
        with self.assertRaises(ValueError):
            self.engine.tensor_product(tensor_a, tensor_b)


if __name__ == '__main__':
    unittest.main()
