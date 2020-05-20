import rps.robotarium as robotarium
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.misc import *
from rps.utilities.controllers import *


from sheep import Sheep
from shepherd import Shepherd

import numpy as np
import time

# Instantiate Robotarium object
N_SHEEP = 2
N_SHEPHERD = 4
N = N_SHEEP + N_SHEPHERD

ITERATIONS = 500

sheeps = [Sheep() for _ in range(N_SHEEP)]
shepherds = [Shepherd() for _ in range(N_SHEPHERD)]

# initial_conditions = np.array(
#     np.mat('1 0.5 -0.5 0 0.28; 0.8 -0.3 -0.75 0.1 0.34; 0 0 0 0 0'))

initial_conditions = np.array(
    np.mat('0 -0.5 -1 1 1 0.5; 0 0 0.1 -0.5 0.8 -0.3; 0 0 0 0 0 0'))


r = robotarium.Robotarium(number_of_robots=N, show_figure=True,
                          initial_conditions=initial_conditions, sim_in_real_time=True, number_of_shepherds = N_SHEPHERD)

# Create barrier certificates to avoid collision
uni_barrier_cert = create_unicycle_barrier_certificate()

# define x initially
x = r.get_poses()
r.step()
si_to_uni_dyn, uni_to_si_states = create_si_to_uni_mapping()

# While the number of robots at the required poses is less
# than N...

for iteration in range(ITERATIONS):

    # Get poses of agents
    x = r.get_poses()
    x_si = uni_to_si_states(x)

    for i in range(x_si.shape[1]):
        (sheeps + shepherds)[i].pos = x_si[:2, i].T

    dxu = np.zeros((2, N))
    for i in range(x_si.shape[1]):
        dxu[:, i] = (sheeps + shepherds)[i].get_control(sheeps, shepherds).T

    # Create safe control inputs (i.e., no collisions)
    dxu = uni_barrier_cert(dxu, x)

    dxu = si_to_uni_dyn(dxu, x)
    # Set the velocities
    r.set_velocities(np.arange(N), dxu)

    # Iterate the simulation
    r.step()

# Call at end of script to print debug information and for your script to run on the Robotarium server properly
r.call_at_scripts_end()
