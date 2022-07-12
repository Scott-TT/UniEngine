import math
import random
from pprint import pprint

import planet_item

def get_random_profile():
    if random.random() < 0.3:
        return ZenMaster()
    return random.choice(fleet_profiles)

class FleetScaling:
    def __init__(self, description=None):
        self.description=description
        pass

    def fill_fleets(self, planet, juice):
        pass

class ZenMaster(FleetScaling):
    def __init__(self):
        FleetScaling.__init__(self, description="Pure balance : every ship type gets the same resources spent (give or take random%)")

    def fill_fleets(self, planet, juice):
        ships = {k: v for k,v in planet_item.fleets.items() if v.juice < juice }
        total_value_per_item = juice / max(1,len(ships))
        for k,v in ships.items():
            if v.simplified_tech_cost() > juice:
                continue
            quantity = math.floor(total_value_per_item / v.juice)
            if quantity > 0:
                planet[k] = quantity

class RatioBalance(FleetScaling):
    def __init__(self, name="Ratio-based", description=None, ratios={}):
        self.ratios = ratios
        self.description = description
        
    def fill_fleets(self, planet, juice):
        fleets = {k: v for k,v in planet_item.fleets.items() if k in self.ratios and self.ratios[k]>0 and v.juice < juice and v.simplified_tech_cost() < juice }
        total_weights = sum([ self.ratios[k] for k,v in fleets.items()])
        if total_weights == 0:
            return
        for k,v in fleets.items():
            quantity = math.floor((self.ratios[k]/total_weights) * juice/v.simplified_cost() * random.gauss(100,10)/100)
            if quantity > 0:
                planet[k] = quantity

class Transporter(RatioBalance):
    def __init__(self):
        RatioBalance.__init__(self
                              ,ratios={"small_cargo_ship":5, "big_cargo_ship":3}
                              )

class LightFighters(RatioBalance):
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        ratios={}
        trick = random.choice(["battleship","battlecruiser","bomber","destroyer","deathstar"])
        RatioBalance.__init__(self, ratios={trick:1})


fleet_profiles = [ ZenMaster(), Transporter(), LightFighters(), CruiseMode(), OneTrick(), GreenWarrior() ]
