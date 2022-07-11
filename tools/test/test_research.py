import unittest

from research import *

class TestResearch(unittest.TestCase):
    def test_cost_computation(self):
        # Manual tech
        tech = Research(metal=200,crystal=1000,deut=200)
        self.assertEqual(200, tech.get_total_cost(1)["metal"])
        self.assertEqual(128000,tech.get_total_cost(8)["crystal"])

        # Registered tech
        tech = all_techs["espionage"]
        self.assertEqual(4000, tech.get_total_cost(3)["crystal"])

        # Registered tech, including dependencies
        tech = all_techs["shielding"]
        self.assertEqual(4600, tech.get_total_cost(1)["crystal"])
