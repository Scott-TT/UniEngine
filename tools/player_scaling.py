import random
import math

import research

class Player:
    def __init__(self, name, id=None, budget=None):
        self.name = name
        self.id = id # db id, only after insert
        self.tech = research.TechTree()
        self.budget = 0
        if budget is not None:
            self.spend_budget_for_science(budget)

    def spend_budget_for_science(self, budget):
        self.budget += budget
        self.tech.spend_budget(budget)

class PlayerScaling:
    def __init__(self):
        pass

    def get_suitable_player(self, target, candidates=None):
        if candidates==None or len(candidates)<1 :
            candidates = all_players
        for player in candidates:
            if player.budget > target:
                return player
        return candidates[-1]

all_players = [
            Player("Inactive", budget=0)
           ,Player("Special Snowflake", budget=2000)
           ,Player("Casual Jim", budget=5000)
           ,Player("Teen spirit", budget=10000)
           ,Player("raz0r", budget=50000)
           ,Player("Koni chew you", budget=100000)
           ,Player("NoSleep", budget=500000)
           ,Player("FightMe", budget=1000000)
           ,Player("Protoss", budget=5000000)
           ,Player("Hard Core Kerry", budget=10000000)
           ,Player("Bob the Builder", budget=50000000)
           ,Player("Grox Empire", budget=100000000)
           ,Player("e-1337", budget=500000000)
           ,Player("Protean", budget=1000000000)
    ]
