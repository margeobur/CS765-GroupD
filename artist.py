'''
This is the artist class that will be responsible for drawing the GUI for each 
of the elements.
'''

import turtle

class Artist:
    
    # Constructor
    # Parameters: Takes in the radius for the GUI element
    def __init__(self, r):
        self.artist = turtle.Turtle()
        self.radius = r
        
    # Method for drawing
    # This method will always draw a circle filled in by that colour for a 
    # for a given position.
    # Parameters:
    #   gx = x coordinate
    #   gy = y coordinate
    #   colour = colour of the element
    def draw(self, gx, gy, colour):
        # fill in the colour
        self.fill_colour(colour)
        
        # draw the body
        self.draw_body(gx, gy)
        
        # draw in other details if necessary
        self.draw_detail()
        
    # Method for drawing the body of the element as a circle
    def draw_body(self, gx, gy):
        # draw the element itself as a circle
        self.artist.penup()
        self.artist.goto(gx, gy)
        self.artist.pendown()
        self.artist.shape("circle")
        self.artist.shapesize(self.radius*2, self.radius*2)
    
    # Method for filling in the colour of the element.
    # This is a template method approach for Artist#draw() invoked at the start
    # of the method
    def fill_colour(self, colour):
        self.artist.fillcolor(colour)
        
    # Method for drawing in other necessary detail for the element.
    # This is a template method approach for Artist#draw() invoked after the 
    # main body of the element is drawn.
    def draw_detail(self):
        pass