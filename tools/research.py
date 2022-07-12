import math
import economy_config

from pprint import pprint

class Research:
    def __init__(self, metal, crystal, deut, dependencies=None):
        self.metal = metal
        self.crystal = crystal
        self.deut = deut
        if dependencies==None:
            self.dependencies=[]
        else:
            self.dependencies = dependencies

    def get_levelup_cost(self, level):
        cost = {}
        for r in ["metal","crystal","deut"]:
            cost[r] = math.floor(getattr(self,r) * (math.pow(2,level-1)))
        return cost

    def get_cost(self, level, levelup_only=None, include_dependencies=None):
        if levelup_only is None or levelup_only == True:
            return self.get_levelup_cost(level)

        if include_dependencies is None:
            include_dependencies = True
        cost = {}
        for r in ["metal","crystal","deut"]:
            total_cost = math.floor(getattr(self,r) * (math.pow(2,level-1)))
            if include_dependencies:
                for dependency in self.dependencies:
                    for dep_tech, dep_level in dependency.items():
                        total_cost += (all_techs[dep_tech].get_cost(level=dep_level, levelup_only=False, include_dependencies=True))[r]
            cost[r] = total_cost
        return cost

    def get_simplified_cost(self, level, levelup_only=None, include_dependencies=None):
        cost = self.get_cost(level, levelup_only=levelup_only, include_dependencies=include_dependencies)
        return cost["metal"]*economy_config.metal_cost_ratio + cost["crystal"]*economy_config.crystal_cost_ratio + cost["deut"]*economy_config.deut_cost_ratio

class TechTree:
    def __init__(self):
        self.tech = {"espionage" : 0
                    ,"computer" : 0
                    ,"weapons" : 0
                    ,"shielding" : 0
                    ,"armour" : 0
                    ,"energy" : 0
                    ,"hyperspace" : 0
                    ,"combustion_drive" : 0
                    ,"impulse_drive" : 0
                    ,"hyperspace_drive" : 0
                    ,"laser" : 0
                    ,"ion" : 0
                    ,"plasma" : 0
                    ,"IRN" : 0
                    ,"astrophysic" : 0
                }

    def print(self):
        pprint(self.tech)

    def spend_budget(self, budget):
        remaining_budget = budget
        upgrade_costs = {}
        # Initialize costs
        for t,level in self.tech.items():
            if level == 0:
                upgrade_costs[t] = all_techs[t].get_simplified_cost(level=1, levelup_only=False, include_dependencies=True)
            else:
                upgrade_costs[t] = all_techs[t].get_simplified_cost(level=level+1, levelup_only=True)
        # Allocate the cheapest possible item, until out of budget
        while remaining_budget > 0:
            cheapest_tech = min(upgrade_costs, key=upgrade_costs.get)
            if upgrade_costs[cheapest_tech] < remaining_budget:
                remaining_budget -= upgrade_costs[cheapest_tech]
                self.tech[cheapest_tech] += 1
                upgrade_costs[cheapest_tech] = all_techs[cheapest_tech].get_simplified_cost(level=self.tech[cheapest_tech]+1, levelup_only=True)
            else:
                break


all_techs = {
     "espionage" : Research(200, 1000, 200)
    ,"computer" : Research(400,600,0)
    ,"weapons" : Research(800,200,0)
    ,"shielding" : Research(200,600,0, dependencies=[{"espionage":3}])
    ,"armour" : Research(1000,0,0)
    ,"energy" : Research(0,800,400)
    ,"hyperspace" : Research(0,4000,2000, dependencies=[{"energy":5},{"shielding":5}])
    ,"combustion_drive" : Research(400,0,600, dependencies=[{"energy":1}])
    ,"impulse_drive" : Research(2000,4000,600, dependencies=[{"energy":1}])
    ,"hyperspace_drive" : Research(10000,20000,6000, dependencies=[{"hyperspace":3}])
    ,"laser" : Research(200,100,0, dependencies=[{"energy":2}])
    ,"ion" : Research(1000,300,0, dependencies=[{"laser":5},{"energy":4}])
    ,"plasma" : Research(2000,4000,0, dependencies=[{"laser":10},{"energy":8},{"ion":5}])
    ,"IRN" : Research(240000,400000,160000, dependencies=[{"computer":8},{"hyperspace":8}])
    ,"astrophysic" : Research(4000,8000,4000)
}
