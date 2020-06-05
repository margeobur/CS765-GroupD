'''
This is the robot artist tester. It will extend the ArtistTester class.
'''

from artist_tester import ArtistTester
from robot_artist import RobotArtist

class RobotArtistTester(ArtistTester):
    # Constructor
    def __init__(self):
        super().__init__()
        
    # Method for drawin the element.
    # In this case it is a single robot
    def draw_element(self):
        artist = RobotArtist(1)
        artist.draw(250, 250, True)

if __name__ == "__main__":
    RobotArtistTester()