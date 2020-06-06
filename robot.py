from brain import EvolvableBrain
import random
import simulation_state
import numpy as np
from maths import polar2vec, rotation2d
import math
import turtle


class Robot:
    def __init__(self, genome):
        # Radius of the robot
        self.radius = 1

        # Robot's x, y position and heading angle
        self.position = np.vstack([
            random.uniform(0, simulation_state.arena_width),
            random.uniform(0, simulation_state.arena_width)
        ])
        self.angle = random.uniform(0, 2.0 * math.pi)

        self.food_battery = 1.0
        self.water_battery = 1.0

        self.l_motor = random.uniform(0, 1)
        self.r_motor = random.uniform(0, 1)

        # Sense colours
        self.r = random.randrange(64, 192)
        self.g = random.randrange(64, 192)
        self.b = random.randrange(64, 192)
        self.alpha = 128

        self.myTurtle = turtle.Turtle()

        self.is_alive = True

        self.brain = EvolvableBrain(genome)
        self.env = None
        self.sensor_values = np.zeros(len(genome.sensors.list))
        self.sensor_vectors = np.array([polar2vec(gene.angle.value) for gene in genome.sensors.list]).transpose()
        self.sensor_signatures = np.array([gene.smell_signature.flatten() for gene in genome.sensors.list]).transpose()
        self.smell_alignment = None

        self.reset()

    def reset(self):
        self.position = np.vstack([
            random.uniform(0, simulation_state.arena_width),
            random.uniform(0, simulation_state.arena_width)
        ])

        self.food_battery = 0.75
        self.water_battery = 0.75
        self.is_alive = True

    def set_environment(self, new_env):
        self.env = new_env
        self.smell_alignment = self.env.thing_signatures.transpose() @ self.sensor_signatures

    def update(self):
        self.l_motor, self.r_motor = self.brain.iterate(self.sensor_values)
        max_speed = 10.0

        if self.is_alive:
            self.position += simulation_state.timestep * polar2vec(self.angle)[:, np.newaxis] * (self.l_motor + self.r_motor) * max_speed
            self.angle += simulation_state.timestep * max_speed * (self.l_motor - self.r_motor) / (2.0 * self.radius)

            self.env.interact_with_robot(self)
            self.food_battery = np.clip(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)
            self.water_battery = np.clip(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)

        if self.food_battery == 0.0 or self.water_battery == 0.0:
            self.is_alive = False
            self.food_battery = 0.0
            self.water_battery = 0.0

    def calculate_change(self):
        # For each (col: sensor), compute unit vector for sensor direction
        absolute_sensor_vectors = rotation2d(self.angle) @ self.sensor_vectors

        # For each (col: sensor), compute absolute position of sensor
        sensor_positions = absolute_sensor_vectors * self.radius + self.position

        # For each (row: thing, col: sensor), compute displacement from displacements from sensor to thing position
        displacements = self.env.thing_positions.transpose()[:, np.newaxis, :] - sensor_positions.transpose()[np.newaxis, :, :]

        # For each (row: thing, col: sensor), compute the euclidean distance between the sensor and the thing
        distances = np.linalg.norm(displacements, None, 2)

        # For each (row: thing, col: sensor), compute the unit vector from sensor to thing
        directions = displacements / distances[:, :, np.newaxis]

        # For each (row: thing, col: sensor), compute dot(sensor vector, sensor to thing direction) ^ 3
        direction_alignments = ((directions * absolute_sensor_vectors.transpose()[np.newaxis, :, :]).sum(2)) ** 3

        # For each (row: thing, col: sensor), compute intensity of sensed value with linear falloff
        impacts = (simulation_state.arena_width - distances) / simulation_state.arena_width

        excitements = impacts * direction_alignments * self.smell_alignment

        self.sensor_values = excitements.max(0)

    def drawOneAntena(self, degrees):
        t = self.myTurtle
        gx = int(self.position[0][0])
        gy = int(self.position[1][0])
        hx = math.cos(self.angle + degrees/180 * math.pi) * self.radius * 28
        hy = math.sin(self.angle + degrees/180 * math.pi) * self.radius * 28
        t.penup()
        t.goto(gx, gy)
        t.pendown()
        t.goto(gx + hx, gy + hy)

    def draw(self):
        if self.is_alive:
            colourValue = 255
        else:
            colourValue = 127

        t = self.myTurtle
        t.clear()
        t.fillcolor(64, 64, 64)
        t.pencolor(colourValue, colourValue, colourValue)
        t.pensize(2)

        gx = self.position[0][0]
        gy = self.position[1][0]
        self.drawOneAntena(-25)
        self.drawOneAntena(25)
        t.penup()
        t.goto(gx, gy)
        t.pendown()
        t.shape("circle")
        t.shapesize(self.radius * 2, self.radius * 2)


    def clear(self):
        self.myTurtle.clear()
        self.myTurtle.hideturtle()