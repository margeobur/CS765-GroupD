import random
import numpy as np
import turtle

from environment import Environment
from robot import Robot
import simulation_state
import json

TRIAL_LENGTH = 1500
N_TRIALS = 1
NUM_SAMPLES = 4
environment_fitnesses = np.zeros(simulation_state.pop_size)
robot_fitnesses = np.zeros(simulation_state.pop_size)
history_size = 500

mean_fitness_history = []
peak_fitness_history = []


def run_trials(environment_genome, robot_genome):
    fitness = 0
    environment = Environment(environment_genome)
    robot = Robot(robot_genome)
    robot.set_environment(environment)
    for _ in range(N_TRIALS):
        turtle.resetscreen()
        environment.reset()
        robot.reset()

        for time in range(TRIAL_LENGTH):
            if time % 100 == 0:
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
        robot.clear()
        environment.clear()

    turtle.resetscreen()
    robot.destroy()
    environment.destroy()

    return fitness / N_TRIALS


def select_and_crossover(genome_a, genome_b, fitness_a, fitness_b):
    winner_genome = genome_a
    loser_genome = genome_b

    if fitness_a > fitness_b:
        winner_genome, loser_genome = loser_genome, winner_genome
        simulation_state.trial_data["winner_genome"] = winner_genome.to_json()
        simulation_state.trial_data["loser_genome"] = loser_genome.to_json()

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

def save_tournament_data():
    outfile = open("Data/tournament_data" + str(simulation_state.tournament) + ".json", "w")
    simulation_state.trial_data["robot_fitnesses"] = robot_fitnesses.tolist()
    simulation_state.trial_data["tournament"] = simulation_state.tournament
    outfile.write(json.dumps(simulation_state.trial_data))
    outfile.close()

def main():
    simulation_state.tournament = 1
    while True:
        random.choice([iterate_evolve_robot, iterate_evolve_environment])()
        save_tournament_data()



