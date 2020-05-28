import random
import robot

def iterate_evolve():
	tournament+=1
	a_id = random.randrange(0, population_size)
	b_id = random.randrange(0, population_size)

	while (a_id == b_id):
		random.randrange(0, population_size)

	print(a_id, b_id)

	#a = robot()
	#a.set_brain(evolvable_brains[a_id])
	#a.set_environment(env)
	#b = robot()
	#b.set_brain(evolvable_brains[b_id])
	#b.set_environment(env)

def main():
	tournament = 1
	evolvable_brains = []
	iterate_evolve()