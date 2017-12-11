#################
## - Kanishk Tantia & Shyan Akmal
## - 2017/12/1
## - Discrete Math Modeling
## - Final Project
#################

## Imports ##
from typing import Dict, List, Tuple, Set
from itertools import combinations, product
from numpy import prod
## ####### ##

## Some Typing ##
ID = int
Vote = bool
## ########### ##


## Resistance Class ##
class Resistance:

	# Class Variables representing knowledge of the game
	# -- these are default initialized to the smallest game example
	nPlayers = 5
	nResistance = 3


	def __init__(self, name: ID, strat: str, nGame: Tuple[int, int] = (5, 3)):
		"""
		- name:      unique ID for the player
		- strat:     a string identifying how the player will play the game
		- suspicion: a dictionary from names to reals, where the value for
		             each player name will equal the current probability 
		             that player is a spy
		- nGame:     (nPlayers, nResistance)
		"""
		self.name = name
		self.strat = strat

		self.suspicion: Dict[ID, float] = {} # Initialized as an empty dictionary

		#! TODO: It might be silly to implement the below within
		#!       the __init__ method
		# Set knowledge of what the game looks like
		Resistance.nPlayers, Resistance.nResistance = nGame

	def __repr__(self):
		rep = f"Resistance Member \
		\n- ID: {self.name} \
		\n- Strategy: {self.strat} \
		\n- Suspicions: {str(self.suspicion)}"

		return rep

	def initSuspicion(self, playerList: List[ID]):
		"""
		Initializes the probability distribution, for a particular resistance
		member, for the likelihood of each player being a spy.

		Should only be called ONCE at the very beginning of gameplay.
		"""
		nSpies = Resistance.nPlayers - Resistance.nResistance

		for player in playerList:
			if player == self.name:
				# The player knows that they themselves are not a spy
				self.suspicion[player] = 0.0
			else:
				# Uniform suspicion for all other players
				# Note that we subtract one from the denominator
				self.suspicion[player] = float(nSpies/(Resistance.nPlayers - 1))


	def updateSuspicion(self, votes: List[Vote], missionList: Set[ID], spyStrat: str = "SIMPLE"):
		"""
		Given the observed votes in the round, and a list of IDs for the players
		who went on the mission, updates the player probability distribution
		using Bayes Rule. 

		Takes in a parameter to determine how exactly the likelihood should
		be calculated.
		"""
		# Holds posterior suspicions
		post: Dict[ID, float] = {}
		evidence: float = self.computeEvidence(votes, missionList, spyStrat)
		# print(f"The Probability of Votes: {evidence}\n")

		for player, prior in self.suspicion.items():
			if player != self.name:
				# Compute likelihood for being a spy
				llhoodSpy: float = self.computeLikelihood(player, votes, missionList, spyStrat)
				# print(f"The Probability of Votes Given that {player} is a spy: {llhoodSpy}")

				# Take the ratios scaled by the prior to get the posterior 
				# probability of being a spy
				postSpy = llhoodSpy/evidence
				post[player] = postSpy

		# Update probabilities at the very end
		self.suspicion = {player:post[player] for player in post}
		self.suspicion[self.name] = 0.0

	def computeEvidence(self, votes: List[Vote], mission: Set[ID], spyStrat: str):
		"""
		Computes the probability of observing a given set of votes. 
		"""
		# # print("#### EVIDENCE ####")

		playerSet: Set[ID] = set(self.suspicion.keys())

		nFailures = len([vote for vote in votes if vote == False])
		# # print(f"We had {nFailures} failures.")

		nSpies = Resistance.nPlayers - Resistance.nResistance

		notMission = playerSet - mission

		evidence = 0.0
		if spyStrat == "SIMPLE":
			missionPoss = list(map(set, list(combinations(mission, nFailures))))
			notMissionPoss = list(map(set, list(combinations(notMission, nSpies - nFailures))))


			for x in missionPoss:
				for y in notMissionPoss:
					prob = self.probAssignment(x, mission)*self.probAssignment(y, notMission)
					evidence += prob

			return evidence

	def computeLikelihood(self, query: ID, votes: List[Vote], mission: Set[ID], spyStrat: str):
		"""
		Computes the probability that we would see some votes and hat
		the query is a spy.
		"""
		playerSet: Set[ID] = set(self.suspicion.keys())

		nFailures = len([vote for vote in votes if vote == False])
		# # print(f"We had {nFailures} failures.")

		nSpies = Resistance.nPlayers - Resistance.nResistance

		notMission = playerSet - mission

		llhood = 0.0

		if spyStrat == "SIMPLE":
			missionPoss = list(map(set, list(combinations(mission, nFailures))))
			notMissionPoss = list(map(set, list(combinations(notMission, nSpies - nFailures))))


			for x in missionPoss:
				for y in notMissionPoss:
					z = x ^ y
					if (query in z):
						prob = self.probAssignment(x, mission)*self.probAssignment(y, notMission)
						llhood += prob

			return llhood

	def probAssignment(self, spies: Set[ID], group: Set[ID], ignore = set()):
		"""
		Given a set of spy candidates from an overall list of people who
		went on a mission, returns the probability exactly those candidates
		are the spies on the mission.

		Takes in an optional parameter ignore, which holds IDs that should be ignored
		in calculations.
		"""
		probOfSpies =  prod([self.suspicion[candidate] for candidate in spies])
		probOfResistance = 1.0
		for player in group:
			if (player not in spies) and (player not in ignore):
				probOfResistance = probOfResistance * (1 - self.suspicion[player])
		
		# print("Spies: ", probOfSpies)
		# print("Resistance: ", probOfResistance)
		return probOfSpies * probOfResistance

	def selectTeam(self, size: int, strat = "INTEL", special = False):
		"""
		Outputs the set of IDs corresponding to the least suspicious players.
		"""
		allIDs = self.suspicion.keys()
		return set(sorted(allIDs, key = lambda x: self.suspicion[x])[0:size])



