from robot import Robot
import numpy as np
from math import exp, log

D_STAR = 0.5  # distance to sheeps
ALPHA = D_STAR**2

REPULSIVE_CONSTANT = 0.1  # between shepherds
SPEED_MULTIPLIER = 10  # for the speed comand


class Shepherd(Robot):
    def __init__(self, pos=[0, 0]):
        super().__init__(pos)

    def get_control(self, sheeps, shepherds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds)
        # potential = lambda x: self.to_sheeps_potential(x, sheeps)
        # potential = lambda x: 1

        return SPEED_MULTIPLIER * self.get_potential_direction(potential)

    def to_shepherd_potential(self, location, shepherds):
        distances = np.array([np.linalg.norm(location - shepherd.pos[:2]) for shepherd in shepherds if shepherd != self])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos[:2]), axis=0, arr=sheeps)
        potentials = REPULSIVE_CONSTANT / distances

        return np.sum(potentials)

    def to_sheep_potential(self, location, sheeps):
        distances = np.array([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos), axis=0, arr=sheeps)
        # potentials = distances + ALPHA * np.exp(-distances)
        potentials = distances + ALPHA / distances
        # potentials = distances

        # print(potentials)

        return np.sum(potentials)

    def to_sheep_line_potential(self, location, sheeps):
        pass

    def line_potential(self, location, point_1, point_2):
        u = point_2 - point_1
        n = u/np.linalg.norm(u)

        v1 = location - point_1
        v2 = location - point_2

        d_norm = np.cross(v1, n)
        d_tan = np.dot(v1, n)

        if d_tan < 0:
            return np.linalg.norm(v1)
        if d_tan > np.dot(u, n):
            return np.linalg.norm(v2)

        return abs(d_norm)

