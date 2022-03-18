from math import pi
from numpy import arccos
from numpy.linalg import norm


def vang(a, b):
    return arccos(a.dot(b)/(norm(a)*norm(b)))


def r2d(x):
    return x * 180 / pi


def getvec(x, num_point):
    return x[:, 1+3*num_point:1+3*(num_point+1)]
