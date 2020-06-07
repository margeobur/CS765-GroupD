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


def run_trials(environment, robot):
    fitness = 0
    for _ in range(N_TRIALS):
        turtle.resetscreen()
        environment.reset()
        robot.set_environment(environment)
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
                print("dead")
                break

        robot.clear()
        environment.clear()

    return fitness / N_TRIALS


def select_and_crossover(genome_a, genome_b, fitness_a, fitness_b):
    winner_genome = genome_a
    loser_genome = genome_b

    if fitness_a > fitness_b:
        winner_genome, loser_genome = loser_genome, winner_genome

    print("this is fitness_a ", fitness_a)
    print("this is fitness_b ", fitness_b)

    loser_genome.crossover(winner_genome)
    loser_genome.mutate()


def iterate_evolve_robot():
    simulation_state.tournament += 1
    a_id, b_id = random.sample(range(len(simulation_state.robot_genomes)), 2)

    robot_genome_a = simulation_state.robot_genomes[a_id]
    robot_genome_b = simulation_state.robot_genomes[b_id]
    robot_a = Robot(robot_genome_a)
    robot_b = Robot(robot_genome_b)

    fitness_a = 0
    fitness_b = 0

    for environment_genome in random.sample(simulation_state.environment_genomes, NUM_SAMPLES):
        environment = Environment(environment_genome)
        fitness_a += run_trials(environment, robot_a)
        fitness_b += run_trials(environment, robot_b)

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
    environment_a = Environment(environment_genome_a)
    environment_b = Environment(environment_genome_b)

    fitness_a = 0
    fitness_b = 0

    for robot_genome in random.sample(simulation_state.robot_genomes, NUM_SAMPLES):
        robot = Robot(robot_genome)
        fitness_a += run_trials(environment_a, robot)
        fitness_b += run_trials(environment_b, robot)

    fitness_a /= NUM_SAMPLES
    fitness_b /= NUM_SAMPLES

    robot_fitnesses[a_id] = fitness_a
    robot_fitnesses[b_id] = fitness_b

    select_and_crossover(environment_genome_a, environment_genome_b, fitness_a, fitness_b)


def main():
    simulation_state.tournament = 1
    while True:
        random.choice([iterate_evolve_robot, iterate_evolve_environment])()
        outfile = open("Data/tournament_data" + str(simulation_state.tournament) + ".json", "w")
        simulation_state.trial_data["robot_fitnesses"] = robot_fitnesses.tolist()
        simulation_state.trial_data["tournament"] = simulation_state.tournament
        print(simulation_state.trial_data)
        outfile.write(json.dumps(simulation_state.trial_data))
        outfile.close()



