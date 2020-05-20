from sheep import Sheep
from shepherd import Shepherd

import numpy as np
import time

sheep = Sheep(pos = np.array([1,1]))
shepherd = Shepherd(pos = np.array([0,0]))
shepherd_2 = Shepherd(pos = np.array([0,0]))
l = [shepherd_2, shepherd]
l.remove(shepherd_2)
print(shepherd_2 == shepherd)
print(shepherd_2 == shepherd_2)
print(l)
print('test', shepherd.get_control([sheep], [shepherd]))
print(sheep.get_distance(shepherd))