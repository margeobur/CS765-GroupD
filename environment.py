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

		if type == ThingType.Food:
			food_xs.add(self.x)
			food_ys.add(self.y)

		elif type == ThingType.Water:
			water_xs.add(self.x)
			water_ys.add(self.y)

		elif type == ThingType.Trap:
			trap_xs.add(self.x)
			trap_ys.add(self.y)

	# def __init__(self, nx, ny, ntype):
	# 	self.x = nx
	# 	self.y = ny
	#
	# 	self.type = ntype
	#
	# 	self.amount = 1.0
	# 	self.radius = 1.0

	def draw():
		#
		return True

	def update():
		if self.amount < 0.0:
			self.amount = 1.0
			self.x = random.randrange(0, arena_width)
			self.y = random.randrange(0, arena_width)

			if type == ThingType.Food:
				self.food_xs.append(self.x)
				self.food_ys.append(self.y)
			elif type == ThingType.Water:
				self.water_xs.append(self.x)
				self.water_ys.append(self.y)
			elif type == ThingType.Trap:
				self.trap_ys.append(self.x)
				self.trap_ys.append(self.y)

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

	def reset():
		for thing in self.foods:
			thing.amount = -1.0
			thing.update()
		for thing in self.waters:
			thing.amount = -1.0
			thing.update()
		for thing in self.traps:
			thing.amount = -1.0
			thing.update()

	def interact_with_robot(robot):
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


	def update():
		for thing in self.foods:
			thing.update()
		for thing in self.waters:
			thing.update()
		for thing in self.traps:
			thing.update()

	def draw():
		#draw stuff
		return True
