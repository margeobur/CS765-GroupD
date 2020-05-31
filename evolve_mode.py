import random
from robot import Robot
import simulation_state


generation = 0
tournament = 0
pop_size = 50

trial_length = 1500
n_trials = 1
fitnesses = []
history_size = 500

mean_fitness_history = []
peak_fitness_history = []


def iterate_evolve():
    global generation
    global tournament
    global pop_size

    tournament += 1
    a_id = random.randrange(0, pop_size)
    b_id = random.randrange(0, pop_size)

    while (a_id == b_id):
        random.randrange(0, pop_size)

    a = Robot()
    a.set_brain(simulation_state.evolvable_brains[a_id])
    a.set_environment(simulation_state.env)
    b = Robot()
    b.set_brain(simulation_state.evolvable_brains[b_id])
    b.set_environment(simulation_state.env)

    a_fitness = 0
    b_fitness = 0

    for i in range(0, n_trials):
        simulation_state.env.reset()
        a.reset()
        b.reset()

    for i in range(0, trial_length):
        if a.is_alive:
            a.calculate_change()
            a.update()
            a_fitness += (a.food_battery + a.water_battery) / 2.0 / trial_length
        if b.is_alive:
            b.calculate_change()
            b.update()
            b_fitness += (b.food_battery + a.water_battery) / 2.0 / trial_length
        simulation_state.env.update()
        if not a.is_alive and not b.is_alive:
            break

    a_fitness /= n_trials
    b_fitness /= n_trials

    fitnesses[a_id] = a_fitness
    fitnesses[b_id] = b_fitness

    winner_id = b_id
    loser_id = a_id

    if fitnesses[a_id] > fitnesses[b_id]:
        winner_id = a_id
        loser_id = b_id

    simulation_state.evolvable_brains[loser_id] = \
        simulation_state.evolvable_brains[winner_id].imprint(simulation_state.evolvable_brains[loser_id])


def main():
    global tournament
    tournament = 1
    simulation_state.evolvable_brains = []
    iterate_evolve()


main()
