import random
import math

import research

class Player:
    def __init__(self, name):
        self.name = name
        self.tech = research.TechTree()

    def spend_budget_for_science(self, budget):
        self.tech.spend_budget(budget)
