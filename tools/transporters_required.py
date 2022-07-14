#!/usr/bin/python3

import sys
import math

resources = 0
for i in range(1,len(sys.argv)):
    resources += int(sys.argv[i]) * 1000
print("Transporters needed to bring back loot (half of available):")
small = math.ceil(resources / 2 / 5000)
large = math.ceil(resources / 2 / 25000)
print(f"    {small} small cargos")
print(f" or {large} big cargos")
recyc = math.ceil(resources / 2 / 20000)
print()
print(f" or {recyc} recyclers")

