import random
import math

import research

class Player:
    def __init__(self, name, id=None, budget=None, fleetsaves=None):
        self.name = name
        self.id = id # db id, only after insert
        self.tech = research.TechTree()
        self.budget = 0
        self.fleetsaves = fleetsaves or []
        if budget is not None:
            self.spend_budget_for_science(budget)

    def spend_budget_for_science(self, budget):
        self.budget += budget
        self.tech.spend_budget(budget)

    def get_fleet_multiplier(self):
        return sum( [ fs.get_fleet_value() for fs in self.fleetsaves ])

class FleetSaveData:
    def __init__(self, name, fleet_value_multiplier, fleet_on_planet_probability):
        self.name = name or ""
        self.fleet_value_multiplier = fleet_value_multiplier
        self.fleet_on_planet_probability = fleet_on_planet_probability

    def get_fleet_value(self):
        print("  checking fleetsave %s"%self.name)
        if not self.fleet_on_planet_probability():
            print("    not on planet")
            return 0
        else:
            print("    added")
            return self.fleet_value_multiplier

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

all_fleetsaves = {}
for item in [
            FleetSaveData("Paranoid Gary", 1, (lambda: False))                              # Never caught flat-flooted
           ,FleetSaveData("Don't even care", 1, (lambda: True))                             # Idiot just leaves everything in plain sight
           ,FleetSaveData("Leftovers", 0.05, (lambda: random.random() < 0.4))               # Just a few ships, ongoing constructions, etc
           ,FleetSaveData("Full fleet, extreme proba", 1, (lambda : random.random() < 0.7)) # Chance of meeting the entire fleet
           ,FleetSaveData("Full fleet, high proba", 1, (lambda : random.random() < 0.4))    # Chance of meeting the entire fleet
           ,FleetSaveData("Full fleet, medium proba", 1, (lambda : random.random() < 0.25)) # Chance of meeting the entire fleet
           ,FleetSaveData("Full fleet, low proba", 1, (lambda : random.random() < 0.15))    # Chance of meeting the entire fleet
           ,FleetSaveData("Full fleet, tiny proba", 1, (lambda : random.random() < 0.08))   # Chance of meeting the entire fleet
           ,FleetSaveData("Stationed squad", 0.1, (lambda: random.random() < 0.1))          # Small chance of having a minor squad stationed there
    ]:
    all_fleetsaves[item.name] = item

common_fleetsaves = [ all_fleetsaves["Leftovers"], all_fleetsaves["Stationed squad"] ]

all_players = [
            Player("Inactive"              ,budget=0            ,fleetsaves=[all_fleetsaves["Don't even care"]])
           ,Player("Special Snowflake"     ,budget=2000         ,fleetsaves=[all_fleetsaves["Don't even care"]])
           ,Player("Casual Jim"            ,budget=5000         ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, extreme proba"]] )
           ,Player("Teen spirit"           ,budget=10000        ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, extreme proba"]] )
           ,Player("raz0r"                 ,budget=50000        ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, high proba"]] )
           ,Player("Koni chew you"         ,budget=100000       ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, high proba"]] )
           ,Player("NoSleep"               ,budget=500000       ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, medium proba"]] )
           ,Player("FightMe"               ,budget=1000000      ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, high proba"]] )
           ,Player("Protoss"               ,budget=5000000      ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, medium proba"]] )
           ,Player("Hard Core Kerry"       ,budget=10000000     ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, medium proba"]] )
           ,Player("Bob the Builder"       ,budget=50000000     ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, tiny proba"]] )
           ,Player("Protean"               ,budget=100000000    ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, low proba"]] )
           ,Player("e-1337"                ,budget=500000000    ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, low proba"]] )
           ,Player("Grox Empire"           ,budget=1000000000   ,fleetsaves=common_fleetsaves + [all_fleetsaves["Full fleet, low proba"]] )
    ]
