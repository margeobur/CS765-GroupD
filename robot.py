from environment import Environment
from brain import EvolvableBrain
import random
import simulation_state
import math

# arena_width
# timestep

class Robot:
	def __init__(self):
		#radius of the robot
		self.radius = 1

		#Sensor angle
		self.beta = 3.14159 / 4

		#Robot's x, y position and heading angle
		self.x = random.randrange(0, simulation_state.arena_width)
		self.y = random.randrange(0, simulation_state.arena_width)
		self.a = random.randrange(0, 2.0*3.14159)

		self.food_battery = 1.0
		self.water_battery = 1.0

		self.l_motor = random.randrange(0,1)
		self.r_motor = random.randrange(0,1)

		#sense colours
		self.r = random.randrange(64, 192)
		self.g = random.randrange(64, 192)
		self.b = random.randrange(64, 192)
		self.alpha = 128

		self.is_alive = True

		self.brain = Brain()
		self.env = Environment()
		self.sensor_values = tuple()

	def reset(self):
		self.x = random.randrange(0, simulation_state.arena_width)
		self.y = random.randrange(0, simulation_state.arena_width)

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
			self.x += simulation_state.timestep * cos(a) * (self.l_motor + self.r_motor) * max_speed
			self.y += simulation_state.timestep * sin(a) * (self.l_motor + self.r_motor) * max_speed
			self.a += simulation_state.timestep * max_speed * (self.l_motor - self.r_motor) / (2.0 * self.radius)

			self.env.interact_with_robot()
			self.food_battery = constrain(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)
			self.water_battery = constrain(self.food_battery - 0.04 * simulation_state.timestep, 0.0, 1.0)

		if self.food_battery == 0.0 or self.water_battery == 0.0:
			self.is_alive = False
			self.food_battery = 0.0
			self.water_battery = 0.0

	def sense(self, sense_vector, thing):
		k = 1.0
		x = sense_vector[0]
		y = sense_vector[1]

		sensor_to_thing = tuple(thing.x - (self.x + x * self.radius), t.y - (self.y + y * self.radius))
		impact = (simulation_state.arena_width - sensor_to_thing.mag()) / simulation_state.arena_width
		attenuation *= attenuation * attenuation
		if attenuation < 0.0:
			attenuation = 0.0
		return impact * attenuation

	def calculate_change(self):
		sense_vectors = []
		sense_vectors.append([a - beta])
		sense_vectors.append([a + beta])

		raw_sensor_value = 0.0
		for i in range(0, len(sense_vectors) + 1):
			raw_sensor_value = 0.0
			for thing in self.env.foods:
				s = sense(sense_vectors[i], thing)
				if s > raw_sensor_value:
					raw_sensor_value = s
			sense_values[0][i] = raw_sensor_value

			raw_sensor_value = 0.0
			for thing in self.env.waters:
				s = sense(sense_vectors[i], thing)
				if s > raw_sensor_value:
					raw_sensor_value = s
			sensor_values[1][i] = raw_sensor_value

			raw_sensor_value = 0.0
			for thing in self.env.traps:
				s = sense(sense_vectors[i], thing)
				if s > raw_sensor_value:
					raw_sensor_value += s
			sense_values[2][i] = raw_sensor_value
