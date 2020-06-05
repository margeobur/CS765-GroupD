'''
This is the artist class for "Things". It will extend the Artist class in 
the artist.py file. If need be, check the Artist class for more detail.
'''

from artist import Artist

class ThingArtist(Artist):
    
    # Constructor
    # Parameters: 
    #   r: radius for the GUI element
    def __init__(self, r, colour):
        super().__init__(r)
        self.COLOUR = colour
        
    # Method for drawing the robot
    # Parameters:
    #   gx: see Artist#draw()
    #   gy: see Artist#draw()
    #   is_alive: a boolean to check if the robot is alive
    def draw(self, gx, gy):
        # fill in the colour
        self.fill_colour()
        
        # draw the main body
        self.draw_body(gx, gy)
        
        # draw the details
        self.draw_detail()
        
    # Method for filling in the colour of the element
    # Parameters:
    #   is_alive: a boolean to check if the robot is alive
    def fill_colour(self):
        super().fill_colour(self.COLOUR)