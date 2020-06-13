import random
import numpy as np
import turtle

from environment import Environment
from robot import Robot
import simulation_state
import json

TRIAL_LENGTH = int(1500 * 0.08 / simulation_state.timestep)
N_TRIALS = 4
NUM_SAMPLES = 15
environment_fitnesses = np.zeros(simulation_state.pop_size)
robot_fitnesses = np.zeros(simulation_state.pop_size)
history_size = 500

trial_data = {}
population_data = {}

def run_trials(environment_genome, robot_genome):
    fitness = 0
    environment = Environment(environment_genome)
    robot = Robot(robot_genome)
    robot.set_environment(environment)
    for _ in range(N_TRIALS):
        if simulation_state.ENABLE_DRAWING:
            turtle.resetscreen()
        environment.reset()
        robot.reset()

        for time in range(TRIAL_LENGTH):
            if simulation_state.ENABLE_DRAWING and time % 50 == 0:
                environment.draw()
                robot.draw()
                turtle.update()
            if robot.is_alive:
                robot.calculate_change()
                robot.update()
                fitness += (robot.food_battery + robot.water_battery) / 2.0 / TRIAL_LENGTH
            environment.update()
            if not robot.is_alive:
                break
        if simulation_state.ENABLE_DRAWING:
            robot.clear()
            environment.clear()

    if simulation_state.ENABLE_DRAWING:
        turtle.resetscreen()
        robot.destroy()
        environment.destroy()

    return fitness / N_TRIALS


def select_and_crossover(genome_a, genome_b, fitness_a, fitness_b):
    global trial_data
    winner_genome = genome_a
    loser_genome = genome_b
    trial_data["peak_fitness"] = fitness_b
    print(f"Tournament fitnesses: A: {fitness_a}\tB: {fitness_b}")

    if fitness_a < fitness_b:
        trial_data["peak_fitness"] = fitness_a
        winner_genome, loser_genome = loser_genome, winner_genome

    trial_data["winner_genome"] = winner_genome.flatten()
    trial_data["loser_genome"] = loser_genome.flatten()

    loser_genome.crossover(winner_genome)
    loser_genome.mutate()


def iterate_evolve_robot():
    simulation_state.tournament += 1
    a_id, b_id = random.sample(range(len(simulation_state.robot_genomes)), 2)

    robot_genome_a = simulation_state.robot_genomes[a_id]
    robot_genome_b = simulation_state.robot_genomes[b_id]

    fitness_a = 0
    fitness_b = 0

    for environment_genome in random.sample(simulation_state.environment_genomes, NUM_SAMPLES):
        fitness_a += run_trials(environment_genome, robot_genome_a)
        fitness_b += run_trials(environment_genome, robot_genome_b)

    fitness_a /= NUM_SAMPLES
    fitness_b /= NUM_SAMPLES

    robot_fitnesses[a_id] = fitness_a
    robot_fitnesses[b_id] = fitness_b

    select_and_crossover(robot_genome_a, robot_genome_b, fitness_a, fitness_b)


def iterate_evolve_environment():
    simulation_state.tournament += 1
    a_id, b_id = random.sample(range(len(simulation_state.environment_genomes)), 2)

    environment_genome_a = simulation_state.environment_genomes[a_id]
    environment_genome_b = simulation_state.environment_genomes[b_id]

    fitness_a = 0
    fitness_b = 0

    for robot_genome in random.sample(simulation_state.robot_genomes, NUM_SAMPLES):
        fitness_a += run_trials(environment_genome_a, robot_genome)
        fitness_b += run_trials(environment_genome_b, robot_genome)

    fitness_a /= NUM_SAMPLES
    fitness_b /= NUM_SAMPLES

    environment_fitnesses[a_id] = fitness_a
    environment_fitnesses[b_id] = fitness_b

    select_and_crossover(environment_genome_a, environment_genome_b, fitness_a, fitness_b)

def init_average_fitness():
    for i, robot_genome in enumerate(simulation_state.robot_genomes):
        environment_genome = random.choice(simulation_state.environment_genomes)
        robot_fitnesses[i] = run_trials(environment_genome, robot_genome)

def save_tournament_data():
    global trial_data
    outfile = open("Data/tournament_data" + str(simulation_state.tournament) + ".json", "w")
    trial_data["tournament"] = simulation_state.tournament
    trial_data["robot_fitnesses"] = robot_fitnesses.tolist()
    trial_data["environment_fitnesses"] = environment_fitnesses.tolist()
    outfile.write(json.dumps(trial_data))
    outfile.close()

def save_population_data():
    global population_data
    outfile = open("Data/population_data_at_tournament" + str(simulation_state.tournament) + ".json", "w")

    population_data["environment_genomes"] = {}
    for env_genome in simulation_state.environment_genomes:
        pos = simulation_state.environment_genomes.index(env_genome)
        population_data["environment_genomes"][str(pos)] = env_genome.flatten()

    population_data["robot_genomes"] = {}
    for robot_genome in simulation_state.robot_genomes:
        pos = simulation_state.robot_genomes.index(robot_genome)
        population_data["robot_genomes"][str(pos)] = robot_genome.flatten()
    outfile.write(json.dumps(population_data))
    outfile.close()

def main():
    init_average_fitness()
    while True:
        random.choice([
            iterate_evolve_robot,
            # iterate_evolve_environment,
        ])()
        save_tournament_data()
        save_population_data()

        if simulation_state.tournament % 1 == 0:
            print("\n")
            print("=" * 100)
            print(f"Tournament {simulation_state.tournament} - summary so far")
            print(" - Robot Population:")
            print([genome.flatten() for genome in simulation_state.robot_genomes])
            print(" - Environment Population:")
            print([genome.flatten() for genome in simulation_state.environment_genomes])
            print(f" - Robot fitnesses: {robot_fitnesses.tolist()}")
            print(f" - Environment fitnesses: {environment_fitnesses.tolist()}")
            print(f" - Best robot fitness: {robot_fitnesses.max()}")
            print(f" - Mean robot fitness: {robot_fitnesses.mean()}")
            print(f" - Best environment fitness: {environment_fitnesses.max()}")
            print(f" - Mean environment fitness: {environment_fitnesses.mean()}")
            print("=" * 100)
            print("\n")
