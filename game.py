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
TEST = False
VERB = False

NUM_ROUNDS = 5
GAME_SIZES = range(5, 11)
SIZES = len(GAME_SIZES)
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
	- gType: TEAM ~ team selection is intelligent, team voting is always accepted
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
	rIDs = set()
	sIDs = set()

	for name in players:
		if name in randSet:
			resistance.append(Resistance(name, rType, (nPlayers, RESISTANCE_NUMS[nPlayers])))
			rIDs.add(name)
		else:
			spies.append(Spy(name, sType, (nPlayers, RESISTANCE_NUMS[nPlayers])))
			sIDs.add(name)

	# Initialize Player Setups
	# - Setup resistance supsicions
	for r in resistance:
		r.initSuspicion(players)
	# - Setup spy supsicions
	for name in players:
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
	winner = False # Corresponds to spies winning
	
	########
	#RANDOM#
	########
	if gType == "RANDOM":
		for rnd in range(NUM_ROUNDS):
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
			# This is omitted in this part, since things are deterministic

			# Score Update - Could Probably be moved to another function
			danger: int = len(sIDs & teamIDs)
			if (nPlayers, rnd) in SPECIAL_MISSIONS:
				if danger > 1:
					sWins += 1
				else:
					rWins += 1
			else:
				if danger > 0:
					sWins += 1
				else:
					rWins += 1
			
			# Check Termination Conditions
			if (rWins > 2):
				if VERB:
					print("\n Resistance Wins!\n")
				winner = True
				break
				# return True

			elif (sWins > 2):
				if VERB:
					print("\n Spies Win!\n")
				break
				# return False
			
			# Update Suspicions
			votes = [False]*danger + [True]*(len(teamIDs) - danger)
			for r in resistance:
				r.updateSuspicion(votes, teamIDs)
	############
	#END RANDOM#
	############

	######
	#TEAM#
	######
	# Case of resistance is intelligence, spies are not really
	elif gType == "TEAM":
		for rnd in range(NUM_ROUNDS):
			if TEST:
				print(f"\n-- Round Number {rnd + 1} --")

			# -Team Selection is Intelligent for Resistance, not for Spies
			# Get the leader
			leaderID = rnd
			leader = False
			for player in resistance:
				if player.name == leaderID:
					leader = player
			for player in spies:
				if player.name == leaderID:
					leader = player

			# Get Team
			isSpecial = (nPlayers, rnd) in SPECIAL_MISSIONS 
			teamIDs = leader.selectTeam(MISSION_NUMS[nPlayers][rnd], "RESIST", isSpecial) 
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

			# Score Update - Could Probably be moved to another function
			danger: int = len(sIDs & teamIDs)
			if (nPlayers, rnd) in SPECIAL_MISSIONS:
				if danger > 1:
					sWins += 1
				else:
					rWins += 1
			else:
				if danger > 0:
					sWins += 1
				else:
					rWins += 1

			# Check Termination Conditions
			if (rWins > 2):
				if VERB:
					print("\n Resistance Wins!\n")
				winner = True
				break
				# return True

			elif (sWins > 2):
				if VERB:
					print("\n Spies Win!\n")
				break
				# return False
			
			# Update Suspicions
			votes = [False]*danger + [True]*(len(teamIDs) - danger)
			for r in resistance:
				r.updateSuspicion(votes, teamIDs)

	##########
	#END TEAM#
	##########

	#######
	#INTEL#
	#######
	# Case of resistance is intelligence, and spies are too
	elif gType == "INTEL":
		for rnd in range(NUM_ROUNDS):
			if TEST:
				print(f"\n-- Round Number {rnd + 1} --")

			# -Team Selection is Intelligent for Resistance, not for Spies
			# Get the leader
			leaderID = rnd
			leader = False
			for player in resistance:
				if player.name == leaderID:
					leader = player
			for player in spies:
				if player.name == leaderID:
					leader = player

			# Get Team - this is literally the only place where the code changed.
			# This should certainly be cleaned up.
			isSpecial = (nPlayers, rnd) in SPECIAL_MISSIONS 
			teamIDs = leader.selectTeam(MISSION_NUMS[nPlayers][rnd], "INTEL", isSpecial) 
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

			# Score Update - Could Probably be moved to another function
			danger: int = len(sIDs & teamIDs)
			if (nPlayers, rnd) in SPECIAL_MISSIONS:
				if danger > 1:
					sWins += 1
				else:
					rWins += 1
			else:
				if danger > 0:
					sWins += 1
				else:
					rWins += 1

			# Check Termination Conditions
			if (rWins > 2):
				if VERB:
					print("\n Resistance Wins!\n")
				winner = True
				break
				# return True

			elif (sWins > 2):
				if VERB:
					print("\n Spies Win!\n")
				break
				# return False
			
			# Update Suspicions
			votes = [False]*danger + [True]*(len(teamIDs) - danger)
			for r in resistance:
				r.updateSuspicion(votes, teamIDs)

	###########
	#END INTEL#
	###########

	#########
	#COMPLEX#
	#########
	# Case where people are intelligent, and resistance
	# will downvote teams that are too suspicious. 
	elif gType == "COMPLEX":
		leaderID = 0
		for rnd in range(NUM_ROUNDS):
			if TEST:
				print(f"\n-- Round Number {rnd + 1} --")

			# -Team Selection is Intelligent 
			teamFails = 0
			teamIDs = set() # defined in the loop below
			while True:
				# Get the leader
				leader = False
				for player in resistance:
					if player.name == leaderID:
						leader = player
				for player in spies:
					if player.name == leaderID:
						leader = player

				# Get Team - this is literally the only place where the code changed.
				# This should certainly be cleaned up.
				isSpecial = (nPlayers, rnd) in SPECIAL_MISSIONS 
				teamIDs = leader.selectTeam(MISSION_NUMS[nPlayers][rnd], "INTEL", isSpecial) 
				if VERB: 
					print(teamIDs)

				if (teamFails == 4):
					# Team is always approved on the fifth time around
					break

				# Voting on the Team - assume spies approve
				votesFor = 0
				threshold = 0.4
				if isSpecial:
					threshold = 0.8
				for player in resistance:
					if player.judgeTeam(teamIDs, threshold):
						votesFor += 1

				if (2*votesFor > MISSION_NUMS[nPlayers][rnd]):
					# Corresponds to team being approved
					break
				else:
					# Corresponds to team not being approved
					teamFails += 1
					leaderID = (leaderID + 1) % nPlayers

			# The current array of people going on the mission
			team = []
			for r in resistance:
				if r.name in teamIDs:
					team.append(r)
			for s in spies:
				if s.name in teamIDs:
					team.append(s)

			# Score Update - Could Probably be moved to another function
			danger: int = len(sIDs & teamIDs)
			if (nPlayers, rnd) in SPECIAL_MISSIONS:
				if danger > 1:
					sWins += 1
				else:
					rWins += 1
			else:
				if danger > 0:
					sWins += 1
				else:
					rWins += 1

			# Check Termination Conditions
			if (rWins > 2):
				if VERB:
					print("\n Resistance Wins!\n")
				winner = True
				break
				# return True

			elif (sWins > 2):
				if VERB:
					print("\n Spies Win!\n")
				break
				# return False
			
			# Update Suspicions
			votes = [False]*danger + [True]*(len(teamIDs) - danger)
			for r in resistance:
				r.updateSuspicion(votes, teamIDs)

			# Get next Team Leader
			leaderID = (leaderID + 1) % nPlayers
		
	## Game Finish ##
	if VERB:
		print("The final states were: ")
		print("\n--- Resistance Members ---")
		for r in resistance:
			print(r)
	## Get Statistics on How Long it takes to figure out spy identities
	"""
	We will return 
	(winner, finRound, perfects, atLeastOne),
	where
	- winner: True if Resistance won, False if Spies won
	- finRound: The Round at which the game terminated
	- perfects: The Number of Resistance members that figured out all spy identities
	- atLeastOne: The Number of resistance members that figured out at least one spy identity
	"""

	perfects = 0
	atLeastOne = 0
	
	for r in resistance:
		info = 0
		susp = r.suspicion
		for x in susp:
			if abs(susp[x] - 1.0) < 10**(-20):
				info += 1
		if (info == (Resistance.nPlayers - Resistance.nResistance)):
			perfects += 1
		if (info > 0):
			atLeastOne += 1
	
	return (winner, rnd+1, perfects, atLeastOne)
	

