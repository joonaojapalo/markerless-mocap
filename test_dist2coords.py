import numpy as np

from dist2coords import solve_positions


def dist(a,b):
    return np.sqrt((a-b).T.dot(a-b))

# D = distance matrix D[i,j] = distance from i to j
D = [
    [0, 2, 2.828, 2, 3.464, 2.828],
    [2, 0, 2, 2.828, 2.828, 3.464],
    [2.828, 2, 0, 2, 2, 2.828],
    [2, 2.828, 2, 0, 2.828, 2],
    [3.464, 2.828, 2, 2.828, 0, 2],
    [2.828, 3.464, 2.828, 2, 2, 0]
]

# solver
pos, err = solve_positions(D)

# print results
print("positions:", pos)
print("Sum of squares remining terms:", err)

# verify distances
for i in range(1, len(D)):
    print("Distance to point %d: %.3f vs. original %.3f" % (i, dist(pos[0], pos[i]), D[0][i]))
