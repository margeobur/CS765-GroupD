import random
import enum

arena_width = 50
# timestep
# mode_evolve

class ThingType(enum.Enum):
	Food = 1
	Water = 2
	Trap = 3

class Thing:
	def __init__(self, ntype):
		self.x = random.randrange(0, arena_width)
		self.y = random.randrange(0, arena_width)

		self.amount = 1.0
		self.radius = 1.0

		self.type = ntype

	# def __init__(self, nx, ny, ntype):
	# 	self.x = nx
	# 	self.y = ny
	#
	# 	self.type = ntype
	#
	# 	self.amount = 1.0
	# 	self.radius = 1.0

	def draw(self):
		#
		return True

	def update(self):
		if self.amount < 0.0:
			self.amount = 1.0
			self.x = random.randrange(0, arena_width)
			self.y = random.randrange(0, arena_width)


class Environment:

	def __init__(self):
		self.foods = []
		self.waters = []
		self.traps = []

		#create 4 food sources and 4 water sources
		for i in range(0, 4):
			self.foods.append(ThingType.Food)
			self.waters.append(ThingType.Water)

		#create 2 traps
		self.traps.append(Thing(ThingType.Trap))
		self.traps.append(Thing(ThingType.Trap))

	def reset(self):
		for thing in self.foods:
			thing.amount = -1.0
			thing.update()
		for thing in self.waters:
			thing.amount = -1.0
			thing.update()
		for thing in self.traps:
			thing.amount = -1.0
			thing.update()

	def interact_with_robot(self, robot):
		consumption_rate = 0.25 * 10.0
		fill_rate = 0.25
		#draw stroke here

		for thing in self.foods:
			if dist(thing.x, thing.y, robot.x, robot.y) < thing.radius:
				thing.amount -= consumption_rate * timestep
				robot.food_battery += fill_rate * timestep


		for thing in self.waters:
			if dist(thing.x, thing.y, robot.x, robot.y) < thing.radius:
				thing.amount -= consumption_rate * timestep
				robot.water_battery += fill_rate * timestep


		for thing in self.traps:
			if dist(thing.x, thing.y, robot.x, robot.y) < thing.radius:
				robot.food_battery = 0.0
				robot.water_battery = 0.0
				robot.is_alive = False


	def update(self):
		for thing in self.foods:
			thing.update()
		for thing in self.waters:
			thing.update()
		for thing in self.traps:
			thing.update()

	def draw(self):
		#draw stuff
		return True
