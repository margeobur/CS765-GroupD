import simulation_state
import evolve_mode
from genome import EnvironmentGenome, RobotGenome
import turtle
import json
import math


LOAD_INITIAL_POPULATION_FROM = None
LOAD_ONLY_THE_BEST_ROBOT = False


def setup():
    environment_genome = EnvironmentGenome()
    environment_genome.from_flattened({
        "water_genes": [{
            "amount": 3,
            "smell_signature": [1, 0, 0, 0, 0]
        }],
        "food_genes": [{
            "amount": 3,
            "smell_signature": [0, 1, 0, 0, 0]
        }],
        "trap_genes": [{
            "amount": 1,
            "smell_signature": [0, 0, 1, 0, 0]
        }]
    })
    test_robot_genome = RobotGenome()
    test_robot_genome.randomise()
    test_robot_genome.sensors.list[0].mapping.from_flattened([  # contra food/water
        {"x": 0.0, "y": -1.0/2},
        {"x": 0.3, "y": -0.3/2},
        {"x": 0.7, "y": 0.3/2},
        {"x": 1.0, "y": 1.0/2},
    ])
    test_robot_genome.sensors.list[3].mapping.from_flattened([  # ipsi food/water
        {"x": 0.0, "y": 1.0/2},
        {"x": 0.3, "y": 0.7/2},
        {"x": 0.7, "y": 0.5/2},
        {"x": 1.0, "y": 0.5/2},
    ])
    test_robot_genome.sensors.list[5].mapping.from_flattened([  # contra trap
        {"x": 0.0, "y": 0.0},
        {"x": 0.3, "y": 0.0},
        {"x": 0.5, "y": 0.0},
        {"x": 1.0, "y": -1.0},
    ])
    test_robot_genome.sensors.list[2].mapping.from_flattened([  # ipsi trap
        {"x": 0.0, "y": 1.0},
        {"x": 0.3, "y": 1.0},
        {"x": 0.7, "y": 0.0},
        {"x": 1.0, "y": -0.5},
    ])
    for i in [4, 6, 7]:
        test_robot_genome.sensors.list[i].mapping.from_flattened(
            test_robot_genome.sensors.list[3].mapping.flatten()
        )
    for i in [1, 9, 10]:
        test_robot_genome.sensors.list[i].mapping.from_flattened(
            test_robot_genome.sensors.list[0].mapping.flatten()
        )
    test_robot_genome.sensors.list[8].mapping.from_flattened(
        test_robot_genome.sensors.list[5].mapping.flatten()
    )
    test_robot_genome.sensors.list[11].mapping.from_flattened(
        test_robot_genome.sensors.list[2].mapping.flatten()
    )
    """
    test_robot_genome.sensors.list[0].mapping.from_flattened([  # contra food/water
        {"x": 0.000, "y": 0.694},
        {"x": 0.026, "y": 0.588},
        {"x": 0.164, "y": 0.127},
        {"x": 1.000, "y": 0.536},
    ])
    test_robot_genome.sensors.list[3].mapping.from_flattened([  # ipsi food/water
        {"x": 0.000, "y": -0.980},
        {"x": 0.023, "y": -0.001},
        {"x": 0.734, "y": 0.851},
        {"x": 1.000, "y": 0.659},
    ])
    test_robot_genome.sensors.list[5].mapping.from_flattened([  # contra trap
        {"x": 0.000, "y": 0.853},
        {"x": 0.537, "y": 0.707},
        {"x": 0.909, "y": 0.432},
        {"x": 1.000, "y": -0.982},
    ])
    test_robot_genome.sensors.list[2].mapping.from_flattened([  # ipsi trap
        {"x": 0.000, "y": 0.390},
        {"x": 0.018, "y": 0.732},
        {"x": 0.488, "y": 0.017},
        {"x": 1.000, "y": 0.148},
    ])
    for i in [4, 6, 7]:
        test_robot_genome.sensors.list[i].mapping.from_flattened(
            test_robot_genome.sensors.list[3].mapping.flatten()
        )
    for i in [1, 9, 10]:
        test_robot_genome.sensors.list[i].mapping.from_flattened(
            test_robot_genome.sensors.list[0].mapping.flatten()
        )
    test_robot_genome.sensors.list[8].mapping.from_flattened(
        test_robot_genome.sensors.list[5].mapping.flatten()
    )
    test_robot_genome.sensors.list[11].mapping.from_flattened(
        test_robot_genome.sensors.list[2].mapping.flatten()
    )
    """
    '''
    test_robot_genome.from_flattened({
        "sensors": [
            {
                "threshold": 0.0,
                "angle": math.pi / 4,
                "smell_signature": [1, 0, 0, 0, 0],
                "mapping": [
                    {"x": 0.0, "y": 0.1},
                    {"x": 1.0, "y": 1.0},
                ],
                "motor_side": "LEFT"
            },
            {
                "threshold": 0.0,
                "angle": math.pi * 7 / 4,
                "smell_signature": [1, 0, 0, 0, 0],
                "mapping": [
                    {"x": 0.0, "y": -0.1},
                    {"x": 1.0, "y": 1.0},
                ],
                "motor_side": "RIGHT"
            },
            {
                "threshold": 0.0,
                "angle": math.pi / 4,
                "smell_signature": [0, 1, 0, 0, 0],
                "mapping": [
                    {"x": 0.0, "y": 0.1},
                    {"x": 1.0, "y": 1.0},
                ],
                "motor_side": "LEFT"
            },
            {
                "threshold": 0.0,
                "angle": math.pi * 7 / 4,
                "smell_signature": [0, 1, 0, 0, 0],
                "mapping": [
                    {"x": 0.0, "y": -0.1},
                    {"x": 1.0, "y": 1.0},
                ],
                "motor_side": "RIGHT"
            },
            {
                "threshold": 0.0,
                "angle": math.pi / 4,
                "smell_signature": [0, 0, 1, 0, 0],
                "mapping": [
                    {"x": 0.0, "y": 0.1},
                    {"x": 1.0, "y": -1.0},
                ],
                "motor_side": "LEFT"
            },
            {
                "threshold": 0.0,
                "angle": math.pi * 7 / 4,
                "smell_signature": [0, 0, 1, 0, 0],
                "mapping": [
                    {"x": 0.0, "y": -0.1},
                    {"x": 1.0, "y": -1.0},
                ],
                "motor_side": "RIGHT"
            },
        ]
    })
    '''
    # Setup the population of robot and environment genomes
    for _ in range(simulation_state.pop_size):
        robot_genome = RobotGenome()
        robot_genome.randomise()
        simulation_state.robot_genomes.append(robot_genome)
        simulation_state.environment_genomes.append(environment_genome)

    simulation_state.robot_genomes[0] = test_robot_genome

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
