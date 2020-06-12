import numpy as np
import turtle
import itertools
from genome import Laterality


class Mapping:
    def __init__(self, gene, is_left):
        self.n_points = len(gene.mapping.list)
        # self.side_weighting = np.array([1, 0] if gene.motor_side.laterality == Laterality.LEFT else [0, 1])
        self.side_weighting = np.array([1, 0] if is_left else [0, 1])
        self.xs = np.array([point.x.value for point in gene.mapping.list])
        self.ys = np.array([point.y.value for point in gene.mapping.list])

    def f(self, x):
        return np.interp(x, self.xs, self.ys) * self.side_weighting

    def draw(self):
        for i in range(0, self.n_points - 1):
            turtle.penup()
            turtle.goto(self.xs[i], -self.ys[i])
            turtle.pendown()
            turtle.goto(self.xs[i + 1], -self.ys[i + 1])
            turtle.done()


class EvolvableBrain:
    def __init__(self, genome):
        self.mappings = [Mapping(gene, i < 6) for i, gene in enumerate(itertools.chain(genome.sensors.list, genome.sensors.list))]

    def iterate(self, sensor_values):
        accumulative_motor_power = [0.5, -0.5]

        for mapping, sensor_value in zip(self.mappings, sensor_values):
            accumulative_motor_power += mapping.f(sensor_value)

        return accumulative_motor_power / 6.0
