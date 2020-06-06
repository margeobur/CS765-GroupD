'''
This is the artist class for "Things". It will extend the Artist class in 
the artist.py file. If need be, check the Artist class for more detail.
'''

from artist import Artist
import turtle
import math

class ThingArtist(Artist):
    
    # Constructor
    # Parameters: 
    #   r: radius for the GUI element
    def __init__(self, r):
        super().__init__(r)
        self.volume = 0
        self.smell_sigs = None

    ''' --------------Setters for build method (head)-------------- '''

    def amount_full(self, max_cap):
        self.max_cap = max_cap
        return self

    def amount_left(self, volume):
        self.volume = volume
        return self

    def smell_signature(self, smell_sigs):
        self.smell_sigs = smell_sigs
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
    # includes fading effects to show 
    def fill_colour(self):
        ratio = self.volume/self.max_cap
        
        (r, g, b) = self.col
        if not (r == 255 and g == 0 and b == 0):
            r = math.floor(r * ratio + 64)
            g = math.floor(g * ratio + 64)
            b = math.floor(b * ratio + 64)

            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255
        
        self.col = (r, g, b)
        super().fill_colour()

    # Method for drawing in the details of the element
    # These include:
    #   smell signature in terms of 4 colours
    def draw_detail(self):
        if self.smell_sigs is not None:
            self.draw_smell_sig()

    # Method for drawing in the smell signatures
    # Parameters:
    #   ...
    # Calculation for colours
    #   let si be element of smell signature
    #   xi = floor((si + 1) * 128)
    #   left-top rgb: x1, 255, x2
    #   left-bottom rgb: x3, x4, x5
    #   right-top rgb: 255 - x1, 0, 255 - x2
    #   right-bottom rgb: 255 - x3, 255 - x4, 255 - x5
    def draw_smell_sig(self):
        dis = self.radius * 5

        # calculate xi for colours 
        x_list = []
        for s in self.smell_sigs:
            x = math.floor((s + 1) * 128)
            x_list.append(x)

        # create the turtles for each of the sensor colours
        for i in range(0, 4):
            t = turtle.Turtle()
            t.radians()
            t.pencolor("black")
            t.pensize(0.3)
            t.shapesize(0.5, 0.5)
            # go to where the robot is 
            t.penup()
            t.goto(self.x_pos, self.y_pos)
            # set direction to up
            t.setheading(0)
            # go to the necessary division and fill colour
            if i == 0:
                # left top corner
                # rgb = x1, 255, x2
                t.left(math.pi/2)
                t.forward(dis)
                t.right(math.pi/2)
                t.forward(dis)
                t.fillcolor(x_list[0], 255, x_list[1])
            elif i == 1:
                # left bottom corner
                # rgb = x3, x4, x5
                t.left(math.pi/2)
                t.forward(dis)
                t.left(math.pi/2)
                t.forward(dis)
                t.fillcolor(x_list[2], x_list[3], x_list[4])
            elif i == 2:
                # right top corner
                # rgb = 255 - x1, 0, 255 - x2
                t.right(math.pi/2)
                t.forward(dis)
                t.left(math.pi/2)
                t.forward(dis)
                t.fillcolor(255 - x_list[0], 0, 255 - x_list[1])
            elif i == 3:
                # right bottom corner
                # rgb = 255 - x3, 255 - x4, 255 - x5
                t.right(math.pi/2)
                t.forward(dis)
                t.right(math.pi/2)
                t.forward(dis)
                t.fillcolor(255 - x_list[2], x_list[3], x_list[4])
            t.pendown()
            t.shape("square")