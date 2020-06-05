'''
This is the parent test class for Artist and its children classes
'''

import turtle
from sys import platform

class ArtistTester:
    
    # Constructor
    def __init__(self):
        arena_size = 500
        
        # TODO: Jin: I know it is hacky but it works on Spyder
        win = None
        try:
            win = turtle.Screen()
        except:
            win = turtle.Screen()
            
        win.setup(arena_size, arena_size)
        win.setworldcoordinates(0, 0, arena_size, arena_size)
        win.bgcolor("black")
        win.title("RobotArtist Tester")
        
        self.draw_element()
    
        win.mainloop()
        if platform=="win32":
            win.exitonclick()
    
    # This is the method that will draw whatever needs to be tested.
    # It is used via the template method.
    def draw_element(self):
        pass
    
if __name__ == "__main__":
    ArtistTester()