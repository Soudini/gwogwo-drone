from robot import Robot
import numpy as np
from math import exp

D_STAR = 1  # distance to sheeps
ALPHA = exp(D_STAR)

REPULSIVE_CONSTANT = 1  # between shepherds
SPEED_MULTIPLIER = 10  # for the speed comand


class Shepherd(Robot):
    def __init__(self, pos=[0, 0]):
        super().__init__(pos)

    def get_control(self, sheeps, shepherds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        potential = lambda x: self.to_sheeps_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds)
        # potential = lambda x: self.to_sheeps_potential(x, sheeps)
        # potential = lambda x: 1
        return SPEED_MULTIPLIER * self.get_potential_direction(potential)

    def to_shepherd_potential(self, location, shepherds):
        distances = np.array([np.linalg.norm(location - shepherd.pos[:2]) for shepherd in shepherds])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos[:2]), axis=0, arr=sheeps)
        potentials = REPULSIVE_CONSTANT * np.exp(-distances)

        return np.sum(potentials)

    def to_sheeps_potential(self, location, sheeps):
        distances = np.array([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos), axis=0, arr=sheeps)
        potentials = distances + ALPHA * np.exp(-distances)
        # potentials = distances

        # print(potentials)

        return np.sum(potentials)
