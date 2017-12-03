#################
## - Kanishk Tantia & Shyan Akmal
## - 2017/12/1
## - Discrete Math Modeling
## - Final Project
#################

## Imports ##
from typing import Dict, List, Tuple
from itertools import combinations
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


	def updateSuspicion(self, votes: List[Vote], missionList: List[ID], spyStrat: str = "SIMPLE"):
		"""
		Given the observed votes in the round, and a list of IDs for the players
		who went on the mission, updates the player probability distribution
		using Bayes Rule. 

		Takes in a parameter to determine how exactly the likelihood should
		be calculated.
		"""
		# Holds posterior suspicions
		post: Dict[ID, float] = {}

		for player, prior in self.suspicion.items():
			if player != self.name:
				# Compute likelihood for being a spy
				llhoodSpy: float = self.computeLikelihood(player, votes, missionList, spyStrat)

				## Testing Stuff
				print(f"Player with id {self.name} thinks that the probability of these votes \
given that player with id {player} is a spy is {llhoodSpy}")
				

				evidence: float = self.computeEvidence(votes, missionList, spyStrat)

				## Testing Stuff
				print(f"Player with id {self.name} thinks that the probability of these votes \
overall is {llhoodSpy}")

				# Take the ratios scaled by the prior to get the posterior 
				# probability of being a spy
				rawPostSpy = llhoodSpy * prior
				postSpy = rawPostSpy/evidence
				post[player] = postSpy

		# Update probabilities at the very end
		self.suspicion = {player:post[player] for player in post}
		self.suspicion[self.name] = 0.0

	def computeEvidence(self, votes: List[Vote], missionList: List[ID], spyStrat: str):
		playerList: List[ID] = list(self.suspicion.keys())

		nFailures = len([vote for vote in votes if vote == False])
		missionSize = len(missionList)

		nSpies = Resistance.nPlayers - Resistance.nResistance

		evidence = 0.0
		if spyStrat == "SIMPLE":
			## In this strategy, we assume that the number of failures in the
			## vote results is equal to the number of spies who went on the mission.
			possWorlds = list(combinations(list(missionList), nFailures))

			for world in possWorlds:
				evidence += self.probAssignment(world, missionList)

		return evidence


	def computeLikelihood(self, query: ID, votes: Dict[ID, Vote], missionList: List[ID], spyStrat: str):
		"""
		Computes the likelihoods we would observe the input voteResults, given that
		the query player was a spy or a resistance member respectively.

		Note that we never compute likelihood for ourselves.
		"""
		playerList: List[ID] = list(self.suspicion.keys())
		print("List of IDs", playerList)

		nFailures = len([vote for vote in votes if vote == False])
		print("Num Failures", nFailures)
		missionSize = len(votes)
		print("Mission Size", missionSize)

		nSpies = Resistance.nPlayers - Resistance.nResistance

		llhood = 0.0
		if spyStrat == "SIMPLE":
			## In this strategy, we assume that the number of failures in the
			## vote results is equal to the number of spies who went on the mission.
			possWorlds = list(combinations(list(missionList), nFailures))

			if (query in votes):
				## Case where the query went on the mission
				# Looking at all possible subsets of the people who went on the mission
				# that could be spies
				worldsOI = [list(x[:]) for x in possWorlds if query in x]
				for world in worldsOI:
					world.remove(query)

				for world in worldsOI:
					probWorld = self.probAssignment(world, missionList, {query})
					llhood += probWorld
			else:
				## Case where the query did not go on the mission
				worldsOI = possWorlds
				scale = (nSpies - 1)/(nSpies - self.suspicion[query])
				for world in worldsOI:
					probWorld = scale * self.probAssignment(world, missionList)
					llhood += probWorld

		return llhood
	def probAssignment(self, spyList: List[ID], missionList: List[ID], ignore = set()):
		"""
		Given a list of spy candidates from an overall list of people who
		went on a mission, returns the probability exactly those candidates
		are the spies on the mission.

		Takes in an optional parameter ignore, which holds IDs that should be ignored
		in calculations.
		"""
		probOfSpies =  prod([self.suspicion[candidate] for candidate in spyList])
		probOfResistance = 1.0
		for player in missionList:
			if (player not in spyList) and (player not in ignore):
				probOfResistance = probOfResistance * (1 - self.suspicion[player])
		
		return probOfSpies * probOfResistance

## Temporary Testing ##
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
	if (ix == 2):
		player.updateSuspicion([True, False], [0, 1])
		print(f"Player {names[ix]} has updated status:\n", player, "\n")


#  Test 2
## ################# ##