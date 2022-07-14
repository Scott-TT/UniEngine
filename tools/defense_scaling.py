import math
import random
import pprint

import planet_item

def get_random_profile():
    return random.choice(defensers_profiles)

class DefenseScaling:
    def __init__(self, description=None, multiplier=None):
        self.description=description
        self.multiplier = multiplier if multiplier is not None else 1
        # Random chance that the defender has been neglecting his defenses
        if random.random() < 0.1:
            self.multiplier *= 0.4

    def get_available_budget(self, juice):
        return math.floor(self.multiplier * juice)

    def fill_defenses(self, planet, juice):
        pass

class ZenMaster(DefenseScaling):
    def __init__(self):
        DefenseScaling.__init__( self
                                ,description="Pure balance : every build type gets the same resources spent (give or take random%)"
                                ,multiplier=1
                               )

    def fill_defenses(self, planet, juice):
        available_budget = self.get_available_budget(juice)
        defense_buildings = {k: v for k,v in planet_item.buildings.items() if v.juice < available_budget }
        total_value_per_item = available_budget / max(1,len(defense_buildings))
        for k,v in defense_buildings.items():
            if v.simplified_tech_cost() > available_budget:
                continue
            quantity = math.floor(total_value_per_item / v.juice * random.gauss(100,15)/100)
            if v.maximum_quantity:
                quantity = min(v.maximum_quantity,quantity)
            if quantity > 0:
                planet[k] = quantity

class RatioBalance(DefenseScaling):
    def __init__(self, name="Ratio-based", balance_by_budget=False, description=None, ratios={}, multiplier=None):
        DefenseScaling.__init__(self, description=description, multiplier=multiplier)
        self.ratios = ratios
        self.balance_by_budget = balance_by_budget
        
    def fill_defenses(self, planet, juice):
        available_budget = self.get_available_budget(juice)
        defense_buildings = {k: v for k,v in planet_item.buildings.items() if k in self.ratios \
                                                                              and self.ratios[k]>0 \
                                                                              and v.juice < available_budget \
                                                                              and v.simplified_tech_cost() < available_budget }
        total_weights = sum([ self.ratios[k] for k,v in defense_buildings.items() if v.maximum_quantity is None])
        if total_weights == 0:
            return
        if self.balance_by_budget:
            # Budget balance means that the ratio applies to budget (X gets half the budget of item Y)
            for k,v in defense_buildings.items():
                quantity = math.floor((self.ratios[k]/total_weights) * available_budget/v.simplified_cost() * random.gauss(100,10)/100)
                if v.maximum_quantity:
                    quantity = min(v.maximum_quantity,quantity)
                if quantity > 0:
                    planet[k] = quantity
        else:
            # Item balance means we want twice as many of item X as we do item Y, regardless of their relative costs
            sum_item_values = sum( [ self.ratios[k] * v.simplified_cost() for k,v in defense_buildings.items() if v.maximum_quantity is None] )
            sum_item_values += sum([ min(v.maximum_quantity,self.ratios[k]) * v.simplified_cost() for k,v in defense_buildings.items() if v.maximum_quantity is not None] )
            for k,v in defense_buildings.items():
                k_budget_ratio = self.ratios[k] * v.simplified_cost() / sum_item_values
                quantity = math.floor(k_budget_ratio * available_budget / v.simplified_cost() * random.gauss(100,10)/100)
                if v.maximum_quantity:
                    quantity = min(v.maximum_quantity,quantity)
                if quantity > 0:
                    planet[k] = quantity
                
class RocketMan(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,description="Rockets. Lots and lots of rockets."
                              ,ratios={"rocket_launcher":100, "small_shield_dome":50, "large_shield_dome":30}
                              ,multiplier=multiplier
                              )

class FodderLover(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={"rocket_launcher":100, "light_laser":100, "small_shield_dome":50, "large_shield_dome":30}
                              )

