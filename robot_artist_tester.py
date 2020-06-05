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
        artist1 = RobotArtist(1)
        artist2 = RobotArtist(1)
        artist3 = RobotArtist(1)
        artist4 = RobotArtist(1)
        dir = random.uniform(0, 2.0 * math.pi)
        sensor_angles = [dir + math.pi, dir + math.pi/2, dir - math.pi/2]
        artist1.x_position(150).y_position(150).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(1.0).water_battery(1.0)
        artist2.x_position(250).y_position(250).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(0.5).water_battery(0.5) 
        artist3.x_position(350).y_position(350).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(0.1).water_battery(0.1)
        artist4.x_position(150).y_position(350).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(0.3).water_battery(0.7)
        artist1.draw()
        artist2.draw()
        artist3.draw()
        artist4.draw()

if __name__ == "__main__":
    RobotArtistTester()