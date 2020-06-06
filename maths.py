import numpy as np


def polar2vec(angle):
    return np.array([np.cos(angle), np.sin(angle)])


def rotation2d(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s], [s, c]])
