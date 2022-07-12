import math
import random
import pprint

import planet_item

def get_random_profile():
    return random.choice(defensers_profiles)

class DefenseScaling:
    def __init__(self, description=None):
        self.description=description
        pass

    def fill_defenses(self, planet, juice):
        pass

class ZenMaster(DefenseScaling):
    def __init__(self):
        DefenseScaling.__init__(self, description="Pure balance : every build type gets the same resources spent (give or take random%)")

    def fill_defenses(self, planet, juice):
        defense_buildings = {k: v for k,v in planet_item.buildings.items() if v.juice < juice }
        total_value_per_item = juice / max(1,len(defense_buildings))
        for k,v in defense_buildings.items():
            if v.simplified_tech_cost() > juice:
                continue
            quantity = math.floor(total_value_per_item / v.juice * random.randint(50,200)/100)
            if v.maximum_quantity:
                quantity = min(v.maximum_quantity,quantity)
            if quantity > 0:
                planet[k] = quantity

class RatioBalance(DefenseScaling):
    def __init__(self, name="Ratio-based", description=None, ratios={}):
        self.ratios = ratios
        self.description = description
        
    def fill_defenses(self, planet, juice):
        defense_buildings = {k: v for k,v in planet_item.buildings.items() if k in self.ratios and self.ratios[k]>0 and v.juice < juice and v.simplified_tech_cost() < juice }
        total_weights = sum([ self.ratios[k] for k,v in defense_buildings.items() if v.maximum_quantity is None])
        if total_weights == 0:
            return
        for k,v in defense_buildings.items():
            quantity = math.floor((self.ratios[k]/total_weights) * juice/v.simplified_cost())
            if v.maximum_quantity:
                quantity = min(v.maximum_quantity,quantity)
            if quantity > 0:
                planet[k] = quantity
                
class RocketMan(RatioBalance):
    def __init__(self):
        RatioBalance.__init__(self
                              ,description="Rockets. Lots and lots of rockets."
                              ,ratios={"rocket_launcher":100, "small_shield_dome":50, "large_shield_dome":30}
                              )

class FodderLover(RatioBalance):
    def __init__(self):
        RatioBalance.__init__(self
                              ,ratios={"rocket_launcher":100, "light_laser":100, "small_shield_dome":50, "large_shield_dome":30}
                              )

class EarlyBalance(RatioBalance):
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
        RatioBalance.__init__(self
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
    def __init__(self):
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
        RatioBalance.__init__(self, ratios=ratios)


defensers_profiles = [  RocketMan(), FodderLover(), BigGun(), FodderHeavy()
                       ,EarlyBalance(), AverageBalance(), LateBalance(), ZenMaster()
                       ,AntiRip(), AntiBattleships()
                       ,OneTrickPony()
                     ]

