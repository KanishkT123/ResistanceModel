#################
## - Kanishk Tantia & Shyan Akmal
## - 2017/12/1
## - Discrete Math Modeling
## - Final Project
#################

## Imports ##
from typing import Dict, List
## ####### ##

## Some Typing ##
ID = int
## ########### ##


## Resistance Class ##
class Resistance:
	def __init__(self, name: ID, strat: str):
		"""
		- name:      unique ID for the player
		- strat:     a string identifying how the player will play the game
		- suspicion: a dictionary from names to reals, where the value for
		             each player name will equal the current probability 
		             that player is a spy
		"""
		self.name = name
		self.strat = strat
		self.suspicion = {} # Initialized as an empty dictionary

	def initSuspicion(self, playerList: List[ID], nResistance):
		"""
		Initializes the probability distribution, for a particular resistance
		member, for the likelihood of each player being a spy.

		Should only be called ONCE at the very beginning of gameplay.
		"""
		nPlayers = len(playerList)
		
		for player in playerList:
			if player == self.name:
				# The player knows that they themselves are not a spy
				self.suspicion[player] = 0
			else:
				# Uniform suspicion for all other players
				self.suspicion[player] = float(1 - (nResistance/nPlayers))


## Temporary Testing ##

## ################# ##