from sheep import Sheep
from shepherd import Shepherd

import numpy as np
import time

sheep = Sheep(pos = np.array([1,1]))
shepherd = Shepherd(pos = np.array([0,0]))
print('test', shepherd.get_control([sheep], [shepherd]))
print(sheep.get_distance(shepherd))