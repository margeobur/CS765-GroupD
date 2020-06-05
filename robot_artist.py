'''
This is the artist class for the robot. It will extend the Artist class in 
the artist.py file. If need be, check the Artist class for more detail.
'''

from artist import Artist
import turtle
import math

class RobotArtist(Artist):
    
    # Constructor
    # Parameters: 
    #   r: radius for the GUI element
    def __init__(self, r):
        super().__init__(r)
        self.x_pos = 0
        self.y_pos = 0
        self.is_alive = True
        self.ori = 0

    ''' --------------Setters for build method (head)-------------- '''

    def alive(self, alive):
        self.is_alive = alive
        return self

    def orientation(self, ori):
        self.ori = ori
        return self

    def sensor_angles(self, sense_angs):
        self.sense_angs = sense_angs
        return self

    ''' --------------Setters for build method (tail)-------------- '''
        
    # Method for drawing the robot
    # Parameters:
    #   ...
    def draw(self):
        turtle.tracer(0, 0)
        # fill in the colour
        self.fill_colour()
        
        # draw the main body
        self.draw_body()
        
        # draw the details
        self.draw_detail()
        turtle.update()
        
    # Method for filling in the colour of the element
    # Parameters:
    #   ...
    def fill_colour(self):
        if self.is_alive:
            self.col = "green"
        else:
            self.col = "brown"
        super().fill_colour()

    # Method for drawing in the details of the robot.
    # These details include:
    #   orientation of the robot
    #   sensors
    #   battery levels
    #   food/water source remaining
    #   smell signature
    #   possibly genes if there is time
    def draw_detail(self):
        self.draw_orientation()
        self.draw_sensors()
            
    # Method for drawing the direction arrow of the robot
    # Parameters:
    #   ...
    def draw_orientation(self):
        dis = self.radius * 30
        t = turtle.Turtle()
        t.radians()
        t.pencolor("white")
        t.pensize(3)
        t.penup()
        t.goto(self.x_pos, self.y_pos)
        # Move ahead of the robot and save the position
        t.setheading(self.ori)
        t.forward(dis)
        t.pendown()
        (x, y) = t.position()

        # draw the arrows
        # left arrow
        t.left(22 * math.pi/36)
        t.forward(self.radius * 20)
        t.penup()
        # right arrow
        t.goto(x, y)
        t.setheading(self.ori)
        t.pendown()
        t.right(22 * math.pi/36)
        t.forward(self.radius * 20)
        t.penup()
        t.goto(0,0)

    # Method for drawing the sense onto the robot
    # Parameters:
    def draw_sensors(self):
        dis = self.radius * 20
        for sa in self.sense_angs:
            t = turtle.Turtle()
            t.radians()
            t.pencolor("white")
            t.fillcolor("black")
            t.pensize(2)
            t.shapesize(0.4, 0.2)
            # go to where the robot is
            t.penup()
            t.goto(self.x_pos, self.y_pos)
            # turn to the direction of where the sensor is
            t.setheading(self.ori + sa)
            # go to the edge of the robot
            t.forward(dis)
            t.pendown()
            # draw a quadralateral
            t.shape("square")



        
    