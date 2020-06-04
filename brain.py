import numpy as np
import turtle
from genome import Laterality


class Mapping:
    def __init__(self, gene):
        self.n_points = len(gene.list)
        self.xs = np.array([point.x.value for point in gene.list])
        self.ys = np.array([point.y.value for point in gene.list])

    def f(self, x):
        return np.interp(x, self.xs, self.ys)

    def draw(self):
        for i in range(0, self.n_points - 1):
            turtle.penup()
            turtle.goto(self.xs[i], -self.ys[i])
            turtle.pendown()
            turtle.goto(self.xs[i + 1], -self.ys[i + 1])
            turtle.done()


class EvolvableBrain:
    def __init__(self, genome):
        self.left_mappings = [Mapping(gene.mapping) for gene in genome.sensors.list
                              if gene.motor_side.laterality == Laterality.LEFT]
        self.right_mappings = [Mapping(gene.mapping) for gene in genome.sensors.list
                               if gene.motor_side.laterality == Laterality.RIGHT]

    def iterate(self, sensor_values):
        lm_accum = 0
        rm_accum = 0

        for mapping, sensor_value in zip(self.left_mappings, sensor_values):
            lm_accum += mapping.f(sensor_value)

        for mapping, sensor_value in zip(self.right_mappings, sensor_values):
            rm_accum += mapping.f(sensor_value)

        return lm_accum / 6.0, rm_accum / 6.0
