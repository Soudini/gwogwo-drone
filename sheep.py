from robot import Robot
import numpy as np
from math import exp

D_STAR = 0.3  # distance to other sheeps
ALPHA = D_STAR**2

REPULSIVE_CONSTANT = 0.5  # from shepherds
SPEED_MULTIPLIER = 0.02  # for the speed comand


class Sheep(Robot):
    id_increment = 0

    def __init__(self, pos=[0, 0]):
        super().__init__(np.array(pos))
        self.id = Sheep.id_increment
        Sheep.id_increment += 1

    def get_control(self, sheeps, shepherds):
        """returns dxu for the robot in numpy array formated as [x,y]"""
        if self.id == 0:
            potential = lambda x: self.to_shepherd_potential(x, shepherds)
        else:
            potential = lambda x: self.to_sheeps_potential(x, sheeps) + self.to_shepherd_potential(x, shepherds)
        # potential = lambda x: self.to_sheeps_potential(x, sheeps)
        # potential = lambda x: 1
        return SPEED_MULTIPLIER * self.get_potential_direction(potential)

    def to_shepherd_potential(self, location, shepherds):
        distances = np.array(
            [np.linalg.norm(location - shepherd.pos[:2]) for shepherd in shepherds if shepherd != self])
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos[:2]), axis=0, arr=sheeps)
        potential = REPULSIVE_CONSTANT / np.min(distances)
        return potential

    def to_sheeps_potential(self, location, sheeps):
        distance = np.min(np.array([np.linalg.norm(location - sheep.pos) for sheep in sheeps if sheep != self]))
        # distances = np.apply_along_axis(lambda sheep: np.linalg.norm(location - sheep.pos), axis=0, arr=sheeps)
        potential = 2 * distance + ALPHA /distance
        # potentials = distances

        return potential
