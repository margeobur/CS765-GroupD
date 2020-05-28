import random
from robot import Robot
from environment import Environment
from brain import EvolvableBrain

# rxs = []
# rys = []
# ras = []
#
# food_xs = []
# food_ys = []
# water_xs = []
# water_ys = []
# trap_xs = []
# trap_ys = []
#
# aspect_ratio_x = 2.0/3.0
# text_size = 20
# arena_width = 40
# timestep = 0.04
# iteration = 0

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
	#user_input = input("Press Enter to start")
	setup()

main()
