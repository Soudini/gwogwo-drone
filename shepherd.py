from robot import Robot
import numpy as np
from math import exp

d_star = 0.2  # distance to sheeps
alpha = exp(d_star)

repulsive_constant = 1  # between shepherds


class Shepherd(Robot):
    def __init__(self, pos=[0, 0]):
        super().__init__(pos)

    def get_control(self, sheeps, shepherds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        # potential = lambda x: self.to_sheeps_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds)
        potential = lambda x: 10*self.to_sheeps_potential(x, sheeps)
        return self.get_potential_direction(potential)

    def to_shepherd_potential(self, location, shepherds):
        distances = np.array([np.linalg.norm(location - shepherd.pos[:2]) for shepherd in shepherds])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos[:2]), axis=0, arr=sheeps)
        potentials = repulsive_constant * np.exp(-distances)

        return np.sum(potentials)

    def to_sheeps_potential(self, location, sheeps):
        distances = np.array([np.linalg.norm(location - sheep.pos) for sheep in sheeps])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos), axis=0, arr=sheeps)
        potentials = distances + alpha * np.exp(-distances)

        print(potentials)

        return np.sum(potentials)