### User Input ###

### TEAM - Resistance and Spies Intelligence Case
# Colecting data
ITERATIONS = 2000
stats: List[List[Tuple[int]]] = [[] for j in GAME_SIZES]
for size in GAME_SIZES:
	for j in range(ITERATIONS):
		x = game(size, "COMPLEX", "COMPLEX", "COMPLEX")
		stats[size - GAME_SIZES[0]].append(x)

# Getting Counts
nResistWins = [0 for j in GAME_SIZES]
finRounds = [{3: 0, 4: 0, 5: 0} for j in GAME_SIZES]
finRoundsResistance = [{3: 0, 4: 0, 5: 0} for j in GAME_SIZES]
finRoundsSpies = [{3: 0, 4: 0, 5: 0} for j in GAME_SIZES]
perfectArr = [{} for j in GAME_SIZES]
atLeastOneArr = [{} for j in GAME_SIZES]
for j in range(SIZES):
	for instance in stats[j]:
		# Counting Wins and Subdivided Rounds to Win
		if instance[0] == True:
			nResistWins[j] += 1
			finRoundsResistance[j][instance[1]] += 1
		else:
			finRoundsSpies[j][instance[1]] += 1
		# Counting Number of Rounds to Win
		finRounds[j][instance[1]] += 1
		# Counting Number of Perfects
		if instance[2] in perfectArr[j]:
			perfectArr[j][instance[2]] += 1
		else:
			perfectArr[j][instance[2]] = 1
		# Counting Number of At Least Ones
		if instance[3] in atLeastOneArr[j]:
			atLeastOneArr[j][instance[3]] += 1
		else:
			atLeastOneArr[j][instance[3]] = 1

