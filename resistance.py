#################
## - Kanishk Tantia & Shyan Akmal
## - 2017/12/1
## - Discrete Math Modeling
## - Final Project
#################

## Imports ##
from typing import Dict, List, Tuple
## ####### ##

## Some Typing ##
ID = int
## ########### ##


## Resistance Class ##
class Resistance:

	# Class Variables representing knowledge of the game
	# -- these are default initialized to the smallest game example
	nPlayers = 5
	nResistance = 3


	def __init__(self, name: ID, strat: str, nGame: Tuple[int, int]):
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

		self.suspicion = {} # Initialized as an empty dictionary

		#! TODO: It might be silly to implement the below within
		#!       the __init__ method
		# Set knowledge of what the game looks like
		Resistance.nPlayers, Resistance.nResistance = nGame

	def initSuspicion(self, playerList: List[ID]):
		"""
		Initializes the probability distribution, for a particular resistance
		member, for the likelihood of each player being a spy.

		Should only be called ONCE at the very beginning of gameplay.
		"""
		for player in playerList:
			if player == self.name:
				# The player knows that they themselves are not a spy
				self.suspicion[player] = 0.0
			else:
				# Uniform suspicion for all other players
				self.suspicion[player] = float(1 - (Resistance.nResistance/Resistance.nPlayers))


	def updateSuspicion(self):
		"""
		Given the observed votes in the round, and a list of IDs for the players
		who went on the mission, updates the player probability distribution
		using Bayes Rule. 

		Takes in a parameter to determine how exactly the likelihood should
		be calculated.
		"""

## Temporary Testing ##

## ################# ##