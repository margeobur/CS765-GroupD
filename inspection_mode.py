import turtle

import simulation_state
import evolve_mode
from robot import Robot

iterations_per_draw = 8

def most_fit_robot_index(robots_genomes, fitnesses):
    max_fitness_i = 0

    for i in range(0, len(fitnesses)):
        if fitnesses[i] > fitnesses[max_fitness_i]:
            max_fitness_i = i

    return max_fitness_i

def inspection_mode():
    r_id = most_fit_robot_index(simulation_state.robot_genomes, evolve_mode.fitnesses)

    robot = Robot(simulation_state.robot_genomes[r_id])
    robot.set_environment(simulation_state.env)
    robot.draw()

    simulation_state.env.reset()
    trial_length = evolve_mode.trial_length

    for i in range(0, trial_length):
        if robot.is_alive:
            robot.calculate_change()
            robot.update()
            simulation_state.env.update()
            if i % iterations_per_draw == 0:
                # simulation_state.env.draw()
                robot.draw()
                turtle.update()
        else:
            break

def writeDead():
    t = turtle.Turtle()
    t.penup()
    t.setx(simulation_state.arena_width/2)
    t.sety(simulation_state.arena_width/2)
    t.pencolor(255, 255, 255)
    t.pendown()
    t.write("DEAD", False, "center", ("sans",16,"normal"))
    t.hideturtle()
    turtle.update()

def main():
    turtle.Screen().title("Inspect Mode")
    inspection_mode()
    writeDead()

