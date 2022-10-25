import math

def rmse(coords1, coords2):
	if len(coords1) != len(coords2):
		raise ValueError("Arrays must have the same size")

	tot = 0
	for i in range(len(coords1)):
		for j in range(3):
			tot += pow(coords1[i][j] - coords2[i][j], 2)

	return math.sqrt(float(tot) / len(coords1))