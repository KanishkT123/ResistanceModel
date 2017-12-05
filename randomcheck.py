#################
## - Shyan Akmal
## - 2017/12/1
## - Discrete Math Modeling
## - Final Project
#################

from typing import List
from math import factorial

def comb(n, k):
	ans = int(factorial(n) / factorial(k) / factorial(n - k))
	return ans

## Computing Random Stuff ##
def probRandomWin(R: int, S: int, M: List[int], specs = {}):
	"""
	R is the number of resistance.
	S is the number of spies.
	M is the a list dictating the length of each mission.
	specs is a set that has indices corresponding to which
	      missions need two spies to be failures. 
	"""
	mProbs = []
	for j in range(len(M)):
		if j not in specs:
			mProbs.append(float(comb(R, M[j])/comb((R+S), M[j])))
		else:
			mProbs.append(float((comb(R, M[j]) + S*comb(R, M[j]-1))/comb((R+S), M[j])))

	# Absolutely hardcoded
	zeroLoss = mProbs[0]*mProbs[1]*mProbs[2]
	oneLoss = mProbs[3] * (mProbs[0]*mProbs[1]*(1-mProbs[2]) + mProbs[1]*mProbs[2]*(1-mProbs[0]) +\
		mProbs[2]*mProbs[0]*(1-mProbs[1]))
	twoLoss = mProbs[4] * (mProbs[0]*mProbs[1]*(1-mProbs[2])*(1-mProbs[3]) +\
	(mProbs[0]*mProbs[2]*(1-mProbs[1])*(1-mProbs[3])) +\
	(mProbs[0]*mProbs[3]*(1-mProbs[1])*(1-mProbs[2])) +\
	(mProbs[1]*mProbs[2]*(1-mProbs[0])*(1-mProbs[3])) +\
	(mProbs[1]*mProbs[3]*(1-mProbs[0])*(1-mProbs[2])) +\
	(mProbs[2]*mProbs[3]*(1-mProbs[0])*(1-mProbs[1])))

	probWin = zeroLoss + oneLoss + twoLoss
	return probWin

print("5 Players: ", probRandomWin(3, 2, [2, 3, 2, 3, 3]))
print("6 Players: ", probRandomWin(4, 2, [2, 3, 4, 3, 4]))
print("7 Players: ", probRandomWin(4, 3, [2, 3, 3, 4, 4], {3}))
print("8 Players: ", probRandomWin(5, 3, [3, 4, 4, 5, 5], {3}))
print("9 Players: ", probRandomWin(6, 3, [3, 4, 4, 5, 5], {3}))
print("10 Players: ", probRandomWin(6, 4, [3, 4, 4, 5, 5], {3}))



