import random
import numpy as np
import simulation_state
import turtle
import itertools


class Thing:
    COLOUR = "black"
    CONSUMPTION_RATE = 0.25 * 10.0
    ROBOT_FILL_RATE = 0.25
    REGROW_RATE = 0.25
    TOTAL_AMOUNT = 4

    def __init__(self, gene, nx=None, ny=None):
        self.amount_when_full = self.TOTAL_AMOUNT / gene.amount.value
        self.amount_left = 0
        self.radius = 1.0

        self.reset()

        if nx is not None and ny is not None:
            self.position = np.array([nx, ny])

    def reset(self):
        self.amount_left = self.amount_when_full
        self.position = np.array([
            random.randrange(0, simulation_state.arena_width),
            random.randrange(0, simulation_state.arena_width)
        ])

    def draw(self):
        # alpha = int(180 * self.amount)
        # Not sure the above line is needed anymore.
        t = turtle.Turtle()
        t.fillcolor(self.COLOUR)
        t.penup()
        t.goto(self.position[0], self.position[1])
        t.pendown()
        t.shape("circle")
        t.shapesize(self.radius * 2, self.radius * 2)

    def update(self):
        if not self.is_gone():
            self.amount_left += self.REGROW_RATE * simulation_state.timestep
            self.amount_left = np.clip(self.amount_left, 0, self.amount_when_full)

    def interact_with_robot(self, robot):
        if not self.is_gone() and np.linalg.norm(self.position - robot.position) < self.radius:
            self.on_touched_by_robot(robot)

    def on_touched_by_robot(self, robot):
        # To be implemented by concrete subclasses.
        pass

    def is_gone(self):
        return self.amount_left <= 0


class Food(Thing):
    COLOUR = "yellow"

    def on_touched_by_robot(self, robot):
        self.amount_left -= self.CONSUMPTION_RATE * simulation_state.timestep
        robot.food_battery += self.ROBOT_FILL_RATE * simulation_state.timestep


class Water(Thing):
    COLOUR = "blue"

    def on_touched_by_robot(self, robot):
        self.amount_left -= self.CONSUMPTION_RATE * simulation_state.timestep
        robot.water_battery += self.ROBOT_FILL_RATE * simulation_state.timestep


class Trap(Thing):
    COLOUR = "red"

    def on_touched_by_robot(self, robot):
        robot.food_battery = 0.0
        robot.water_battery = 0.0
        robot.is_alive = False


class Environment:
    def __init__(self, genome):
        self.foods = []
        self.waters = []
        self.traps = []

        for gene in genome.foodGenes.list:
            for _ in range(int(gene.amount.value)):
                self.foods.append(Food(gene))

        for gene in genome.waterGenes.list:
            for _ in range(int(gene.amount.value)):
                self.waters.append(Water(gene))

        # Ensure number of traps = number of (water + food)
        trap_written_sum = sum([trap.amount.value for trap in genome.trapGenes.list])
        trap_amount_multiplier = (len(self.foods) + len(self.waters)) / trap_written_sum

        for gene in genome.trapGenes.list:
            for _ in range(int(gene.amount.value * trap_amount_multiplier)):
                self.traps.append(Trap(gene))

    def everything(self):
        return itertools.chain(self.foods, self.waters, self.traps)

    def reset(self):
        for thing in self.everything():
            thing.reset()

    def interact_with_robot(self, robot):
        for thing in self.everything():
            thing.interact_with_robot(robot)

    def update(self):
        for thing in self.everything():
            thing.update()

    def draw(self):
        for thing in self.everything():
            thing.draw()
