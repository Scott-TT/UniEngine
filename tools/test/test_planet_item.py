import unittest

import planet_item

class TestResearch(unittest.TestCase):
    def test_cost_computation(self):
        item = planet_item.fleets["recycler"]
        self.assertEqual(10000,item.metal)
        self.assertEqual(74000,item.simplified_tech_cost())
