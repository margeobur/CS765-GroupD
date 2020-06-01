import random
import enum
import numpy as np
import simulation_state
import turtle


class ThingType(enum.Enum):
    Food = 1
    Water = 2
    Trap = 3


class Thing:
    def __init__(self, ntype, nx=None, ny=None):
        self.amount = 1.0
        self.radius = 1.0
        self.type = ntype

        if nx is None and ny is None:
            self.position = np.array([
                random.randrange(0, simulation_state.arena_width),
                random.randrange(0, simulation_state.arena_width)
            ])
        else:
            self.position = np.array([nx, ny])

    def draw(self):
        # alpha = int(180 * self.amount)
        # Not sure the above line is needed anymore.
        t = turtle.Turtle()
        if self.type == ThingType.Food:
            t.fillcolor("yellow")
        elif self.type == ThingType.Water:
            t.fillcolor("blue")
        else:
            t.fillcolor("red")
        t.penup()
        t.goto(self.position[0], self.position[1])
        t.pendown()
        t.shape("circle")
        t.shapesize(self.radius * 2, self.radius * 2)

    def update(self):
        if self.amount < 0.0:
            self.amount = 1.0
            self.position = np.array([
                random.randrange(0, simulation_state.arena_width),
                random.randrange(0, simulation_state.arena_width)
            ])


class Environment:

    def __init__(self):
        self.foods = []
        self.waters = []
        self.traps = []

        # create 4 food sources and 4 water sources
        for i in range(0, 4):
            self.foods.append(Thing(ThingType.Food))
            self.waters.append(Thing(ThingType.Water))

        # create 2 traps
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
        # draw stroke here

        for thing in self.foods:
            if np.linalg.norm(thing.position - robot.position) < thing.radius:
                thing.amount -= consumption_rate * simulation_state.timestep
                robot.food_battery += fill_rate * simulation_state.timestep

        for thing in self.waters:
            if np.linalg.norm(thing.position - robot.position) < thing.radius:
                thing.amount -= consumption_rate * simulation_state.timestep
                robot.water_battery += fill_rate * simulation_state.timestep

        for thing in self.traps:
            if np.linalg.norm(thing.position - robot.position) < thing.radius:
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
        win = turtle.Screen()
        win.setup(simulation_state.arena_width, simulation_state.arena_width)
        win.setworldcoordinates(0, 0, simulation_state.arena_width, simulation_state.arena_width)
        win.bgcolor("black")
        win.title("Arena")
        for f in self.foods:
            f.draw()
        for w in self.waters:
            w.draw()
        for t in self.traps:
            t.draw()
        win.mainloop()
