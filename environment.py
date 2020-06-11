import random
import numpy as np
import simulation_state
import turtle
import itertools

from environment_artist import EnvironmentArtist
from thing_artist import ThingArtist

class Thing:
    COLOUR = "black"
    CONSUMPTION_RATE = 0.1
    ROBOT_FILL_RATE = 0.25
    REGROW_RATE = 0.025
    TOTAL_AMOUNT = 4

    def __init__(self, gene, nx=None, ny=None):
        self.amount_when_full = self.TOTAL_AMOUNT / gene.amount.value
        self.amount_left = 0
        self.radius = 20
        self.smell_signature = gene.smell_signature.flatten()

        if simulation_state.ENABLE_DRAWING:
            self.artist = ThingArtist(self.radius)

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
        self.artist\
            .x_position(self.position[0])\
            .y_position(self.position[1])\
            .colour(self.COLOUR)\
            .amount_left(self.amount_left)\
            .smell_signature(self.smell_signature)\
            .amount_full(self.amount_when_full)\
            .amount_left(self.amount_left)
        self.artist.draw()

    def clear(self):
        self.artist.clear()

    def destroy(self):
        self.artist.destroy()

    def update(self):
        if not self.is_gone():
            self.amount_left += self.REGROW_RATE * simulation_state.timestep
            if self.amount_left > self.amount_when_full:
                self.amount_left = self.amount_when_full

    def interact_with_robot(self, robot):
        if not self.is_gone():
            self.on_touched_by_robot(robot)

    def on_touched_by_robot(self, robot):
        # To be implemented by concrete subclasses.
        pass

    def is_gone(self):
        return self.amount_left <= 0


class Food(Thing):
    COLOUR = (255, 255, 0) # yellow in rgb

    def on_touched_by_robot(self, robot):
        self.amount_left -= self.CONSUMPTION_RATE * simulation_state.timestep
        robot.food_battery += self.ROBOT_FILL_RATE * simulation_state.timestep


class Water(Thing):
    COLOUR = (0, 0, 255) # blue in rgb

    def on_touched_by_robot(self, robot):
        self.amount_left -= self.CONSUMPTION_RATE * simulation_state.timestep
        robot.water_battery += self.ROBOT_FILL_RATE * simulation_state.timestep


class Trap(Thing):
    COLOUR = (255, 0, 0) # red in rgb

    def on_touched_by_robot(self, robot):
        robot.food_battery = 0.0
        robot.water_battery = 0.0
        robot.is_alive = False


class Environment:
    def __init__(self, genome):
        self.foods = []
        self.waters = []
        self.traps = []
        self.thing_positions = None

        for gene in genome.food_genes.list:
            for _ in range(int(gene.amount.value)):
                self.foods.append(Food(gene))

        for gene in genome.water_genes.list:
            for _ in range(int(gene.amount.value)):
                self.waters.append(Water(gene))

        # Ensure number of traps = number of (water + food)
        trap_written_sum = sum([trap.amount.value for trap in genome.trap_genes.list])
        trap_amount_multiplier = (len(self.foods) + len(self.waters)) / trap_written_sum

        for gene in genome.trap_genes.list:
            for _ in range(int(gene.amount.value * trap_amount_multiplier)):
                self.traps.append(Trap(gene))

        self.thing_signatures = np.array([thing.smell_signature for thing in self.everything()]).transpose()
        # self.artist = EnvironmentArtist(1, foods, waters, traps)
        self.thing_radii = np.array([thing.radius for thing in self.everything()])

    def everything(self):
        return itertools.chain(self.foods, self.waters, self.traps)

    def reset(self):
        for thing in self.everything():
            thing.reset()
        self.thing_positions = np.array([thing.position for thing in self.everything()]).transpose()

    def interact_with_robot(self, robot):
        interaction_distances = robot.radius + self.thing_radii
        distances = np.linalg.norm(self.thing_positions - robot.position, axis=0)
        things_are_interacting = distances < interaction_distances
        for thing, is_interacting in zip(self.everything(), things_are_interacting):
            if is_interacting:
                thing.interact_with_robot(robot)

    def update(self):
        for thing in self.everything():
            thing.update()

    def draw(self):
        for thing in self.everything():
            thing.draw()

    def clear(self):
        for thing in self.everything():
            thing.clear()

    def destroy(self):
        for thing in self.everything():
            thing.destroy()
