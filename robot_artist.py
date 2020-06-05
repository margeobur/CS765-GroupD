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
    
    def smell_signatures(self, smell_sigs):
        self.smell_sigs = smell_sigs
        return self

    def water_battery(self, water_batts):
        self.water_batts = water_batts
        return self
    
    def food_battery(self, food_batts):
        self.food_batts = food_batts
        return self

    ''' --------------Setters for build method (tail)-------------- '''
        
    # Method for drawing the robot
    # Parameters:
    #   ...
    def draw(self):
        if self.is_alive:
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
        self.col = "green"
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
        self.draw_batteries()
            
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
        t.hideturtle()

    # Method for drawing the senses on the robot
    # Parameters:
    #   ...
    def draw_sensors(self):
        dis = self.radius * 20
        for sa in self.sense_angs:
            t = turtle.Turtle()
            t.radians()
            t.pencolor("white")
            t.fillcolor("black")
            t.pensize(2)
            t.shapesize(0.6, 0.3)
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

    # Method for drawing the battery level on the robot
    # Parameters:
    #   ...
    def draw_batteries(self):
        dis = self.radius * 7
        size = self.radius * 10

        # draw food battery
        tf = turtle.Turtle()
        tf.radians()
        tf.pencolor("black")
        tf.fillcolor("yellow")
        tf.pensize(2)
        tf.shapesize(self.food_batts, 0.5)
        # go to robot's right hand side body
        tf.penup()
        tf.goto(self.x_pos, self.y_pos)
        tf.setheading(self.ori)
        tf.right(math.pi/2)
        tf.forward(dis)
        tf.pendown()
        tf.shape("square")

        # draw water battery
        tw = turtle.Turtle()
        tw.radians()
        tw.pencolor("black")
        tw.fillcolor("blue")
        tw.pensize(2)
        tw.shapesize(self.water_batts, 0.5)
        # go to robot's left hand side body
        tw.penup()
        tw.goto(self.x_pos, self.y_pos)
        tw.setheading(self.ori)
        tw.left(math.pi/2)
        tw.forward(dis)
        tw.pendown()
        tw.shape("square")



        
    