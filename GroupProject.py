import simulation_state
import evolve_mode
from robot import Robot
from environment import Environment
from brain import EvolvableBrain
import turtle

def setup():
    simulation_state.env = Environment()

    for i in range(0, simulation_state.pop_size):
        b = EvolvableBrain()
        b.randomise()
        simulation_state.evolvable_brains.append(b)

    for i in range(0, simulation_state.pop_size):
        r = Robot()
        r.set_brain(simulation_state.evolvable_brains[i])
        r.set_environment(simulation_state.env)
        simulation_state.robots.append(r)

def main():
    setup()
    win = turtle.Screen()
    win.setup(simulation_state.arena_width, simulation_state.arena_width)
    win.setworldcoordinates(0, 0, simulation_state.arena_width, simulation_state.arena_width)
    win.bgcolor("black")
    win.title("Arena")
    simulation_state.env.draw()
    evolve_mode.main()
    win.mainloop()


main()