s = ""
s += f"Number of Resistance Wins: \n {nResistWins} \n\
Numbers of Ending Rounds: \n {finRounds} \n\
Numbers of Resistance Ending Rounds: \n {finRoundsResistance} \n\
Numbers of Spy Ending Rounds: \n {finRoundsSpies} \n\
Number of perfects: \n {perfectArr} \n\
Number of at least ones: \n {atLeastOneArr} \n"

COMPLEX_STATS_FNAME = "complexStats-0.4.txt"
bothStats = open(COMPLEX_STATS_FNAME, 'w')
bothStats.write(s)
bothStats.close()

# COMPLEX_STATS_FNAME = "complexStats.txt"
# bothStats = open(COMPLEX_STATS_FNAME, 'w')
# bothStats.write(s)
# bothStats.close()

# INTEL_STATS_FNAME = "both-intel.txt"
# bothStats = open(INTEL_STATS_FNAME, 'w')
# bothStats.write(s)
# bothStats.close()

# TEAM_STATS_FNAME = "resistance-intel.txt"
# intelStats = open(TEAM_STATS_FNAME, 'w')
# intelStats.write(s)
# intelStats.close()

# ### Random - Random case
# # Collecting data
# ITERATIONS = 2000
# stats: List[List[Tuple[int]]] = [[] for j in GAME_SIZES]
# for size in GAME_SIZES:
# 	for j in range(ITERATIONS):
# 		x = game(size, "SIMPLE", "SIMPLE")
# 		stats[size - GAME_SIZES[0]].append(x)

# # Getting Counts
# nResistWins = [0 for j in GAME_SIZES]
# finRounds = [{3: 0, 4: 0, 5: 0} for j in GAME_SIZES]
# finRoundsResistance = [{3: 0, 4: 0, 5: 0} for j in GAME_SIZES]
# finRoundsSpies = [{3: 0, 4: 0, 5: 0} for j in GAME_SIZES]
# perfectArr = [{} for j in GAME_SIZES]
# atLeastOneArr = [{} for j in GAME_SIZES]
# for j in range(SIZES):
# 	for instance in stats[j]:
# 		# Counting Wins and Subdivided Rounds to Win
# 		if instance[0] == True:
# 			nResistWins[j] += 1
# 			finRoundsResistance[j][instance[1]] += 1
# 		else:
# 			finRoundsSpies[j][instance[1]] += 1
# 		# Counting Number of Rounds to Win
# 		finRounds[j][instance[1]] += 1
# 		# Counting Number of Perfects
# 		if instance[2] in perfectArr[j]:
# 			perfectArr[j][instance[2]] += 1
# 		else:
# 			perfectArr[j][instance[2]] = 1
# 		# Counting Number of At Least Ones
# 		if instance[3] in atLeastOneArr[j]:
# 			atLeastOneArr[j][instance[3]] += 1
# 		else:
# 			atLeastOneArr[j][instance[3]] = 1

# s = ""
# s += f"Number of Resistance Wins: \n {nResistWins} \n\
# Numbers of Ending Rounds: \n {finRounds} \n\
# Numbers of Resistance Ending Rounds: \n {finRoundsResistance} \n\
# Numbers of Spy Ending Rounds: \n {finRoundsSpies} \n\
# Number of perfects: \n {perfectArr} \n\
# Number of at least ones: \n {atLeastOneArr} \n"

# RAND_STATS_FNAME = "randomstats.txt"
# randStats = open(RAND_STATS_FNAME, 'w')
# randStats.write(s)
# randStats.close()








