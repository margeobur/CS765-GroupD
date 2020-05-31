import random
from robot import Robot
from environment import Environment
from brain import EvolvableBrain


def setup():
    pop_size = 30
    env = Environment()
    evolvable_brains = []
    robots = []

    for i in range(0, pop_size):
        b = EvolvableBrain()
        b.randomise()
        evolvable_brains.append(b)

    for i in range(0, pop_size):
        r = Robot()
        r.set_brain(evolvable_brains[i])
        r.set_environment(env)
        robots.append(r)


def main():
    # user_input = input("Press Enter to start")
    setup()


main()
