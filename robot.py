from brain import EvolvableBrain
import random
import simulation_state
import numpy as np
from maths import polar2vec
import math
import turtle


class Robot:
	def __init__(self, genome):
		# Radius of the robot
		self.radius = 1

		# Robot's x, y position and heading angle
		self.position = np.array([
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

		self.is_alive = True

		self.brain = EvolvableBrain(genome)
		self.env = None
		self.sensor_values = np.zeros(len(genome.sensors.list))
		self.sensor_angles = np.array([gene.angle.value for gene in genome.sensors.list])
		self.sensor_signatures = np.array([gene.smell_signature.flatten() for gene in genome.sensors.list])

	def reset(self):
		self.position = np.array([
			random.uniform(0, simulation_state.arena_width),
			random.uniform(0, simulation_state.arena_width)
		])

		self.food_battery = 0.75
		self.water_battery = 0.75
		self.is_alive = True

	def set_environment(self, new_env):
		self.env = new_env

	def update(self):
		self.l_motor, self.r_motor = self.brain.iterate(self.sensor_values)
		max_speed = 10.0

		if self.is_alive:
			self.position += simulation_state.timestep * polar2vec(self.angle) * (self.l_motor + self.r_motor) * max_speed
			self.angle += simulation_state.timestep * max_speed * (self.l_motor - self.r_motor) / (2.0 * self.radius)

			self.env.interact_with_robot(self)
			self.food_battery = np.clip(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)
			self.water_battery = np.clip(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)

		if self.food_battery == 0.0 or self.water_battery == 0.0:
			self.is_alive = False
			self.food_battery = 0.0
			self.water_battery = 0.0

	def sense(self, sensor_angle, sensor_signature, thing):
		sense_vector = polar2vec(self.angle + sensor_angle)
		sensor_to_thing = thing.position - (self.position + sense_vector * self.radius)
		sensor_to_thing_magnitude = np.linalg.norm(sensor_to_thing)
		impact = (simulation_state.arena_width - sensor_to_thing_magnitude) / simulation_state.arena_width
		attenuation = np.dot(sense_vector, sensor_to_thing / sensor_to_thing_magnitude)

		# TODO (Ernest): Why is it cubed?
		attenuation *= attenuation * attenuation

		smell_alignment = np.dot(sensor_signature, thing.smell_signature)

		if attenuation < 0.0:
			attenuation = 0.0
		return impact * attenuation * smell_alignment

	def calculate_change(self):
		for i, (angle, signature) in enumerate(zip(self.sensor_angles, self.sensor_signatures)):
			self.sensor_values[i] = max([self.sense(angle, signature, thing) for thing in self.env.everything()])

	def draw(self):
		alpha = 127
		t = turtle.Turtle()
		if self.is_alive:
			alpha = 255
		t.fillcolor(64, 64, 64)
		t.pensize(0.125)
		t.pencolor(255, 255, 255)
		gx = self.position[0]
		gy = self.position[1]
		t.penup()
		t.goto(gx, gy)
		t.pendown()
		t.shape("circle")
		t.shapesize(self.radius*2, self.radius*2)
		# hx = math.cos(self.angle) * self.radius
		# hy = math.sin(self.angle) * self.radius
		# t.penup()
		# t.goto(gx, gy)
		# t.pendown()
		# t.goto(gx+hx, gy+hy)


