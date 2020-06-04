import random
from robot import Robot
import simulation_state

generation = 0
tournament = 0

trial_length = 1500
n_trials = 1
fitnesses = [0] * simulation_state.pop_size
history_size = 500

mean_fitness_history = []
peak_fitness_history = []


def iterate_evolve():
    global generation
    global tournament

    tournament += 1
    a_id = random.randrange(0, simulation_state.pop_size)
    b_id = random.randrange(0, simulation_state.pop_size)

    while a_id == b_id:
        random.randrange(0, simulation_state.pop_size)

    a = Robot(simulation_state.robot_genomes[a_id])
    a.set_environment(simulation_state.env)
    a.draw()
    b = Robot(simulation_state.robot_genomes[b_id])
    b.set_environment(simulation_state.env)
    b.draw()

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

    simulation_state.robot_genomes[loser_id].crossover(simulation_state.robot_genomes[winner_id])


def main():
    global tournament
    tournament = 1
    iterate_evolve()

