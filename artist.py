'''
This is the artist class that will be responsible for drawing the GUI for each 
of the elements.
'''

import turtle

class Artist:
    
    # Constructor
    # Parameters: Takes in the radius for the GUI element
    def __init__(self, r):
        # TODO: Jin: I know it looks hacky, but it works on Spyder
        try:
            self.artist = turtle.Turtle()
        except:
            self.artist = turtle.Turtle()
        
        self.radius = r

    ''' --------------Setters for build method (head)-------------- '''

    def x_position(self, x):
        self.x_pos = x
        return self

    def y_position(self, y):
        self.y_pos = y
        return self

    def colour(self, colour):
        self.col = colour
        return self

    ''' --------------Setters for build method (tail)-------------- '''
        
    # Method for drawing
    # This method will always draw a circle filled in by that colour for a 
    # for a given position.
    # Parameters:
    #   ...
    def draw(self):
        turtle.tracer(0, 0)

        # fill in the colour
        self.fill_colour()
        
        # draw the body
        self.draw_body()
        
        # draw in other details if necessary
        self.draw_detail()
        turtle.update()
        
    # Method for drawing the body of the element as a circle
    def draw_body(self):
        # draw the element itself as a circle
        self.artist.penup()
        self.artist.goto(self.x_pos, self.y_pos)
        self.artist.pendown()
        self.artist.shape("circle")
        self.artist.shapesize(self.radius*2, self.radius*2)
    
    # Method for filling in the colour of the element.
    # This is a template method approach for Artist#draw() invoked at the start
    # of the method
    def fill_colour(self):
        self.artist.fillcolor(self.col)
        
    # Method for drawing in other necessary detail for the element.
    # This is a template method approach for Artist#draw() invoked after the 
    # main body of the element is drawn.
    def draw_detail(self):
        pass