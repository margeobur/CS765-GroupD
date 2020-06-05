'''
This is the robot artist tester. It will extend the ArtistTester class.
'''

from artist_tester import ArtistTester
from robot_artist import RobotArtist
import random
import math
import turtle

class RobotArtistTester(ArtistTester):
    # Constructor
    def __init__(self):
        super().__init__()
        
    # Method for drawin the element.
    # In this case it is a single robot
    def draw_element(self):
        artist = RobotArtist(1)
        dir = random.uniform(0, 2.0 * math.pi)
        sensor_angles = [dir + math.pi, dir + math.pi/2, dir - math.pi/2]
        artist.x_position(250).y_position(250).alive(True).orientation(dir).sensor_angles(sensor_angles)
        artist.draw()

if __name__ == "__main__":
    RobotArtistTester()