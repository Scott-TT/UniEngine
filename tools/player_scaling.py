import random
import math

import research

class Player:
    def __init__(self, name, budget=None):
        self.name = name
        self.tech = research.TechTree()
        if budget is not None:
            self.spend_budget_for_science(budget)

    def spend_budget_for_science(self, budget):
        self.tech.spend_budget(budget)
