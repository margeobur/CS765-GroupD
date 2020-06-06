import inspection_mode
import simulation_state
import evolve_mode
from genome import EnvironmentGenome, RobotGenome
import turtle


def setup():
    # Setup the population of robot and environment genomes
    for _ in range(simulation_state.pop_size):
        robot_genome = RobotGenome()
        robot_genome.randomise()
        simulation_state.robot_genomes.append(robot_genome)

        environment_genome = EnvironmentGenome()
        environment_genome.randomise()
        simulation_state.environment_genomes.append(environment_genome)


def main():
    setup()
    win = turtle.Screen()
    win.setup(simulation_state.arena_width, simulation_state.arena_width)
    win.setworldcoordinates(0, 0, simulation_state.arena_width, simulation_state.arena_width)
    win.bgcolor("black")
    win.title("Arena")
    win.colormode(255)
    win.tracer(False)
    # win.delay(16)
    win.update()

    evolve_mode.main()
    turtle.done()


main()
