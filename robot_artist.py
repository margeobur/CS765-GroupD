'''
This is the artist class for the robot. It will extend the Artist class in 
the artist.py file. If need be, check the Artist class for more detail.
'''

from artist import Artist

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
    def draw(self, gx, gy, is_alive):
        # fill in the colour
        self.fill_colour(is_alive)
        
        # draw the main body
        self.draw_body(gx, gy)
        
        # draw the details
        self.draw_detail()
        
    # Method for filling in the colour of the element
    # Parameters:
    #   is_alive: a boolean to check if the robot is alive
    def fill_colour(self, is_alive):
        if is_alive:
            super().fill_colour("green")
        else:
            super().fill_colour("brown")
            
    
    
    
        
    