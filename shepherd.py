from robot import Robot
import numpy as np
from math import exp, log

D_STAR = 0.1  # distance to sheeps
ALPHA = D_STAR**2  # for repulsive potential towards sheep
BETA = exp(D_STAR)  # for repulsive potential towards sheep links

REPULSIVE_CONSTANT = 5*ALPHA  # between shepherds
SPEED_MULTIPLIER = 10  # for the speed command


class Shepherd(Robot):
    def __init__(self, pos=[0, 0], sheep_number=None):
        super().__init__(pos)
        self.sheep_number = sheep_number

    def get_control(self, sheeps, shepherds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        return SPEED_MULTIPLIER * self.get_potential_direction(self.get_potential(sheeps, shepherds))

    def get_potential(self, sheeps, shepherds):
        potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds) + self.to_sheep_line_potential(x, sheeps)
        # potential = lambda x: self.to_sheep_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds)
        # potential = lambda x: self.to_sheep_line_potential(x, sheeps)
        # potential = lambda x: self.to_sheeps_potential(x, sheeps)
        # potential = lambda x: 1

        return potential

    def to_shepherd_potential(self, location, shepherds):
        distances = np.array([np.linalg.norm(location - shepherd.pos[:2]) for shepherd in shepherds if shepherd != self])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos[:2]), axis=0, arr=sheeps)
        potentials = REPULSIVE_CONSTANT / distances

        return np.sum(potentials)

    def to_sheep_potential(self, location, sheeps):
        # distances = np.array([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
        # potentials = distances + ALPHA * np.exp(-distances)
        # potentials = distances + ALPHA / distances
        # potentials = distances

        # print(potentials)
        # return np.sum(potentials)

        # finally we take into account only the closest sheep
        distance = np.min([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
        return distance + ALPHA / distance

    def to_sheep_line_potential(self, location, sheeps):
        line_distances = [self.line_distance(location, sheeps[i].pos, sheeps[j].pos) for j in range(len(sheeps)) for i in range(j+1, len(sheeps))]
        # potentials = [self.repulsive_line_potential(location, sheeps[i], sheeps[j]) for j in range(len(sheeps)) for i in range(j+1, len(sheeps))]
        potential = BETA * exp(-np.min(line_distances))
        return potential

    def repulsive_line_potential(self, location, sheep_1, sheep_2):
        dist = sheep_1.get_distance(sheep_2)
        return BETA/dist * exp(-self.line_distance(location, sheep_1.pos, sheep_2.pos))

    def line_distance(self, location, point_1, point_2):
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

