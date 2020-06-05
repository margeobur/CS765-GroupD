'''
This is the artist class for the environment. There will be a single turtle for 
the environment, that will draw all the "things" in it.
'''

from artist import Artist
import turtle

class EnvironmentArtist(Artist):
    
    # Constructor
    # Parameters:
    #   r: radius for the GUI element
    #   foods: array of foods in the environment
    #   waters: array of waters in the environment
    #   traps: array of traps in the environement
    def __init__(self, r, foods, waters, traps):
        super().__init__(r)
        self.foods = []
        self.waters = []
        self.traps = []
        self.setup(foods, waters, traps)
        
    # Method for drawing all the things in the environment
    def draw_all(self):
        self.draw_foods()
        self.draw_waters()
        self.draw_traps()
    
    # Method for drawing all the foods in the environment
    def draw_foods(self):
        for f in self.foods:
            self.draw(f.position[0], f.position[1], f.COLOUR)
    
    # Method for drawing all the waters in the environment
    def draw_waters(self):
        for w in self.waters:
            self.draw(w.position[0], w.position[1], w.COLOUR)
            
    # Method for drawing all the traps in the environment
    def draw_traps(self):
        for t in self.traps:
            self.draw(t.position[0], t.position[1], t.COLOUR)
            
            
            