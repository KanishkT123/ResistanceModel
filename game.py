#################
## - Kanishk Tantia & Shyan Akmal
## - 2017/12/1
## - Discrete Math Modeling
## - Final Project
#################

## Local Imports ##
from resistance import *
from spy import *
##               ##

## Imports ##
from typing import List
from itertools import combinations
from random import sample
## ####### ##

### Number Players -> Number Resistance ###
TEST = True 
RESISTANCE_NUMS = {5: 3, 6: 4, 7: 4, 8: 5, 9: 6, 10: 6}

### Main Game Loop ###
def game(nPlayers: int, rType: str, sTrype: str):

	## Initialize the Game ##
	# Get the players
	randSpec = sample(set(combinations(range(nPlayers), RESISTANCE_NUMS[nPlayers])), 1)[0]
	randSet = {x for x in randSpec}
	print(type(randSpec), len(randSpec))
	resistance: List = []
	spies: List = []

	for name in range(nPlayers):
		if name in randSet:
			resistance.append(Resistance(name, "SIMPLE"))
		else:
			spies.append(Spy(name, "SIMPLE"))

	# Initialize Player Setups
	# - Setup resistance supsicions
	for r in resistance:
		r.initSuspicion(range(nPlayers))
	# - Setup spy supsicions
	for j in range(nPlayers):
		if name in randSet:
			Spy.suspicion[name] = 0
		else:
			Spy.suspicion[name] = 1

	### Print what we just created
	if TEST:
		for r in resistance:
			print(r)
		for s in spies:
			print(s)
	##                     ##

### User Input ###
game(5, "SIMPLE", "SIMPLE")
