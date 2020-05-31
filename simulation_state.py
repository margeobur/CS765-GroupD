from robot import Robot
from environment import Environment
from brain import EvolvableBrain


aspect_ratio_x = 2.0/3.0
text_size = 20
arena_width = 40
timestep = 0.04
iteration = 0

pop_size = 30
env = None
evolvable_brains = []
robots = []


def setup():
    global env
    global iteration
    iteration = 0
    env = Environment()

    for i in range(0, pop_size):
        b = EvolvableBrain()
        b.randomise()
        evolvable_brains.append(b)

    for i in range(0, pop_size):
        r = Robot()
        r.set_brain(evolvable_brains[i])
        r.set_environment(env)
        robots.append(r)
