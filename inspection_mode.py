import turtle

import simulation_state
import evolve_mode
from environment import Environment
from robot import Robot

iterations_per_draw = 8

def most_fit_genome_index(fitnesses):
    max_fitness_i = 0

    for i in range(0, len(fitnesses)):
        if fitnesses[i] > fitnesses[max_fitness_i]:
            max_fitness_i = i

    return max_fitness_i

def inspection_mode():
    r_id = most_fit_genome_index(evolve_mode.robot_fitnesses)
    e_id = most_fit_genome_index(evolve_mode.environment_fitnesses)

    env = Environment(simulation_state.environment_genomes[e_id])

    robot = Robot(simulation_state.robot_genomes[r_id])
    robot.set_environment(env)
    robot.draw()

    TRIAL_LENGTH = evolve_mode.TRIAL_LENGTH

    for i in range(0, TRIAL_LENGTH):
        if robot.is_alive:
            robot.calculate_change()
            robot.update()
            env.update()
            if i % iterations_per_draw == 0:
                env.draw()
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

