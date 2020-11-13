import run
import unittest
from app.discspring import *
from flask import request

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = run.app.test_client()
        self.app.testing = True

    def test_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_Force(self):
        spring = DiscSpring([200,180,8,3,1,1], "Ti-6Al-4V", 108500, 0.34)
        self.assertAlmostEqual(spring.find_force(2), 8526.04, 1)

    def test_Stress(self):
        spring = DiscSpring([200,180,8,3,1,1], "Ti-6Al-4V", 108500, 0.34)
        self.assertAlmostEqual(spring.find_stress(2)[1], -944.45, 1)

if __name__ == '__main__':
    unittest.main()