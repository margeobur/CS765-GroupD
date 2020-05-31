from environment import Environment
from brain import EvolvableBrain
import random
import simulation_state
import math
import numpy as np

# arena_width
# timestep

class Robot:
	def __init__(self):
		#radius of the robot
		self.radius = 1

		#Sensor angle
		self.beta = 3.14159 / 4

		#Robot's x, y position and heading angle
		self.position = np.array([
			random.uniform(0, simulation_state.arena_width),
			random.uniform(0, simulation_state.arena_width)
		])
		self.a = random.uniform(0, 2.0*3.14159)

		self.food_battery = 1.0
		self.water_battery = 1.0

		self.l_motor = random.uniform(0, 1)
		self.r_motor = random.uniform(0, 1)

		#sense colours
		self.r = random.randrange(64, 192)
		self.g = random.randrange(64, 192)
		self.b = random.randrange(64, 192)
		self.alpha = 128

		self.is_alive = True

		self.brain = EvolvableBrain()
		self.env = Environment()
		self.sensor_values = tuple()

	def reset(self):
		self.x = random.uniform(0, simulation_state.arena_width)
		self.y = random.uniform(0, simulation_state.arena_width)

		self.food_battery = 0.75
		self.water_battery = 0.75
		self.is_alive = True

	def set_brain(self, b):
		self.brain = b

	def set_environment(self, new_env):
		self.env = new_env

	def update(self):
		self.brain.iterate()
		max_speed = 10.0

		if self.is_alive:
			self.x += simulation_state.timestep * np.cos(self.a) * (self.l_motor + self.r_motor) * max_speed
			self.y += simulation_state.timestep * np.sin(self.a) * (self.l_motor + self.r_motor) * max_speed
			self.a += simulation_state.timestep * max_speed * (self.l_motor - self.r_motor) / (2.0 * self.radius)

			self.env.interact_with_robot()
			self.food_battery = np.clip(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)
			self.water_battery = np.clip(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)

		if self.food_battery == 0.0 or self.water_battery == 0.0:
			self.is_alive = False
			self.food_battery = 0.0
			self.water_battery = 0.0

	def sense(self, sense_vector, thing):
		sensor_to_thing = thing.position - (self.position + sense_vector * self.radius)
		sensor_to_thing_magnitude = np.linalg.norm(sensor_to_thing)
		impact = (simulation_state.arena_width - sensor_to_thing_magnitude) / simulation_state.arena_width
		attenuation = np.dot(sense_vector, sensor_to_thing / sensor_to_thing_magnitude)

		# TODO (Ernest): Why is it cubed?
		attenuation *= attenuation * attenuation

		if attenuation < 0.0:
			attenuation = 0.0
		return impact * attenuation

	def calculate_change(self):
		sense_vectors = [np.array([np.cos(self.a - self.beta), np.sin(self.a - self.beta)]),
						 np.array([np.cos(self.a + self.beta), np.sin(self.a + self.beta)])]

		raw_sensor_value = 0.0
		for i in range(0, len(sense_vectors) + 1):
			raw_sensor_value = 0.0
			for thing in self.env.foods:
				s = self.sense(sense_vectors[i], thing)
				if s > raw_sensor_value:
					raw_sensor_value = s
			self.sense_values[0][i] = raw_sensor_value

			raw_sensor_value = 0.0
			for thing in self.env.waters:
				s = self.sense(sense_vectors[i], thing)
				if s > raw_sensor_value:
					raw_sensor_value = s
			self.sensor_values[1][i] = raw_sensor_value

			raw_sensor_value = 0.0
			for thing in self.env.traps:
				s = self.sense(sense_vectors[i], thing)
				if s > raw_sensor_value:
					raw_sensor_value += s
			self.sense_values[2][i] = raw_sensor_value
