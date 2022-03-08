from math import remainder
import numpy as np

def solve_positions(distance_matrix, n_dim=3):
    """
    Build coordinate base from point-to-point distance matrix.
    See: https://math.stackexchange.com/questions/156161/finding-the-coordinates-of-points-from-distance-matrix
    
    Arguments:

        distance_matrix :
            [
                [0, 1, 2], # distace from point 0 to other points
                [1, 0, 4], # distace from point 1 to other points
                [2, 4, 0] # distace from point 2 to other points
            ]
        
        n_dim           : number of dimensions to search for

    Returns:
        positions:  np.array -- point positions as rows
        err:        float -- mean square sum of terms not fitted
    """
    # build Gram matrix
    D = distance_matrix
    Ni = len(D)
    M = np.zeros(Ni**2).reshape([Ni, Ni])

    for i in range(len(D)):
        for j in range(len(D[i])):
            M[i, j] = 0.5 * ((D[0][j]**2) + (D[i][0]**2) - (D[i][j]**2))

    # solve base
    (S, U) = np.linalg.eig(M)

    # normalize corner coordinates as rows of X
    X = U.dot(np.sqrt(np.diag(np.abs(S))))
    pos = X[:, 0:n_dim]

    # error
    remainder_terms = X[:, n_dim:-1].flatten()
    err = np.sqrt(np.sum(remainder_terms**2)) / len(remainder_terms)

    return pos, err