class EarlyBalance(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "rocket_launcher":60
                                       ,"light_laser":200
                                       ,"heavy_laser":20
                                       ,"small_shield_dome":4
                                       ,"large_shield_dome":3
                                       ,"ion_cannon": 10
                                       ,"gauss_cannon": 4
                                       ,"antiballistic_missile":10
                                       }
                              )

class BigGun(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "rocket_launcher":1000
                                       ,"light_laser":500
                                       ,"heavy_laser":0
                                       ,"small_shield_dome":10
                                       ,"large_shield_dome":8
                                       ,"ion_cannon": 40
                                       ,"gauss_cannon": 20
                                       ,"plasma_turret": 10
                                       ,"antiballistic_missile":10
                                       }
                              )
 
class FodderHeavy(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "rocket_launcher":500
                                       ,"light_laser":100
                                       ,"heavy_laser":25
                                       ,"small_shield_dome":10
                                       ,"large_shield_dome":8
                                       ,"ion_cannon": 8
                                       ,"gauss_cannon": 3
                                       ,"plasma_turret": 1
                                       ,"antiballistic_missile":10
                                       }
                              )

class AntiRip(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "rocket_launcher":2000
                                       ,"light_laser":3000
                                       ,"heavy_laser":1000
                                       ,"small_shield_dome":500
                                       ,"large_shield_dome":400
                                       ,"ion_cannon": 1000
                                       ,"gauss_cannon": 750
                                       ,"plasma_turret": 600
                                       ,"antiballistic_missile":100
                                       }
                              )

class AntiBattleships(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "rocket_launcher":1000
                                       ,"light_laser":500
                                       ,"heavy_laser":50
                                       ,"small_shield_dome":300
                                       ,"large_shield_dome":250
                                       ,"ion_cannon": 50
                                       ,"gauss_cannon": 35
                                       ,"plasma_turret": 10
                                       ,"antiballistic_missile":100
                                       }
                              )
        
class LateBalance(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "rocket_launcher":1000
                                       ,"light_laser":0
                                       ,"heavy_laser":300
                                       ,"small_shield_dome":300
                                       ,"large_shield_dome":250
                                       ,"ion_cannon": 0
                                       ,"gauss_cannon": 0
                                       ,"plasma_turret": 20
                                       ,"antiballistic_missile":20
                                       }
                              )

class AverageBalance(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "rocket_launcher":20
                                       ,"light_laser":100
                                       ,"heavy_laser":10
                                       ,"small_shield_dome":3
                                       ,"large_shield_dome":2
                                       ,"ion_cannon": 20
                                       ,"gauss_cannon": 10
                                       ,"plasma_turret": 5
                                       ,"antiballistic_missile":1
                                       }
                              )

class OneTrickPony(RatioBalance):
    def __init__(self, multiplier=None):
        ratios = {"small_shield_dome":10,"large_shield_dome":10}
        pick_order = [ k for k in list(planet_item.buildings) if planet_item.buildings[k].maximum_quantity is None ]
        random.shuffle(pick_order)
        main_trick = pick_order[0]
        ratios[main_trick] = 100
        for i in range(1,len(pick_order)-1):
            if random.random() < 0.5:
                ratios[pick_order[i]] = 10
            else:
                break
        RatioBalance.__init__(self, multiplier=multiplier, ratios=ratios)

defensers_profiles = [ RocketMan()          # Only rockets
                      ,FodderLover()        # Rockets and light lasers
                      ,FodderHeavy()        # Rockets and light lasers covering some big guns
                      ,EarlyBalance()
                      ,AverageBalance()
                      ,LateBalance()
                      ,ZenMaster()          # Every defense gets the same budget
                      ,BigGun()             # Specialized against early/midgame large ships
                      ,AntiRip()            # Specialized against deathstars
                      ,AntiBattleships()    # Specialized against battleships
                      ,OneTrickPony()       # Picks a random defense and mostly sticks to it
                     ]

