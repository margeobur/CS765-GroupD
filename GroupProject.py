import simulation_state
import evolve_mode
from genome import EnvironmentGenome, RobotGenome
from robot import Robot
from environment import Environment
import turtle


def setup():
    environment_genome = EnvironmentGenome()
    environment_genome.randomise()
    simulation_state.env = Environment(environment_genome)

    for _ in range(simulation_state.pop_size):
        robot_genome = RobotGenome()
        robot_genome.randomise()
        simulation_state.robot_genomes.append(robot_genome)
        robot = Robot(robot_genome)
        robot.set_environment(simulation_state.env)
        simulation_state.robots.append(robot)


def main():
    setup()
    win = turtle.Screen()
    win.setup(simulation_state.arena_width, simulation_state.arena_width)
    win.setworldcoordinates(0, 0, simulation_state.arena_width, simulation_state.arena_width)
    win.bgcolor("black")
    win.title("Arena")
    win.colormode(255)
    simulation_state.env.draw()
    evolve_mode.main()
    win.mainloop()


main()