## Temporary Testing ##
TESTING = False
if TESTING:
	#  Test 1
	#  - The setup here is very silly since we're imagining everyone is resistance
	A = Resistance(0, "SIMPLE")
	B = Resistance(1, "SIMPLE")
	C = Resistance(2, "SIMPLE")
	D = Resistance(3, "SIMPLE")
	E = Resistance(4, "SIMPLE")

	players = [A, B, C, D, E]
	names = ["A", "B", "C", "D", "E"]
	for ix, player in enumerate(players):
		player.initSuspicion(range(5))
		print(f"Player {names[ix]} status: \n", player, "\n")

	# Imagine we start with players A, B going on a mission, and there is one failure observed
	for ix, player in enumerate(players):
		# Just test the first player
		print("If A and B go on a mission, and exactly one fails...\n")
		player.updateSuspicion([True, False], {0, 1})
		print("\nCalculations Finished.\n")
		print(f"Player {names[ix]} has updated status:\n", player, "\n")


	# Imagine after this, we have A and D go on a mission, and there is one failure observed
	for ix, player in enumerate(players):
		# Just test the first player
		print("If A and B go on a mission, and exactly one fails...\n")
		player.updateSuspicion([True, False], {0, 1})
		print("\nCalculations Finished.\n")
		print(f"Player {names[ix]} has updated status:\n", player, "\n")


	# Imagine after this, we have A and D go on a mission, and there is one failure observed
	for ix, player in enumerate(players):
		# Just test the first player
		print("If A and B go on a mission, and exactly one fails...\n")
		player.updateSuspicion([True, False], {0, 3})
		print("\nCalculations Finished.\n")
		print(f"Player {names[ix]} has updated status:\n", player, "\n")


	#  Test 2
	## ################# ##