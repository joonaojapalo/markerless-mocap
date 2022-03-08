import numpy as np

from dist2coords import solve_positions
from dltx import DLTcalib, DLTrecon

# load dataset
from datasets.table.calibration_coords import cameras, world_distances


def compute_fit_error(cameras, L_arr):
    err_squares = 0.0
    for i, _ in enumerate(cameras[0]):
        x = [cameras[j][i] for j in range(len(cameras))]
        y = DLTrecon(n_dim, n_cam, L_arr, x)
        err_squares += ((y - world_pos[i])**2).sum()
    return np.sqrt(err_squares) / len(cameras[0])


n_dim = 3   # 3D world
n_cam = len(cameras)

world_pos, err = solve_positions(world_distances, n_dim)
print("World positions fit error (MRS): %.2f" % (err,))
print("World positions:\n", world_pos)

L_arr = []
for i, cam in enumerate(cameras):
    L, err = DLTcalib(n_dim, world_pos, np.array(cam))
    L_arr.append(L)
    print("Error of the calibration of camera %i (in pixels): %.3f" % (i, err))

# transform (pixel coords from all cameras)
query_pixels = [
    # cup trace points
    [
        [1957, 1593], [1301, 1852]
    ],
    [
        [2204, 1603], [2615, 2006]
    ]
]

fit_err = compute_fit_error(cameras, L_arr)
print("Camera fit error (MSE): %.3f" % fit_err)

p_prev = None
for i, x in enumerate(query_pixels):
    assert(n_cam == len(x))
    y = DLTrecon(n_dim, n_cam, L_arr, x)
    print("Projected:", y)

    if p_prev is not None:
        delta = np.sqrt((y - p_prev).dot(y - p_prev))
        print("Delta %.2f cm" % (delta,))

    p_prev = y
