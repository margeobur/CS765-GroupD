'''
This is the artist class for "Things". It will extend the Artist class in 
the artist.py file. If need be, check the Artist class for more detail.
'''

from artist import Artist
import turtle

class ThingArtist(Artist):
    
    # Constructor
    # Parameters: 
    #   r: radius for the GUI element
    def __init__(self, r):
        super().__init__(r)

    ''' --------------Setters for build method (head)-------------- '''

    

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
        super().fill_colour()