import unittest

from research import *

class TestResearch(unittest.TestCase):
    def test_cost_computation(self):
        tech = all_techs["espionage"]
        self.assertEqual(4000, tech.get_cost(3)["crystal"])

    def test_levelup_cost(self):
        tech = all_techs["espionage"]
        self.assertEqual(2000, tech.get_levelup_cost(2)["crystal"])
        self.assertEqual(4000, tech.get_cost(level=3, levelup_only=True)["crystal"])

    def test_cost_with_dependencies(self):
        tech = all_techs["shielding"]
        self.assertEqual(4600, tech.get_cost(1, levelup_only=False, include_dependencies=True)["crystal"]) #600 + 4k from espionage 3

    def test_budget_allocation_basic(self):
        tech_tree = TechTree()
        tech_tree.spend_budget(2000)
        self.assertEqual(1, tech_tree.tech["armour"])

    def test_budget_allocation_complex(self):
        tech_tree = TechTree()
        tech_tree.spend_budget(150000)
        self.assertEqual(6, tech_tree.tech["laser"])
        self.assertEqual(4, tech_tree.tech["armour"])
        self.assertEqual(3, tech_tree.tech["combustion_drive"])
