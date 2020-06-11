import simulation_state
import evolve_mode
from genome import EnvironmentGenome, RobotGenome
import turtle
import json


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
