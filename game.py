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
from typing import List, Dict, Tuple
from itertools import combinations
from random import sample
## ####### ##

### Constants Used Throughout ###
TEST = True 
VERB = True

NUM_ROUNDS = 5
# Number of Players -> Number of Resistanc Members
RESISTANCE_NUMS: Dict[int, int] = {5: 3, 6: 4, 7: 4, 8: 5, 9: 6, 10: 6}
# Number of Players -> Mission Sizes
MISSION_NUMS: Dict[int, List[int]] = {5: [2, 3, 2, 3, 3], 6: [2, 3, 4, 3, 4],
7: [2, 3, 3, 4, 4], 8: [3, 4, 4, 5, 5], 9: [3, 4, 4, 5, 5], 10: [3, 4, 4, 5, 5]}
# (Number of Players, Mission # Index)
SPECIAL_MISSIONS: Set[Tuple[int, int]] = {(7, 3), (8, 3), (9, 3), (10, 3)}

### Main Game Loop ###
def game(nPlayers: int, rType: str = "SIMPLE", sType: str = "SIMPLE", gType: str = "RANDOM"):
	"""
	- gType: RANDOM ~ team selection is random, team voting is always accepted
	- gType: TEAM ~ team selection is intelligent, team voting is random
	- gType: INTEL ~ team selection is intelligent, team voting is intelligent (for resistance and spies)
	- gType: COMPLEX ~ this is TEAM mode, but spies follow ADV strategy instead of SIMPLE
	"""

	## Initialize the Game ##
	# Get the players
	players: List[ID] = range(nPlayers)
	randSpec = sample(set(combinations(players, RESISTANCE_NUMS[nPlayers])), 1)[0]
	randSet = {x for x in randSpec}
	resistance: List = []
	spies: List = []

	for name in players:
		if name in randSet:
			resistance.append(Resistance(name, rType))
		else:
			spies.append(Spy(name, sType))

	# Initialize Player Setups
	# - Setup resistance supsicions
	for r in resistance:
		r.initSuspicion(players)
	# - Setup spy supsicions
	for j in players:
		if name in randSet:
			Spy.suspicion[name] = 0
		else:
			Spy.suspicion[name] = 1

	### Print what we just created
	if TEST:
		print("\nResistance Members:")
		for r in resistance:
			print(r)
		print("\nSpies:")
		for s in spies:
			print(s)
	##                     ##

	## Main Game Loop ##
	rWins, sWins = (0, 0)

	for rnd in range(NUM_ROUNDS):
		if gType == "RANDOM":
			if TEST:
				print(f"\n-- Round Number {rnd + 1} --")

			# -Team Selection is Random
			teamIDs = set(sample(set(players), MISSION_NUMS[nPlayers][rnd]))
			if VERB: 
				print(teamIDs)

			# The current array of people going on the mission
			team = []
			for r in resistance:
				if r.name in teamIDs:
					team.append(r)
			for s in spies:
				if s.name in teamIDs:
					team.append(s)

			# if VERB:
				# print(f"On the Mission: {team}")

			# -Voting on Teams - We Always Accept (nothing here)

			# Mission Vote

			# Check Termination Conditions

			# Update Suspicions



	# -Team Voting

	# - Mission Voting



	

### User Input ###
game(5, "SIMPLE", "SIMPLE")
