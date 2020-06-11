import simulation_state
import evolve_mode
from genome import EnvironmentGenome, RobotGenome
import turtle
import json


LOAD_INITIAL_POPULATION_FROM = None
LOAD_ONLY_THE_BEST_ROBOT = False


def setup():
    environment_genome = EnvironmentGenome()
    environment_genome.from_flattened({
        "water_genes": [{
            "amount": 1,
            "smell_signature": [1, 0, 0, 0, 0]
        }],
        "food_genes": [{
            "amount": 1,
            "smell_signature": [0, 1, 0, 0, 0]
        }],
        "trap_genes": [{
            "amount": 1,
            "smell_signature": [0, 0, 1, 0, 0]
        }]
    })
    # Setup the population of robot and environment genomes
    for _ in range(simulation_state.pop_size):
        robot_genome = RobotGenome()
        robot_genome.randomise()
        simulation_state.robot_genomes.append(robot_genome)
        simulation_state.environment_genomes.append(environment_genome)

    if LOAD_INITIAL_POPULATION_FROM is not None:
        best_robot_index = None
        with open(f"Data/tournament_data{LOAD_INITIAL_POPULATION_FROM}.json") as file:
            a = json.load(file)
            max_fitness = max(a["robot_fitnesses"])
            best_robot_index = a["robot_fitnesses"].index(max_fitness)

        with open(f"Data/population_data_at_tournament{LOAD_INITIAL_POPULATION_FROM}.json") as file:
            a = json.load(file)
            for key, genome in a["environment_genomes"].items():
                simulation_state.environment_genomes[int(key)].from_flattened(genome)
            if LOAD_ONLY_THE_BEST_ROBOT:
                for i in range(simulation_state.pop_size):
                    simulation_state.robot_genomes[i].from_flattened(a["robot_genomes"][str(best_robot_index)])
            else:
                for key, genome in a["robot_genomes"].items():
                    simulation_state.robot_genomes[int(key)].from_flattened(genome)


def main():
    setup()
    win = turtle.Screen()
    win.setup(simulation_state.arena_width, simulation_state.arena_width)
    win.setworldcoordinates(0, 0, simulation_state.arena_width, simulation_state.arena_width)
    win.bgcolor("black")
    win.title("Arena")
    win.colormode(255)
    win.tracer(0)
    win.delay(16)
    win.update()
    evolve_mode.main()
    win.mainloop()


main()
