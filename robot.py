from brain import EvolvableBrain
from genome import RobotGenome, EnvironmentGenome
from environment import Environment
import random
import simulation_state
import numpy as np
from maths import polar2vec, rotation2d
import math
import turtle

from robot_artist import RobotArtist


class Robot:
	def __init__(self, genome):
		# Radius of the robot
		self.radius = 20.0

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

		self.is_alive = True

		self.brain = EvolvableBrain(genome)
		self.env = None
		self.sensor_values = np.zeros(len(genome.sensors.list))
		self.sensor_angles = [gene.angle.value for gene in genome.sensors.list]
		self.sensor_vectors = np.array([polar2vec(gene.angle.value) for gene in genome.sensors.list]).transpose()
		self.sensor_signatures = np.array([gene.smell_signature.flatten() for gene in genome.sensors.list]).transpose()
		self.smell_alignment = None

		# An artist for handling the GUI
		self.artist = RobotArtist(self.radius)\
			.sensor_angles(self.sensor_angles)

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
			self.food_battery = np.clip(self.food_battery - 0.01 * simulation_state.timestep, 0.0, 1.0)
			self.water_battery = np.clip(self.food_battery - 0.01 * simulation_state.timestep, 0.0, 1.0)

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
		distances = np.linalg.norm(displacements, axis=2)

		# For each (row: thing, col: sensor), compute the unit vector from sensor to thing
		directions = displacements / distances[:, :, np.newaxis]

		# For each (row: thing, col: sensor), compute dot(sensor vector, sensor to thing direction) ^ 3
		direction_alignments = ((directions * absolute_sensor_vectors.transpose()[np.newaxis, :, :]).sum(2)) ** 3
		direction_alignments = direction_alignments.clip(min=0)

		# For each (row: thing, col: sensor), compute intensity of sensed value with linear falloff
		impacts = (simulation_state.arena_width - distances) / simulation_state.arena_width

		excitements = impacts * direction_alignments * self.smell_alignment

		self.sensor_values = excitements.max(0)

	def draw(self):
		alpha = 127
		t = turtle.Turtle()
		if self.is_alive:
			alpha = 255
		
		self.artist\
			.x_position(self.position[0][0])\
			.y_position(self.position[1][0])\
			.alive(self.is_alive)\
			.orientation(self.angle)\
			.food_battery(self.food_battery)\
			.water_battery(self.water_battery)\
			.smell_signatures(self.sensor_signatures.transpose())
		self.artist.draw()

	def clear(self):
		self.artist.clear()


def test():
	robot_genome = RobotGenome()
	robot_genome.from_flattened({
		"sensors": [
			{
				"threshold": 0,
				"mapping": [
					{"x": 0.0, "y": 0.0},
					{"x": 1.0, "y": 1.0}
				],
				"smell_signature": [1, 0, 0, 0, 0],
				"motor_side": "LEFT",
				"angle": math.pi / 4
			},
			{
				"threshold": 0,
				"mapping": [
					{"x": 0.0, "y": 0.0},
					{"x": 1.0, "y": 1.0}
				],
				"smell_signature": [1, 1, 0, 0, 0],
				"motor_side": "RIGHT",
				"angle": math.pi * 7 / 4
			}
		]
	})
	robot = Robot(robot_genome)
	environment_genome = EnvironmentGenome()
	environment_genome.from_flattened({
		"water_genes": [{
			"amount": 1,
			"smell_signature": [1, 0, 0, 0, 0]
		}],
		"food_genes": [{
			"amount": 1,
			"smell_signature": [0, 0, 0, 0, 0]
		}],
		"trap_genes": [{
			"amount": 1,
			"smell_signature": [0, 1, 0, 0, 0]
		}]
	})
	environment = Environment(environment_genome)
	robot.set_environment(environment)
	environment.reset()
	robot.reset()
	robot.position = np.vstack([100.0, 100.0])
	robot.angle = 0
	environment.waters[0].position = np.array([140, 140])
	environment.foods[0].position = np.array([140, 100])
	environment.traps[0].position = np.array([160, 60])
	environment.thing_positions = np.array([thing.position for thing in environment.everything()]).transpose()
	robot.calculate_change()
	print(robot.sensor_values)
	robot.update()
	print(robot.position)
	robot.update()
	print(robot.position)
	print(robot.angle)

	win = turtle.Screen()
	win.setup(simulation_state.arena_width, simulation_state.arena_width)
	win.setworldcoordinates(0, 0, simulation_state.arena_width, simulation_state.arena_width)
	win.bgcolor("black")
	win.title("Arena")
	win.colormode(255)
	win.tracer(0)
	win.delay(16)
	environment.draw()
	robot.draw()
	turtle.update()
	win.mainloop()


if __name__ == "__main__":
	test()
