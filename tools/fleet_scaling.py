import math
import random
from pprint import pprint

import planet_item

def get_random_profile():
    if random.random() < 0.3:
        return ZenMaster()
    return random.choice(fleet_profiles)

class FleetScaling:
    def __init__(self, description=None, multiplier=None):
        self.description=description
        self.multiplier = multiplier if multiplier is not None else 1

    def get_available_budget(self, juice):
        return math.floor(self.multiplier * juice)

    def fill_fleets(self, planet):
        pass

class ZenMaster(FleetScaling):
    def __init__(self, multiplier=None):
        FleetScaling.__init__(self, multiplier=multiplier, description="Pure balance : every ship type gets the same resources spent (give or take random%)")

    def fill_fleets(self, planet, juice):
        available_budget = self.get_available_budget(juice)
        ships = {k: v for k,v in planet_item.fleets.items() if v.juice < available_budget }
        total_value_per_item = available_budget / max(1,len(ships))
        for k,v in ships.items():
            if v.simplified_tech_cost() > available_budget:
                continue
            quantity = math.floor(total_value_per_item / v.juice)
            if quantity > 0:
                planet[k] = quantity

class RatioBalance(FleetScaling):
    def __init__(self, balance_by_budget=False, description=None, ratios={}, multiplier=None):
        FleetScaling.__init__(self, description=description, multiplier=multiplier)
        self.ratios = ratios
        self.balance_by_budget = balance_by_budget
        
    def fill_fleets(self, planet, juice):
        available_budget = self.get_available_budget(juice)
        fleets = {k: v for k,v in planet_item.fleets.items() if k in self.ratios \
                                                                and self.ratios[k]>0 \
                                                                and v.juice < available_budget \
                                                                and v.simplified_tech_cost() < available_budget }
        total_weights = sum([ self.ratios[k] for k,v in fleets.items()])
        if total_weights == 0:
            return
        if self.balance_by_budget:
            # Budget balance means that the ratio applies to budget (X gets half the budget of item Y)
            for k,v in fleets.items():
                ship_ratio = self.ratios[k]/total_weights
                ship_cost = v.simplified_cost()
                quantity = math.floor(ship_ratio * available_budget / ship_cost * random.gauss(100,10)/100)
                if quantity > 0:
                    planet.parameters[k] = quantity
        else:
            # Item balance means we want twice as many of item X as we do item Y, regardless of their relative costs
            sum_item_values = sum( [ self.ratios[k] * v.simplified_cost() for k,v in fleets.items()] )
            for k,v in fleets.items():
                k_budget_ratio = self.ratios[k] * v.simplified_cost() / sum_item_values
                quantity = math.floor(k_budget_ratio * available_budget / v.simplified_cost() * random.gauss(100,10)/100)
                if quantity > 0:
                    planet.parameters[k] = quantity

class Transporter(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self, multiplier=multiplier
                              ,ratios={"small_cargo_ship":5, "big_cargo_ship":3}
                              )

class LightFighters(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "small_cargo_ship":0
                                       ,"big_cargo_ship":0
                                       ,"light_fighter":100
                                       ,"heavy_fighter":5
                                       ,"cruiser":0
                                       ,"battleship":0
                                       ,"battlecruiser":0
                                       ,"recycler":0
                                       ,"bomber":0
                                       ,"destroyer":0
                                       ,"deathstar":0
                                      }
                              )

class CruiseMode(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "small_cargo_ship":10
                                       ,"big_cargo_ship":0
                                       ,"light_fighter":100
                                       ,"heavy_fighter":5
                                       ,"cruiser":20
                                       ,"battleship":0
                                       ,"battlecruiser":0
                                       ,"recycler":0
                                       ,"bomber":0
                                       ,"destroyer":0
                                       ,"deathstar":0
                                      }
                              )

class GreenWarrior(RatioBalance):
    def __init__(self, multiplier=None):
        RatioBalance.__init__(self
                              ,multiplier=multiplier
                              ,ratios={ "small_cargo_ship":0
                                       ,"big_cargo_ship":5
                                       ,"light_fighter":0
                                       ,"heavy_fighter":0
                                       ,"cruiser":0
                                       ,"battleship":0
                                       ,"battlecruiser":0
                                       ,"recycler":100
                                       ,"bomber":0
                                       ,"destroyer":0
                                       ,"deathstar":0
                                      }
                              )


class OneTrick(RatioBalance):
    def __init__(self, multiplier=None):
        ratios={}
        trick = random.choice(["battleship","battlecruiser","bomber","destroyer","deathstar"])
        RatioBalance.__init__(self, multiplier=multiplier, ratios={trick:1})


fleet_profiles = [ ZenMaster()
                  ,Transporter()        # Non-combat fleet, mostly transporters
                  ,LightFighters()
                  ,CruiseMode()
                  ,OneTrick()
                  ,GreenWarrior()       # Non-combat fleet, mostly recyclers
                 ]
