import numpy as np

from dltx import DLTrecon, DLTcalib


def print_h(msg):
    """
    Utility for printing underlined message ("heading").
    """
    print("\n%s\n%s\n" % (msg, "-" * len(msg)))


def test_3d():
    # Tests of DLTx
    print_h("Test of camera calibration and point reconstruction based on direct linear transformation (DLT).")
    print("3D (x, y, z) coordinates (in cm) of the corner of a cube (the measurement error is at least 0.2 cm):")
    xyz = [[0, 0, 0], [0, 12.3, 0], [14.5, 12.3, 0], [14.5, 0, 0], [
        0, 0, 14.5], [0, 12.3, 14.5], [14.5, 12.3, 14.5], [14.5, 0, 14.5]]
    print(np.asarray(xyz))
    print("2D (u, v) coordinates (in pixels) of 4 different views of the cube:")
    uv1 = [[1302, 1147], [1110, 976], [1411, 863], [1618, 1012],
           [1324, 812], [1127, 658], [1433, 564], [1645, 704]]
    uv2 = [[1094, 1187], [1130, 956], [1514, 968], [1532, 1187],
           [1076, 854], [1109, 647], [1514, 659], [1523, 860]]
    uv3 = [[1073, 866], [1319, 761], [1580, 896], [1352, 1016],
           [1064, 545], [1304, 449], [1568, 557], [1313, 668]]
    uv4 = [[1205, 1511], [1193, 1142], [1601, 1121], [1631, 1487],
           [1157, 1550], [1139, 1124], [1628, 1100], [1661, 1520]]
    print("uv1:")
    print(np.asarray(uv1))
    print("uv2:")
    print(np.asarray(uv2))
    print("uv3:")
    print(np.asarray(uv3))
    print("uv4:")
    print(np.asarray(uv4))

    print_h(
        "Use 4 views to perform a 3D calibration of the camera with 8 points of the cube:")
    nd = 3
    nc = 4
    L1, err1 = DLTcalib(nd, xyz, uv1)
    print("Camera calibration parameters based on view #1:")
    print(L1)
    print("Error of the calibration of view #1 (in pixels):")
    print(err1)

    # -----------------
    L2, err2 = DLTcalib(nd, xyz, uv2)
    print("Camera calibration parameters based on view #2:")
    print(L2)
    print("Error of the calibration of view #2 (in pixels):")
    print(err2)

    # -----------------
    L3, err3 = DLTcalib(nd, xyz, uv3)
    print("Camera calibration parameters based on view #3:")
    print(L3)
    print("Error of the calibration of view #3 (in pixels):")

    # -----------------
    print(err3)
    L4, err4 = DLTcalib(nd, xyz, uv4)
    print("Camera calibration parameters based on view #4:")
    print(L4)
    print("Error of the calibration of view #4 (in pixels):")
    print(err4)
    xyz1234 = np.zeros((len(xyz), 3))
    L1234 = [L1, L2, L3, L4]
    for i in range(len(uv1)):
        xyz1234[i, :] = DLTrecon(
            nd, nc, L1234, [uv1[i], uv2[i], uv3[i], uv4[i]])

    # -----------------
    print("Reconstruction of the same 8 points based on 4 views and the camera calibration parameters:")
    print(xyz1234)
    print("Mean error of the point reconstruction using the DLT (error in cm):")
    print(np.mean(np.sqrt(np.sum((np.array(xyz1234)-np.array(xyz))**2, 1))))


def test_2d():
    print_h("Test of the 2D DLT")
    print("2D (x, y) coordinates (in cm) of the corner of a square (the measurement error is at least 0.2 cm):")
    xy = [[0, 0], [0, 12.3], [14.5, 12.3], [14.5, 0]]
    print(np.asarray(xy))
    print("2D (u, v) coordinates (in pixels) of 2 different views of the square:")
    uv1 = [[1302, 1147], [1110, 976], [1411, 863], [1618, 1012]]
    uv2 = [[1094, 1187], [1130, 956], [1514, 968], [1532, 1187]]
    print("uv1:")
    print(np.asarray(uv1))
    print("uv2:")
    print(np.asarray(uv2))

    # -----------------
    print_h("Use 2 views to perform a 2D calibration of the camera with 4 points of the square:")
    nd = 2
    nc = 2

    L1, err1 = DLTcalib(nd, xy, uv1)
    print("Camera calibration parameters based on view #1:")
    print(L1)
    print("Error of the calibration of view #1 (in pixels):")
    print(err1)

    L2, err2 = DLTcalib(nd, xy, uv2)
    print("Camera calibration parameters based on view #2:")
    print(L2)
    print("Error of the calibration of view #2 (in pixels):")
    print(err2)

    # ----------
    xy12 = np.zeros((len(xy), 2))
    L12 = [L1, L2]
    for i in range(len(uv1)):
        xy12[i, :] = DLTrecon(nd, nc, L12, [uv1[i], uv2[i]])

    # -----------------
    print("Reconstruction of the same 4 points based on 2 views and the camera calibration parameters:")
    print(xy12)
    print("Mean error of the point reconstruction using the DLT (error in cm):")
    print(np.mean(np.sqrt(np.sum((np.array(xy12)-np.array(xy))**2, 1))))

    print("")
    print("Use only one view to perform a 2D calibration of the camera with 4 points of the square:")
    nd = 2
    nc = 1
    L1, err1 = DLTcalib(nd, xy, uv1)
    print("Camera calibration parameters based on view #1:")
    print(L1)
    print("Error of the calibration of view #1 (in pixels):")
    print(err1)

    # -----------------
    xy1 = np.zeros((len(xy), 2))
    for i in range(len(uv1)):
        xy1[i, :] = DLTrecon(nd, nc, L1, uv1[i])
    print("Reconstruction of the same 4 points based on one view and the camera calibration parameters:")
    print(xy1)
    print("Mean error of the point reconstruction using the DLT (error in cm):")
    print(np.mean(np.sqrt(np.sum((np.array(xy1)-np.array(xy))**2, 1))))


if __name__ == "__main__":
    test_3d()
#    test_2d()
