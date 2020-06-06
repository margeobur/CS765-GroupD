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
    # In this case it is a few single robot
    def draw_element(self):
        artist1 = RobotArtist(1)
        artist2 = RobotArtist(1)
        artist3 = RobotArtist(1)
        artist4 = RobotArtist(1)
        smell_sig1 = [-0.6692384698663982, -0.4058080337461456, -0.5856871543135049, -0.9942005212095189, -0.09659883151229631]
        smell_sig2 = [-0.1581927130390064, 0.5243553799375225, 0.49507282599854596, -0.008671600933305434, 0.04489397170966969]
        smell_sig3 = [-0.096316806460637, 0.4338130167438412, 0.3601080121137903, -0.8140349133602223, 0.9253748921591534]
        smell_sig_list = (smell_sig1, smell_sig2, smell_sig3)
        dir = random.uniform(0, 2.0 * math.pi)
        sensor_angles = [dir + math.pi, dir + math.pi/2, dir - math.pi/2]
        artist1.x_position(150).y_position(150).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(1.0).water_battery(1.0).smell_signatures(smell_sig_list)
        artist2.x_position(250).y_position(250).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(0.5).water_battery(0.5).smell_signatures(smell_sig_list)
        artist3.x_position(350).y_position(350).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(0.1).water_battery(0.1).smell_signatures(smell_sig_list)
        artist4.x_position(150).y_position(350).alive(True).orientation(
            dir).sensor_angles(sensor_angles).food_battery(0.3).water_battery(0.7).smell_signatures(smell_sig_list)
        artist1.draw()
        artist2.draw()
        artist3.draw()
        artist4.draw()

if __name__ == "__main__":
    RobotArtistTester()