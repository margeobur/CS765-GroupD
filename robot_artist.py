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
        
    # Method for drawing the robot
    # Parameters:
    #   gx: see Artist#draw()
    #   gy: see Artist#draw()
    #   is_alive: a boolean to check if the robot is alive
    def draw(self, gx, gy, is_alive, dir):
        # fill in the colour
        self.fill_colour(is_alive)
        
        # draw the main body
        self.draw_body(gx, gy)
        
        # draw the details
        self.draw_detail(gx, gy, dir)
        
    # Method for filling in the colour of the element
    # Parameters:
    #   is_alive: a boolean to check if the robot is alive
    def fill_colour(self, is_alive):
        if is_alive:
            super().fill_colour("green")
        else:
            super().fill_colour("brown")

    # Method for drawing in the details of the robot.
    # These details include:
    #   orientation of the robot
    #   sensors
    #   battery levels
    #   food/water source remaining
    #   smell signature
    #   possibly genes if there is time
    def draw_detail(self, gx, gy, dir):
        self.draw_orientation(gx, gy, dir)
            
    # Method for drawing the direction arrow of the robot
    # Parameters:
    #   dir: the direction at which the robot is heading
    def draw_orientation(self, gx, gy, dir):
        dis = self.radius * 30
        t = turtle.Turtle()
        t.radians()
        t.pencolor("white")
        t.pensize(3)
        t.penup()
        t.goto(gx, gy)
        # Move ahead of the robot and save the position
        t.setheading(dir)
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
        t.setheading(dir)
        t.pendown()
        t.right(22 * math.pi/36)
        t.forward(self.radius * 20)
        t.penup()

    
        
    