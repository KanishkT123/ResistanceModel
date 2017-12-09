#################
## - Kanishk Tantia & Shyan Akmal
## - 2017/12/1
## - Discrete Math Modeling
## - Final Project
#################

## Imports ##
from typing import Dict, List, Tuple, Set
## ####### ##

## Some Typing ##
ID = int
Vote = bool
## ########### ##

## Spy Class ##
class Spy:

	# Class Variables representing knowledge of the game
	# -- these are default initialized to the smallest game example
	nPlayers = 5
	nResistance = 3
	suspicion = {}


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


		#! TODO: It might be silly to implement the below within
		#!       the __init__ method
		# Set knowledge of what the game looks like
		Spy.nPlayers, Spy.nResistance = nGame

	def __repr__(self):
		rep = f"Spy Member ^_^\
		\n- ID: {self.name} \
		\n- Strategy: {self.strat} "
		return rep